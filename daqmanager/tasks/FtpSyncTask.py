from multiprocessing import Process
import Queue

from PyQt4 import QtCore

from common.configutils import *
from best.daqmanager.tasks.helpers.ftpmirror import *


### Running tasks ###

class FtpSyncTask(QtCore.QThread):
    ""
    data_downloaded = QtCore.pyqtSignal(object)

    def __init__(self, file):
        QtCore.QThread.__init__(self)
        self.file=file
        self.queue=Queue()

        self.writer = Process(target=ftp_mirror, args=(self.queue,))

    def run(self):
        # info = urllib2.urlopen(self.url).info()
        # parse_inu(self.queue)
        self.writer.start()
        self.writer.join()
        self.ftp_sync.emit('%s' % (self.file))

    def update(self,queue):
      while 1:
        msg = queue.get()         # Read from the queue and do nothing
        if (msg == 'result: '):
            self.data_downloaded.emit('%s' % self.parse_result(msg))
            break
        else:
            self.data_downloaded.emit('%s' % (msg))

    def parse_result(self,msg):
        ""
        # return "PARSED: "+msg
        self.data_downloaded.emit('Result: %s' % (msg))
        
### test setup ###        
### test ftp sync basic ###
# from common.utils.configutil import *
config=Config("../config.xml")
login="test"
passwd="test123"
ip=('localhost',21)
localdir="D:/Demo/ftptest"
remotedir="data"


ftp=FtpClient(ip,login,passwd,localdir,remotedir)

ftp_mirror(ip,login,passwd,localdir,remotedir)


### test list and pwd ###
print ftp.list()
# "Sync %s out of %s" % count, total


                 
### test gui task thread
# task=FtpSyncTask(logger,client,pbar)

