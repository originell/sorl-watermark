import tempfile

import pytest
from PIL import Image as PILImage

from sorl_watermarker.engines.vips_engine import Engine as VipsEngine

from .base import BACKGROUND_IMG_PATH, get_expected_image, get_pixels, OPTIONS_TO_TEST


def watermark_image(options: dict) -> dict:
    """Creates a watermarked image."""
    # https://github.com/python-pillow/Pillow/issues/835
    with open(BACKGROUND_IMG_PATH, "rb") as fd:
        bg_img = VipsEngine().get_image(fd)
    options = options.copy()
    options["format"] = "PNG"
    marked_img = VipsEngine().watermark(bg_img, options)
    return marked_img


@pytest.mark.parametrize("option", OPTIONS_TO_TEST)
def test_engine(option):
    marked = watermark_image(option)
    expected = get_expected_image(
        list(option.keys())[0], list(option.values())[0], engine="vips"
    )
    with open(marked["source"], "rb") as image_file:
        with PILImage.open(image_file) as verification_img:
            marked_from_disk_pixels = get_pixels(verification_img)
            # compare pixel by pixel with an extra assert because it makes the diff easier
            # to read. should also be failing faster.
            for idx, expected_pixel in enumerate(get_pixels(expected)):
                # We have to use approx() because apparently Wand doesnt work 100%
                # deterministic? Or our pixel-by-pixel comparison is buggy somewhere.
                # So we compare with a tolerance of +- 48. That hopefully still helps in
                # spotting major regressions.
                # Update: actually we have to use 49 because in CI it's off by one.
                assert (
                    pytest.approx(expected_pixel, abs=64)
                    == marked_from_disk_pixels[idx]
                )
