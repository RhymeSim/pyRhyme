try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def draw_plots_attr(xt, xu, xs, xn, xx, yt, yu, ys, yn, yx, c, bg, fg, se):
    """
    Parameter
    xt: xtitle
    xu: xunit
    xs: xscale
    xn: xmin
    xx: xmax
    yt: ytitle
    yu: yunit
    ys: yscale
    yn: ymin
    yx: ymax
    c: color
    bg: background
    fg: foreground
    se: spatial extents
    """

    aa = visit.AnnotationAttributes()
    v2da = visit.View2DAttributes()

    # Annotation Attributes
    aa.axes2D.lineWidth = 0

    aa.axes2D.xAxis.title.visible = 1
    aa.axes2D.xAxis.title.font.font = aa.axes2D.xAxis.title.font.Arial
    aa.axes2D.xAxis.title.font.scale = 0.8
    aa.axes2D.xAxis.title.font.useForegroundColor = 0
    aa.axes2D.xAxis.title.font.color = c
    aa.axes2D.xAxis.title.font.bold = 0
    aa.axes2D.xAxis.title.font.italic = 0
    aa.axes2D.xAxis.title.userTitle = 1
    aa.axes2D.xAxis.title.title = xt
    aa.axes2D.xAxis.title.userUnits = 1
    aa.axes2D.xAxis.title.units = xu
    aa.axes2D.xAxis.label.font.font = aa.axes2D.xAxis.label.font.Arial
    aa.axes2D.xAxis.label.font.bold = 0
    aa.axes2D.xAxis.label.font.italic = 0
    aa.axes2D.xAxis.label.font.useForegroundColor = 0
    aa.axes2D.xAxis.label.font.color = c

    aa.axes2D.yAxis.title.visible = 1
    aa.axes2D.yAxis.title.font.font = aa.axes2D.yAxis.title.font.Arial
    aa.axes2D.yAxis.title.font.scale = 0.8
    aa.axes2D.yAxis.title.font.useForegroundColor = 0
    aa.axes2D.yAxis.title.font.color = c
    aa.axes2D.yAxis.title.font.bold = 0
    aa.axes2D.yAxis.title.font.italic = 0
    aa.axes2D.yAxis.title.userTitle = 1
    aa.axes2D.yAxis.title.title = yt
    aa.axes2D.yAxis.title.userUnits = 1
    aa.axes2D.yAxis.title.units = yu
    aa.axes2D.yAxis.label.font.font = aa.axes2D.yAxis.label.font.Arial
    aa.axes2D.yAxis.label.font.bold = 0
    aa.axes2D.yAxis.label.font.italic = 0
    aa.axes2D.yAxis.label.font.useForegroundColor = 0
    aa.axes2D.yAxis.label.font.color = c

    aa.timeInfoFlag = 1

    aa.legendInfoFlag = 1

    aa.userInfoFlag = 1
    aa.userInfoFont.font = aa.userInfoFont.Arial
    aa.userInfoFont.scale = 1
    aa.userInfoFont.useForegroundColor = 0
    aa.userInfoFont.color = c
    aa.userInfoFont.bold = 0
    aa.userInfoFont.italic = 0

    aa.databaseInfoFlag = 1
    aa.databaseInfoFont.font = aa.databaseInfoFont.Arial
    aa.databaseInfoFont.scale = 1
    aa.databaseInfoFont.useForegroundColor = 0
    aa.databaseInfoFont.color = c
    aa.databaseInfoFont.bold = 0
    aa.databaseInfoFont.italic = 0
    aa.databaseInfoExpansionMode = aa.File
    aa.databaseInfoTimeScale = 1
    aa.databaseInfoTimeOffset = 0

    aa.backgroundMode = aa.Solid # Solid, Gradient, Image, ImageSphere
    aa.backgroundColor = bg
    aa.foregroundColor = fg
    aa.gradientBackgroundStyle = aa.Radial # TopToBottom, BottomToTop, LeftToRight, RightToLeft, Radial
    aa.gradientColor1 = (0, 0, 255, 255)
    aa.gradientColor2 = (0, 0, 0, 255)
    aa.backgroundImage = ""
    aa.imageRepeatX = 1
    aa.imageRepeatY = 1


    # View2D Attributes
    if xs == 'log':
        v2da.xScale = v2da.LOG
    elif xs == 'linear':
        v2da.xScale = v2da.LINEAR

    if ys == 'log':
        v2da.yScale = v2da.LOG
    elif ys == 'linear':
        v2da.yScale = v2da.LINEAR

    spatial_extents = [
        xn if xn is not None else se[0],
        xx if xx is not None else se[1],
        yn if yn is not None else se[2],
        yx if yx is not None else se[3],
    ]

    v2da.viewportCoords = (0.2, 0.95, 0.15, 0.90)
    v2da.windowCoords = tuple(spatial_extents)

    return aa, v2da
