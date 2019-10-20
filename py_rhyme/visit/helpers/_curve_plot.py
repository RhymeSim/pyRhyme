try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _attr(rs, ds):
    """
    Parameter
    rs: range scale, log or linear
    ds: domain scale, log or linear
    """
    ca = ViewCurveAttributes()
    ca.rangeScale = ca.LOG if rs == 'log' else ca.LINEAR
    ca.domainScale = ca.LOG if ds == 'log' else ca.LINEAR

    return ca


def _check(plot_obj):
    if 'type' in plot_obj and plot_obj['type'] == 'Curve':
        return True
    else:
        return False
