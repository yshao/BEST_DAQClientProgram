# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'motormonitorwidget.ui'
#
# Created: Tue Sep 23 15:37:18 2014
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

class Ui_MotorMonitorWidget(object):
    def setupUi(self, MotorMonitorWidget):
        MotorMonitorWidget.setObjectName(_fromUtf8("MotorMonitorWidget"))
        MotorMonitorWidget.resize(400, 300)

        self.retranslateUi(MotorMonitorWidget)
        QtCore.QMetaObject.connectSlotsByName(MotorMonitorWidget)

    def retranslateUi(self, MotorMonitorWidget):
        MotorMonitorWidget.setWindowTitle(_translate("MotorMonitorWidget", "MotorMonitorWidget", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MotorMonitorWidget = QtGui.QWidget()
    ui = Ui_MotorMonitorWidget()
    ui.setupUi(MotorMonitorWidget)
    MotorMonitorWidget.show()
    sys.exit(app.exec_())

