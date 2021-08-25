# coding: utf-8
# author: v.bazhin@gmail.com

from __future__ import print_function
import os
from PIL import Image as PILImage
from django.conf import settings
import unittest

settings.configure(
    THUMBNAIL_WATERMARK="mark.png", STATICFILES_DIRS=("src",), SECRET_KEY="SUPERSECRET"
)


POSITIONS_TO_TEST = (
    "center",
    "south east",
    "south west",
    "north west",
    "north east",
    "50 50",
    "50 -50",
    "-50 -50",
    "-50 50",
)

OPACITY_TO_TEST = (1, 0.75, 0.5)

SIZE_TO_TEST = ("100%", "75%", "50%", "200%", "100x100")


class BaseCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseCase, self).__init__(*args, **kwargs)
        self.root_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir)
        )
        self.img_dir = os.path.join(
            self.root_dir, "src", "control_instances", "created_with_pil", "png"
        )
        self.bg_path = os.path.join(self.root_dir, "src", "bg.png")
        self.engine = "Sorl watermark engine"

    def get_comparable_image(self, options):
        raise NotImplementedError("The method should return the PIL image object")

    def get_pixels_list(self, image, denominator=10000):
        """
        Creating the rgba tuples pixels list.
        For the faster execution the resulting list length is reduced.
        List length = all_image_pixels/denominator.

        """
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        image_pixels = list(image.getdata())
        short_list = [
            pixel for loop, pixel in enumerate(image_pixels) if loop % denominator == 0
        ]
        return short_list

    def verify_watermark(self, option="watermark_pos", value="default"):
        """
        Compare two rgba pixels list
        """
        print(
            "{engine} Testing {option}: {value}".format(
                engine=getattr(self.engine, "name", str()), option=option, value=value
            )
        )
        image_path = os.path.join(self.img_dir, option, "{}.png".format(value))
        if value == "default":
            options = dict()
        else:
            options = {option: value}
        mark = self.get_comparable_image(options)
        # https://github.com/python-pillow/Pillow/issues/835
        with open(image_path, "rb") as image_file:
            with PILImage.open(image_file) as pre_image:
                test_image_pixels = self.get_pixels_list(pre_image)
        self.assertEqual(self.get_pixels_list(mark), test_image_pixels)

    def test_position(self):
        self.verify_watermark()
        for position in POSITIONS_TO_TEST:
            self.verify_watermark(value=position)

    def test_opacity(self):
        for alpha in OPACITY_TO_TEST:
            self.verify_watermark(option="watermark_alpha", value=alpha)

    def test_size(self):
        for size in SIZE_TO_TEST:
            self.verify_watermark(option="watermark_size", value=size)
