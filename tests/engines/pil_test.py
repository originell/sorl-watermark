import unittest
from PIL import Image as PILImage
from base_case import BaseCase



from sorl_watermarker.engines.pil_engine import Engine as PILEngine


class PILTestCase(unittest.TestCase, BaseCase):

    def setUp(self):
        self.engine = PILEngine()
        self.bg_path = 'src/bg.png'
        self.img_dir = 'src/control_instances/created_with_pil/png/'

    def get_comparable_image(self, options):
        bg = PILImage.open(self.bg_path)
        mark = self.engine.watermark(bg, options)
        return mark


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PILTestCase, 'test'))
    return suite