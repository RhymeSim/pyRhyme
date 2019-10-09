try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def slice_attr(ot, v, at):
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

    return sa
