from ..main import PyRhyme
from py_rhyme.tests.chombo import *

def test_main_init():
    rhyme = PyRhyme(TEST_CHOMBO_PATH)

    assert (rhyme.snap['attr']['problem_domain'] == GRID).all()

    assert rhyme.snap['attr']['num_levels'] == NUM_LEVELS
    assert rhyme.snap['attr']['num_components'] == NUM_COMPONENTS

    for i in range(NUM_COMPONENTS):
        assert rhyme.snap['attr']['component_%d' % i] == FIELDS[i]

    assert rhyme.snap['attr']['iteration'] == ITERATION
    assert rhyme.snap['attr']['time'] == TIME

    assert rhyme.snap['levels'][0]['dx'] == tuple([ l / g for l, g in zip(LENGTHS, GRID)])
    assert rhyme.snap['levels'][0]['ref_ratio'] == 2.0

    assert rhyme.snap['levels'][0]['boxes']['max'] == 0
    assert rhyme.snap['levels'][0]['boxes'][0]['corner'][3:6] == tuple([ g - 1 for g in GRID ])
    assert len(rhyme.snap['levels'][0]['boxes'][0]['offset']) == NUM_COMPONENTS

    assert len(rhyme.snap['levels'][0]['data']) == len(FIELDS) * GRID[0] * GRID[1] * GRID[2]
