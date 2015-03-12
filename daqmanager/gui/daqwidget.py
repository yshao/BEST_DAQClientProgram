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
### ui files
from ui_daqwidget import Ui_DAQWidget

### utils
from common.utils import *
from common.testutils import *
from common.sqliteutils import *
from common.configutils import *
from common.fileutils import *

from best.daqmanager.tasks.FtpSyncTask import FtpSyncTask
from best.daqmanager.tasks.DecodeTask import DecodeTask


### py files
# from test.daqmanager.tasks.DecodeTask import *
# from test.daqmanager.tasks.FtpSyncTask import *


###
# script_name = re.sub('\..*','',os.path.basename(sys.argv[0]))
# starting_dir = os.getcwd()

# start_message="DataMan"
# logger=create_logger(script_name,start_message)

# DATA_DIR="c:/test_station/Demo/Data"

# print os.environ['PATH']
# print os.environ['ComSpec']
# print os.environ['DAQMANAGER_HOME']

# DAQMANAGER_HOME=os.environ['DAQMANAGER_HOME']

# print DAQMANAGER_HOME

from multiprocessing import Process, Queue

class ClientLogger:
    def __init__(self,gui_logger):
        self.gui_logger=gui_logger

    def log_info(self,txt):
        self.gui_logger.append(txt)
        # logger.info(txt)

    def log_error(self,txt):
        self.gui_logger.append(txt)
        # logger.error(txt)

    def log_warn(self,txt):
        self.gui_logger.append(txt)
        # logger.warn(txt)


class DAQWidget(QtGui.QWidget):
    ### connects widgets and signals ###
    def __init__(self, parent = None):
        super(DAQWidget, self).__init__(parent)
        self.ui = Ui_DAQWidget()
        self.ui.setupUi(self)

        ### init ###
        # self.logger = ClientLogger(self.ui.outLogBrowser)
        # self.config = Config('config.xml')
        # print self.config.get("IP_ENCODER")
        # self.config.read("daqmanager.log")

        ### gui init ###
        #--- Config Group ---
        # self.ui.outServiceOn.setText("Off")
        # self.ui.outSize.setText("Size of folder: "+ str(self.folder_calc_size()))

        #--- inputs group ---
        # self.ui.inPlot.clicked.connect(self.guiPlot)

        #--- output group ---
        #self.ui.buttonSendCommand.setEnabled(0)

        ### connect signals to commands ###
        
        self.ui.inFtpSync.clicked.connect(self.guiFtpSync)
        self.ui.inDecode.clicked.connect(self.guiDecode)
        # self.ui.inPlot.clicked.connect(self.gui_visualizing)
        # self.ui.inSendConfig.clicked.connect(self.gui_send_config)
        # self.ui.inUpdateSoftware.clicked.connect(self.gui_update_software)
        # self.ui.inOpenRawDirFolder.clicked.connect(self.openFolder)

        # self.ui.inSetDB.clicked.connect(self.selectFile)
        # self.ui.inSetRawDir.clicked.connect(self.selectFile)

        # self.ui.inEnableSynchronizing.checked(self.gui_start_mirroring)
        # self.ui.inEnableProcessing.checked(self.gui_start_processing)
        # self.ui.buttonSendCommand.clicked.connect(self.send_command)
        # self.ui.buttonSync.clicked.connect(self.sync)


        exit=QtGui.QAction(self)
        # self.setWindowTitle("Processing PBar")

    def selectFile(self):   #Open a dialog to locate the sqlite file and some more...
        path = QtGui.QFileDialog.getOpenFileName(None,QtCore.QString.fromLocal8Bit("Select database:"),"*.sqlite")
        if path:
            self.database = path # To make possible cancel the FileDialog and continue loading a predefined db
        self.openDBFile()


    def closeEvent(self,event):
        reply=QtGui.QMessageBox.question(self,'Message',"Are you sure to quit?",QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if reply==QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    ### event handler methods###
    def guiFtpSync(self):
        logger=self.parent().logger
        
        daqclient=self.parent().daqclient
        
        task=FtpSyncTask(logger,daqclient,self.ui.FtpSyncPBar)
        task.run()        
        
        
    def guiDecode(self):
        logger=self.parent().logger        
        daqclient=self.parent().daqclient                        
        
        task=DecodeTask(logger,daqclient,self.ui.DecodePBar)
        task.run()
        
            
    def parse_daqdecoder(self,s):
        ""
        result={}

        pattern = re.compile(r"""\|\s*                 # opening bar and whitespace
                                 '(?P<name>.*?)'       # quoted name
                                 \s*\|\s*(?P<n1>.*?)   # whitespace, next bar, n1
                                 \s*\|\s*(?P<n2>.*?)   # whitespace, next bar, n2
                                 \s*\|""", re.VERBOSE)
        match = pattern.match(s)

        name = match.group("name")
        n1 = float(match.group("n1"))
        n2 = float(match.group("n2"))


        result.update({'packets_found': n1})
        result.update({'packets_discarded', n2})
        return result

    def parse_ftpmirror(self,s):
        ""
        result={}

        pattern = re.compile(r"""\|\s*                 # opening bar and whitespace
                                 '(?P<name>.*?)'       # quoted name
                                 \s*\|\s*(?P<n1>.*?)   # whitespace, next bar, n1
                                 \s*\|\s*(?P<n2>.*?)   # whitespace, next bar, n2
                                 \s*\|""", re.VERBOSE)
        match = pattern.match(s)

        # name = match.group("name")

        # n1 = float(match.group("n1"))
        # n2 = float(match.group("n2"))
        n1 = 1
        n2 = 2


        result.update({'files_transferred': n1})
        return result


    def openFolder(self):
        self.logger.log_info("Open Folder")
        webbrowser.open ('file://'+ self.ui.inDataFolder.text())

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    daq = DAQWidget()
    daq.show()
    sys.exit(app.exec_())