from best.common.sqliteutils import DaqDB

#init
db=DaqDB("test.db")
# db.create_table("data",['data'])
from best.common.configutils import *

from PyQt4 import QtCore

### Running tasks ###

class CollectTask(QtCore.QThread):
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



db.insert_raws('data','data')