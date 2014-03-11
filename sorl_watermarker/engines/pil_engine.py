from sorl.thumbnail.engines.pil_engine import Engine as PILEngine
from sorl_watermarker.engines.base import WatermarkEngineBase


try:
    from PIL import Image, ImageEnhance
except ImportError:
    import Image, ImageEnhance


class Engine(WatermarkEngineBase, PILEngine):
    """
    PIL based thumbnailing engine with watermark support.
    """

    # the following is heavily copied from
    # http://code.activestate.com/recipes/362879-watermark-with-pil/
    def _watermark(self, image, watermark_path, opacity, size, position_str):
        watermark = Image.open(watermark_path)
        if opacity < 1:
            watermark = self._reduce_opacity(watermark, opacity)
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        # create a transparent layer the size of the image and draw the
        # watermark in that layer.
        if not size:
            mark_size = watermark.size
        else:
            mark_size = self._get_new_watermark_size(size, watermark.size)
            options = {'crop': 'center',
                       'upscale': False}
            watermark = self.scale(watermark, mark_size, options)
            watermark = self.crop(watermark, mark_size, options)
        layer = Image.new('RGBA', image.size, (0,0,0,0))
        position = self._define_watermark_position(position_str, image.size, mark_size)
        layer.paste(watermark, position)
        return Image.composite(layer, image, layer)


    def _reduce_opacity(self, image, opacity):
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        else:
            image = image.copy()
        alpha = image.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        image.putalpha(alpha)
        return image

