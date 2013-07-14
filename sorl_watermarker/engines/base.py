import os


from django.contrib.staticfiles.finders import find
from sorl.thumbnail.engines.base import EngineBase as ThumbnailEngineBase
from sorl_watermarker.parsers import parse_geometry
from sorl_watermarker.conf import settings


class WatermarkEngineBase(ThumbnailEngineBase):
    """
    Extend sorl.thumbnail base engine to support watermarks.
    """
    def create(self, image, geometry, options):
        image = super(WatermarkEngineBase, self).create(image, geometry,
                                                        options)
        if (settings.THUMBNAIL_WATERMARK_ALWAYS or
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
        watermark_img = options.get('watermark', settings.THUMBNAIL_WATERMARK)

        if not watermark_img:
            raise AttributeError('Trying to apply a watermark, '
                                 'however no THUMBNAIL_WATERMARK defined, '
                                 'and watermark not set on tag')
        watermark_path = find(watermark_img)

        if not 'watermark_alpha' in options:
            options['watermark_alpha'] = settings.THUMBNAIL_WATERMARK_OPACITY

        if 'watermark_size' in options or settings.THUMBNAIL_WATERMARK_SIZE:
            mark_sizes = options.get('watermark_size', settings.THUMBNAIL_WATERMARK_SIZE)
            options['watermark_size'] = parse_geometry(
                                            mark_sizes,
                                            self.get_image_ratio(image))
        else:
            options['watermark_size'] = False

        if not 'watermark_pos' in options:
            options['watermark_pos'] = settings.THUMBNAIL_WATERMARK_POSITION


        return self._watermark(image, watermark_path,
                               options['watermark_alpha'],
                               options['watermark_size'], options['watermark_pos'])
