from pgmagick import Geometry, Image
from sorl.thumbnail.engines.pgmagick_engine import Engine as MagickEngine


class Engine(MagickEngine):
    """
    PGMagick based engine with watermark support.
    """
    pass
