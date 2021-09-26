import pytest
from PIL import Image

from sorl_watermarker.engines.pil_engine import Engine as PILEngine

from .base import (
    BACKGROUND_IMG_PATH,
    get_expected_image,
    OPTIONS_TO_TEST,
    assert_approx,
)


def watermark_image(
    options: dict,
    bg_format: str,
    mark_format: str,
    thumb_format: str,
) -> Image:
    """Creates a watermarked image."""
    # https://github.com/python-pillow/Pillow/issues/835
    options = options.copy()
    options["format"] = thumb_format.upper()
    options["watermark"] = f"mark.{mark_format}"
    with open(f"{BACKGROUND_IMG_PATH}.{bg_format}", "rb") as bg_file:
        with Image.open(bg_file) as bg_img:
            marked_img = PILEngine().watermark(bg_img, options)
    return marked_img


@pytest.mark.parametrize("option,format_variation", OPTIONS_TO_TEST)
def test_engine(option, format_variation):
    marked = watermark_image(
        option,
        bg_format=format_variation[0],
        mark_format=format_variation[1],
        thumb_format=format_variation[2],
    )
    key, value = list(option.items())[0]
    expected = get_expected_image(
        key,
        value=value,
        engine="pil",
        bg_format=format_variation[0],
        mark_format=format_variation[1],
        thumb_format=format_variation[2],
    )
    assert_approx(marked, expected, 47)
