try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _attr(ot, v, at):
    """
    Parameter
    ot: OriginType
    v: Value
    at: AxisType
    """
    sa = visit.SliceAttributes()

    if ot == 'Percent' or ot == sa.Percent:
        sa.originType = sa.Percent
        sa.originPercent = v

    sa.axisType = __get_axis(at, sa.XAxis, sa.YAxis, sa.ZAxis)

    return sa


def _check(op_obj):
    return True if 'type' in op_obj and op_obj['type'] == 'Slice' else False


def _kwargs(o, ot, op, at):
    """
    o: operator object
    ot: origint type
    op: origin percent
    at: axis type
    """

    return {
        'origin_type': ot if ot is not None else o['origin_type'],
        'origin_percent': op if op is not None else o['origin_percent'],
        'axis_type': at if at is not None else o['axis_type'],
    }


def __get_axis(axis, x, y, z):
    if type(axis) is str:
        if axis.lower() == 'x':
            return x
        elif axis.lower() == 'y':
            return y
        elif axis.lower() == 'z':
            return z
        else:
            raise RuntimeError('Unknown axis!', axis)
    else:
        if axis in [x, y, z]:
            return axis
        else:
            raise RuntimeError('Unknonw axis!', axis)
