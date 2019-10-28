from .helpers import _dataset
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
        self.d = _dataset._open(path)


    def _active_h5(self):
        h5 = self.d[self.d['state']['active']]

        if not h5['opened']:
            h5 = _dataset._open_individual_h5[h5['path']]

        return h5['h5']


    def _pick(self, coord, variable):
        """
        NB: Only works on single level, single box datasets
        TODO: Make this AMR compatible
        """
        h5 = self._active_h5()

        try:
            i = h5['attr']['comp'].index(variable)
        except Exception as err:
            print('Unknown variable!', variable)
            return

        grid = h5['attr']['ProblemDomain']

        id = coord[0] + coord[1] * grid[1] + coord[2] * grid[1] * grid[2]
        id += i * h5['levels'][0]['len_data']

        return h5['levels'][0]['data'][id]


    def lineout(self, p1, p2, variable):
        h5 = self._active_h5()

        sample = _lineout._sample(
            p1, p2, h5['attr']['ProblemDomain'], h5['levels'][0]['dx'])

        line = [
            (sample[i]['dist'], self._pick(sample[i]['coord'], variable))
            for i in range(sample['len'])
        ]

        return line, sample
