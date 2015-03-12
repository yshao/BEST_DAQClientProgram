# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)
import webbrowser
from PyQt4 import QtCore, QtGui
### ui files
from ui_statuswidget import Ui_StatusWidget
from common.utils import *
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

class StatusWidget(QtGui.QWidget):
    ### connects widgets and signals ###
    def __init__(self, parent):
        super(StatusWidget, self).__init__(parent)
        self.ui = Ui_StatusWidget()
        self.ui.setupUi(self)

        ### init ###
        # self.logger = ClientLogger(self.ui.outLogBrowser)
        self.config = self.parent().config
        # print self.config.get("IP_ENCODER")
        self.initComputerStatus()

        ### gui init ###
        #--- Config Group ---
        self.ui.outArchIP.setText(self.config.get("IP_ARCHIVAL"))
        self.ui.outEncIP.setText(self.config.get("IP_ENCODER"))
        self.ui.outRadIP.setText(self.config.get("IP_RADIOMETER_22-30"))

        # self.ui.outDataHost.setText(self.config.get("LOCAL_DB_DIR"))
        # self.ui.outDataFolder.setText(self.config.get("LOCAL_DATA_DIR"))

        #--- inputs group ---
        self.ui.inScan.clicked.connect(self.guiScan)

        #--- output group ---
        #self.ui.buttonSendCommand.setEnabled(0)

        ### connect signals to commands ###
        # self.ui.inServiceOn.clicked.connect(self.gui_start_mirroring)
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

    ### init methods ###
    def initComputerStatus(self):
        "initalize computer objects corresponding to status map"

        # status=QWidget()
        #
        # self.ui.containerStatus.addWidget(status)


    ### event handler methods ###
    def guiScan(self):
        "scanning DAQ network for devices"
        self.parent().logger.log_info("Scanning IP")

        ipMap=self.parent().config.read_ip()
        # print ipMap
        result=scan_network(list)

        # for k,v in result.iteritems():
        #     self.statusMap[k]["ipConnect"]=

        self.refreshComputerStatus()



    def openFolder(self):
        self.logger.log_info("Open Folder")
        webbrowser.open ('file://'+ self.ui.inDataFolder.text())


    ### event helper methods ###
    def refreshComputerStatus(self):
        ""

        # self.ui.containerStatus..ipConnect.setText("Yes")
        # self.ui.containerStatus.archival.ipConnect.setText("Yes")
        # self.ui.containerStatus.archival.ipConnect.setText("Yes")

    ### methods and algorithm ###
    def folder_calc_size(self):
        ""
        total_size = 0
        start_path=self.config.get("LOCAL_DIR")

        start_path="//192.168.1.223/data/source"
        # print start_path
        for dirpath, dirnames, filenames in os.walk(start_path):
            # print dirpath
            # print dirnames
            # print filenames
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # print fp
                total_size += os.path.getsize(fp)

        # print total_size

        return total_size



if __name__ == '__main__':
    ""
    # import sys
    # app = QtGui.QApplication(sys.argv)
    # status = StatusWidget()
    # status.show()
    # sys.exit(app.exec_())


