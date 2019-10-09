import re, time
from .pseudocolor_helper import pseudocolor_attr
from .slice_helper import slice_attr
from .draw_plots_helper import draw_plots_attr
from .line_helper import new_line

try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')



class VisitAPI:
    """
    VisIt python package to generate different plots based on Rhyme chombo outpus
    """

    def __init__(self, visit_lib_dir=None, interactive=True):
        """
        Initializing a VisitAPI object

        Parameter
        visit_lib_dir: Path to VisIt python packages directory
        interactive: If False, VisIt viewer will be shut down
        """

        if not interactive: visit.AddArgument("-nowin")

        if visit.Launch() != 1:
            raise RuntimeError('Unable to launch VisIt.')


    def open(self, path):
        """
        Loading one or a sequence of chombo files

        Parameter
        path: Path to chombo file(s)
            Use globbing to open a sequence of files
            e.g. /path/to/result_0000.chombo.h5
        """

        ds = path + ' database' if '*' in path else path

        if visit.OpenDatabase(ds, 0, 'Chombo') != 1:
            raise RuntimeWarning('Unable to open database:', path)


    def pseudocolor(self, var, scaling='log', zmin=None, zmax=None,
        ct='RdYlBu', invert_ct=0):
        """
        Adding a Pseudocolor plot

        Parameter
        var: Variable to be plotted
        scaling: log, linear
        ct: Name of color table to be used
        invert_ct: If 1, colors will be inverted
        """
        if visit.AddPlot( 'Pseudocolor', var, 1, 1 ) != 1:
            raise RuntimeWarning('Unable to add Pseudocolor plot.')

        psa = pseudocolor_attr(scaling, zmin, zmax, ct, invert_ct)
        visit.SetPlotOptions(psa)


    def pseudocolor_try_colortables(self, sleep=1.5):
        """Trying all available colorTables on an **already drawn** plot"""
        p = visit.PseudocolorAttributes()

        ct_orig = p.colorTableName
        invrt_orig = p.invertColorTable

        for ct in visit.ColorTableNames():
            for invrt in (0, 1):
                print('Trying:', ct, 'invert', invrt)

                p.colorTableName = ct
                p.invertColorTable = invrt
                visit.SetPlotOptions(p)

                time.sleep(sleep)

        p.colorTableName = ct_orig
        p.invertColorTable = invrt_orig
        visit.SetPlotOptions(p)



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

        sa = slice_attr(origin_type, val, axis_type)
        visit.SetOperatorOptions(sa)


    def draw_plots(self, xtitle='X', xunit='Mpc', xscale='linear', xmin=None, xmax=None,
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

        return ao


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

        visit.SetQueryOutputToObject()

        if q in queries:
            return visit.Query(q)
        else:
            raise RuntimeWarning('Invalid query!')


    def close(self):
        """
        Closing VisIt windwo
        """

        if visit.Close() != 1:
            raise RuntimeError('Unable to close VisIt.')
