try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _attr(p1, p2):
    """
    Parameter
    p1, p2: normalized (0 <= p1 <= 1) positions
    ls: line style: solid, dash, dot, dotdash
    """
    attr = visit.LineoutAttributes()

    attr.point1 = _normalized_position_to_real(p1)
    attr.point2 = _normalized_position_to_real(p2)

    attr.interactive = 0
    attr.ignoreGlobal = 0
    attr.samplingOn = 0
    attr.numberOfSamplePoints = 50
    attr.reflineLabels = 0

    return attr


def _check(p):
    if 'type' in p and p['type'] == 'Curve' \
        and 'operators' in p and 0 in p['operators'] \
        and 'type' in p['operators'][0] \
        and p['operators'][0]['type'] == 'Lineout':
        return True

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


def _kwargs(p, v, p1, p2, lw, cc):
    """
    p: plot object
    v: variable
    lw: line width
    cc: curve color
    p1, p2: point 1 & 2
    """
    if 'operators' not in p or 0 not in p['operators']:
        raise RuntimeError('Wrong plot object!', p)

    return {
        'variable': v if v is not None else p['variable'],
        'point1': p1 if p1 is not None else p['operators'][0]['point1'],
        'point2': p2 if p2 is not None else p['operators'][0]['point2'],
        'line_width': lw if lw is not None else p['line_width'],
        'curve_color': cc if cc is not None else p['curve_color'],
    }
