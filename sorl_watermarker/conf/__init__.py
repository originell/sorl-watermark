from django.conf import settings as user_settings
from django.utils.functional import LazyObject

from sorl_watermarker.conf import defaults as watermark_defaults


class Settings(object):
    pass


class LazySettings(LazyObject):
    def _setup(self):
        self._wrapped = Settings()
        for obj in (watermark_defaults, user_settings):
            for attr in dir(obj):
                if attr == attr.upper():
                    setattr(self, attr, getattr(obj, attr))


settings = LazySettings()
