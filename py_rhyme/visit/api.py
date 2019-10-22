import time, copy, os, re
from pprint import pprint

from .helpers import _pseudocolor
from .helpers import _curve
from .helpers import _slice
from .helpers import _view
from .helpers import _line
from .helpers import _database
from .helpers import _metadata
from .helpers import _lineout
from .helpers import _annotation

try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


class VisItAPI:

    def __init__(self, interactive=True):
        """
        interactive: If False, VisIt viewer will be shut down
        """
        if not interactive: visit.AddArgument("-nowin")

        if visit.Launch() != 1:
            raise RuntimeError('Unable to launch VisIt.')

        visit.SetTreatAllDBsAsTimeVarying(1)
        visit.SetQueryOutputToObject()


    def open(self, path):
        _database._open(path)


    def cycle(self, c, reset_view=False):
        _database._change_state(c)
        if reset_view:
            self.reset_view()


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
        wid = self.active_window_id()
        md = self.get_metadata()
        diff = [abs(t - time) for time in md['windows'][wid]['times']]
        cycle = diff.index(min(diff))

        self.cycle(cycle)


    def active_window_id(self):
        ga = visit.GetGlobalAttributes()
        return ga.windows[ga.activeWindow]


    def new_window(self):
        if visit.AddWindow() != 1:
            raise RuntimeWarning('Unable to create a new window!')


    def pseudocolor(self, variable='rho', scaling='log', zmin=None, zmax=None,
        ct='RdYlBu', invert_ct=0):
        if visit.AddPlot('Pseudocolor', variable, 1, 1) != 1:
            raise RuntimeWarning('Unable to add Pseudocolor plot.')

        psa = _pseudocolor._attr(variable, scaling, zmin, zmax, ct, invert_ct)
        visit.SetPlotOptions(psa)


    def pseudocolor_try_colortables(self, sleep=1.5):
        md = self.get_metadata()
        orig = self.find_pseudocolor(md['windows'][self.active_window_id]['plots'])

        for ct in visit.ColorTableNames():
            for invert in (0, 1):
                print('Trying:', ct, 'invert', invert)
                _pseudocolor._set_colortable(ct, orig['scaling'], invert)
                time.sleep(sleep)

        _pseudocolor._set_colortable(orig['ct'], orig['scaling'], orig['invert_ct'])


    def pseudocolor_colortable(self, ct):
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


    def slice(self, origin_type='Percent', origin_percent=50, axis_type='z'):
        if visit.AddOperator('Slice', 0) != 1:
            raise RuntimeWarning('Unable to add Slice operator')

        sa = _slice._attr(origin_type, origin_percent, axis_type)
        visit.SetOperatorOptions(sa)


    def lineout(self, variable='rho', point1=(0, .5, .5), point2=(1, .5, .5),
        curve_color=(0, 0, 0, 255), line_width=4):
        if re.match('^operators/Lineout/*.', variable):
            var = variable
        else:
            var = 'operators/Lineout/' + variable

        if visit.AddPlot('Curve', var, 1, 1) != 1:
            raise RuntimeWarning('Unable to plot lineout!', variable)

        la = _lineout._attr(point1, point2)
        ca = _curve._attr(line_width, curve_color)

        visit.SetOperatorOptions(la)
        visit.SetPlotOptions(ca)


    def reset_view(self):
        if visit.ResetView() != 1:
            raise RuntimeWarning('Unable to reset the view!')


    def draw(self, xtitle='X', xunit='Mpc', xscale='linear', xmin=None, xmax=None,
        ytitle='Y', yunit='Mpc', yscale='linear', ymin=None, ymax=None,
        color=(0, 0, 0, 255), bg=(255, 255, 255, 255), fg=(0, 0, 0, 255)):

        if visit.DrawPlots() != 1:
            raise RuntimeWarning('Unable to draw plots.')

        annot = _annotation._attr(xtitle, xunit, ytitle, yunit, color, bg, fg)
        curve = _view._curve(xscale, yscale, xn=xmin, xx=xmax, yn=ymin, yx=ymax)
        view2d = _view._2d(xscale, yscale)

        visit.SetAnnotationAttributes(annot)
        visit.SetViewCurve(curve)
        visit.SetView2D(view2d)


    def redraw(self, variable=None, scaling=None, zmin=None, zmax=None, ct=None,
        origin_type=None, origin_percent=None, axis_type=None, line_width=None,
        curve_color=None, point1=None, point2=None, convert_points=None,
        xtitle=None, ytitle=None, xunit=None, yunit=None,
        xscale=None, yscale=None, color=None, bg=None, fg=None):

        wid = self.active_window_id()
        md = self.get_metadata()

        if wid not in md['windows'] or len(md['windows'][wid]['plots']) < 1:
            raise RuntimeError('No plots found in this window!')

        if visit.DeleteActivePlots() != 1:
            raise RuntimeError('Unable to delete mesh plots!')

        if visit.DeleteAllPlots() != 1:
            raise RuntimeError('Unable to delete pseudocolor and contour plots')

        plots = md['windows'][wid]['plots']
        view = md['windows'][wid]['view']

        for p in plots.values():
            if _pseudocolor._check(p):
                kwargs = _pseudocolor._kwargs(p, variable, scaling, zmin, zmax, ct)
                self.pseudocolor(**kwargs)

                for o in p['operators'].values():
                    if _slice._check(o):
                        kwargs = _slice._kwargs(o, origin_type, origin_percent, axis_type)
                        self.slice(**kwargs)

                v, a = view['2d'], view['annotation']

            elif _lineout._check(p):
                kwargs = _lineout._kwargs(p, variable, point1, point2, line_width, curve_color)
                self.lineout(**kwargs)
                v, a = view['curve'], view['annotation']

            else:
                raise RuntimeError('Unknown plot!', p)

        kwargs = _view._kwargs(a, v, xtitle, ytitle, xunit, yunit,
            xscale, yscale, color, bg, fg)
        self.draw(**kwargs)


    def line(self, p1=(0.75, 0.75), p2=(0.75, 0.75), width=1,
        color=(0, 0, 0, 255), opacity=255, begin_arrow=0, end_arrow=0):
        ao = new_line(p1, p2, width, color, opacity, begin_arrow, end_arrow)


    def query(self, q=''):
        queries = visit.Queries()

        if q in queries:
            return visit.Query(q)
        else:
            raise RuntimeWarning('Invalid query!', q)


    def query_over_time(self, q='', range_scale='log', domain_scale='linear'):
        queries = visit.QueriesOverTime()

        if q in queries:
            wid = self.active_window_id()

            if visit.QueryOverTime(q) != 1:
                raise RuntimeWarning('Unable to run the query_over_time!', q)

            visit.SetActiveWindow(aw)
        else:
            raise RuntimeWarning('Invalid query_over_time!', q)


    def minimum_over_time(self):
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
            if print_it: pprint(wmd)
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

        if print_it: pprint(md)

        return md
