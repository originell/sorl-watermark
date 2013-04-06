import os

from django.conf import settings
from django.contrib.staticfiles.finders import find
from sorl.thumbnail.engines.base import EngineBase as ThumbnailEngineBase
from sorl_watermarker.parsers import parse_geometry

# TODO: Put this in it's own package, as done by sorl.thumbnail
STATIC_ROOT = getattr(settings, 'STATIC_ROOT')

THUMBNAIL_WATERMARK = getattr(settings, 'THUMBNAIL_WATERMARK', False)
THUMBNAIL_WATERMARK_ALWAYS = getattr(settings, 'THUMBNAIL_WATERMARK_ALWAYS',
                                     True)
THUMBNAIL_WATERMARK_OPACITY = getattr(settings, 'THUMBNAIL_WATERMARK_OPACITY',
                                      1)
assert 0 <= THUMBNAIL_WATERMARK_OPACITY <= 1 # TODO: raise a ValueError here?

THUMBNAIL_WATERMARK_SIZE = getattr(settings, 'THUMBNAIL_WATERMARK_SIZE', False)

THUMBNAIL_WATERMARK_POSITION = getattr(settings, 'THUMBNAIL_WATERMARK_POSITION', False)

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

        Takes care of all the options handling.
        """
        watermark_img = options.get('watermark', THUMBNAIL_WATERMARK)

        if not watermark_img:
            raise AttributeError('Trying to apply a watermark, '
                                 'however no THUMBNAIL_WATERMARK defined, and watermark not set on tag')
        watermark_path = find(watermark_img)

        if not 'watermark_alpha' in options:
            options['watermark_alpha'] = THUMBNAIL_WATERMARK_OPACITY

        if not 'watermark_size' in options and THUMBNAIL_WATERMARK_SIZE:
            options['watermark_size'] = THUMBNAIL_WATERMARK_SIZE
        elif 'watermark_size' in options:
            options['watermark_size'] = parse_geometry(
                                            options['watermark_size'],
                                            self.get_image_ratio(image),
                                        )
        else:
            options['watermark_size'] = False

        # Position added
        if not 'watermark_pos' in options:
            options['watermark_pos'] = THUMBNAIL_WATERMARK_POSITION


        return self._watermark(image, watermark_path,
                               options['watermark_alpha'],
                               options['watermark_size'], options['watermark_pos'])
