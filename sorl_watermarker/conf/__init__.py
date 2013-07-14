from django.conf import settings
from django.utils.functional import LazyObject
from sorl_watermarker.conf import defaults


class Settings(object):
    pass


class LazySettings(LazyObject):
    def _setup(self):
        self._wrapped = Settings()
        for obj in (defaults, settings):
            for attr in dir(obj):
                if attr == attr.upper():
                    setattr(self, attr, getattr(obj, attr))


settings = LazySettings()