import subprocess, os, sys


class VisitAPI:
    """
    VisIt python package to generate different plots based on Rhyme chombo outpus
    """

    DATA_STRUCTURE = {
        'path': '',
        'plots': [],
    }


    def __init__(self, visit_lib_dir=None, interactive=True):
        """
        Initializing a VisitAPI object

        Parameter
        visit_lib_dir: Path to VisIt python packages directory
        interactive: If False, VisIt viewer will be shut down
        """

        self.interactive = interactive

        if visit_lib_dir is None:
            visit_lib_dir = '/opt/visit/current/linux-x86_64/lib/site-packages'

        if os.path.exists(visit_lib_dir):
            if visit_lib_dir not in sys.path:
                sys.path.append(visit_lib_dir)
        else:
            raise RuntimeError(visit_lib_dir, 'does not exists')

        import visit

        self.visit = visit

        if not interactive: self.visit.AddArgument("-nowin")

        if self.visit.Launch() == 1:
            print('VisIt has been successfully launched.')
        else:
            raise RuntimeError('Unable to launch VisIt.')

        self.visit.SetActivePlots(0)

        self.ds = self.DATA_STRUCTURE


    def load(self, path):
        """
        Loading one or a sequence of chombo files

        Parameter
        path: Path to chombo file(s)
            Use globbing to open a sequence of files
            e.g. /path/to/result_*.chombo.h5
        """
        if self.visit.OpenDatabase(path, 0, 'Chombo') == 1:
            self.ds['path'] = path
        else:
            raise RuntimeWarning('Unable to open database:', path)


    def pseudocolor(self, variable, inherit_sil=1, apply_operators=1,
        scaling='log', minimum=None, maximum=None, colortable='RdYlBu',
        invert_colortable=0):
        """
        Adding a Pseudocolor plot

        Parameter
        variable: Variable to be plotted
        inherit_sil: If 1 the plot will inherit Subset Inclusion Lattice
            Restriction
        apply_operators: If 1 operators from active plot will be applied
            on this plot also
        scaling: log, linear
        colortable: Name of color table to be used
        invert_colortable: If 1, colors will be inverted
        """

        pa = self.visit.PseudocolorAttributes()

        if scaling is 'log':
            pa.scaling = pa.Log
        elif scaling is 'linear':
            pa.scaling = pa.Linear

        if minimum is None:
            pa.minFlag = 0
        else:
            pa.minFlag = 1
            pa.min = minimum

        if maximum is None:
            pa.maxFlag = 0
        else:
            pa.maxFlag = 1
            pa.max = maximum

        # Todo: Make color table based on the histogram of data
        #       check this: https://www.visitusers.org/index.php?title=Creating_a_color_table
        #       and this: https://www.visitusers.org/index.php?title=Converting_color_tables
        pa.colorTableName = colortable
        pa.invertColorTable = invert_colortable

        if self.visit.AddPlot(
            'Pseudocolor', variable, inherit_sil, apply_operators
        ) == 1:
            self.ds['plots'].append(
                _plot_structure(type='Pseudocolor', var=variable))
        else:
            raise RuntimeWarning('Unable to add Pseudocolor plot.')

        self.visit.SetPlotOptions(pa)


    def slice(self, all=0,
        origin_type='Percent',
        value=50,
        axis_type='ZAxis'):
        """
        Adding a slice operator

        Parameter
        all: If 1, the operator will be applied to all plots
        origin_type: Type of slicing (Intercept, Point, Percent, Zone, Node)
        value: Argument of origin,
            Intercept: <Number>
            Point: <list Number, Number, Number>
            Percent: <Number>
            Zone: <Number>
            Node: <Number>
        axis_type: XAxis, YAxis, ZAxis
        """

        slice_attr = _operator_structure(type='Slice')
        sa = self.visit.SliceAttributes()

        # TODO: Write condition for other types
        if origin_type is 'Percent':
            sa.originType = sa.Percent
            sa.originPercent = value
            slice_attr['origin_type'] = {'type': origin_type, 'Percent': value}


        if axis_type is 'XAxis':
            sa.axisType = sa.XAxis
            sa.normal = (1, 0, 0)
            slice_attr['axis_type'] = axis_type
        elif axis_type is 'YAxis':
            sa.axisType = sa.YAxis
            sa.normal = (0, 1, 0)
            slice_attr['axis_type'] = axis_type
        elif axis_type is 'ZAxis':
            sa.axisType = sa.ZAxis
            sa.normal = (0, 0, 1)
            slice_attr['axis_type'] = axis_type
        else:
            raise RuntimeWarning(axis_type, 'is not a valid axis type.')


        if self.visit.AddOperator('Slice', all) == 1:
            if all == 1:
                for p in self.ds['plots']:
                    p['operators'].append(slice_attr)
                    p['dimentionality'] = 2
            else:
                self.ds['plots'][-1]['operators'].append(slice_attr)
                self.ds['plots'][-1]['dimentionality'] = 2
        else:
            raise RuntimeWarning('Unable to add Slice operator')

        self.visit.SetOperatorOptions(sa)


    def draw_plots(self, xtitle='X', xunit='Mpc', xscale='linear',
        ytitle='Y', yunit='Mpc', yscale='linear'):
        """
        Drawing plots on VisIt viewer
        """
        aa = self.visit.AnnotationAttributes()

        aa.axes2D.xAxis.label.visible = 1
        aa.axes2D.xAxis.label.font.font = aa.axes2D.xAxis.label.font.Arial
        aa.axes2D.xAxis.title.visible = 1
        aa.axes2D.xAxis.title.font.font = aa.axes2D.xAxis.title.font.Arial
        aa.axes2D.xAxis.title.font.bold = 0
        aa.axes2D.xAxis.title.font.italic = 0
        aa.axes2D.xAxis.title.title = xtitle
        aa.axes2D.xAxis.title.units = xunit

        aa.axes2D.yAxis.label.visible = 1
        aa.axes2D.yAxis.label.font.font = aa.axes2D.yAxis.label.font.Arial
        aa.axes2D.yAxis.title.visible = 1
        aa.axes2D.yAxis.title.font.font = aa.axes2D.yAxis.title.font.Arial
        aa.axes2D.yAxis.title.font.bold = 0
        aa.axes2D.yAxis.title.font.italic = 0
        aa.axes2D.yAxis.title.title = ytitle
        aa.axes2D.yAxis.title.units = yunit

        aa.userInfoFlag = 1
        aa.userInfoFont.font = aa.userInfoFont.Arial

        aa.databaseInfoFlag = 1
        aa.databaseInfoFont.font = aa.databaseInfoFont.Arial
        aa.databaseInfoExpansionMode = aa.Smart

        aa.timeInfoFlag = 1
        aa.legendInfoFlag = 1

        aa.backgroundColor = (255, 255, 255, 255)
        aa.foregroundColor = (0, 0, 0, 255)

        aa.gradientBackgroundStyle = aa.Radial # TopToBottom, BottomToTop, LeftToRight, RightToLeft, Radial
        aa.gradientColor1 = (0, 0, 255, 255)
        aa.gradientColor2 = (0, 0, 0, 255)
        aa.backgroundMode = aa.Solid # Solid, Gradient, Image, ImageSphere
        aa.backgroundImage = ""

        self.visit.SetAnnotationAttributes(aa)

        v2da = self.visit.View2DAttributes()

        if xscale is 'log':
            v2da.xScale = v2da.LOG
        elif xscale is 'linear':
            v2da.xScale = v2da.LINEAR

        if yscale is 'log':
            v2da.yScale = v2da.LOG
        elif yscale is 'linear':
            v2da.yScale = v2da.LINEAR

        # v2da.windowCoords =
        v2da.viewportCoords = (0.2, 0.95, 0.15, 0.95)

        self.visit.SetView2D(v2da)

        if self.interactive:
            if self.visit.DrawPlots() != 1:
                raise RuntimeWarning('Unable to draw plots.')


    def get_min(self):
        """Send Min Query to VisIt"""

        query_result = self.visit.Query('Min')
        found = re.search('=\ (.+?)\ ', query_result)

        if found:
            return float(found.group(1))
        else:
            raise RuntimeWarning('Min has not found')


    def get_max(self):
        """Send Max Query to VisIt"""

        query_result = self.visit.Query('Max')
        found = re.search('=\ (.+?)\ ', query_result)

        if found:
            return float(found.group(1))
        else:
            raise RuntimeWarning('Max has not found')


    def close(self):
        """
        Closing VisIt windwo
        """

        if self.visit.Close() == 1:
            self.ds = self.DATA_STRUCTURE
        else:
            raise RuntimeError('Unable to close VisIt.')


def _plot_structure(type='', var=0, operators=[], dimentionality=3):
    """Generating a default plot structure"""
    return {'type': type, 'var': var, 'operators': operators,
        'dimentionality': dimentionality}


def _operator_structure(type, origin_type={}, axis_type=''):
    """Generating default operator structure"""
    return {'type': type, 'origin_type': origin_type, 'axis_type': axis_type}
