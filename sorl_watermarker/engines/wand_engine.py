from sorl.thumbnail.engines.wand_engine import Engine as WandEngine

from .base import WatermarkEngineBase


class Engine(WatermarkEngineBase, WandEngine):
    """Wand based thumbnailing engine with watermark support."""

    name = "Wand"

    def _watermark(self, image, watermark_path, opacity, size, position_str):
        with open(watermark_path, "rb") as image_file:
            watermark = self.get_image(image_file)

        # TODO: test that this is the RGBA conversion equivalent. and it works with
        #       jpg/png mixture
        if image.format != "png":
            image.format = "png"

        if not size:
            mark_size = watermark.size
        else:
            mark_size = tuple(self._get_new_watermark_size(size, watermark.size))
            options = {"crop": "center", "upscale": mark_size > watermark.size}
            watermark = self.scale(watermark, mark_size, options)
            watermark = self.crop(watermark, mark_size, options)
        if position_str == "tile":
            image.texture(watermark)
        else:
            position = self._define_watermark_position(
                position_str, image.size, mark_size
            )
            image.watermark(
                watermark, transparency=1 - opacity, left=position[0], top=position[1]
            )
        del watermark
        return image
