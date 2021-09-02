import logging
import mimetypes
import subprocess
from io import BytesIO

from django.utils.encoding import smart_str
from sorl.thumbnail.engines.convert_engine import Engine as ConvertEngine, EngineError

from ..conf import settings
from .base import WatermarkEngineBase

logger = logging.getLogger(__name__)


class Engine(WatermarkEngineBase, ConvertEngine):
    """Convert based thumbnailing engine with watermark support."""

    name = "Convert"

    def _watermark(self, image, watermark_path, opacity, size, position_str):
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
            mark_size = tuple(self._get_new_watermark_size(size, mark_size))
            options = {"crop": "center", "upscale": mark_size > watermark["size"]}
            watermark = self.scale(watermark, mark_size, options)
            watermark = self.crop(watermark, mark_size, options)
            img_type = mimetypes.guess_type(watermark_path)[0]
            write_options = {"quality": 100}
            if img_type == "image/jpeg":
                write_options["format"] = "JPEG"
            elif img_type == "image/png":
                write_options["format"] = "PNG"
            else:
                raise RuntimeError(
                    "Watermark with Convert Engine only supports JPEG and PNG watermarks for now."
                )
            next_watermark = BytesIO()
            self.write(watermark, write_options, next_watermark)
            next_watermark.seek(0)
            watermark = self.get_image(next_watermark)
        position = self._define_watermark_position(
            position_str, image["size"], mark_size
        )
        args = settings.THUMBNAIL_WATERMARK_COMPOSITE.split(" ")
        if position_str == "tile":
            args.append('-tile')
        if opacity < 1:
            # -watermark would be the logical option. But it leads to black/white images.
            # According to https://legacy.imagemagick.org/Usage/annotating/#watermarking
            # dissolve is the better choice. However, even with dissolve they state:
            # """
            # This works very well, but parts of the watermark will disappear on images
            # with pure white and black pixels. That is dissolving white on white and
            # black on black will not be visible in the final image. As these two colors
            # are very common, it is better to do some extra pre-processing of the
            # watermark so that is uses various shades of grey rather than pure white
            # and black. (See "Greyed Dissolve" below)
            # """
            # So if you are running into this, please open up an issue on github.
            args.append("-dissolve")
            args.append(f"{int(opacity * 100)}%")
        args.append("-gravity")
        args.append("NorthWest")
        args.append("-geometry")
        geometry_str = ""
        for pos in position:
            if pos > 0:
                geometry_str += f'+{pos}'
            else:
                geometry_str += f'-{pos}'
        args.append(geometry_str)
        args.append(watermark['source'])
        args.append(image["source"])
        args.append(image["source"])
        args = map(smart_str, args)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        returncode = p.wait()
        out, err = p.communicate()

        if returncode:
            raise EngineError(
                f"The command {args!r} exited with a non-zero exit code and printed this to stderr: {err}"
            )
        elif err:
            logger.error("Captured stderr: %s", err)
        del watermark
        return image
