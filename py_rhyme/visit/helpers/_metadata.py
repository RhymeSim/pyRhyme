import os


try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _generate():
    metadata = { 'windows': {} }

    windows = visit.GetGlobalAttributes().windows

    for wid in windows:
        visit.SetActiveWindow(wid)

        metadata['windows'][wid] = {}
        window = metadata['windows'][wid]

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

        for pid in range(visit.GetNumPlots()):
            window['plots'][pid] = {}
            plot = window['plots'][pid]

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

            plot['operators'] = {}

            for oid in range(len(plot_obj.operatorNames)):
                plot['operators'][oid] = {}
                operator = plot['operators'][oid]

                op = visit.GetOperatorOptions(oid)

                operator['type'] = plot_obj.operatorNames[oid]
                operator['origin_type'] = op.originType
                operator['origin_percent'] = op.originPercent
                operator['axis_type'] = op.axisType

        return metadata
