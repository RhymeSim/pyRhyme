try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _attr(p1, p2, cc, lw):
    """
    Parameter
    p1, p2: normalized (0 <= p1 <= 1) positions
    ls: line style: solid, dash, dot, dotdash
    cc: line color
    lw: line width
    """
    lo_attr = visit.LineoutAttributes()

    lo_attr.point1 = _normalized_position_to_real(p1)
    lo_attr.point2 = _normalized_position_to_real(p2)

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
    c_attr.designator = ''
    c_attr.doBallTimeCue = 0
    c_attr.ballTimeCueColor = cc
    c_attr.timeCueBallSize = 0.01
    c_attr.doLineTimeCue = 0
    c_attr.lineTimeCueColor = cc
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
    if 'type' in p and p['type'] == 'Curve':
        if 0 in p['operators']:
            if 'type' in p['operators'][0] and p['operators'][0]['type'] == 'Lineout':
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def _normalized_position_to_real(point):
    """
    Parameter
    point: Normalized position (w.r.t mesh dimensions)
    """
    md = visit.GetMetaData(visit.GetWindowInformation().activeSource)

    offsets = md.GetMeshes(0).minSpatialExtents
    lengths = [x - o for x, o in zip(md.GetMeshes(0).maxSpatialExtents, offsets)]

    return tuple([p * l + o for p, l, o in zip(point, lengths, offsets)])


def _real_position_to_normalized(point):
    md = visit.GetMetaData(visit.GetWindowInformation().activeSource)

    offsets = md.GetMeshes(0).minSpatialExtents
    lengths = [x - o for x, o in zip(md.GetMeshes(0).maxSpatialExtents, offsets)]

    return tuple([(p - o) / l for p, l, o in zip(point, lengths, offsets)])
