try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _attr(p1, p2, w, c, o, ba, ea):
    """
    Parameter
    p1, p2: Begin/end points
    w: width
    c: color
    o: opacity
    ba: Begin arrow
    ea: End arrow
    """
    ao = visit.CreateAnnotationObject('Line2D')

    ao.visible = 1
    ao.active = 1
    ao.position = p1
    ao.position2 = p2
    ao.width = w
    ao.color = c
    ao.opacity = o
    ao.beginArrow = ba
    ao.endArrow = ea

    return ao
