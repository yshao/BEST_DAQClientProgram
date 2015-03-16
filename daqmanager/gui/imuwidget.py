# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)
import webbrowser
import threading
from PyQt4 import QtCore, QtGui
### ui files
from ui_imuwidget import Ui_IMUWidget
from common.utils import *
from common.configutils import *
from common.fileutils import *

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


class IMUWidget(QtGui.QWidget):
    ### connects widgets and signals ###
    def __init__(self, parent = None):
        super(IMUWidget, self).__init__(parent)
        self.ui = Ui_IMUWidget()
        self.ui.setupUi(self)

        ### init ###
        # self.logger = ClientLogger(self.ui.outLogBrowser)
        # self.config = Config('C:/Users/Ping/Workspace/DAQ/test/common/config.xml')
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

    ### event handler methods###
    def on_plotting_done(self,result):
        self.logger.log_info("-".join(["RESULT",result]))

    def parse_plotting(self,s):
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


        result.update({'datasets_plotted': n1})
        return result

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

    def gui_send_config(self):
        self.logger.log_info("INIT: "+"Sending config file over... ")

        username=self.config.get("USERNAME")
        password=self.config.get("PASSWORD")
        remote_dir=self.config.get("REMOTE_APP_DIR")
        file=self.config.get("DAQ_CONFIG_FILE")
        host=self.config.get("IP_ENCODER")
        ip1=(host,21)

        host=self.config.get("IP_RADIOMETER_22-30")
        ip2=(host,21)

        host=self.config.get("IP_ARCHIVAL")
        ip3=(host,21)

        self.logger.log_info("EXEC: send_config")

        t1=threading.Thread(self.send_config(),(ip1,file,remote_dir))
        t2=threading.Thread(self.send_config(),(ip2,file,remote_dir))
        t3=threading.Thread(self.send_config(),(ip3,file,remote_dir))

        # print threading.currentThread(t1), t1.is_alive()
        # print threading.currentThread(t2), t2.is_alive()

        result=''
        while 1:
          if not t1.is_alive():
              # out=t1.
              out=''
              result = self.parse_send_config(out)
              break

        if (result != ''):
            self.logger.log_info("RESULT: "+str(result))
        else:
            self.logger.log_info("RESULT: none")

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

    def send_config(self):
        ""

    def start_mirroring(self):
        ""

    def start_processing(self):
        ""


if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    # plotbar = PlotDialog()
    # plotbar.show()
    # sys.exit(app.exec_())


