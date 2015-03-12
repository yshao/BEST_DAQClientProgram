# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ftppbar.ui'
#
# Created: Wed Sep 10 12:17:22 2014
#      by: PyQt4 UI code generator 4.11
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_FtpSyncDialog(object):
    def setupUi(self, FtpSyncDialog):
        FtpSyncDialog.setObjectName(_fromUtf8("FtpSyncDialog"))
        FtpSyncDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(FtpSyncDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.outPBar = QtGui.QProgressBar(FtpSyncDialog)
        self.outPBar.setProperty("value", 24)
        self.outPBar.setObjectName(_fromUtf8("outPBar"))
        self.verticalLayout.addWidget(self.outPBar)
        self.inFtpSync = QtGui.QPushButton(FtpSyncDialog)
        self.inFtpSync.setObjectName(_fromUtf8("inFtpSync"))
        self.verticalLayout.addWidget(self.inFtpSync)
        self.outLogBrowser = QtGui.QTextBrowser(FtpSyncDialog)
        self.outLogBrowser.setObjectName(_fromUtf8("outLogBrowser"))
        self.verticalLayout.addWidget(self.outLogBrowser)

        self.retranslateUi(FtpSyncDialog)
        QtCore.QMetaObject.connectSlotsByName(FtpSyncDialog)

    def retranslateUi(self, FtpSyncDialog):
        FtpSyncDialog.setWindowTitle(_translate("FtpSyncDialog", "Ftp Sync", None))
        self.inFtpSync.setText(_translate("FtpSyncDialog", "Sync", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FtpSyncDialog = QtGui.QDialog()
    ui = Ui_FtpSyncDialog()
    ui.setupUi(FtpSyncDialog)
    FtpSyncDialog.show()
    sys.exit(app.exec_())

