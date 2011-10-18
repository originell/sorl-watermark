from pgmagick import Geometry, Image
from sorl.thumbnail.engines.pgmagick_engine import Engine as MagickEngine
from sorl.watermark.engines.base import WatermarkEngineBase


class Engine(WatermarkEngineBase, MagickEngine):
    """
    PGMagick based engine with watermark support.
    """
    def _watermark(self, image, mark, opacity, position,
                   mark_width, mark_height):
        if opacity < 1:
            mark = mark.opacity(opacity * 65535) # Quantum is an
                                                 # unsigned short
        # create a transparent layer the size of the image and draw the
        # watermark in that layer.
        im_size = image.size
        mark_size = mark.size
        position = (im_size[0]-mark_size[0], im_size[1]-mark_size[1])
        return image.composite(mark, position)
