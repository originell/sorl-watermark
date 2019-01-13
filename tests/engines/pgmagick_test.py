# coding: utf-8
# author: v.bazhin@gmail.com

from sorl_watermarker.engines.pgmagick_engine import Engine as PGEngine
from .base_case import BaseCase
from pgmagick import Image as PGImage
from PIL import Image as PILImage
import unittest
import os
import copy


class PGmagickTestCase(BaseCase):
    def __init__(self, *args, **kwargs):
        super(PGmagickTestCase, self).__init__(*args, **kwargs)
        self.engine = PGEngine()
        self.temp_dir = os.path.join(self.root_dir, "src", "temp")

    def setUp(self):
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
        path_kwargs = {
            "option_key": str(list(options.keys())[0]),
            "option_value": str(list(options.values())[0]),
        }
        temp_image_path = os.path.join(
            self.temp_dir, "{option_key}_{option_value}.png".format(**path_kwargs)
        )
        marked_image.write(temp_image_path)
        # https://github.com/python-pillow/Pillow/issues/835
        with open(temp_image_path, "rb") as image_file:
            with PILImage.open(image_file) as mark:
                os.remove(temp_image_path)
                return copy.deepcopy(mark)

    def tearDown(self):
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)


def pgmagick_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PGmagickTestCase, "test"))
    return suite
