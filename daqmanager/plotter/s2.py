from PyQt4 import QtCore
from PyQt4.QtCore import QObject, SIGNAL, QThread

class Panel(QObject):
    updateSignal=QtCore.pyqtSignal()

    def __init__(self,QWidget = None):
        QObject.__init__(self)


        self.taskRead=ReadTask()

        self.taskDecode=DecodeTask()

        self.connect(self.taskDecode, SIGNAL('task_decode'),self.handleDecodeTask)

        self.taskRead.run()
        self.taskDecode.run()

    def handleDecodeTask(self):
        ""
        # "do something"

        self.updateSignal.emit("task_update")




class DecodeTask(QThread):
    commitSignal = QtCore.pyqtSignal()

    def __init__(self, parent=QObject):
        QtCore.QObject.__init__(self)
        self.count = 1


    def commit(self):
        self.count += 1
        if self.count > 10:
            self.commitSignal.emit("task_commit")

    def run(self):
        while(1):
            self.commit()


class ReadTask(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self)
        self.connect(self.parent(),SIGNAL('task_update'),self.update)

    def update(self):
        print "perform update"

    def run(self):
        self.update()

if __name__ == '__main__':
    panel = Panel()






