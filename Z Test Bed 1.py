from PyQt4 import QtCore
import pyqtgraph as pg

x = ['02/2015', '03/2015']
y = [1, 2]
xdict = dict(enumerate(x))

win = pg.GraphicsWindow()
stringaxis = pg.AxisItem(orientation='bottom')
stringaxis.setTicks([xdict.items()])
plot = win.addPlot(axisItems={'bottom': stringaxis})
curve = plot.plot([key for key in xdict.keys()], y)

if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()