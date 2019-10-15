try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def pseudocolor_plot_attr(variable, scaling, zmin, zmax, ct, invert_ct):
    """
    Creating pseudocolor objects
    """
    psa = visit.PseudocolorAttributes()

    if scaling == 'log':
        psa.scaling = psa.Log
    elif scaling == 'linear':
        psa.scaling = psa.Linear
    else:
        raise RuntimeWarning('Unknonw scaling', scaling)

    psa.minFlag = 0 if zmin is None else 1
    psa.min = zmin if zmin is not None else 0
    psa.maxFlag = 0 if zmax is None else 1
    psa.max = zmax if zmax is not None else 0
    psa.colorTableName = ct
    psa.invertColorTable = invert_ct

    pso = _new_pseudocolor_object()
    pso['variable'] = variable
    pso['scaling'] = scaling
    pso['min'] = zmin
    pso['max'] = zmax
    pso['ct'] = ct
    pso['invert_ct'] = invert_ct

    return psa, pso


def pseudocolor_plot_colortable():
    """
    Make a color table based on the histogram of data
    check this: https://www.visitusers.org/index.php?title=Creating_a_color_table
    and this: https://www.visitusers.org/index.php?title=Converting_color_tables
    """
    pass


def is_pseudocolor_plot(plot_obj):
    """
    Return True if the object is a pseudocolor object
    """
    if 'type' in plot_obj and plot_obj['type'] == 'pseudocolor':
        return True
    else:
        return False


def set_pseudocolor_plot_colortable(plot_obj, ct):
    plot_obj['ct'] = ct


def set_pseudocolor_plot_variable(plot_obj, var):
    plot_obj['variable'] = var


def _new_pseudocolor_object():
    return {
        'type': 'pseudocolor',
        'variable': '',
        'scaling': '',
        'min': 0,
        'max': 0,
        'ct': '',
        'invert_ct': 0
    }
