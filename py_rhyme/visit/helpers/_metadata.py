import os
from . import _lineout


try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _get_plot_operator(plot_obj, oid):
    operator = {}

    op = visit.GetOperatorOptions(oid)

    operator['type'] = plot_obj.operatorNames[oid]

    if operator['type'] == 'Slice':
        operator['origin_type'] = op.originType
        operator['origin_percent'] = op.originPercent
        operator['axis_type'] = op.axisType
    elif operator['type'] == 'Lineout':
        operator['point1'] = _lineout._real_position_to_normalized(op.point1)
        operator['point2'] = _lineout._real_position_to_normalized(op.point2)
    else:
        raise RuntimeError('Unknow operator!', operator['type'])

    return operator


def _get_plot_operators(plot_obj):
    operators = {}

    for oid in range(len(plot_obj.operatorNames)):
        operators[oid] = _get_plot_operator(plot_obj, oid)

    return operators


def _get_plot(pid):
    plot = {}

    plot_obj = visit.GetPlotList().GetPlots(pid)
    plot_opt = visit.GetPlotOptions()

    plot['type'] = visit.PlotPlugins()[plot_obj.plotType]
    plot['variable'] = plot_obj.plotVar

    if plot['type'] == 'Pseudocolor':
        plot['scaling'] = plot_opt.scaling
        plot['min'] = plot_opt.min if plot_opt.minFlag != 0 else None
        plot['max'] = plot_opt.max if plot_opt.maxFlag != 0 else None
        plot['ct'] = plot_opt.colorTableName
        plot['invert_ct'] = plot_opt.invertColorTable
    elif plot['type'] == 'Curve':
        plot['line_width'] = plot_opt.lineWidth
        plot['curve_color'] = plot_opt.curveColor
    else:
        raise RuntimeError('Unknow plot', plot['type'])

    plot['operators'] = _get_plot_operators(plot_obj)

    return plot


def _get_current_view2d():
    view = {}

    attr = visit.GetView2D()
    view['window_coords'] = attr.windowCoords
    view['xscale'] = attr.xScale
    view['yscale'] = attr.yScale

    return view


def _get_current_annotation():
    annot = {}

    attr = visit.GetAnnotationAttributes()
    annot['xtitle'] = attr.axes2D.xAxis.title.title
    annot['ytitle'] = attr.axes2D.yAxis.title.title
    annot['xunit'] = attr.axes2D.xAxis.title.units
    annot['yunit'] = attr.axes2D.yAxis.title.units
    annot['color'] = attr.axes2D.xAxis.title.font.color
    annot['bg'] = attr.backgroundColor
    annot['fg'] = attr.foregroundColor

    return annot


def _get_current_curve():
    curve = {}

    attr = visit.GetViewCurve()
    curve['domain_coords'] = attr.domainCoords
    curve['range_coords'] = attr.rangeCoords
    curve['domain_scale'] = attr.domainScale
    curve['range_scale'] = attr.rangeScale

    return curve


def _get_window(wid):
    window = {}

    visit.SetActiveWindow(wid)

    info = visit.GetWindowInformation()
    ds = info.activeSource
    id = os.path.basename(ds.replace(' database', '').replace('*', 'database'))

    sliders = info.timeSliders
    cycle = info.timeSliderCurrentStates[sliders.index(ds)]

    md = visit.GetMetaData(ds)
    vars = [md.GetScalars(i).name for i in range(md.GetNumScalars())]

    window['database'] = ds
    window['id'] = id
    window['cycle'] = cycle
    window['cycles'] = md.cycles
    window['ncycles'] = len(md.cycles)
    window['times'] = md.times
    window['variables'] = vars
    window['extents'] = info.extents
    window['plots'] = {}

    window['view'] = {
        'annotation': _get_current_annotation(),
        '2d': _get_current_view2d(),
        'curve': _get_current_curve(),
    }

    for pid in range(visit.GetNumPlots()):
        window['plots'][pid] = _get_plot(pid)

    return window


def _get():
    metadata = { 'windows': {} }

    windows = visit.GetGlobalAttributes().windows

    for wid in windows:
        metadata['windows'][wid] = _get_window(wid)

    return metadata
