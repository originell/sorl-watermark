from sorl.thumbnail.engines.pil_engine import Engine as PILEngine
from sorl_watermarker.engines.base import WatermarkEngineBase
from django.core.exceptions import ImproperlyConfigured

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
        watermark = self.get_image(open(watermark_path))
        if opacity < 1:
            watermark = self._reduce_opacity(watermark, opacity)
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        # create a transparent layer the size of the image and draw the
        # watermark in that layer.
        if not size:
            mark_size = watermark.size
        else:
            mark_size = self._get_new_size(size, watermark.size)
            options = {'crop': 'center',
                       'upscale': False}
            watermark = self.scale(watermark, mark_size, options)
            watermark = self.crop(watermark, mark_size, options)
        layer = Image.new('RGBA', image.size, (0,0,0,0))
        position = self._define_position(position_str, image.size, mark_size)
        layer.paste(watermark, position)
        return Image.composite(layer, image, layer)

    def _get_new_size(self, size, mark_default_size):
        # TODO: It may be worth to make an ability to set
        if hasattr(size, '__getitem__'):
            # a tuple or any iterable already
            mark_size = size
        elif isinstance(size, float):
            mark_size = map(lambda coord: int(coord*size), mark_default_size)
            # TODO: Might be useful to expose the crop/upscale options
            #       to django settings
        else:
            raise ImproperlyConfigured('Watermark sizes must be a pair '
                                       'of integers or a float number')
        return mark_size

    def _reduce_opacity(self, image, opacity):
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        else:
            image = image.copy()
        alpha = image.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        image.putalpha(alpha)
        return image

    def _define_position(self, position_string, im_size, mark_size):
        pos_list = position_string.split(' ')
        coords = {'x': {'west': 0,
                        'east': im_size[0] - mark_size[0]},
                  'y': {'north': 0,
                        'south': im_size[1] - mark_size[1]}, }
        # if values can be parsed as numeric
        try:
            x_abs = int(pos_list[0])
            y_abs = int(pos_list[1])
            # values below 0
            x_pos = x_abs if x_abs >= 0 else coords['x']['east'] + x_abs
            y_pos = y_abs if y_abs >= 0 else coords['y']['south'] + y_abs
            position = (x_pos, y_pos)
        # if the values are not a pair of numbers
        except ValueError:
            if pos_list == ['center']:
                position = (coords['x']['east']/2, coords['y']['south']/2)
            else:
                x_val = [lon for lon in pos_list if lon in coords['x']]
                y_val = [lat for lat in pos_list if lat in coords['y']]
                x_key = x_val[0] if len(x_val) > 0 else 'east'
                y_key = y_val[0] if len(y_val) > 0 else 'south'
                position = (coords['x'][x_key], coords['y'][y_key])
        return position

