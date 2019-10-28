import re


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


    def _active_id(self):
        return self.d['state']['active']


    def _active_h5(self):
        h5 = self.d[self._active_id()]

        if not h5['opened']:
            h5['h5'] = _dataset._open_individual_h5[h5['path']]

        return h5


    def _get_h5(self, id):
        if id < 0 or id > self.d['info']['num_of_files']:
            raise RuntimeError('Out of range file id!', id)

        h5 = self.d[id]

        if not h5['opened']:
            h5['h5'] = _dataset._open_individual_h5(h5['path'])

        return h5


    def _parse_variable(self, variable):
        if re.match('[a-zA-Z0-9_]*\.\.$', variable):
            v = variable[:-2]
            time_derivative = 2
        elif re.match('[a-zA-Z0-9_]*\.$', variable):
            v = variable[:-1]
            time_derivative = 1
        else:
            v = variable
            time_derivative = 0

        return v, time_derivative


    def _variable_id(self, variable):
        h5 = self._active_h5()['h5']

        if variable in h5['attr']['comp']:
            return h5['attr']['comp'].index(variable)

        return None


    def _coordinate_to_id(self, coord):
        grid = self._active_h5()['h5']['attr']['ProblemDomain']
        return coord[0] + coord[1] * grid[1] + coord[2] * grid[1] * grid[2]


    def _pick(self, coord, variable):
        """
        NB: Only works on single level, single box datasets
        TODO: Make this AMR compatible
        """
        h5 = self._active_h5()['h5']

        v, d = self._parse_variable(variable)
        i = self._variable_id(v)

        id = self._coordinate_to_id(coord)
        id += i * h5['levels'][0]['len_data']

        if d == 2:
            h5m1 = self._get_h5(self._active_id() - 1)['h5']
            h5p1 = self._get_h5(self._active_id() + 1)['h5']
            return (
                h5p1['levels'][0]['data'][id]
                - 2 * h5['levels'][0]['data'][id]
                + h5p1['levels'][0]['data'][id]
            ) / (
                h5['attr']['time'] - h5m1['attr']['time']
            )**2

        elif d == 1:
            h5m1 = self._get_h5(self._active_id() - 1)['h5']
            return (
                h5['levels'][0]['data'][id]
                - h5m1['levels'][0]['data'][id]
            ) / (
                h5['attr']['time'] - h5m1['attr']['time']
            )

        else:
            return h5['levels'][0]['data'][id]


    def lineout(self, p1, p2, variable):
        h5 = self._active_h5()['h5']

        sample = _lineout._sample(
            p1, p2, h5['attr']['ProblemDomain'], h5['levels'][0]['dx'])

        line = {
            'x': [sample[i]['dist'] for i in range(sample['len'])],
            'y': [self._pick(sample[i]['coord'], variable) for i in range(sample['len'])],
        }

        return line, sample
