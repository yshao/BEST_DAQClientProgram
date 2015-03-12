# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pbar.ui'
#
# Created: Tue Sep 09 11:46:37 2014
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

class Ui_PBarDialog(object):
    def setupUi(self, PBarDialog):
        PBarDialog.setObjectName(_fromUtf8("PBarDialog"))
        PBarDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(PBarDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.outPBar = QtGui.QProgressBar(PBarDialog)
        self.outPBar.setProperty("value", 24)
        self.outPBar.setObjectName(_fromUtf8("outPBar"))
        self.verticalLayout.addWidget(self.outPBar)
        self.inProcessData = QtGui.QPushButton(PBarDialog)
        self.inProcessData.setObjectName(_fromUtf8("inProcessData"))
        self.verticalLayout.addWidget(self.inProcessData)
        self.outLogBrowser = QtGui.QTextBrowser(PBarDialog)
        self.outLogBrowser.setObjectName(_fromUtf8("outLogBrowser"))
        self.verticalLayout.addWidget(self.outLogBrowser)

        self.retranslateUi(PBarDialog)
        QtCore.QMetaObject.connectSlotsByName(PBarDialog)

    def retranslateUi(self, PBarDialog):
        PBarDialog.setWindowTitle(_translate("PBarDialog", "Dialog", None))
        self.inProcessData.setText(_translate("PBarDialog", "PushButton", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PBarDialog = QtGui.QDialog()
    ui = Ui_PBarDialog()
    ui.setupUi(PBarDialog)
    PBarDialog.show()
    sys.exit(app.exec_())

