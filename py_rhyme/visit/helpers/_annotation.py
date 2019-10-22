try:
    import visit
except ImportError:
    raise RuntimeError('Unable to import VisIt!')


def _attr(xt, xu, yt, yu, c, bg, fg):
    """
    Parameter
    xt: xtitle
    xu: xunit
    yt: ytitle
    yu: yunit
    c: color
    bg: background
    fg: foreground
    """
    attr = visit.AnnotationAttributes()

    attr.axes2D.lineWidth = 0

    attr.axes2D.xAxis.title.visible = 1
    attr.axes2D.xAxis.title.font.font = attr.axes2D.xAxis.title.font.Arial
    attr.axes2D.xAxis.title.font.scale = 0.8
    attr.axes2D.xAxis.title.font.useForegroundColor = 0
    attr.axes2D.xAxis.title.font.color = c
    attr.axes2D.xAxis.title.font.bold = 0
    attr.axes2D.xAxis.title.font.italic = 0
    attr.axes2D.xAxis.title.userTitle = 1
    attr.axes2D.xAxis.title.title = xt
    attr.axes2D.xAxis.title.userUnits = 1
    attr.axes2D.xAxis.title.units = xu
    attr.axes2D.xAxis.label.font.font = attr.axes2D.xAxis.label.font.Arial
    attr.axes2D.xAxis.label.font.bold = 0
    attr.axes2D.xAxis.label.font.italic = 0
    attr.axes2D.xAxis.label.font.useForegroundColor = 0
    attr.axes2D.xAxis.label.font.color = c

    attr.axes2D.yAxis.title.visible = 1
    attr.axes2D.yAxis.title.font.font = attr.axes2D.yAxis.title.font.Arial
    attr.axes2D.yAxis.title.font.scale = 0.8
    attr.axes2D.yAxis.title.font.useForegroundColor = 0
    attr.axes2D.yAxis.title.font.color = c
    attr.axes2D.yAxis.title.font.bold = 0
    attr.axes2D.yAxis.title.font.italic = 0
    attr.axes2D.yAxis.title.userTitle = 1
    attr.axes2D.yAxis.title.title = yt
    attr.axes2D.yAxis.title.userUnits = 1
    attr.axes2D.yAxis.title.units = yu
    attr.axes2D.yAxis.label.font.font = attr.axes2D.yAxis.label.font.Arial
    attr.axes2D.yAxis.label.font.bold = 0
    attr.axes2D.yAxis.label.font.italic = 0
    attr.axes2D.yAxis.label.font.useForegroundColor = 0
    attr.axes2D.yAxis.label.font.color = c

    attr.timeInfoFlag = 1

    attr.legendInfoFlag = 1

    attr.userInfoFlag = 1
    attr.userInfoFont.font = attr.userInfoFont.Arial
    attr.userInfoFont.scale = 1
    attr.userInfoFont.useForegroundColor = 0
    attr.userInfoFont.color = c
    attr.userInfoFont.bold = 0
    attr.userInfoFont.italic = 0

    attr.databaseInfoFlag = 1
    attr.databaseInfoFont.font = attr.databaseInfoFont.Arial
    attr.databaseInfoFont.scale = 1
    attr.databaseInfoFont.useForegroundColor = 0
    attr.databaseInfoFont.color = c
    attr.databaseInfoFont.bold = 0
    attr.databaseInfoFont.italic = 0
    attr.databaseInfoExpansionMode = attr.File
    attr.databaseInfoTimeScale = 1
    attr.databaseInfoTimeOffset = 0

    attr.backgroundMode = attr.Solid # Solid, Gradient, Image, ImageSphere
    attr.backgroundColor = bg
    attr.foregroundColor = fg
    attr.gradientBackgroundStyle = attr.Radial # TopToBottom, BottomToTop, LeftToRight, RightToLeft, Radial
    attr.gradientColor1 = (0, 0, 255, 255)
    attr.gradientColor2 = (0, 0, 0, 255)
    attr.backgroundImage = ""
    attr.imageRepeatX = 1
    attr.imageRepeatY = 1

    return attr
