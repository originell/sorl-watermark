# -*- coding: utf-8 -*-

from django.conf import settings
import unittest
from PIL import Image as PILImage

settings.configure(THUMBNAIL_WATERMARK = 'mark.png',
                   STATICFILES_DIRS = ('src/', ), )

# importing Engine after configuring django.conf.settings
from sorl_watermarker.engines.pil_engine import Engine as PILEngine


class PILTestCase(unittest.TestCase):

    def setUp(self):
        self.bg = PILImage.open('src/bg.png')
        self.engine = PILEngine()
        self.img_dir = 'src/control_instances/pngs/'

    def get_pixels_list(self, image, denom=1000):
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        image_pixels = list(image.getdata())
        short_list = [pixel for loop, pixel in enumerate(image_pixels)
                      if loop%denom == 0]
        return short_list

    def verify_watermark(self, option='watermark_pos', value='default'):
        print 'Testing position: ' + str(value)
        pre_image = PILImage.open(self.img_dir + option + '/' + str(value) + '.png')
        if value == 'default':
            options = dict()
        else:
            options = {option: value}
        mark = self.engine.watermark(self.bg, options)
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

if __name__ == '__main__':
    unittest.main()

