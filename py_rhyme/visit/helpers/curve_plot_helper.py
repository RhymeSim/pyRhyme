try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def curve_plot_attr(rs, ds):
    """
    Parameter
    rs: range scale, log or linear
    ds: domain scale, log or linear
    """
    ca = ViewCurveAttributes()
    ca.rangeScale = ca.LOG if rs == 'log' else ca.LINEAR
    ca.domainScale = ca.LOG if ds == 'log' else ca.LINEAR

    co = _new_curve_plot_object()
    co['range_scale'] = rs
    co['domain_scale'] = ds

    return ca, co


def _new_curve_plot_object():
    return {
        'type': 'curve',
        'variable': '',
        'range_sclae': '',
        'domain_scale': '',
    }


def is_curve_plot(plot_obj):
    if 'type' in plot_obj and plot_obj['type'] == 'curve':
        return True
    else:
        return False


def set_curve_plot_variable(plot_obj, var):
    plot_obj['variable'] = var
