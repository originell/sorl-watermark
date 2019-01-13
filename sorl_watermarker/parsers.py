from sorl.thumbnail.parsers import parse_geometry as xy_geometry_parser


def parse_geometry(geometry, ratio=None):
    """
    Enhanced parse_geometry parser with percentage support.
    """
    if "%" not in geometry:
        # fall back to old parser
        return xy_geometry_parser(geometry, ratio)
    # parse with float so geometry strings like "42.11%" are possible
    return float(geometry.strip("%")) / 100.0
