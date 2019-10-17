import os, glob, re


try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _open_database(chombo_path):
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

    _new_expressions(vars)


def _change_state(state):
    nstates = visit.GetDatabaseNStates()

    while state < 0 or state >= nstates:
        if state < 0:
            state += nstates
        elif state >= nstates:
            state -= nstates

    if visit.SetTimeSliderState(state) != 1:
        raise RuntimeWarning('Unable to change database state to:', state)


def _new_expressions(vars):
    if 'rho' not in vars:
        return

    rho2v2 = ''

    # Momenta
    for rhov in ['rho_u', 'rho_v', 'rho_w']:
        if rhov in vars:
            visit.DefineScalarExpression(rhov[-1], rhov + ' / rho')
            rho2v2 += rhov + '^2' if len(rho2v2) < 1 else ' + ' + rhov + '^2'

    if len(rho2v2) < 1 or 'e_tot' not in vars:
        return

    visit.DefineScalarExpression('rho2v2', rho2v2)
    visit.DefineScalarExpression('v2', rho2v2 + ' / rho^2')
    visit.DefineScalarExpression('|v|', 'sqrt(v2)')

    visit.DefineScalarExpression('e_kin', '0.5 * rho2v2 / rho')
    visit.DefineScalarExpression('e_int', 'e_tot - e_kin')

    visit.DefineScalarExpression('p_mon', 'e_int * (5.0/3 - 1)')
    visit.DefineScalarExpression('p_di', 'e_int * (7.0/5 - 1)')
    visit.DefineScalarExpression('p', 'p_mon')
