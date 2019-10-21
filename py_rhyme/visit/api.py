import time, copy, os
from .helpers import _pseudocolor
from .helpers import _curve_plot
from .helpers import _slice
from .helpers import _draw
from .helpers import _line
from .helpers import _database
from .helpers import _metadata
from .helpers import _lineout

try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


class VisItAPI:
    """
    VisIt wrapper
    """

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


    def open(self, path):
        _database._open(path)

    def cycle(self, c):
        _database._change_state(c)

    def next_cycle(self):
        visit.TimeSliderNextState()

    def prev_cycle(self):
        visit.TimeSliderPreviousState()

    def ncycles(self):
        info = visit.GetWindowInformation()
        return len(visit.GetMetaData(info.activeSource).cycles)

    def current_cycle(self):
        info = visit.GetWindowInformation()
        return info.timeSliderCurrentStates[info.activeTimeSlider]

    def time(self, t):
        """
        Changing the snapshot with the closes time to t

        NB: We assme the list of times is not sorted!
        """
        wid = self.active_window_id()
        md = self.get_metadata()
        diff = [abs(t - time) for time in md['windows'][wid]['times']]
        cycle = diff.index(min(diff))

        self.cycle(cycle)

    def active_window_id(self):
        ga = visit.GetGlobalAttributes()
        return ga.windows[ga.activeWindow]

    def active_window(self):
        ga = visit.GetGlobalAttributes()
        return ga.windows[ga.activeWindow]

    def windows(self):
        return visit.GetGlobalAttributes().windows

    def new_window(self):
        if visit.AddWindow() != 1:
            raise RuntimeWarning('Unable to create a new window!')


    def pseudocolor(self, var, scaling='log', zmin=None, zmax=None,
        ct='RdYlBu', invert_ct=0):
        """
        Parameter
        var: Variable to be plotted
        scaling: log, linear
        ct: Name of the color table to be used
        invert_ct: If 1, color table will be inverted
        """
        if visit.AddPlot( 'Pseudocolor', var, 1, 1 ) != 1:
            raise RuntimeWarning('Unable to add Pseudocolor plot.')

        psa = _pseudocolor._attr(var, scaling, zmin, zmax, ct, invert_ct)
        visit.SetPlotOptions(psa)


    def pseudocolor_try_colortables(self, sleep=1.5):
        """Trying all available colorTables on an **already drawn** plot"""
        md = self.get_metadata()
        orig = self.find_pseudocolor(md['windows'][self.active_window_id]['plots'])

        for ct in visit.ColorTableNames():
            for invert in (0, 1):
                print('Trying:', ct, 'invert', invert)
                _pseudocolor._set_colortable(ct, orig['scaling'], invert)
                time.sleep(sleep)

        _pseudocolor._set_colortable(orig['ct'], orig['scaling'], orig['invert_ct'])


    def pseudocolor_colortable(self, ct):
        """Changing a pseudocolor plot color table"""
        md = self.get_metadata()
        plot = self.find_pseudocolor(md['windows'][self.active_window_id]['plots'])

        if not plot:
            raise RuntimeError('No pseudocolor found in this window!')

        if ct not in visit.ColorTableNames():
            raise RuntimeError('Color table not found!')

        _pseudocolor._set_colortable(ct, plot['scaling'], plot['invert_ct'])


    def find_pseudocolor(self, plots):
        for plot in plots:
            if _pseudocolor._check(plot):
                return plot

        return None


    def slice(self, origin_type='Percent', percent=50, axis_type='ZAxis'):
        """
        Parameter
        origin_type: Type of slicing (Intercept, Point, Percent, Zone, Node)
        percent: Argument of origin,
            Intercept: <Number>
            Point: <list Number, Number, Number>
            Percent: <Number>
            Zone: <Number>
            Node: <Number>
        axis_type: XAxis, YAxis, ZAxis
        """
        if visit.AddOperator('Slice', 0) != 1:
            raise RuntimeWarning('Unable to add Slice operator')

        sa = _slice._attr(origin_type, percent, axis_type)
        visit.SetOperatorOptions(sa)


    def lineout(self, variable, point1, point2, line_color=(0, 0, 0, 255),
        line_width=4):
        if visit.AddPlot('Curve', 'operators/Lineout/' + variable, 1, 1) != 1:
            raise RuntimeWarning('Unable to plot lineout!', variable)

        la, ca = _lineout._attr(point1, point2, lc=line_color, lw=line_width)
        visit.SetOperatorOptions(la)
        visit.SetPlotOptions(ca)


    def draw(self, xtitle='X', xunit='Mpc', xscale='linear', xmin=None, xmax=None,
        ytitle='Y', yunit='Mpc', yscale='linear', ymin=None, ymax=None,
        color=(0, 0, 0, 255), bg=(255, 255, 255, 255), fg=(0, 0, 0, 255)):
        """
        Drawing plots on VisIt viewer
        """
        if visit.DrawPlots() != 1:
            raise RuntimeWarning('Unable to draw plots.')

        se = self.query('SpatialExtents')['extents']

        aa, v2da = _draw._attr(xtitle, xunit, xscale, xmin, xmax,
        ytitle, yunit, yscale, ymin, ymax, color, bg, fg, se)

        visit.SetAnnotationAttributes(aa)
        visit.SetView2D(v2da)


    def redraw(self, variable=None, scaling=None, zmin=None, zmax=None, ct=None,
        origin_type=None, percent=None, axis_type=None):
        wid = self.active_window_id()
        md = self.get_metadata()

        if wid not in md['windows'] or len(md['windows'][wid]['plots']) < 1:
            raise RuntimeError('No plots found in this window!')

        if visit.DeleteActivePlots() != 1:
            raise RuntimeError('Unable to delete mesh plots!')
        if visit.DeleteAllPlots() != 1:
            raise RuntimeError('Unable to delete pseudocolor and contour plots')

        for p in md['windows'][wid]['plots'].values():
            if _pseudocolor._check(p):
                var = p['variable'] if variable is None else variable
                sc = p['scaling'] if scaling is None else scaling
                zmn = p['min'] if zmin is None else zmin
                zmx = p['max'] if zmax is None else zmax
                ct = p['ct'] if ct is None else ct

                self.pseudocolor(var, scaling=sc, zmin=zmn, zmax=zmx,
                    ct=ct, invert_ct=p['invert_ct'])

                for o in p['operators'].values():
                    if _slice._check(o):
                        ot = o['origin_type'] if origin_type is None else origin_type
                        p = o['origin_percent'] if percent is None else percent
                        at = o['axis_type'] if axis_type is None else axis_type
                        self.slice(origin_type=ot, percent=p, axis_type=at)


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
            raise RuntimeWarning('Invalid query!', q)


    def query_over_time(self, q='', range_scale='log', domain_scale='linear'):
        queries = visit.QueriesOverTime()

        if q in queries:
            aw = self.active_window()

            if visit.QueryOverTime(q) != 1:
                raise RuntimeWarning('Unable to run the query_over_time:', q)

            wid = self.active_window_id()
            visit.SetActiveWindow(wid)

            pi = visit.GetPlotInformation()
            pi['windowId'] = wid

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


    def raise_exception_if_window_is_not_drawn(self):
        drawn = True

        for pid in range(visit.GetNumPlots()):
            plot = visit.GetPlotList().GetPlots(pid)
            if plot.plotType != plot.Completed:
                drawn = False

        return drawn


    def get_window_metadata(self, print_it=False, key=None):
        wmd = _metadata._get_window(self.active_window_id())

        if key is None:
            if print_it: print(wmd)
            return wmd
        else:
            if key not in wmd:
                if print_it: print('Unknow key! keys:', wmd.keys())
                return None
            else:
                if print_it: print(wmd[key])
                return wmd[key]


    def get_metadata(self, print_it=False):
        wid = self.active_window_id()
        md = _metadata._get()
        visit.SetActiveWindow(wid)

        if print_it: print(md)

        return md


    def close(self):
        """
        Closing VisIt windwo
        """
        if visit.Close() != 1:
            raise RuntimeError('Unable to close VisIt.')
