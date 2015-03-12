# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'controlwidget.ui'
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

class Ui_ControlWidget(object):
    def setupUi(self, ControlWidget):
        ControlWidget.setObjectName(_fromUtf8("ControlWidget"))
        ControlWidget.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(ControlWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.progressBar = QtGui.QProgressBar(ControlWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 6, 0, 1, 2)
        self.label = QtGui.QLabel(ControlWidget)
        self.label.setStyleSheet(_fromUtf8("border: 1px solid black"))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)
        self.inSendConfig = QtGui.QPushButton(ControlWidget)
        self.inSendConfig.setObjectName(_fromUtf8("inSendConfig"))
        self.gridLayout.addWidget(self.inSendConfig, 5, 1, 1, 1)
        self.inSendSW = QtGui.QPushButton(ControlWidget)
        self.inSendSW.setObjectName(_fromUtf8("inSendSW"))
        self.gridLayout.addWidget(self.inSendSW, 4, 1, 1, 1)
        self.inCommandSel = QtGui.QComboBox(ControlWidget)
        self.inCommandSel.setObjectName(_fromUtf8("inCommandSel"))
        self.inCommandSel.addItem(_fromUtf8(""))
        self.inCommandSel.addItem(_fromUtf8(""))
        self.inCommandSel.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.inCommandSel, 0, 0, 1, 1)
        self.inCommandSend = QtGui.QPushButton(ControlWidget)
        self.inCommandSend.setObjectName(_fromUtf8("inCommandSend"))
        self.gridLayout.addWidget(self.inCommandSend, 0, 1, 1, 1)
        self.pushButton = QtGui.QPushButton(ControlWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(ControlWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)

        self.retranslateUi(ControlWidget)
        QtCore.QMetaObject.connectSlotsByName(ControlWidget)

    def retranslateUi(self, ControlWidget):
        ControlWidget.setWindowTitle(_translate("ControlWidget", "ControlWidget", None))
        self.label.setText(_translate("ControlWidget", "Display:", None))
        self.inSendConfig.setText(_translate("ControlWidget", "Update Config", None))
        self.inSendSW.setText(_translate("ControlWidget", "Update DAQ Software", None))
        self.inCommandSel.setItemText(0, _translate("ControlWidget", "SETTIME", None))
        self.inCommandSel.setItemText(1, _translate("ControlWidget", "STARTDAQ", None))
        self.inCommandSel.setItemText(2, _translate("ControlWidget", "STOPDAQ", None))
        self.inCommandSend.setText(_translate("ControlWidget", "Send", None))
        self.pushButton.setText(_translate("ControlWidget", "Stop", None))
        self.pushButton_2.setText(_translate("ControlWidget", "Start", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ControlWidget = QtGui.QWidget()
    ui = Ui_ControlWidget()
    ui.setupUi(ControlWidget)
    ControlWidget.show()
    sys.exit(app.exec_())

