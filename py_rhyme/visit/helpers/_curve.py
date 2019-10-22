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
