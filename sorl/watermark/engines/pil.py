from sorl.thumbnail.engines.pil_engine import Engine as PILEngine

try:
    from PIL import Image, ImageEnhance
except ImportError:
    import Image, ImageEnhance


class Engine(PILEngine):
    """
    PIL based thumbnailing engine with watermark support.
    """

    # the following is heavily copied from
    # http://code.activestate.com/recipes/362879-watermark-with-pil/
    def _watermark(self, image, mark, opacity, position):
                   #mark_width, mark_height):
        if opacity < 1:
            mark = reduce_opacity(mark, opacity)
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        # create a transparent layer the size of the image and draw the
        # watermark in that layer.
        im_size = image.size
        mark_size = mark.size
        layer = Image.new('RGBA', im_size, (0,0,0,0))
        position = (im_size[0]-mark_size[0], im_size[1]-mark_size[1])
        layer.paste(mark, position)
        return Image.composite(layer, image, layer)

    def _reduce_opacity(image, opacity):
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        else:
            image = image.copy()
        alpha = image.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        image.putalpha(alpha)
        return image
