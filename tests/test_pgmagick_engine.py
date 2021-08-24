import tempfile

import pytest
from pgmagick import Image
from PIL import Image as PILImage

from sorl_watermarker.engines.pgmagick_engine import Engine as PGMagickEngine

from .base import BACKGROUND_IMG_PATH, get_expected_image, get_pixels, OPTIONS_TO_TEST


def watermark_image(options: dict) -> Image:
    """Creates a watermarked image."""
    # https://github.com/python-pillow/Pillow/issues/835
    bg_img = Image(BACKGROUND_IMG_PATH)
    marked_img = PGMagickEngine().watermark(bg_img, options)
    return marked_img


@pytest.mark.parametrize("option", OPTIONS_TO_TEST)
def test_engine(option):
    # pgmagick does do slightly different colors & alpha. so using it's own set of
    # approved images
    expected = get_expected_image(
        list(option.keys())[0], list(option.values())[0], engine="pgmagick"
    )
    marked = watermark_image(option)
    # use PIL to get the raw pixels. could probably be done via PGmagick as well,
    # but we already know the PIL api ;-)
    with tempfile.NamedTemporaryFile() as tmpfile:
        marked.write(tmpfile.name)
        tmpfile.seek(0)
        with PILImage.open(tmpfile) as pil_mark:
            assert get_pixels(expected) == get_pixels(pil_mark)
