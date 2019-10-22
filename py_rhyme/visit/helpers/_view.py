try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _2d(xs, ys):
    """
    Parameter
    xs: xscale
    ys: yscale
    """
    attr = visit.View2DAttributes()

    attr.xScale = __get_scaling(xs, attr.LINEAR, attr.LOG)
    attr.yScale = __get_scaling(ys, attr.LINEAR, attr.LOG)

    attr.viewportCoords = (0.2, 0.95, 0.15, 0.90)

    return attr


def _curve(ds, rs):
    """
    Parameter
    rs: range scale, log or linear
    ds: domain scale, log or linear
    """
    attr = visit.ViewCurveAttributes()

    attr.domainScale = __get_scaling(ds, attr.LINEAR, attr.LOG)
    attr.rangeScale = __get_scaling(rs, attr.LINEAR, attr.LOG)

    attr.viewportCoords = (0.2, 0.95, 0.15, 0.90)

    return attr


def __get_scaling(scale, linear=0, log=1):
    if type(scale) is str:
        if scale.lower() == 'log':
            return log
        elif scale.lower() == 'linear':
            return linear
        else:
            raise RuntimeError('Unknown scaling!', scale)
    else:
        if scale in [log, linear]:
            return scale
        else:
            raise RuntimeError('Unknown scaling!', scale)
