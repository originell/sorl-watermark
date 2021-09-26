import copy
import os
import random
import shutil

import pytest
from django.core.files.images import ImageFile
from django.template import Context, Template
from sorl.thumbnail import default

from .base import BACKGROUND_IMG_PATH, OPTIONS_TO_TEST as BASE_OPTIONS_TO_TEST

TEMPLATE_BASE = "{% load thumbnail %}"
AVAILABLE_ENGINES = [
    "sorl_watermarker.engines.pil_engine.Engine",
    "sorl_watermarker.engines.wand_engine.Engine",
    "sorl_watermarker.engines.pgmagick_engine.Engine",
    "sorl_watermarker.engines.convert_engine.Engine",
    "sorl_watermarker.engines.vips_engine.Engine",
]
ENGINE_TEST_PARAMS = []
for engine_to_test in AVAILABLE_ENGINES:
    options_to_test = copy.deepcopy(list(BASE_OPTIONS_TO_TEST))
    # add some random combinations on top
    for i in range(20):
        how_many = random.randint(1, 5)
        random_opt_combination = {}
        for rando in random.sample(options_to_test, k=how_many):
            for rando_key, rando_value in rando.items():
                random_opt_combination[rando_key] = rando_value
        options_to_test.append(random_opt_combination)
    for engine_opts in options_to_test:
        ENGINE_TEST_PARAMS.append([engine_to_test, engine_opts])


@pytest.fixture
def media_cleanup(settings):
    yield
    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, "test"), ignore_errors=True)


def test_no_watermark(mocker, db, settings, media_cleanup):
    settings.THUMBNAIL_ENGINE = "sorl_watermarker.engines.pil_engine.Engine"
    with open(str(BACKGROUND_IMG_PATH), "rb") as fd:
        ret_img = default.engine.get_image(fd)
    mocked_watermark = mocker.patch(
        "sorl_watermarker.engines.pil_engine.Engine.watermark", return_value=ret_img
    )
    template = Template(TEMPLATE_BASE + '{% thumbnail image "100x100" crop="center" %}')
    with open(str(BACKGROUND_IMG_PATH), "rb") as fd:
        rendered = template.render(Context({"image": ImageFile(fd)}))
        assert rendered.startswith("/media")
    assert mocked_watermark.call_count == 1
    assert mocked_watermark.call_args[0][1] == {
        "crop": "center",
        "format": "JPEG",
        "quality": 95,
        "colorspace": "RGB",
        "upscale": True,
        "cropbox": None,
        "rounded": None,
        "padding": False,
        "padding_color": "#ffffff",
        "image_info": {"dpi": (72.009, 72.009), "Comment": "Created with GIMP"},
    }


# this is quite a huge test that simply validates engines overwrite watermark()
# correctly, if at all.
@pytest.mark.parametrize("engine,option", ENGINE_TEST_PARAMS)
def test_watermark_options(mocker, db, settings, media_cleanup, engine, option):
    settings.THUMBNAIL_ENGINE = engine
    # bypass cache. we don't need it in our tests. we want to check that options are
    # correctly passed into our watermark handling.
    mocker.patch("tests.watermark_tests_app.kvstore.TestKVStore.set", return_value=None)
    with open(str(BACKGROUND_IMG_PATH), "rb") as fd:
        ret_img = default.engine.get_image(fd)
    mocked_watermark = mocker.patch(
        "sorl_watermarker.engines.pil_engine.Engine.watermark", return_value=ret_img
    )

    tag_args = " ".join(
        [
            f'{options_key}="{options_value}"'
            for options_key, options_value in option.items()
        ]
    )
    djhtml = (
        f'{TEMPLATE_BASE}{{% thumbnail image "400x300" crop="center" {tag_args} %}}'
    )
    template = Template(djhtml)
    with open(str(BACKGROUND_IMG_PATH), "rb") as fd:
        rendered = template.render(Context({"image": ImageFile(fd)}))
        assert rendered.startswith("/media")
    assert mocked_watermark.call_count == 1, f"watermarking not called: {djhtml}"

    expected_options = {
        "crop": "center",
        "format": "JPEG",
        "quality": 95,
        "colorspace": "RGB",
        "upscale": True,
        "cropbox": None,
        "rounded": None,
        "padding": False,
        "padding_color": "#ffffff",
        "image_info": {"dpi": (72.009, 72.009), "Comment": "Created with GIMP"},
    }
    # everything is passed in as string.
    fixture_opts = {k: str(v) for k, v in option.items()}
    expected_options.update(fixture_opts)
    assert mocked_watermark.call_args[0][1] == expected_options
