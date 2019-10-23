try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _define(vars):
    # Adding time derivatives
    for v in vars:
        __add_derivatives(v)

    if 'rho' not in vars:
        return

    rho2v2 = ''

    # Momenta
    for rhov in ['rho_u', 'rho_v', 'rho_w']:
        if rhov in vars:
            visit.DefineScalarExpression(rhov[-1], rhov + ' / rho')
            __add_derivatives(rhov[-1])
            rho2v2 += rhov + '^2' if len(rho2v2) < 1 else ' + ' + rhov + '^2'

    if len(rho2v2) < 1 or 'e_tot' not in vars:
        return

    visit.DefineScalarExpression('rho2v2', rho2v2)
    __add_derivatives('rho2v2')
    visit.DefineScalarExpression('v2', rho2v2 + ' / rho^2')
    __add_derivatives('v2')
    visit.DefineScalarExpression('|v|', 'sqrt(v2)')
    __add_derivatives('|v|')

    visit.DefineScalarExpression('e_kin', '0.5 * rho2v2 / rho')
    __add_derivatives('e_kin')
    visit.DefineScalarExpression('e_int', 'e_tot - e_kin')
    __add_derivatives('e_int')

    visit.DefineScalarExpression('p_mon', 'e_int * (5.0/3 - 1)')
    __add_derivatives('p_mon')
    visit.DefineScalarExpression('p_di', 'e_int * (7.0/5 - 1)')
    __add_derivatives('p_di')
    visit.DefineScalarExpression('p', 'p_mon')
    __add_derivatives('p')


def __add_derivatives(v):
    visit.DefineScalarExpression(v + '.', __dot_expr(v))
    visit.DefineScalarExpression(v + '..', __ddot_expr(v))

def __dot_expr(v):
    return '(<' + v + '> - pos_cmfe(<[-1]id:' + v + '>, Mesh, 0.)) ' \
        + '/ (<time_derivative/Mesh_time> - <time_derivative/Mesh_lasttime>)'

def __ddot_expr(v):
    return '(pos_cmfe(<[1]id:' + v + '>, Mesh, 0.) - 2 * <' + v + '> ' \
        + '+ pos_cmfe(<[-1]id:' + v + '>, Mesh, 0.)) ' \
        + '/ (<time_derivative/Mesh_time> - <time_derivative/Mesh_lasttime>)^2'
