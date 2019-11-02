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


    def lineout(self, p1, p2, variable):
        sample = _lineout._sample(p1, p2, self.ds.problem_domain(), self.ds.dx(0))

        dot = self.exprs.dot(variable)

        id = self.ds.active_snap

        y = {
            -1: { 't': 0.0, 'p': [] },
            0: { 't': 0.0, 'p': [] },
            1: { 't': 0.0, 'p': [] }
        }

        if dot < 0 or dot > 2:
            raise RuntimeError('Requested time derivative has not implemented!')

        if dot >= 0:
            y[0]['p'] = self.ds.pick(sample['coords'], self.exprs.id(variable))
            y[0]['t'] = self.ds.time()
        elif dot >= 1:
            self.ds.jump_to(id - 1)
            y[-1]['p'] = self.ds.pick(sample['coords'], self.exprs.id(variable))
            y[-1][t] = self.ds.time()
        elif dot >= 2:
            self.ds.jump_to(id + 1)
            y[1]['p'] = self.ds.pick(sample['coords'], self.exprs.id(variable))
            y[1]['t'] = self.ds.time()


        if dot == 0:
            ys = y[0]['p']
        elif dot == 1:
            dt = y[0]['t'] - y[1]['t']
            ys = [(p - pm1) / dt for p, pm1 in zip(y[0]['p'], y[-1]['p'])]
        elif dot == 2:
            dt2 = (y[0]['t'] - y[1]['t'])**2
            ys = [(pp1 - 2 * p + pm1) / dt2
                for pp1, p, pm1 in zip(y[1]['p'], y[0]['p'], y[-1]['p'])]

        return { 'x': sample['x'], 'y': ys }
