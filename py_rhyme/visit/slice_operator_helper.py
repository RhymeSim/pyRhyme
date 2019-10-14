try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def slice_operator_attr(ot, v, at):
    """
    Parameter
    ot: OriginType
    v: Value
    at: AxisType
    """
    sa = visit.SliceAttributes()

    if ot is 'Percent':
        sa.originType = sa.Percent
        sa.originPercent = v

    if at is 'XAxis':
        sa.axisType = sa.XAxis
    elif at is 'YAxis':
        sa.axisType = sa.YAxis
    elif at is 'ZAxis':
        sa.axisType = sa.ZAxis
    else:
        raise RuntimeWarning(at, 'is not a valid axis type.')

    so = _new_slice_operator_object()
    so['origin_type'] = ot
    so['value'] = v
    so['axis_type'] = at

    return sa, so


def _new_slice_operator_object():
    return {
        'type': 'slice',
        'origin_type': '',
        'value': 0,
        'axis_type': '',
    }


def is_slice_operator(op_obj):
    if 'type' in op_obj and op_obj['type'] is 'slice':
        return True
    else:
        return False
