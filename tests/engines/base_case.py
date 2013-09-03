# coding: utf-8
# author: v.bazhin@gmail.com

from PIL import Image as PILImage
from django.conf import settings
settings.configure(THUMBNAIL_WATERMARK = 'mark.png',
                   STATICFILES_DIRS = ('src/', ), )


class BaseCase(object):

    def setUp(self):
        self.engine = 'Sorl watermark engine'
        self.bg_path = 'Watermark background image'
        self.temp_path = 'Temporary folder for non PIL the testing images'
        self.img_dir = 'The source of the proper images examples'

    def get_comparable_image(self, options):
        raise NotImplementedError('The method should return the PIL image object')

    def get_pixels_list(self, image, denominator=10000):
        """
        Creating the rgba tuples pixels list.
        For the faster execution the resulting list length is reduced.
        List length = all_image_pixels/denominator.

        """
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        image_pixels = list(image.getdata())
        short_list = [pixel for loop, pixel in enumerate(image_pixels)
                      if loop%denominator == 0]
        return short_list


    def verify_watermark(self, option='watermark_pos', value='default'):
        """
        Compare two rgba pixels list
        """
        print 'Testing ' + option + ': ' + str(value)
        pre_image = PILImage.open(self.img_dir + option + '/' + str(value) + '.png')
        if value == 'default':
            options = dict()
        else:
            options = {option: value}
        mark = self.get_comparable_image(options)
        self.assertEqual(self.get_pixels_list(mark), self.get_pixels_list(pre_image))


    def test_position(self):
        self.verify_watermark()
        self.verify_watermark(value='center')
        self.verify_watermark(value='south east')
        self.verify_watermark(value='south west')
        self.verify_watermark(value='north east')
        self.verify_watermark(value='north west')
        self.verify_watermark(value='50 50')
        self.verify_watermark(value='50 -50')
        self.verify_watermark(value='-50 -50')
        self.verify_watermark(value='-50 50')


    def test_opacity(self):
        self.verify_watermark(option='watermark_alpha', value=1)
        self.verify_watermark(option='watermark_alpha', value=0.75)
        self.verify_watermark(option='watermark_alpha', value=0.5)


    def test_size(self):
        self.verify_watermark(option='watermark_size', value="100%")
        self.verify_watermark(option='watermark_size', value="75%")
        self.verify_watermark(option='watermark_size', value="50%")
        self.verify_watermark(option='watermark_size', value="100x100")