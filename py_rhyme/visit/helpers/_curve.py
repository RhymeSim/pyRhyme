try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _attr(lw, cc):
    """
    Parameter
    lw: line width
    cc: curve color
    """
    attr = visit.CurveAttributes()

    attr.showLines = 1
    attr.lineWidth = lw
    attr.showPoints = 0
    attr.symbol = attr.Point  # Point, TriangleUp, TriangleDown, Square, Circle, Plus, X
    attr.pointSize = 5
    attr.pointFillMode = attr.Static  # Static, Dynamic
    attr.pointStride = 1
    attr.symbolDensity = 50
    attr.curveColorSource = attr.Custom  # Cycle, Custom
    attr.curveColor = (0, 0, 0, 255)
    attr.showLegend = 1
    attr.showLabels = 0
    attr.designator = ''
    attr.doBallTimeCue = 0
    attr.ballTimeCueColor = cc
    attr.timeCueBallSize = 0.01
    attr.doLineTimeCue = 0
    attr.lineTimeCueColor = cc
    attr.lineTimeCueWidth = 0
    attr.doCropTimeCue = 0
    attr.timeForTimeCue = 0
    attr.fillMode = attr.NoFill  # NoFill, Solid, HorizontalGradient, VerticalGradient
    attr.fillColor1 = (255, 0, 0, 255)
    attr.fillColor2 = (255, 100, 100, 255)
    attr.polarToCartesian = 0
    attr.polarCoordinateOrder = attr.R_Theta  # R_Theta, Theta_R
    attr.angleUnits = attr.Radians  # Radians, Degrees

    return attr


def _check(plot_obj):
    return True if 'type' in plot_obj and plot_obj['type'] == 'Curve' else False


def _query(q='MinMax', rmin=None, rmax=None):
    """
    rmin, rmax: minimum and maximum of domain of interest
    """
    queries = ['MinMax']
    result = {}

    if type(q) is not str:
        print('Only string queries can be processed!')
        return result

    for i in range(visit.GetNumPlots()):
        visit.SetActivePlots(i)
        info = visit.GetPlotInformation()

        if 'Curve' in info:
            x, y = __cut_curve_values(info['Curve'], rmin, rmax)

            if q.lower() == 'minmax':
                imin = y.index(min(y))
                imax = y.index(max(y))
                result[i] = {
                    'min': (x[imin], y[imin]), 'max': (x[imax], y[imax])
                }
            else:
                print('Unknown query!', q)
                print('Use these queries:', queries)

    return result


def __cut_curve_values(curve, rmin, rmax):
    x = curve[::2]
    y = curve[1::2]

    if rmin is not None and rmax is not None:
        if rmin > rmax:
            raise RuntimeError('rmax must be greater than rmin')

    i, j = 0, len(x)

    if rmin is not None and rmin > x[0]:
        i = [p[0] for p in enumerate(x) if p[1] > rmin][0]

    if rmax is not None and rmax > x[0]:
        j = [p[0] for p in enumerate(x) if p[1] < rmax][-1] + 1

    return x[i:j], y[i:j]
