import time, copy, os
from .helpers.pseudocolor_plot_helper import pseudocolor_plot_attr, \
    is_pseudocolor_plot, set_pseudocolor_plot_colortable, \
    set_pseudocolor_plot_variable
from .helpers.curve_plot_helper import curve_plot_attr, is_curve_plot, \
    set_curve_plot_variable
from .helpers.slice_operator_helper import slice_operator_attr, \
    is_slice_operator
from .helpers.draw_plots_helper import draw_plots_attr
from .helpers.line_helper import new_line

from ._database_handler import _open_database

try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


class VisItAPI:
    """
    VisIt wrapper
    """

    METADATA = {
        'windows': [],
    }

    SCALING_TYPES = { 'log': 1, 'linear': 2 }


    def __init__(self, interactive=True):
        """
        Parameter
        interactive: If False, VisIt viewer will be shut down
        """

        if not interactive: visit.AddArgument("-nowin")

        if visit.Launch() != 1:
            raise RuntimeError('Unable to launch VisIt.')

        visit.SetTreatAllDBsAsTimeVarying(1)
        visit.SetQueryOutputToObject()

        self.metadata = self.METADATA
        self.metadata['windows'].append(self._new_window_object())


    def open(self, path):
        path, id, cycle, cycles, times, vars = _open_database(path)

        wid = self.active_window_id()
        self.metadata['windows'][wid]['database'] = path
        self.metadata['windows'][wid]['id'] = id
        self.metadata['windows'][wid]['cycle'] = cycle
        self.metadata['windows'][wid]['cycles'] = cycles
        self.metadata['windows'][wid]['ncycles'] = len(cycles)
        self.metadata['windows'][wid]['times'] = times
        self.metadata['windows'][wid]['variables'] = vars


    def cycle(self, c):
        """
        Changing the snapshot to a given cycle index
        """
        if not self.is_window_drawn():
            raise RuntimeWarning('Window is not drawn!')
            return

        n_cycles = visit.GetDatabaseNStates()

        if not 0 <= c < n_cycles:
            raise RuntimeWarning('Out of range of cycles!', c, ' out of ', n_cycles)

        if visit.SetTimeSliderState(c) != 1:
            raise RuntimeWarning('Unable to change database state to:', c)

        wid = self.active_window_id()
        self.metadata['windows'][wid]['cycle'] = c


    def next_cycle(self):
        visit.TimeSliderNextState()


    def prev_cycle(self):
        visit.TimeSliderPreviousState()


    def time(self, t):
        """
        Changing the snapshot with the closes time to t

        NB: We assme the list of times is not sorted!
        """
        wid = self.active_window_id()
        diff = [abs(t - time) for time in self.metadata['windows'][wid]['times']]

        cycle = diff.index(min(diff))

        self.cycle(cycle)


    def pseudocolor(self, var, scaling='log', zmin=None, zmax=None,
        ct='RdYlBu', invert_ct=0):
        """
        Adding a Pseudocolor plot

        Parameter
        var: Variable to be plotted
        scaling: log, linear
        ct: Name of color table to be used
        invert_ct: If 1, colors will be inverted

        TODO
        if var is all, plot all variables:
            SetActivePlots((0,1,2))
        GetNumPlots()
        """
        if visit.AddPlot( 'Pseudocolor', var, 1, 1 ) != 1:
            raise RuntimeWarning('Unable to add Pseudocolor plot.')

        psa, pso = pseudocolor_plot_attr(var, scaling, zmin, zmax, ct, invert_ct)
        visit.SetPlotOptions(psa)

        wid = self.active_window_id()
        self.metadata['windows'][wid]['plots'].append(pso)
        set_pseudocolor_plot_variable(
            self.metadata['windows'][wid]['plots'][-1], var)


    def pseudocolor_try_colortables(self, sleep=1.5):
        """Trying all available colorTables on an **already drawn** plot"""
        if not self.is_window_drawn():
            raise RuntimeWarning('Window is not drawn!')
            return

        p = visit.PseudocolorAttributes()

        ct_orig = visit.GetActiveContinuousColorTable()
        invrt_orig = p.invertColorTable
        scaling_orig = p.scaling

        for ct in visit.ColorTableNames():
            for invrt in (0, 1):
                print('Trying:', ct, 'invert', invrt)

                p.colorTableName = ct
                p.invertColorTable = invrt
                p.scaling = scaling_orig
                visit.SetPlotOptions(p)

                time.sleep(sleep)

        p.colorTableName = ct_orig
        p.invertColorTable = invrt_orig
        p.scaling = scaling_orig
        visit.SetPlotOptions(p)


    def pseudocolor_colortable(self, ct):
        """Changing a pseudocolor plot color table"""
        wid = self.active_window_id()
        pid = pseudocolor_plotid(wid)

        if pid < 0:
            raise RuntimeError('No pseudocolor found in this window!')

        if ct not in visit.ColorTableNames():
            raise RuntimeError('Color table not found!')

        p = visit.PseudocolorAttributes()
        p.colorTableName = ct
        visit.SetPlotOptions(p)

        set_pseudocolor_plot_colortable(
            self.metadata['windows'][wid]['plots'][pid], ct)


    def pseudocolor_plotid(wid):
        for i, plot in enumerate(self.metadata['windows'][wid]['plots']):
            if is_pseudocolor_plot(plot):
                return i

        return -1


    def slice(self, origin_type='Percent', val=50, axis_type='ZAxis', all=1):
        """
        Adding a slice operator

        Parameter
        all: If 1, the operator will be applied to all plots
        origin_type: Type of slicing (Intercept, Point, Percent, Zone, Node)
        val: Argument of origin,
            Intercept: <Number>
            Point: <list Number, Number, Number>
            Percent: <Number>
            Zone: <Number>
            Node: <Number>
        axis_type: XAxis, YAxis, ZAxis
        """
        if visit.AddOperator('Slice', all) != 1:
            raise RuntimeWarning('Unable to add Slice operator')

        sa, so = slice_operator_attr(origin_type, val, axis_type)
        visit.SetOperatorOptions(sa)

        wid = self.active_window_id()
        self.metadata['windows'][wid]['operators'].append(so)
        self.metadata['windows'][wid]['drawn'] = False


    def draw(self, xtitle='X', xunit='Mpc', xscale='linear', xmin=None, xmax=None,
        ytitle='Y', yunit='Mpc', yscale='linear', ymin=None, ymax=None,
        color=(0, 0, 0, 255), bg=(255, 255, 255, 255), fg=(0, 0, 0, 255)):
        """
        Drawing plots on VisIt viewer
        """
        if visit.DrawPlots() != 1:
            raise RuntimeWarning('Unable to draw plots.')

        se = self.query('SpatialExtents')['extents']

        aa, v2da = draw_plots_attr(xtitle, xunit, xscale, xmin, xmax,
        ytitle, yunit, yscale, ymin, ymax, color, bg, fg, se)

        visit.SetAnnotationAttributes(aa)
        visit.SetView2D(v2da)

        wid = self.active_window_id()
        self.metadata['windows'][wid]['drawn'] = True


    def redraw(self, variable=None, scaling=None, zmin=None, zmax=None, ct=None,
        origin_type=None, val=None, axis_type=None):
        wid = self.active_window_id()

        if len(self.metadata['windows'][wid]['plots']) < 1:
            raise RuntimeError('No plots found in this window!')

        plots = copy.deepcopy(self.metadata['windows'][wid]['plots'])
        operators = copy.deepcopy(self.metadata['windows'][wid]['operators'])

        if visit.DeleteActivePlots() != 1:
            raise RuntimeError('Unable to delete mesh plots!')
        if visit.DeleteAllPlots() != 1:
            raise RuntimeError('Unable to delete pseudocolor and contour plots')

        self.metadata['windows'][wid]['plots'] = []
        self.metadata['windows'][wid]['operators'] = []

        for p in plots:
            if is_pseudocolor_plot(p):
                var = p['variable'] if variable is None else variable
                sc = p['scaling'] if scaling is None else scaling
                zmn = p['min'] if zmin is None else zmin
                zmx = p['max'] if zmax is None else zmax
                ct = p['ct'] if ct is None else ct
                self.pseudocolor(var, scaling=sc, zmin=zmn, zmax=zmx,
                    ct=ct, invert_ct=p['invert_ct'])
            elif is_curve_plot(p):
                pass

        for o in operators:
            if is_slice_operator(o):
                ot = o['origin_type'] if origin_type is None else origin_type
                v = o['value'] if val is None else val
                at = o['axis_type'] if axis_type is None else axis_type
                self.slice(origin_type=ot, val=v, axis_type=at)


    def change_variable(self, variable):
        self.redraw(variable=variable)


    def change_scaling(self, scaling):
        self.redraw(scaling=scaling)


    def change_layer(self, layer, origin_type=None, axis_type=None):
        self.redraw(origin_type=origin_type, val=layer, axis_type=None)


    def line(self, p1=(0.75, 0.75), p2=(0.75, 0.75), width=1,
        color=(0, 0, 0, 255), opacity=255, begin_arrow=0, end_arrow=0):
        """
        Drawing a line

        Parameter
        p1, p2: Start and ending points, <tuple float, float>
        width: 0 < <float> < 1
        color: 0 < <quadruple int, int, int, int> < 255
        opacity: 0 < <int> < 255
        begin_arrow: Add arrow shape to the begining of the line, 0 or 1
        end_arrow: Add arrow shape to the end of the line, 0 or 1

        Return
        Line name, annotation object
        """

        ao = new_line(p1, p2, width, color, opacity, begin_arrow, end_arrow)


    def invert(self):
        """Inverting background and foreground colors"""
        visit.InvertBackgroundColor()


    def query(self, q=''):
        """
        Run a Query

        Parameter
        q: Query string
        """
        queries = visit.Queries()

        if q in queries:
            return visit.Query(q)
        else:
            raise RuntimeWarning('Invalid query!')


    def query_over_time(self, q='', range_scale='log', domain_scale='linear'):
        queries = visit.QueriesOverTime()

        if q in queries:
            aw = self.active_window()

            if visit.QueryOverTime(q) != 1:
                raise RuntimeWarning('Unable to run the query_over_time:', q)

            window_id = visit.GetQueryOverTimeAttributes().windowId
            visit.SetActiveWindow(window_id)

            pi = visit.GetPlotInformation()
            pi['windowId'] = window_id

            visit.SetActiveWindow(aw)
            return pi
        else:
            raise RuntimeWarning('Invalid query_over_time!')


    def minimum_over_time(self):
        """
        TODO:
        ViewCurveAttributes
        SetViewCurve
        """
        cmin = self.query_over_time('Min')
        cmin['min'] = min(cmin['Curve'][1::2])
        return cmin


    def maximum_over_time(self):
        cmax = self.query_over_time('Max')
        cmax['max'] = max(cmax['Curve'][1::2])
        return cmax


    def _new_window_object(self):
        return {
            'database': '',
            'variables': [],
            'cycle': 0,
            'id': '',
            'plots': [],
            'operators': [],
            'drawn': False,
            'cycles': [],
            'times': [],
        }


    def active_window_id(self):
        ga = visit.GetGlobalAttributes()
        return ga.activeWindow


    def active_window(self):
        ga = visit.GetGlobalAttributes()
        return ga.windows[ga.activeWindow]


    def windows(self):
        return visit.GetGlobalAttributes().windows


    def is_window_drawn(self):
        wid = self.active_window_id()

        if self.metadata['windows'][wid]['drawn']:
            return True
        else:
            return False


    def close(self):
        """
        Closing VisIt windwo
        """
        if visit.Close() != 1:
            raise RuntimeError('Unable to close VisIt.')
