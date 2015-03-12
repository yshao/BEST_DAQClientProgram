# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

from PyQt4 import QtCore, QtGui, QtXml
from PyQt4.QtGui import QMainWindow
### ui files
from best.daqmanager.plotterwidget import PlotterWidget
from best.common.utils import *
from best.common.testutils import *
from best.common.sqliteutils import *
from best.common.configutils import *
from best.common.fileutils import *
from best.common.guiutils import *

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