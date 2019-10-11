try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def curve_attr(rs, ds):
    """
    Parameter
    rs: range scale
    ds: domain scale
    """
    ca = ViewCurveAttributes()
