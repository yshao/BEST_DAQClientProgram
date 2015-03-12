# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sensorwidget.ui'
#
# Created: Sun Oct 19 16:38:46 2014
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

class Ui_SensorWidget(object):
    def setupUi(self, SensorWidget):
        SensorWidget.setObjectName(_fromUtf8("SensorWidget"))
        SensorWidget.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(SensorWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton = QtGui.QPushButton(SensorWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.containerSensors = QtGui.QScrollArea(SensorWidget)
        self.containerSensors.setWidgetResizable(True)
        self.containerSensors.setObjectName(_fromUtf8("containerSensors"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 251))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.containerSensors.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.containerSensors, 0, 0, 1, 1)

        self.retranslateUi(SensorWidget)
        QtCore.QMetaObject.connectSlotsByName(SensorWidget)

    def retranslateUi(self, SensorWidget):
        SensorWidget.setWindowTitle(_translate("SensorWidget", "SensorWidget", None))
        self.pushButton.setText(_translate("SensorWidget", "Plot", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SensorWidget = QtGui.QWidget()
    ui = Ui_SensorWidget()
    ui.setupUi(SensorWidget)
    SensorWidget.show()
    sys.exit(app.exec_())

