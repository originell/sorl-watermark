import os
import re
import logging
import mimetypes
import subprocess

from django.utils.encoding import smart_str
from sorl.thumbnail.engines.vipsthumbnail_engine import Engine as VipsEngine
from sorl.thumbnail.engines.convert_engine import EngineError
from sorl.thumbnail.base import EXTENSIONS


from ..conf import settings
from .base import WatermarkEngineBase

logger = logging.getLogger(__name__)
orientation_re = re.compile(r"exif-\w+-Orientation: (?P<orientation>\d)")
VIPS_BLEND_MODE_OVER = 2


class Engine(WatermarkEngineBase, VipsEngine):
    """Convert based thumbnailing engine with watermark support."""

    name = "vipsthumbnail"

    def _watermark(
        self, image, watermark_path, opacity, size, position_str, img_format
    ):
        to_cleanup = []
        with open(watermark_path, "rb") as image_file:
            # this returns a dict!
            watermark = self.get_image(image_file)
        # this stores the size on the image dict
        self.get_image_size(watermark)
        self.get_image_size(image)

        # TODO: test that this is the RGBA conversion equivalent. and it works with
        #       jpg/png mixture

        mark_size = watermark["size"]
        if size:
            mark_size = self._get_new_watermark_size(size, mark_size)
            options = {"crop": "center", "upscale": mark_size > watermark["size"]}
            # Crop is not implemented by parent engine. vipsthumbnails does support the
            # "-c" flag though... continued below...
            # do_crop = not options['upscale'] and mark_size != watermark['size']
            watermark = self.scale(watermark, mark_size, options)
            mark_size = watermark["size"]
            # ... continued from above:
            # watermark = self.crop(watermark, mark_size, options)
            # However, I am not enabling this for now. Need a good testcase first.
            # if do_crop:
            #     watermark['options']['crop'] = True
        position = self._define_watermark_position(
            position_str, image["size"], mark_size
        )

        # First, crop and scale the watermark, if so wished.
        processed_watermark_source = watermark["source"]
        if watermark["options"]:
            args = settings.THUMBNAIL_VIPSTHUMBNAIL.split(" ")
            for vips_option, vips_option_value in watermark["options"].items():
                if vips_option == "crop":
                    args.append("-c")
                    continue
                args.append(f"--{vips_option}")
                if vips_option_value is not None:
                    args.append(f"{vips_option_value}")
            # specify output
            # older vipsthumbnails used -o, this was renamed to -f in 8.0, use
            # -o here for compatibility.
            args.append("-o")
            img_type = mimetypes.guess_type(watermark_path)[0]
            mark_suffix = mimetypes.guess_extension(img_type)
            mark_suffixed = f"{watermark['source']}{mark_suffix}"
            args.append(mark_suffixed)
            # specify input
            args.append(watermark["source"])
            processed_watermark_source = mark_suffixed
            self._run_command(args)
            to_cleanup.append(mark_suffixed)

        # Then (optionally) reduce opacity of our watermark image
        suffix = f".{EXTENSIONS[img_format]}"
        output = f"{image['source']}{suffix}"
        if opacity < 1:
            args = settings.THUMBNAIL_WATERMARK_VIPS.split(" ")
            args.append("linear")
            args.append(processed_watermark_source)
            opacity_output = f"{processed_watermark_source}_reduced_alpha{suffix}"
            args.append(opacity_output)
            args.append("1")
            args.append(f"0 0 0 -{int((1 - opacity) * 255)}")
            self._run_command(args)
            processed_watermark_source = opacity_output
            to_cleanup.append(opacity_output)

        # Then watermark the actual image
        if position_str == "tile":
            tiling_root = os.path.splitext(image["source"])[0]
            tiling_output = f"{tiling_root}_tiling_00{suffix}"
            tile_source = image["source"]
            x_iter = 0
            y_iter = 0
            for x_pos in range(0, image["size"][0], watermark["size"][0]):
                x_iter += 1
                for y_pos in range(0, image["size"][1], watermark["size"][1]):
                    y_iter += 1
                    args = settings.THUMBNAIL_WATERMARK_VIPS.split(" ")
                    args.append("composite")
                    args.append(f"{tile_source} {processed_watermark_source}")
                    args.append(tiling_output)
                    args.append(VIPS_BLEND_MODE_OVER)
                    args.append("--x")
                    args.append(x_pos)
                    args.append("--y")
                    args.append(y_pos)
                    self._run_command(args)
                    tile_source = tiling_output
                    to_cleanup.append(tile_source)
                    tiling_output = f"{tiling_root}_tiling_{x_iter}{y_iter}{suffix}"
            # we can't delete our last run-through because that's what we return.
            to_cleanup.pop()
            output = tile_source
        else:
            args = settings.THUMBNAIL_WATERMARK_VIPS.split(" ")
            args.append("composite")
            args.append(f"{image['source']} {processed_watermark_source}")
            args.append(output)
            args.append(VIPS_BLEND_MODE_OVER)
            args.append("--x")
            args.append(position[0])
            args.append("--y")
            args.append(position[1])
            self._run_command(args)

        del watermark
        image["source"] = output
        for del_fpath in to_cleanup:
            os.remove(del_fpath)
        return image

    def _run_command(self, args):
        args = [smart_str(arg) for arg in args]
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        returncode = p.wait()
        out, err = p.communicate()
        if returncode:
            raise EngineError(
                f"The command {args!r} exited with a non-zero exit code and printed this to stderr: {err}"
            )
        elif err:
            logger.error("Captured stderr: %s", err)

    def _flip_dimensions(self, image):
        orientation = self._get_exif_orientation(image)
        return orientation and orientation in [5, 6, 7, 8]

    def _get_exif_orientation(self, image):
        args = settings.THUMBNAIL_VIPSHEADER.split(" ")
        args.append("-a")
        args.append(image["source"])
        try:
            p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
        except:  # noqa: E722
            return None

        match = orientation_re.match(str(p.stdout.read()))
        if match and match.group("orientation"):
            return int(match.group("orientation"))
