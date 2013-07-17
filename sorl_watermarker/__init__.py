from sorl.thumbnail.conf import defaults as thumb_defaults
from sorl_watermarker.conf import defaults as watermark_defaults

# replaces the default sorl-thumbnail engine with the sorl-watermarker default one
setattr(thumb_defaults, 'THUMBNAIL_ENGINE', watermark_defaults.THUMBNAIL_ENGINE)
