from sorl.thumbnail.engines.pil_engine import Engine as PILEngine

try:
    from PIL import Image, ImageEnhance
except ImportError:
    import Image
    import ImageEnhance

from .base import WatermarkEngineBase


class Engine(WatermarkEngineBase, PILEngine):
    """PIL based thumbnailing engine with watermark support."""

    name = "PIL"

    def _watermark(
        self, image, watermark_path, opacity, size, position_str, img_format
    ):
        # have to do this because of the confirmed pillow bug to prevent resources
        # leakage
        # https://github.com/python-pillow/Pillow/issues/835
        with open(watermark_path, "rb") as image_file:
            with Image.open(image_file) as pil_watermark:
                watermark = pil_watermark.copy()
        # convert everything to RGBA. smarter code would only do this based on given
        # input and wanted outcome, but this feels good enough and easier to reason with.
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        if watermark.mode != "RGBA":
            watermark = watermark.convert("RGBA")
        if opacity < 1:
            watermark = self._reduce_opacity(watermark, opacity)
        # create a transparent layer the size of the image and draw the
        # watermark in that layer.
        if not size:
            mark_size = watermark.size
        else:
            mark_size = self._get_new_watermark_size(size, watermark.size)
            options = {"crop": "center", "upscale": mark_size > watermark.size}
            watermark = self.scale(watermark, mark_size, options)
            watermark = self.crop(watermark, mark_size, options)
        layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        if position_str == "tile":
            for x_pos in range(0, image.size[0], watermark.size[0]):
                for y_pos in range(0, image.size[1], watermark.size[1]):
                    layer.paste(watermark, (x_pos, y_pos))
        else:
            position = self._define_watermark_position(
                position_str, image.size, mark_size
            )
            layer.paste(watermark, position)
        del watermark
        composite = Image.composite(layer, image, layer)
        # WORKAROUND: Forcefully convert JPGs to RGB.
        #             Pillow < 4.2 allowed saving RGBA JPG which implied this conversion
        #             below. See #28 for details.
        if img_format.lower() in ["jpeg", "jpg"] and composite.mode == "RGBA":
            # Forgive me: this can hurt you. converting transparency away seems to make
            # things more 'white'. So in the future if some github issue shows up with
            # this, we might have to allow for an option to configure if transparency
            # should be composed together from Black or White.
            composite = composite.convert("RGB")
        return composite

    def _reduce_opacity(self, image, opacity):
        alpha = image.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        image.putalpha(alpha)
        return image
