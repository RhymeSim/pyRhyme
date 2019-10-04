#!/usr/bin/env python

import h5py
import numpy as np

GRID = [16, 16, 16]
LENGTHS = [1.0, 1.0, 1.0]
FIELDS = ( 'field_0', 'field_1' )
NUM_COMPONENTS = len(FIELDS)
ITERATION = 123
TIME = 2.34e5
DIMENTIONALITY = 3
NUM_LEVELS = 1
TEST_CHOMBO_PATH = 'py_rhyme/tests/assets/3d.chombo.h5'


def create():
    """Creating a chombo file based on above constants."""

    box_dtype = [
        ('lo_i', np.int),
        ('lo_j', np.int),
        ('lo_k', np.int),
        ('hi_i', np.int),
        ('hi_j', np.int),
        ('hi_k', np.int),
    ]

    chombo = h5py.File(TEST_CHOMBO_PATH, 'w')

    chombo.attrs['ProblemDomain'] = np.array(GRID, dtype=np.int)

    for i, f in enumerate(FIELDS):
        chombo.attrs['component_%d' % i] = np.string_(FIELDS[i])

    chombo.attrs['num_levels'] = NUM_LEVELS
    chombo.attrs['num_components'] = NUM_COMPONENTS

    chombo.attrs['iteration'] = ITERATION
    chombo.attrs['time'] = TIME

    chombo_global = chombo.create_group('Chombo_global')
    chombo_global.attrs['SpaceDim'] = DIMENTIONALITY

    # level 0
    lev_0 = chombo.create_group('level_0')
    box_0 = ( 0, 0, 0, GRID[0] - 1, GRID[1] - 1, GRID[2] - 1 )
    data_0 = []

    for i in range(len(FIELDS)):
        data_0.append([
            i * 1e2 + i * 1 + j * 1e-2 + k * 1e-4
            for i in range(GRID[0])
            for j in range(GRID[1])
            for k in range(GRID[2])
        ])

    lev_0.attrs['dx'] = [ l / g for l, g in zip(LENGTHS, GRID) ]
    lev_0.attrs['prob_domain'] = box_0 # np.array([box_0], dtype=box_dtype)
    lev_0.attrs['ref_ratio'] = [2.0]

    boxes_0 = lev_0.create_dataset('boxes', (1,), dtype=box_dtype)
    boxes_0[0] = box_0

    lev_0['data:datatype=0'] = sum(data_0, [])

    chombo.close()
