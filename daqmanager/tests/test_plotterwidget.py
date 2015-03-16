# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

from PyQt4 import QtGui
from PyQt4.QtGui import QMainWindow
### ui files
from common.configutils import *

from mpl import *


class TestWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.config=Config('../config.xml')

        # plotter = PlotterWidget()
        mpl=mplWidget()
        self.setCentralWidget(mpl)

import sys
app = QtGui.QApplication(sys.argv)
window=TestWindow()
window.show()
sys.exit(app.exec_())