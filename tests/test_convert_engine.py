import pytest
from PIL import Image as PILImage

from sorl_watermarker.engines.convert_engine import Engine as ConvertEngine

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
) -> dict:
    """Creates a watermarked image."""
    # https://github.com/python-pillow/Pillow/issues/835
    options = options.copy()
    options["format"] = thumb_format.upper()
    options["watermark"] = f"mark.{mark_format}"
    with open(f"{BACKGROUND_IMG_PATH}.{bg_format}", "rb") as bg_file:
        bg_img = ConvertEngine().get_image(bg_file)
    marked_img = ConvertEngine().watermark(bg_img, options)
    return marked_img


@pytest.mark.parametrize("option,format_variation", OPTIONS_TO_TEST)
def test_engine(option, format_variation):
    key, value = list(option.items())[0]
    expected = get_expected_image(
        key,
        value,
        engine="convert",
        bg_format=format_variation[0],
        mark_format=format_variation[1],
        thumb_format=format_variation[2],
    )
    marked = watermark_image(
        option,
        bg_format=format_variation[0],
        mark_format=format_variation[1],
        thumb_format=format_variation[2],
    )
    with PILImage.open(marked["source"]) as pil_mark:
        assert_approx(pil_mark, expected, 64)
