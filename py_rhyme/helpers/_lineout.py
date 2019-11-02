"""
_lineout helper

NB: Right now this helper only works on uniform grids
"""

from math import sqrt


def _sample(p0, p1, grid, dx, n_intervals):
    """
    Parameter
    p0, p1: Normalized position of the ends of the line, e.g. (0.02, 0.76, 0.4)
    grid: dimensions of the grid
    dx: cell sizes of the uniform grid
    n_intervals: number of intervals between p1 and p0
    """
    if len(p0) != len(p1) != 3:
        raise RuntimeError('Only 3D points!', p0, p1)

    X0 = [p * g * d for p, g, d in zip(p0, grid, dx)]
    X1 = [p * g * d for p, g, d in zip(p1, grid, dx)]

    dl_vec = [(x1 - x0) / n_intervals for x0, x1 in zip(X0, X1)]
    dl = sqrt(sum([x**2 for x in dl_vec]))

    actual_coords = [
        [x0 + i * l for x0, l in zip(X0, dl_vec)]
        for i in range(n_intervals + 1)
    ]

    return {
        'x': [i * dl for i in range(n_intervals + 1)],
        'actual_coords': actual_coords,
        'coords': [
            [int(max(0, x - 1e-5*x) / d) for x, d in zip(act, dx)]
            for act in actual_coords
        ]
    }


def _segment(p0, p1, grid):
    """
    Returns segments of the line between p0 and p1 based on the intersection of
    the line and the mesh
    """
    pass
