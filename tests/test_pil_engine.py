import pytest
from PIL import Image

from sorl_watermarker.engines.pil_engine import Engine as PILEngine

from .base import BACKGROUND_IMG_PATH, get_expected_image, get_pixels, OPTIONS_TO_TEST


def watermark_image(options: dict) -> Image:
    """Creates a watermarked image."""
    # https://github.com/python-pillow/Pillow/issues/835
    with open(BACKGROUND_IMG_PATH, "rb") as bg_file:
        with Image.open(bg_file) as bg_img:
            marked_img = PILEngine().watermark(bg_img, options)
    return marked_img


@pytest.mark.parametrize("option", OPTIONS_TO_TEST)
def test_engine(option):
    marked = watermark_image(option)
    expected = get_expected_image(list(option.keys())[0], list(option.values())[0])
    assert get_pixels(marked) == get_pixels(expected)
