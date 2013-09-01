
from pgmagick import Image as PGImage
from PIL import Image as PILImage
from base_case import BaseCase
import unittest



from sorl_watermarker.engines.pgmagick_engine import Engine as PGEngine

class PGmagickTestCase(unittest.TestCase, BaseCase):

    def setUp(self):
        self.engine = PGEngine()
        self.bg_path = 'src/bg.png'
        self.temp_path = 'src/temp/temp.png'
        self.img_dir = 'src/control_instances/created_with_pil/png/'

    def get_comparable_image(self, options):
        bg = PGImage(self.bg_path)
        marked_image = self.engine.watermark(bg, options)
        marked_image.write(self.temp_path + str(options.keys()[0]) + str(options.values()[0]) + '.png')
        mark = PILImage.open(self.temp_path + str(options.keys()[0]) + str(options.values()[0]) + '.png')
        return mark


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PGmagickTestCase, 'test'))
    return suite