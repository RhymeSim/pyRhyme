import re

from .api import Chombo
from .api import Expression

from .helpers import _lineout


class PyRhyme:
    """
    Reading and maniputaling Rhyme chombo outputs
    """

    def __init__(self, path):
        """
        Initializing a PyRhyme object by:
        - opening a dataset
        - loading the specified chombo file
        """
        self.ds = Chombo(path)
        self.exprs = Expression(self.ds.active()['h5']['attrs']['components'])


    def lineout(self, p1, p2, variable, n_intervals=1024):
        line = _lineout._sample(
            p1, p2, self.ds.problem_domain(), self.ds.dx(0), n_intervals)

        id = self.ds.active_snap
        dot = self.exprs.dot(variable)

        if dot < 0 or dot > 1:
            raise RuntimeError('Requested time derivative has not implemented!')

        y = { x: { 't': 0.0, 'p': [] } for x in [-1, 0, 1] }

        y[0]['p'] = self.ds.pick(line['coords'], self.exprs.id(variable))
        y[0]['t'] = self.ds.time()

        if dot >= 1:
            self.ds.jump_to(id - 1)
            y[-1]['p'] = self.ds.pick(line['coords'], self.exprs.id(variable))
            y[-1]['t'] = self.ds.time()

        self.ds.jump_to(id)

        if dot == 0:
            ys = y[0]['p']
        elif dot == 1:
            dt = y[0]['t'] - y[-1]['t']
            ys = [(p - pm1) / dt for p, pm1 in zip(y[0]['p'], y[-1]['p'])]

        return { 'x': line['x'], 'y': ys }
