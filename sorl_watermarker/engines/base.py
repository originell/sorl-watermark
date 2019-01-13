import os
from functools import wraps

from django.contrib.staticfiles.finders import find
from django.core.exceptions import ImproperlyConfigured

from sorl.thumbnail.engines.base import EngineBase as ThumbnailEngineBase

from ..conf import settings
from ..parsers import parse_geometry


def handle_padding(fn):
    @wraps(fn)
    def wrapped(self, image, geometry, options):
        watermark_before_padding = options.get(
            "watermark_before_padding", settings.THUMBNAIL_WATERMARK_BEFORE_PADDING
        )
        padding = False
        if watermark_before_padding:
            if options.get("padding") and self.get_image_size(image) != geometry:
                # remove padding option, add it later
                padding = options["padding"]
                options["padding"] = False

        image = fn(self, image, geometry, options)

        if watermark_before_padding:
            if padding and self.get_image_size(image) != geometry:
                # add padding after watermark
                options["padding"] = padding
                image = self.padding(image, geometry, options)
        return image

    return wrapped


class WatermarkEngineBase(ThumbnailEngineBase):
    """
    Extend sorl.thumbnail base engine to support watermarks.
    """

    name = "BaseEngine"

    @handle_padding
    def create(self, image, geometry, options):
        image = super(WatermarkEngineBase, self).create(image, geometry, options)
        if (
            settings.THUMBNAIL_WATERMARK_ALWAYS
            or "watermark" in options
            or "watermark_pos" in options
            or "watermark_size" in options
            or "watermark_alpha" in options
        ):
            image = self.watermark(image, options)
            # WORKAROUND: Forcefully convert JPGs to RGB.
            #             Pillow < 4.2 allowed this. Since then, one has to forcefully
            #             convert. Which makes sense as JPGs can't have an alpha
            #             channel.
            #             See #28 for details.
            if options.get("format", "").lower() == "jpeg" and image.mode == "RGBA":
                image = image.convert("RGB")
        return image

    def watermark(self, image, options):
        """
        Wrapper for ``_watermark``

        Takes care of all the options handling.
        """
        watermark_img = options.get("watermark", settings.THUMBNAIL_WATERMARK)
        if not watermark_img:
            raise AttributeError("No THUMBNAIL_WATERMARK defined or set on tag.")
        watermark_path = find(watermark_img)
        if not watermark_path:
            raise RuntimeError("Could not find the configured watermark file.")
        if not os.path.isfile(watermark_path):
            raise RuntimeError("Set watermark does not point to a file.")

        if "cropbox" not in options:
            options["cropbox"] = None
        if "watermark_alpha" not in options:
            options["watermark_alpha"] = settings.THUMBNAIL_WATERMARK_OPACITY

        mark_sizes = options.get("watermark_size", settings.THUMBNAIL_WATERMARK_SIZE)
        if mark_sizes:
            try:
                options["watermark_size"] = parse_geometry(
                    mark_sizes, self.get_image_ratio(image, options)
                )
            except TypeError as e:
                raise TypeError(
                    "Please, update sorl-thumbnail package version to  >= 11.12b. %s"
                    % e
                )
        else:
            options["watermark_size"] = False

        if "watermark_pos" not in options:
            options["watermark_pos"] = settings.THUMBNAIL_WATERMARK_POSITION

        return self._watermark(
            image,
            watermark_path,
            options["watermark_alpha"],
            options["watermark_size"],
            options["watermark_pos"],
        )

    def _watermark(self, image, watermark_path, opacity, size, position_str):
        """
        Returns a combined thumbnail with a imposed watermark

        Implemented by the used engine.
        """
        raise NotImplementedError()

    def _get_new_watermark_size(self, size, mark_default_size):
        """
        New size can be passed as a pair of valuer (tuple) or
        a fsloat (persentage case)
        """
        if hasattr(size, "__getitem__"):
            # a tuple or any iterable already
            mark_size = size
        elif isinstance(size, float):
            mark_size = map(lambda coord: int(coord * size), mark_default_size)
        else:
            raise ImproperlyConfigured(
                "Watermark sizes must be a pair " "of integers or a float number"
            )
        return mark_size

    def _define_watermark_position(self, position_string, im_size, mark_size):
        pos_list = position_string.split(" ")
        coords = {
            "x": {"west": 0, "east": im_size[0] - mark_size[0]},
            "y": {"north": 0, "south": im_size[1] - mark_size[1]},
        }
        # if values can be parsed as numeric
        try:
            x_abs = int(pos_list[0])
            y_abs = int(pos_list[1])
            # values below 0
            x_pos = x_abs if x_abs >= 0 else int(coords["x"]["east"]) + x_abs
            y_pos = y_abs if y_abs >= 0 else int(coords["y"]["south"]) + y_abs
            position = (int(x_pos), int(y_pos))
        # if the values are not a pair of numbers
        except ValueError:
            if pos_list == ["center"]:
                position = (int(coords["x"]["east"] / 2), int(coords["y"]["south"] / 2))
            else:
                x_val = [lon for lon in pos_list if lon in coords["x"]]
                y_val = [lat for lat in pos_list if lat in coords["y"]]
                x_key = x_val[0] if len(x_val) > 0 else "east"
                y_key = y_val[0] if len(y_val) > 0 else "south"
                position = (int(coords["x"][x_key]), int(coords["y"][y_key]))
        return position
