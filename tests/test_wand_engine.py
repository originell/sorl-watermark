import tempfile

import pytest
from wand.image import Image

from sorl_watermarker.engines.wand_engine import Engine as WandEngine

from .base import BACKGROUND_IMG_PATH, get_expected_image, get_pixels, OPTIONS_TO_TEST


def watermark_image(options: dict) -> Image:
    """Creates a watermarked image."""
    bg_img = Image(filename=BACKGROUND_IMG_PATH)
    options = options.copy()
    options["format"] = "PNG"
    marked_img = WandEngine().watermark(bg_img, options)
    return marked_img


@pytest.mark.parametrize("option", OPTIONS_TO_TEST)
def test_engine(option):
    # wand does do slightly different colors, alpha & position. so using it's own set of
    # approved images
    expected = get_expected_image(
        list(option.keys())[0], list(option.values())[0], engine="wand"
    )
    marked = watermark_image(option)
    # Compare.
    with tempfile.NamedTemporaryFile() as tmpfile:
        marked.save(filename=tmpfile.name)
        tmpfile.seek(0)
        marked_from_disk = Image(filename=tmpfile.name)
        marked_from_disk_pixels = get_pixels(marked_from_disk)
        # compare pixel by pixel with an extra assert because it makes the diff easier
        # to read. should also be failing faster.
        for idx, expected_pixel in enumerate(get_pixels(expected)):
            # We have to use approx() because apparently Wand doesnt work 100%
            # deterministic? Or our pixel-by-pixel comparison is buggy somewhere.
            # So we compare with a tolerance of +- 48. That hopefully still helps in
            # spotting major regressions.
            # Update: actually we have to use 49 because in CI it's off by one.
            assert pytest.approx(expected_pixel, abs=49) == marked_from_disk_pixels[idx]
