#!/usr/bin/env python

import h5py
import numpy as np

GRID = [16, 16, 16]
LENGTHS = [1.0, 1.0, 1.0]
FILENAME = 'py_rhyme/tests/assets/3d.chombo.h5'


def create():
    """Creating a chombo file based on above constants."""

    grid = GRID
    lengths = LENGTHS
    filename = FILENAME

    box_dtype = [
        ('lo_i', np.int),
        ('lo_j', np.int),
        ('lo_k', np.int),
        ('hi_i', np.int),
        ('hi_j', np.int),
        ('hi_k', np.int),
    ]

    chombo = h5py.File(filename, 'w')

    chombo.attrs['ProblemDomain'] = np.array(grid, dtype=np.int)

    chombo.attrs['component_0'] = np.string_('field_0')
    chombo.attrs['component_1'] = np.string_('field_1')
    chombo.attrs['num_levels'] = 1
    chombo.attrs['num_components'] = 2

    chombo.attrs['iteration'] = 1
    chombo.attrs['time'] = 1.23e4

    chombo_global = chombo.create_group('Chombo_global')
    chombo_global.attrs['SpaceDim'] = [3]

    # level 0
    lev_0 = chombo.create_group('level_0')
    box_0 = ( 0, 0, 0, grid[0] - 1, grid[1] - 1, grid[2] - 1 )
    data_0_field_0 = [
        1 * 1e2 + i * 1 + j * 1e-2 + k * 1e-4
        for i in range(grid[0])
        for j in range(grid[1])
        for k in range(grid[2])
    ]
    data_0_field_1 = [
        2 * 1e2 + i * 1 + j * 1e-2 + k * 1e-4
        for i in range(grid[0])
        for j in range(grid[1])
        for k in range(grid[2])
    ]

    lev_0.attrs['dx'] = [ l / g for l, g in zip(lengths, grid) ]
    lev_0.attrs['prob_domain'] = np.array([box_0], dtype=box_dtype)
    lev_0.attrs['ref_ratio'] = [2.0]

    boxes_0 = lev_0.create_dataset('boxes', (1,), dtype=box_dtype)
    boxes_0[0] = box_0

    lev_0['data:datatype=0'] = data_0_field_0 + data_0_field_1

    chombo.close()
