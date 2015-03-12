# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)
import webbrowser
import os
import re
import sys
import threading
from inspect import stack
from threading import Thread
from PyQt4 import QtCore, QtGui, QtXml
from PyQt4.QtGui import QWidget
### ui files
from ui_testdatawidget import Ui_TestDataWidget
from common.utils import *
from common.testutils import *
from common.sqliteutils import *
from common.configutils import *
from common.fileutils import *
from common.netutils import *

### py files
# from parser_inu import *


script_name = re.sub('\..*','',os.path.basename(sys.argv[0]))
starting_dir = os.getcwd()

start_message="DataMan"
logger=create_logger(script_name,start_message)

DATA_DIR="c:/test_station/Demo/Data"

# print os.environ['PATH']
# print os.environ['ComSpec']
# print os.environ['DAQMANAGER_HOME']

# DAQMANAGER_HOME=os.environ['DAQMANAGER_HOME']

# print DAQMANAGER_HOME

from best.daqmanager.gui.mpl import mplWidget
from PyQt4.QtCore import QObject, SIGNAL

class TestDataWidget(QtGui.QWidget):
    ### connects widgets and signals ###
    def __init__(self, parent):
        super(TestDataWidget, self).__init__(parent)
        self.ui = Ui_TestDataWidget()
        self.ui.setupUi(self)


        ### init ###
        self.mpl=mplWidget()
        self.logger = self.parent().logger
        self.config = self.parent().config
        # print self.config.get("IP_ENCODER")
        self.initComputerStatus()

        ### init ###
        #--- Config Group ---
        # self.ui.outDataHost.setText(self.config.get("LOCAL_DB_DIR"))
        # self.ui.outDataFolder.setText(self.config.get("LOCAL_DATA_DIR"))

        #--- inputs group ---
        self.ui.inGetData.clicked.connect(self.guiScanNetwork)
        self.ui.inGetData.clicked.connect(self.guiGetData)
        self.ui.inDecode.clicked.connect(self.guiDecode)
        self.ui.inConvert.clicked.connect(self.guiConvert)
        self.ui.inPlot.clicked.connect(self.guiPlot)


        self.connect(self.asyncUiControl, SIGNAL('task_connect()'),self.sigScanNetwork)
        self.connect(self.asyncUiControl, SIGNAL('task_getDataTask()'),self.sigGetData)
        self.connect(self.asyncUiControl, SIGNAL('task_decodeTask()'),self.sigDecode)
        self.connect(self.asyncUiControl, SIGNAL('task_convertDataTask()'),self.sigConvertData)
        self.connect(self.asyncUiControl, SIGNAL('task_plotDataTask()'),self.sigPlotData)

        exit=QtGui.QAction(self)


    ### init methods ###
    def initComputerStatus(self):
        "initalize computer objects corresponding to status map"

        # status=QWidget()
        #
        # self.ui.containerStatus.addWidget(status)


    ### event handler methods ###
    def guiScanData(self):
        ""

    def guiGetData(self):
        ""


    def guiDecode(self):
        ""

    def guiConvert(self):
        ""

    def guiPlot(self):
        ""
        self.mpl.plot()
        self.mpl.show()

    #### signals handler ###
    def sigGetData(self):
        ""
        self.ui.outLogBrowser.append("GetData")
        self.logger("GetData")

        state, numFiles, currFile = self.asyncUiControl.get_result(3)

    def sigDecode(self):
        ""
        self.ui.outLogBrowser.append("DecodeData")
        self.logger("DecodeData")

        state, numFiles, currFile = self.asyncUiControl.get_result(3)

    def sigConvertData(self):
        ""
        self.ui.outLogBrowser.append("ConvertData")
        self.logger("ConvertData")

        state, numFiles, currFile = self.asyncUiControl.get_result(3)

    def sigPlotData(self):
        ""
        self.ui.outLogBrowser.append("PlotData")
        self.logger("PlotData")

        state, numFiles, currFile = self.asyncUiControl.get_result(3)

    ### event helper methods ###
    def refreshComputerStatus(self):
        ""

        # self.ui.containerStatus..ipConnect.setText("Yes")
        # self.ui.containerStatus.archival.ipConnect.setText("Yes")
        # self.ui.containerStatus.archival.ipConnect.setText("Yes")







# if __name__ == '__main__':
#     ""
#     # import sys
#     # app = QtGui.QApplication(sys.argv)
#     # w = TestDataWidget()
#     # w.show()
#     # sys.exit(app.exec_())




