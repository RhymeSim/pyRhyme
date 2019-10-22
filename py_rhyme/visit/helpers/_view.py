try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _2d_attr(xs, ys):
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
