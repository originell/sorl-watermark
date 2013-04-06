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
    def _watermark(self, image, watermark_path, opacity, size, position_string): #, position):
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
            if hasattr(size, '__getitem__'):
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



        position = self._define_position(position_string, im_size, mark_size )
     #   position = (im_size[0]-2*mark_size[0], im_size[1]-2*mark_size[1])
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

    def _define_position(self, position_string, im_size, mark_size):
        pos_list = position_string.split(' ')
        longitude_values = {'west':0, 'east':im_size[0]-mark_size[0]}
        latitude_values =  {'north':0, 'south':im_size[1]-mark_size[1]}
        # if values can be parsed as numeric
        try:
            x_abs_value = int(pos_list[0])
            y_abs_value = int(pos_list[1])
            # values below 0
            x_pos = x_abs_value if x_abs_value >= 0 else longitude_values['east'] \
                                                         + x_abs_value
            y_pos = y_abs_value if y_abs_value >= 0 else latitude_values['south'] \
                                                         + y_abs_value
            position = (x_pos, y_pos)
        # if the values are not a pair of numbers
        except ValueError:
            if pos_list == ['center']:
                position = (longitude_values['east']/2,latitude_values['south']/2)
            else:
                lon_val = [lon for lon in pos_list if lon in longitude_values]
                lat_val = [lat for lat in pos_list if lat in latitude_values]
                lon_key = lon_val[0] if len(lon_val) > 0 else 'east'
                lat_key = lat_val[0] if len(lat_val) > 0 else 'south'
                position = (longitude_values[lon_key], latitude_values[lat_key])
        return position

