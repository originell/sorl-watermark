import os

from django.conf import settings
from sorl.thumbnail.engines.base import EngineBase as ThumbnailEngineBase


# TODO: Put this in it's own package, as done by sorl.thumbnail
STATIC_ROOT = getattr(settings, 'STATIC_ROOT')
THUMBNAIL_WATERMARK = getattr(settings, 'THUMBNAIL_WATERMARK', False)
THUMBNAIL_WATERMARK_ALWAYS = getattr(settings, 'THUMBNAIL_WATERMARK_ALWAYS',
                                     True)
THUMBNAIL_WATERMARK_OPACITY = getattr(settings, 'THUMBNAIL_WATERMARK_OPACITY',
                                      1)
assert 0 <= THUMBNAIL_WATERMARK_OPACITY <= 1


class WatermarkEngineBase(ThumbnailEngineBase):
    """
    Extend sorl.thumbnail base engine to support watermarks.
    """
    def create(self, image, geometry, options):
        image = super(WatermarkEngineBase, self).create(image, geometry,
                                                        options)
        if (THUMBNAIL_WATERMARK_ALWAYS or
                'watermark'       in options or
                'watermark_pos'   in options or
                'watermark_size'  in options or
                'watermark_alpha' in options):
            image = self.watermark(image, options)
        return image

    def watermark(self, image, options):
        """
        Wrapper for ``_watermark``
        """
        if not THUMBNAIL_WATERMARK:
            raise AttributeError('Trying to apply a watermark, '
                                 'however no THUMBNAIL_WATERMARK defined')
        watermark_path = os.path.join(STATIC_ROOT, THUMBNAIL_WATERMARK)

        if not 'watermark_alpha' in options:
            options['watermark_alpha'] = THUMBNAIL_WATERMARK_OPACITY

        return self._watermark(image, watermark_path,
                               options['watermark_alpha'])
