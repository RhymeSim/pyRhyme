try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _attr(variable, scaling, zmin, zmax, ct, invert_ct):
    """
    Creating pseudocolor objects
    """
    psa = visit.PseudocolorAttributes()

    if scaling == 'log':
        psa.scaling = psa.Log
    elif scaling == 'linear':
        psa.scaling = psa.Linear
    elif scaling in [psa.Linear, psa.Log, psa.Skew]:
        psa.scaling = scaling
    else:
        raise RuntimeWarning('Unknonw scaling', scaling)


    psa.minFlag = 0 if zmin is None else 1
    psa.min = zmin if zmin is not None else 0
    psa.maxFlag = 0 if zmax is None else 1
    psa.max = zmax if zmax is not None else 0
    psa.colorTableName = ct
    psa.invertColorTable = invert_ct

    return psa


def _colortable():
    """
    Make a color table based on the histogram of data
    check this: https://www.visitusers.org/index.php?title=Creating_a_color_table
    and this: https://www.visitusers.org/index.php?title=Converting_color_tables
    """
    pass


def _set_colortable(ct, scaling, invert=0):
    p = visit.PseudocolorAttributes()
    p.colorTableName = ct
    p.scaling = scaling
    p.invertColorTable = invert
    visit.SetPlotOptions(p)



def _check(plot_obj):
    return True if 'type' in plot_obj and plot_obj['type'] == 'Pseudocolor' else False
