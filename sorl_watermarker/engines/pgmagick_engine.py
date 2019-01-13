from sorl_watermarker.engines.base import WatermarkEngineBase

from pgmagick import ChannelType
from pgmagick import CompositeOperator as CoOp
from pgmagick import Geometry, Image, ImageType
from pgmagick import QuantumOperator as QuOp
from sorl.thumbnail.engines.pgmagick_engine import Engine as MagickEngine


class Engine(WatermarkEngineBase, MagickEngine):
    """
    PGMagick based engine with watermark support.
    """

    name = "PGMagick"

    def _watermark(self, image, watermark_path, opacity, size, position_str):
        with open(watermark_path, "rb") as watermark_file:
            watermark = self.get_image(watermark_file)
        image_size = self.get_image_size(image)
        layer = Image(Geometry(image_size[0], image_size[1]), "transparent")
        if opacity < 1:
            self._reduce_opacity(watermark, opacity)
        if not size:
            mark_size = self.get_image_size(watermark)
        else:
            mark_size = tuple(
                self._get_new_watermark_size(size, self.get_image_size(watermark))
            )
            options = {
                "crop": "center",
                "upscale": mark_size > self.get_image_size(watermark),
            }
            watermark = self.scale(watermark, mark_size, options)
            watermark = self.crop(watermark, mark_size, options)
        if position_str == "tile":
            for x_pos in range(0, image_size[0], mark_size[0]):
                for y_pos in range(0, image_size[1], mark_size[1]):
                    layer.composite(watermark, x_pos, y_pos, CoOp.OverCompositeOp)
        else:
            position = self._define_watermark_position(
                position_str, image_size, mark_size
            )
            layer.composite(watermark, position[0], position[1], CoOp.OverCompositeOp)
        image.composite(layer, 0, 0, CoOp.OverCompositeOp)
        return image

    def _reduce_opacity(self, watermark, opacity):
        """
        Returns an image with reduced opacity. Converts image to RGBA if needs.

        Simple watermark.opacity(65535 - int(65535 * opacity) would not work for
        images with the Opacity channel (RGBA images). So we have to convert RGB or any
        other type to RGBA in this case
        """

        if watermark.type() != ImageType.TrueColorMatteType:
            watermark.type(ImageType.TrueColorMatteType)
        depth = 255 - int(255 * opacity)
        watermark.quantumOperator(ChannelType.OpacityChannel, QuOp.MaxQuantumOp, depth)
