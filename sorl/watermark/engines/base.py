from django.conf import settings
from sorl.thumbnail.engines.base import EngineBase as ThumbnailEngineBase

THUMBNAIL_WATERMARK_ALWAYS = getattr(settings, 'THUMBNAIL_WATERMARK_ALWAYS',
                                     True)

class WatermarkEngineBase(ThumbnailEngineBase):
    """
    Extend sorl.thumbnail base engine to support watermarks.
    """
    def create(self, image, geometry, options):
        image = super(ThumbnailEngineBase, self).create(image, geometry,
                                                        options)
        if (THUMBNAIL_WATERMARK_ALWAYS or
                'watermark' in options or
                'watermark_size' in options or
                'watermark_pos' in options):
            image = image.watermark(image, geometry, options)
        return image

    def watermark(self, image, geometry, options):
        """
        Wrapper for ``_watermark``
        """
        raise NotImplementedError

