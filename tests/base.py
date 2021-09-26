import os
from typing import List, Union

import pytest
from PIL import Image as PILImage
from wand.image import Image as WandImage

FIXTURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "fixtures"))

FIXTURES_IMG_PIL_DIR = os.path.join(
    FIXTURES_DIR, "control_instances", "created_with_pil"
)
FIXTURES_IMG_PGMAGICK_DIR = os.path.join(
    FIXTURES_DIR, "control_instances", "created_with_pgmagick"
)

BACKGROUND_IMG_PATH = os.path.join(FIXTURES_DIR, "bg")

OPTIONS_TO_TEST = [
    [{"watermark_pos": "center"}, ["png", "png", "png"]],
    [{"watermark_pos": "center"}, ["png", "png", "jpg"]],
    [{"watermark_pos": "center"}, ["png", "jpg", "jpg"]],
    [{"watermark_pos": "center"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_pos": "center"}, ["jpg", "jpg", "png"]],
    [{"watermark_pos": "center"}, ["jpg", "png", "png"]],
    [{"watermark_pos": "south east"}, ["png", "png", "png"]],
    [{"watermark_pos": "south east"}, ["png", "png", "jpg"]],
    [{"watermark_pos": "south east"}, ["png", "jpg", "jpg"]],
    [{"watermark_pos": "south east"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_pos": "south east"}, ["jpg", "jpg", "png"]],
    [{"watermark_pos": "south east"}, ["jpg", "png", "png"]],
    [{"watermark_pos": "south west"}, ["png", "png", "png"]],
    [{"watermark_pos": "south west"}, ["png", "png", "jpg"]],
    [{"watermark_pos": "south west"}, ["png", "jpg", "jpg"]],
    [{"watermark_pos": "south west"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_pos": "south west"}, ["jpg", "jpg", "png"]],
    [{"watermark_pos": "south west"}, ["jpg", "png", "png"]],
    [{"watermark_pos": "north west"}, ["png", "png", "png"]],
    [{"watermark_pos": "north west"}, ["png", "png", "jpg"]],
    [{"watermark_pos": "north west"}, ["png", "jpg", "jpg"]],
    [{"watermark_pos": "north west"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_pos": "north west"}, ["jpg", "jpg", "png"]],
    [{"watermark_pos": "north west"}, ["jpg", "png", "png"]],
    [{"watermark_pos": "north east"}, ["png", "png", "png"]],
    [{"watermark_pos": "north east"}, ["png", "png", "jpg"]],
    [{"watermark_pos": "north east"}, ["png", "jpg", "jpg"]],
    [{"watermark_pos": "north east"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_pos": "north east"}, ["jpg", "jpg", "png"]],
    [{"watermark_pos": "north east"}, ["jpg", "png", "png"]],
    [{"watermark_pos": "50 50"}, ["png", "png", "png"]],
    [{"watermark_pos": "50 50"}, ["png", "png", "jpg"]],
    [{"watermark_pos": "50 50"}, ["png", "jpg", "jpg"]],
    [{"watermark_pos": "50 50"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_pos": "50 50"}, ["jpg", "jpg", "png"]],
    [{"watermark_pos": "50 50"}, ["jpg", "png", "png"]],
    [{"watermark_pos": "50 -50"}, ["png", "png", "png"]],
    [{"watermark_pos": "50 -50"}, ["png", "png", "jpg"]],
    [{"watermark_pos": "50 -50"}, ["png", "jpg", "jpg"]],
    [{"watermark_pos": "50 -50"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_pos": "50 -50"}, ["jpg", "jpg", "png"]],
    [{"watermark_pos": "50 -50"}, ["jpg", "png", "png"]],
    [{"watermark_pos": "-50 -50"}, ["png", "png", "png"]],
    [{"watermark_pos": "-50 -50"}, ["png", "png", "jpg"]],
    [{"watermark_pos": "-50 -50"}, ["png", "jpg", "jpg"]],
    [{"watermark_pos": "-50 -50"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_pos": "-50 -50"}, ["jpg", "jpg", "png"]],
    [{"watermark_pos": "-50 -50"}, ["jpg", "png", "png"]],
    [{"watermark_pos": "-50 50"}, ["png", "png", "png"]],
    [{"watermark_pos": "-50 50"}, ["png", "png", "jpg"]],
    [{"watermark_pos": "-50 50"}, ["png", "jpg", "jpg"]],
    [{"watermark_pos": "-50 50"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_pos": "-50 50"}, ["jpg", "jpg", "png"]],
    [{"watermark_pos": "-50 50"}, ["jpg", "png", "png"]],
    [{"watermark_pos": "tile"}, ["png", "png", "png"]],
    [{"watermark_pos": "tile"}, ["png", "png", "jpg"]],
    [{"watermark_pos": "tile"}, ["png", "jpg", "jpg"]],
    [{"watermark_pos": "tile"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_pos": "tile"}, ["jpg", "jpg", "png"]],
    [{"watermark_pos": "tile"}, ["jpg", "png", "png"]],
    [{"watermark_alpha": 1}, ["png", "png", "png"]],
    [{"watermark_alpha": 1}, ["png", "png", "jpg"]],
    [{"watermark_alpha": 1}, ["png", "jpg", "jpg"]],
    [{"watermark_alpha": 1}, ["jpg", "jpg", "jpg"]],
    [{"watermark_alpha": 1}, ["jpg", "jpg", "png"]],
    [{"watermark_alpha": 1}, ["jpg", "png", "png"]],
    [{"watermark_alpha": 0.75}, ["png", "png", "png"]],
    [{"watermark_alpha": 0.75}, ["png", "png", "jpg"]],
    [{"watermark_alpha": 0.75}, ["png", "jpg", "jpg"]],
    [{"watermark_alpha": 0.75}, ["jpg", "jpg", "jpg"]],
    [{"watermark_alpha": 0.75}, ["jpg", "jpg", "png"]],
    [{"watermark_alpha": 0.75}, ["jpg", "png", "png"]],
    [{"watermark_alpha": 0.5}, ["png", "png", "png"]],
    [{"watermark_alpha": 0.5}, ["png", "png", "jpg"]],
    [{"watermark_alpha": 0.5}, ["png", "jpg", "jpg"]],
    [{"watermark_alpha": 0.5}, ["jpg", "jpg", "jpg"]],
    [{"watermark_alpha": 0.5}, ["jpg", "jpg", "png"]],
    [{"watermark_alpha": 0.5}, ["jpg", "png", "png"]],
    [{"watermark_size": "100%"}, ["png", "png", "png"]],
    [{"watermark_size": "100%"}, ["png", "png", "jpg"]],
    [{"watermark_size": "100%"}, ["png", "jpg", "jpg"]],
    [{"watermark_size": "100%"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_size": "100%"}, ["jpg", "jpg", "png"]],
    [{"watermark_size": "100%"}, ["jpg", "png", "png"]],
    [{"watermark_size": "75%"}, ["png", "png", "png"]],
    [{"watermark_size": "75%"}, ["png", "png", "jpg"]],
    [{"watermark_size": "75%"}, ["png", "jpg", "jpg"]],
    [{"watermark_size": "75%"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_size": "75%"}, ["jpg", "jpg", "png"]],
    [{"watermark_size": "75%"}, ["jpg", "png", "png"]],
    [{"watermark_size": "50%"}, ["png", "png", "png"]],
    [{"watermark_size": "50%"}, ["png", "png", "jpg"]],
    [{"watermark_size": "50%"}, ["png", "jpg", "jpg"]],
    [{"watermark_size": "50%"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_size": "50%"}, ["jpg", "jpg", "png"]],
    [{"watermark_size": "50%"}, ["jpg", "png", "png"]],
    [{"watermark_size": "200%"}, ["png", "png", "png"]],
    [{"watermark_size": "200%"}, ["png", "png", "jpg"]],
    [{"watermark_size": "200%"}, ["png", "jpg", "jpg"]],
    [{"watermark_size": "200%"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_size": "200%"}, ["jpg", "jpg", "png"]],
    [{"watermark_size": "200%"}, ["jpg", "png", "png"]],
    [{"watermark_size": "100x100"}, ["png", "png", "png"]],
    [{"watermark_size": "100x100"}, ["png", "png", "jpg"]],
    [{"watermark_size": "100x100"}, ["png", "jpg", "jpg"]],
    [{"watermark_size": "100x100"}, ["jpg", "jpg", "jpg"]],
    [{"watermark_size": "100x100"}, ["jpg", "jpg", "png"]],
    [{"watermark_size": "100x100"}, ["jpg", "png", "png"]],
]


# this used to be 10k, but that makes it too unprecise.
# tradeoff is that pytest takes longer to calculate the diff on inequality.
def get_pixels(
    image: Union[PILImage.Image, WandImage], denominator: int = 1000
) -> List[int]:
    """Creates an RGBA pixel list from an engine's image.

    For faster execution the resulting list length is reduced::

        List length = all_image_pixels / denominator
    """
    binary_read_method = None
    if isinstance(image, PILImage.Image):
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        binary_read_method = image.getdata
    elif isinstance(image, WandImage):
        binary_read_method = image.export_pixels
    else:
        raise RuntimeError(f"Unknown image class supplied: '{type(image)}'")
    short_list = [
        pixel
        for idx, pixel in enumerate(binary_read_method())
        if idx % denominator == 0
    ]
    return short_list


def get_expected_image_path(
    option: str,
    value: str = None,
    engine: str = None,
    bg_format: str = "png",
    mark_format: str = "png",
    thumb_format: str = "png",
) -> str:
    """Loads the matching control instance."""
    if value is None:
        value = "default"

    fixtures_dir = FIXTURES_IMG_PIL_DIR
    if engine and engine.lower() == "pgmagick":
        fixtures_dir = FIXTURES_IMG_PGMAGICK_DIR
    return os.path.join(
        fixtures_dir,
        f"{option}_{value}__{bg_format}_{mark_format}_{thumb_format}.{thumb_format}",
    )


def get_expected_image(
    option: str,
    value: str = None,
    engine: str = "pil",
    bg_format: str = "png",
    mark_format: str = "png",
    thumb_format: str = "png",
) -> Union[PILImage.Image, WandImage]:
    """Loads the matching control instance.

    Different engines will give you different return values.

    * ``engine="pil"``, ``engine="pgmagick"`` or ``engine="pgmagick"`` will return a PIL
      Image.
    * ``engine="wand"`` will return a Wand Image
    """
    image_path = get_expected_image_path(
        option, value, engine, bg_format, mark_format, thumb_format
    )
    if engine.lower() in ["pgmagick", "pil", "pillow", "convert", "vips"]:
        # https://github.com/python-pillow/Pillow/issues/835
        with open(image_path, "rb") as image_file:
            with PILImage.open(image_file) as verification_img:
                return verification_img.copy()
    if engine.lower() == "wand":
        return WandImage(filename=image_path)
    raise RuntimeError(f"Unknown engine: '{engine}'")


def assert_approx(actual, expected, diff):
    """Compare with a little bit of leeway on each pixel's value."""
    # compare pixel by pixel with an extra assert because it makes the diff easier
    # to read. should also be failing faster.
    actual_pixels = get_pixels(actual)
    for idx, expected_pixel in enumerate(get_pixels(expected)):
        # We have to use approx() because not every engine seems to be 100%
        # deterministic? Or our pixel-by-pixel comparison is buggy somewhere.
        # So we compare with a tolerance. That hopefully still helps in spotting major
        # regressions.
        assert (
            pytest.approx(expected_pixel, abs=diff) == actual_pixels[idx]
        ), f"leeway ({diff}) not big enough between {actual_pixels[idx]} and {expected_pixel}"
