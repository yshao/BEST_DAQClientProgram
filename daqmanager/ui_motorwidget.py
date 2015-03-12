# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'motorwidget.ui'
#
# Created: Sun Oct 19 16:38:45 2014
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

class Ui_MotorWidget(object):
    def setupUi(self, MotorWidget):
        MotorWidget.setObjectName(_fromUtf8("MotorWidget"))
        MotorWidget.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(MotorWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.inScript = QtGui.QTextEdit(MotorWidget)
        self.inScript.setObjectName(_fromUtf8("inScript"))
        self.gridLayout.addWidget(self.inScript, 1, 0, 1, 2)
        self.inProfileOpt = QtGui.QComboBox(MotorWidget)
        self.inProfileOpt.setObjectName(_fromUtf8("inProfileOpt"))
        self.inProfileOpt.addItem(_fromUtf8(""))
        self.inProfileOpt.addItem(_fromUtf8(""))
        self.inProfileOpt.addItem(_fromUtf8(""))
        self.inProfileOpt.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.inProfileOpt, 0, 0, 1, 1)
        self.inOpenScript = QtGui.QPushButton(MotorWidget)
        self.inOpenScript.setObjectName(_fromUtf8("inOpenScript"))
        self.gridLayout.addWidget(self.inOpenScript, 2, 0, 1, 1)
        self.inDownloadProfile = QtGui.QPushButton(MotorWidget)
        self.inDownloadProfile.setObjectName(_fromUtf8("inDownloadProfile"))
        self.gridLayout.addWidget(self.inDownloadProfile, 0, 1, 1, 1)
        self.inOpenMotorMonitor = QtGui.QPushButton(MotorWidget)
        self.inOpenMotorMonitor.setObjectName(_fromUtf8("inOpenMotorMonitor"))
        self.gridLayout.addWidget(self.inOpenMotorMonitor, 3, 0, 1, 1)
        self.inDownloadProgram = QtGui.QPushButton(MotorWidget)
        self.inDownloadProgram.setObjectName(_fromUtf8("inDownloadProgram"))
        self.gridLayout.addWidget(self.inDownloadProgram, 3, 1, 1, 1)
        self.inOpenScriptLine = QtGui.QLineEdit(MotorWidget)
        self.inOpenScriptLine.setObjectName(_fromUtf8("inOpenScriptLine"))
        self.gridLayout.addWidget(self.inOpenScriptLine, 2, 1, 1, 1)

        self.retranslateUi(MotorWidget)
        QtCore.QMetaObject.connectSlotsByName(MotorWidget)

    def retranslateUi(self, MotorWidget):
        MotorWidget.setWindowTitle(_translate("MotorWidget", "MotorWidget", None))
        self.inProfileOpt.setItemText(0, _translate("MotorWidget", "1 Radiometer", None))
        self.inProfileOpt.setItemText(1, _translate("MotorWidget", "2 Radiometers", None))
        self.inProfileOpt.setItemText(2, _translate("MotorWidget", "3 Radiometers", None))
        self.inProfileOpt.setItemText(3, _translate("MotorWidget", "4 Radiometers", None))
        self.inOpenScript.setText(_translate("MotorWidget", "Open Script", None))
        self.inDownloadProfile.setText(_translate("MotorWidget", "Download Profile", None))
        self.inOpenMotorMonitor.setText(_translate("MotorWidget", "Motor Monitor", None))
        self.inDownloadProgram.setText(_translate("MotorWidget", "Download Program", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MotorWidget = QtGui.QWidget()
    ui = Ui_MotorWidget()
    ui.setupUi(MotorWidget)
    MotorWidget.show()
    sys.exit(app.exec_())

