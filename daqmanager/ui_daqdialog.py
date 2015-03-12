# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'daqdialog.ui'
#
# Created: Sun Sep 21 23:39:07 2014
#      by: PyQt4 UI code generator 4.9.6
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

class Ui_SimpleDAQDialog(object):
    def setupUi(self, SimpleDAQDialog):
        SimpleDAQDialog.setObjectName(_fromUtf8("SimpleDAQDialog"))
        SimpleDAQDialog.resize(258, 192)
        self.gridLayout = QtGui.QGridLayout(SimpleDAQDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.outLogBrowser = QtGui.QTextBrowser(SimpleDAQDialog)
        self.outLogBrowser.setObjectName(_fromUtf8("outLogBrowser"))
        self.gridLayout.addWidget(self.outLogBrowser, 4, 0, 1, 2)
        self.inSend = QtGui.QPushButton(SimpleDAQDialog)
        self.inSend.setObjectName(_fromUtf8("inSend"))
        self.gridLayout.addWidget(self.inSend, 1, 1, 1, 1)
        self.inDetect = QtGui.QPushButton(SimpleDAQDialog)
        self.inDetect.setObjectName(_fromUtf8("inDetect"))
        self.gridLayout.addWidget(self.inDetect, 0, 1, 1, 1)
        self.inSendOpt = QtGui.QComboBox(SimpleDAQDialog)
        self.inSendOpt.setObjectName(_fromUtf8("inSendOpt"))
        self.inSendOpt.addItem(_fromUtf8(""))
        self.inSendOpt.addItem(_fromUtf8(""))
        self.inSendOpt.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.inSendOpt, 1, 0, 1, 1)
        self.inStartDAQ = QtGui.QPushButton(SimpleDAQDialog)
        self.inStartDAQ.setObjectName(_fromUtf8("inStartDAQ"))
        self.gridLayout.addWidget(self.inStartDAQ, 2, 1, 1, 1)
        self.inFtpSync = QtGui.QPushButton(SimpleDAQDialog)
        self.inFtpSync.setObjectName(_fromUtf8("inFtpSync"))
        self.gridLayout.addWidget(self.inFtpSync, 3, 1, 1, 1)

        self.retranslateUi(SimpleDAQDialog)
        QtCore.QMetaObject.connectSlotsByName(SimpleDAQDialog)

    def retranslateUi(self, SimpleDAQDialog):
        SimpleDAQDialog.setWindowTitle(_translate("SimpleDAQDialog", "Simple DAQ Control", None))
        self.inSend.setText(_translate("SimpleDAQDialog", "Send", None))
        self.inDetect.setText(_translate("SimpleDAQDialog", "Detect", None))
        self.inSendOpt.setItemText(0, _translate("SimpleDAQDialog", "HOME", None))
        self.inSendOpt.setItemText(1, _translate("SimpleDAQDialog", "FORWARD", None))
        self.inSendOpt.setItemText(2, _translate("SimpleDAQDialog", "STOP", None))
        self.inStartDAQ.setText(_translate("SimpleDAQDialog", "Start DAQ", None))
        self.inFtpSync.setText(_translate("SimpleDAQDialog", "FtpSync", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SimpleDAQDialog = QtGui.QDialog()
    ui = Ui_SimpleDAQDialog()
    ui.setupUi(SimpleDAQDialog)
    SimpleDAQDialog.show()
    sys.exit(app.exec_())

