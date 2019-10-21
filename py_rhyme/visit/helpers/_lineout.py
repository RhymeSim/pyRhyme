try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _attr(p1, p2, ls='solid', lc=(0, 0, 0, 255), lw=4):
    """
    Parameter
    p1, p2: normalized (0 <= p1 <= 1) positions
    ls: line style: solid, dash, dot, dotdash
    lc: line color
    lw: line width
    """
    lo_attr = visit.LineoutAttributes()
    info = visit.GetWindowInformation()

    lo_attr.point1 = p1 * info.extents
    lo_attr.point2 = p2 * info.extents

    lo_attr.interactive = 0
    lo_attr.ignoreGlobal = 0
    lo_attr.samplingOn = 0
    lo_attr.numberOfSamplePoints = 50
    lo_attr.reflineLabels = 0


    c_attr = visit.CurveAttributes()

    c_attr.showLines = 1
    c_attr.lineWidth = lw
    c_attr.showPoints = 0
    c_attr.symbol = c_attr.Point  # Point, TriangleUp, TriangleDown, Square, Circle, Plus, X
    c_attr.pointSize = 5
    c_attr.pointFillMode = c_attr.Static  # Static, Dynamic
    c_attr.pointStride = 1
    c_attr.symbolDensity = 50
    c_attr.curveColorSource = c_attr.Custom  # Cycle, Custom
    c_attr.curveColor = (0, 0, 0, 255)
    c_attr.showLegend = 1
    c_attr.showLabels = 0
    c_attr.designator = "designator"
    c_attr.doBallTimeCue = 0
    c_attr.ballTimeCueColor = lc
    c_attr.timeCueBallSize = 0.01
    c_attr.doLineTimeCue = 0
    c_attr.lineTimeCueColor = lc
    c_attr.lineTimeCueWidth = 0
    c_attr.doCropTimeCue = 0
    c_attr.timeForTimeCue = 0
    c_attr.fillMode = c_attr.NoFill  # NoFill, Solid, HorizontalGradient, VerticalGradient
    c_attr.fillColor1 = (255, 0, 0, 255)
    c_attr.fillColor2 = (255, 100, 100, 255)
    c_attr.polarToCartesian = 0
    c_attr.polarCoordinateOrder = c_attr.R_Theta  # R_Theta, Theta_R
    c_attr.angleUnits = c_attr.Radians  # Radians, Degrees

    return lo_attr, c_attr


def _check(p):
    return True if 'type' in p and p['operators']['type'] == 'Lineout' else False
