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

    if ot == 'Percent' or ot == sa.Percent:
        sa.originType = sa.Percent
        sa.originPercent = v

    if at == 'XAxis':
        sa.axisType = sa.XAxis
    elif at == 'YAxis':
        sa.axisType = sa.YAxis
    elif at == 'ZAxis':
        sa.axisType = sa.ZAxis
    elif at in [sa.XAxis, sa.YAxis, sa.ZAxis]:
        sa.axisType = at
    else:
        raise RuntimeWarning(at, 'is not a valid axis type.')

    return sa


def is_slice_operator(op_obj):
    if 'type' in op_obj and op_obj['type'] == 'Slice':
        return True
    else:
        return False
