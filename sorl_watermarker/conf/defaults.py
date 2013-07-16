from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

STATIC_ROOT = getattr(settings, 'STATIC_ROOT')
THUMBNAIL_WATERMARK = getattr(settings, 'THUMBNAIL_WATERMARK', False)
THUMBNAIL_WATERMARK_ALWAYS = getattr(settings, 'THUMBNAIL_WATERMARK_ALWAYS', True)
THUMBNAIL_WATERMARK_OPACITY = getattr(settings, 'THUMBNAIL_WATERMARK_OPACITY', 1)
# should we do this here? If yes, we have to check every value
if not 0 < THUMBNAIL_WATERMARK_OPACITY <= 1:
    raise ImproperlyConfigured
THUMBNAIL_WATERMARK_SIZE = getattr(settings, 'THUMBNAIL_WATERMARK_SIZE', False)
THUMBNAIL_WATERMARK_POSITION = getattr(settings, 'THUMBNAIL_WATERMARK_POSITION', 'south east')
