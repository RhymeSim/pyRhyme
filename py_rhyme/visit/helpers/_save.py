try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _attr(d, id, v, c, t, w_in, h_in, dpi):
    """
    d: directory
    id: unique version id string
    c, t: cycle, time
    v: variable name
    w_in, h_in: width, height in inch
    dpi: dot per inch
    """
    attr = visit.SaveWindowAttributes()

    if type(d) is str:
        attr.outputToCurrentDirectory = 0
        attr.outputDirectory = d
    else:
        attr.outputToCurrentDirectory = 1
        attr.outputDirectory = "./"

    attr.fileName = __filename(id, v, c, t)
    attr.format = attr.PNG
    attr.family = 0
    attr.width = w_in * dpi
    attr.height = h_in * dpi
    attr.quality = dpi
    attr.compression = attr.PackBits

    return attr


def __filename(id, v, c, t):
    return '{:s}_{:s}_{:05d}_{:.2e}'.format(id, v, c, t)
