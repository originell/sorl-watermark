# coding: utf-8
# author: v.bazhin@gmail.com

from base_case import BaseCase
from sorl_watermarker.engines.pgmagick_engine import Engine as PGEngine
from pgmagick import Image as PGImage
from PIL import Image as PILImage
import unittest
import os


class PGmagickTestCase(unittest.TestCase, BaseCase):

    def setUp(self):
        self.engine = PGEngine()
        self.bg_path = 'src/bg.png'
        self.temp_dir = 'src/temp/'
        self.img_dir = 'src/control_instances/created_with_pil/png/'
        # Above all, we need to create the temp folder, if not exists
        if not os.path.exists(self.temp_dir):
            os.mkdir(self.temp_dir)


    def get_comparable_image(self, options):
        """
        Creates a watermarked image with pgmagick engine and reopens it
        to return comparable PIL Image instance
        """
        bg = PGImage(self.bg_path)
        marked_image = self.engine.watermark(bg, options)
        temp_image_path = self.temp_dir + str(options.keys()[0]) + \
                          "_" + str(options.values()[0]) + '.png'
        marked_image.write(temp_image_path)
        mark = PILImage.open(temp_image_path)
        os.remove(temp_image_path)
        return mark


    def tearDown(self):
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)



def pgmagick_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PGmagickTestCase, 'test'))
    return suite