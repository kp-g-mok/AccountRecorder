from PyQt4.QtCore import *
from PyQt4.QtGui import *
import vispy.mpl_plot as plt
import sys

app = QApplication(sys.argv)
win = QMainWindow()
plt.plot([1,2,3,4], [1,4,9,16])
vispyCanvas=plt.show()[0]
win.setCentralWidget(vispyCanvas.native)
win.show()