try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _attr(d, id, c, w_in, h_in, dpi):
    """
    d: directory
    id: unique version id string
    c: cycle
    w_in, h_in: width, height in inch
    dpi: dot per inch
    """
    attr = visit.SaveWindowAttributes()

    if type(d) is str:
        attr.outputToCurrentDirectory = 0
        attr.outputDirectory = d
    else:
        attr.outputToCurrentDirectory = 1
        attr.outputDirectory = "."

    attr.fileName = __filename(id, c)
    attr.format = attr.PNG
    attr.family = 0
    attr.width = w_in * dpi
    attr.height = h_in * dpi
    attr.quality = dpi
    attr.compression = attr.PackBits

    return attr


def __filename(id, c):
    return id + '_' + ('%05d' % c)
