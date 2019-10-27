"""
_lineout helper

NB: Right now this helper only works on uniform grids
"""


def _populate(p0, p1, dimensions, sampling=1000):
    """
    Parameter
    p0, p1: Normalized position of the ends of the line, e.g. (0.02, 0.4)
    dimensions: dimensions of the grid
    sampling: number of dots on the final line
    """
    if len(p0) != len(p1) != 3:
        raise RuntimeError('Only 3D points!', p0, p1)

    X0 = [p[i] * dimension[i] for i in range(len(p0))]
    X1 = [p[i] * dimension[i] for i in range(len(p1))]

    dots = __walk(X0, X1)


def __walk(X0, X1):
    pass
