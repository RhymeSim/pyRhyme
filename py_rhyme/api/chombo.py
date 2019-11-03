import os, glob, re
import h5py

from functools import reduce

from .helpers import _chombo
from .helpers import _column_major


class Chombo:
    """
    Handling loading/manipulating chombo file(s)

    dataset: stroes chombo HDF5 files
        dataset is immutable, but we lazy loading HDF files
        { id: {
            path: <str>,
            h5: {
                'file': <h5py.File>,
                'attrs': {},
                'levles': {
                    level_id: {
                        dx: <tuple float>,
                        ref_ratio: <float>,
                        data: <numpy.narray>,
                        boxes: {
                            box_id: {
                                center: <tuple float>,
                                offset: <list int>,
                            },
                        },
                    },
                },
            },
        }}

    active_snap: stores id of the currently active snapshot
        the only real class state that we should track of
    """
    dataset = {}
    active_snap = 0


    def __init__(self, path):
        """
        Setting up dataset
        """

        self._orig_path = path

        # Check if there is a dataset
        matches = re.findall('[0-9]{5}', path)
        ls = glob.glob(path.replace(matches[-1], '*')) if matches else [path]

        for i, p in enumerate(ls):
            self.dataset[i] = {}
            self.dataset[i]['path'] = p
            self.dataset[i]['h5'] = {}

        # Setting up the state of the object
        self.active_snap = ls.index(path)


    def _load(self, i):
        """
        Loading the ith chombo file
        """

        if 'h5' in self.dataset[i] and self.dataset[i]['h5'] :
            return

        f = h5py.File(self.dataset[i]['path'], 'r')

        h5 = self.dataset[i]['h5']
        h5['file'] = f
        h5['attrs'] = _chombo._attrs(f)
        h5['levels'] = _chombo._levels(f)

        self.active_snap = i


    def pick(self, points, variable_id):
        """
        points: list of point coordinates
        variable_id: zero-based variable id
        """
        try:
            iter(points[0])
        except TypeError:
            points = [ points ]

        g = self.problem_domain()

        box_len = variable_id * reduce(lambda x, y: x * y, g)

        ids = [
            box_len + _column_major._indices_to_id(p, g)
            for p in points
        ]

        return [self.active()['h5']['levels'][0]['data'][i] for i in ids]


    def active(self):
        """
        Returns currently active snapshot
        """
        self._load(self.active_snap)
        return self.dataset[self.active_snap]


    def jump_to(self, i):
        """
        Returns the ith snapshot
        """
        id = self._snapshot_id(i)
        self.active_snap = id


    def num_of_components(self):
        return self.active()['h5']['attrs']['num_components']


    def time(self):
        return self.active()['h5']['attrs']['time']


    def problem_domain(self):
        return self.active()['h5']['attrs']['ProblemDomain']


    def dx(self, level):
        if level < 0 or level >= len(self.active()['h5']['levels']):
            raise RuntimeError('Out of bound level!', level)

        return self.active()['h5']['levels'][level]['dx']


    def num_of_snapshots(self):
        return len(self.dataset)


    def _snapshot_id(self, id):
        len_dataset = len(self.dataset)

        if id < 0 or id >= len_dataset:
            raise RuntimeError('Invalid snapshot id!', id)
        elif id < 0:
            while id < 0:
                id += len_dataset
        elif id >= len_dataset:
            while id >= len_dataset:
                id -= len_dataset

        return id
