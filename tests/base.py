import os
from typing import List

from PIL import Image

FIXTURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "fixtures"))

FIXTURES_IMG_PIL_DIR = os.path.join(
    FIXTURES_DIR, "control_instances", "created_with_pil", "png"
)
FIXTURES_IMG_PGMAGICK_DIR = os.path.join(
    FIXTURES_DIR, "control_instances", "created_with_pgmagick", "png"
)

BACKGROUND_IMG_PATH = os.path.join(FIXTURES_DIR, "bg.png")

OPTIONS_TO_TEST = (
    # Positions
    {"watermark_pos": "center"},
    {"watermark_pos": "south east"},
    {"watermark_pos": "south west"},
    {"watermark_pos": "north west"},
    {"watermark_pos": "north east"},
    {"watermark_pos": "50 50"},
    {"watermark_pos": "50 -50"},
    {"watermark_pos": "-50 -50"},
    {"watermark_pos": "-50 50"},
    {"watermark_pos": "tile"},
    # Opacity
    {"watermark_alpha": 1},
    {"watermark_alpha": 0.75},
    {"watermark_alpha": 0.5},
    # Sizes
    {"watermark_size": "100%"},
    {"watermark_size": "75%"},
    {"watermark_size": "50%"},
    {"watermark_size": "200%"},
    {"watermark_size": "100x100"},
)

# this used to be 10k, but that makes it too unprecise.
# tradeoff is that pytest takes longer to calculate the diff on inequality.
def get_pixels(image: Image, denominator: int = 1000) -> List[int]:
    """Creates an RGBA pixel list from a ``PIL.Image``.

    For faster execution the resulting list length is reduced::

        List length = all_image_pixels/denominator.
    """
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    short_list = [
        pixel for idx, pixel in enumerate(image.getdata()) if idx % denominator == 0
    ]
    return short_list


def get_expected_image(option: str, value: str = None, engine: str = None) -> Image:
    """Loads the matching control instance."""
    if value is None:
        value = "default"

    fixtures_dir = FIXTURES_IMG_PIL_DIR
    if engine and engine.lower() == "pgmagick":
        fixtures_dir = FIXTURES_IMG_PGMAGICK_DIR
    image_path = os.path.join(fixtures_dir, f"{option}_{value}.png")
    # https://github.com/python-pillow/Pillow/issues/835
    with open(image_path, "rb") as image_file:
        with Image.open(image_file) as verification_img:
            return verification_img.copy()
