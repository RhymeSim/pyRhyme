try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _2d(xs, ys, xn=None, xx=None, yn=None, yx=None):
    """
    Parameter
    xs: xscale
    ys: yscale
    xn, xx: xmin, xmax
    yn, yx: ymin, ymax
    """
    attr = visit.View2DAttributes()

    attr.xScale = __get_scaling(xs, attr.LINEAR, attr.LOG)
    attr.yScale = __get_scaling(ys, attr.LINEAR, attr.LOG)

    attr.viewportCoords = (0.2, 0.95, 0.15, 0.90)

    visit.ResetView()
    v = visit.GetView2D()

    window = [
        xn if xn is not None else v.windowCoords[0],
        xx if xx is not None else v.windowCoords[1],
        yn if yn is not None else v.windowCoords[2],
        yx if yx is not None else v.windowCoords[3],
    ]

    attr.windowCoords = tuple(window)

    return attr


def _curve(ds, rs, xn=None, xx=None, yn=None, yx=None):
    """
    Parameter
    rs: range scale, log or linear
    ds: domain scale, log or linear
    xn, xx: xmin, xmax
    yn, yx: ymin, ymax
    """
    attr = visit.ViewCurveAttributes()

    attr.domainScale = __get_scaling(ds, attr.LINEAR, attr.LOG)
    attr.rangeScale = __get_scaling(rs, attr.LINEAR, attr.LOG)

    attr.viewportCoords = (0.2, 0.95, 0.15, 0.90)

    visit.ResetView()
    cv = visit.GetViewCurve()

    d = [
        xn if xn is not None else cv.domainCoords[0],
        xx if xx is not None else cv.domainCoords[1],
    ]

    r = [
        yn if yn is not None else cv.rangeCoords[0],
        yx if yx is not None else cv.rangeCoords[1],
    ]

    domainCoords = tuple(d)
    rangeCoords = tuple(r)

    return attr


def _kwargs(a, v, xt, yt, xu, yu, xs, ys, c, bg, fg):
    """
    a: annotation object
    v: view object (e.g. curve, 2d, ...)
    xt, yt: axis title
    xu, tu: axis unit
    xs, ys: axis scaling
    c, bg, fg: color, background, foreground
    """
    return {
        'xtitle': xt if xt is not None else a['xtitle'],
        'ytitle': yt if yt is not None else a['ytitle'],
        'xunit': xu if xu is not None else a['xunit'],
        'yunit': yu if yu is not None else a['yunit'],
        'xscale': xs if xs is not None else v['xscale'],
        'yscale': ys if ys is not None else v['yscale'],
        'color': c if c is not None else a['color'],
        'bg': bg if bg is not None else a['bg'],
        'fg': fg if fg is not None else a['fg'],
    }


def __get_scaling(scale, linear=0, log=1):
    if type(scale) is str:
        if scale.lower() == 'log':
            return log
        elif scale.lower() == 'linear':
            return linear
        else:
            raise RuntimeError('Unknown scaling!', scale)
    else:
        if scale in [linear, log]:
            return scale
        else:
            raise RuntimeError('Unknown scaling!', scale)
