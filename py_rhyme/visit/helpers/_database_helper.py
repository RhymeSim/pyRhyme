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
        id = os.path.basename(
            os.path.splitext(chombo_path.replace(matches[-1], 'database'))[0]
        ).replace('.', '_')
    else:
        cycle = 0
        path = chombo_path
        id = os.path.basename(chombo_path).replace('.', '_')

    if visit.OpenDatabase(path, cycle, 'Chombo') != 1:
        raise RuntimeError('Unable to open database:', path)

    md = visit.GetMetaData(path)

    vars = []
    for i in range(md.GetNumScalars()):
        vars.append(md.GetScalars(i).name)

    vars = vars + __new_expressions(vars)

    return path, id, cycle, md.cycles, md.times, vars


def _change_state(state):
    nstates = visit.GetDatabaseNStates()

    while state < 0 or state >= nstates:
        if state < 0:
            state += nstates
        elif state >= nstates:
            state -= nstates

    if visit.SetTimeSliderState(state) != 1:
        raise RuntimeWarning('Unable to change database state to:', state)


def __new_expressions(vars):
    extra_vars = []

    if 'rho' not in vars:
        return extra_vars

    rho2v2 = ''

    # Momenta
    for rhov in ['rho_u', 'rho_v', 'rho_w']:
        if rhov in vars:
            visit.DefineScalarExpression(rhov[-1], rhov + ' / rho')
            extra_vars.append(rhov[-1])
            rho2v2 += rhov + '^2' if len(rho2v2) < 1 else ' + ' + rhov + '^2'

    if len(rho2v2) < 1 or 'e_tot' not in vars:
        return extra_vars

    visit.DefineScalarExpression('rho2v2', rho2v2)
    extra_vars.append('rho2v2')
    visit.DefineScalarExpression('v2', rho2v2 + ' / rho^2')
    extra_vars.append('v2')
    visit.DefineScalarExpression('|v|', 'sqrt(v2)')
    extra_vars.append('|v|')


    visit.DefineScalarExpression('e_kin', '0.5 * rho2v2 / rho')
    extra_vars.append('e_kin')
    visit.DefineScalarExpression('e_int', 'e_tot - e_kin')
    extra_vars.append('e_int')
    visit.DefineScalarExpression('p_mon', 'e_int * (5.0/3 - 1)')
    extra_vars.append('p_mon')
    visit.DefineScalarExpression('p_di', 'e_int * (7.0/5 - 1)')
    extra_vars.append('p_di')
    visit.DefineScalarExpression('p', 'p_mon')
    extra_vars.append('p')

    return extra_vars
