import tempfile

import pytest
from PIL import Image as PILImage

from sorl_watermarker.engines.convert_engine import Engine as ConvertEngine

from .base import BACKGROUND_IMG_PATH, get_expected_image, get_pixels, OPTIONS_TO_TEST


def watermark_image(options: dict) -> dict:
    """Creates a watermarked image."""
    # https://github.com/python-pillow/Pillow/issues/835
    with open(BACKGROUND_IMG_PATH, 'rb') as fd:
        bg_img = ConvertEngine().get_image(fd)
    marked_img = ConvertEngine().watermark(bg_img, options)
    return marked_img


@pytest.mark.parametrize("option", OPTIONS_TO_TEST)
def test_engine(option):
    expected = get_expected_image(
        list(option.keys())[0], list(option.values())[0], engine="convert"
    )
    marked = watermark_image(option)
    with PILImage.open(marked['source']) as pil_mark:
        marked_from_disk_pixels = get_pixels(pil_mark)
        # compare pixel by pixel with an extra assert because it makes the diff easier
        # to read. should also be failing faster.
        for idx, expected_pixel in enumerate(get_pixels(expected)):
            # We have to use approx() because apparently PIL doesnt read the files
            # written by Convert back 100% the same?
            assert pytest.approx(expected_pixel, abs=64) == marked_from_disk_pixels[idx]

