import os, glob, re
from . import _expression


try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _open(chombo_path):
    """
    Opening a chombo database (or file) based on a given path to a chombo file
    """
    matches = re.findall('[0-9]{5}', chombo_path)

    ls = glob.glob(chombo_path.replace(matches[-1], '*'))

    if len(ls) > 1:
        cycle = ls.index(chombo_path)
        path = os.path.splitext(chombo_path.replace(matches[-1], '*'))[0] + ' database'
    else:
        cycle = 0
        path = chombo_path

    if visit.OpenDatabase(path, cycle, 'Chombo') != 1:
        raise RuntimeError('Unable to open database:', path)

    md = visit.GetMetaData(path)

    vars = []
    for i in range(md.GetNumScalars()):
        vars.append(md.GetScalars(i).name)

    _expression._define(vars)


def _change_state(state):
    nstates = visit.GetDatabaseNStates()

    while state < 0 or state >= nstates:
        if state < 0:
            state += nstates
        elif state >= nstates:
            state -= nstates

    if visit.SetTimeSliderState(state) != 1:
        raise RuntimeWarning('Unable to change database state to:', state)
