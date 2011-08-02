from sorl.thumbnail.engines.pil_engine import Engine as PILEngine
from sorl.watermark.engines.base import WatermarkEngineBase

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
    def _watermark(self, image, watermark_path, opacity, size): #, position):
                   #mark_width, mark_height):
        watermark = self.get_image(open(watermark_path))
        if opacity < 1:
            watermark = self._reduce_opacity(watermark, opacity)
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        # create a transparent layer the size of the image and draw the
        # watermark in that layer.
        im_size = image.size

        mark_size = watermark.size
        if size:
            if hasattr(size, '__iterable__'):
                # a tuple or any iterable already
                mark_size = size
            else:
                # percentages hopefully
                mark_size = map(lambda coord: coord*size, mark_size)
            # TODO: Might be useful to expose the crop/upscalce options
            #       to django settings
            watermark = self.scale(watermark, mark_size, {'crop': 'center',
                                                          'upscale': False})

        layer = Image.new('RGBA', im_size, (0,0,0,0))
        position = (im_size[0]-mark_size[0], im_size[1]-mark_size[1])
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
