try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def pseudocolor_attr(scaling, zmin, zmax, ct, invert_ct):
    """
    Creating pseudocolor objects
    """
    psa = visit.PseudocolorAttributes()
    psa.scaling = psa.Log if scaling is 'log' else psa.Linear
    psa.minFlag = 0 if zmin is None else 1
    psa.min = zmin if zmin is not None else 0
    psa.maxFlag = 0 if zmax is None else 1
    psa.max = zmax if zmax is not None else 0
    psa.colorTableName = ct
    psa.invertColorTable = invert_ct

    return psa


def pseudocolor_colortable():
    """
    Make a color table based on the histogram of data
    check this: https://www.visitusers.org/index.php?title=Creating_a_color_table
    and this: https://www.visitusers.org/index.php?title=Converting_color_tables
    """
    pass
