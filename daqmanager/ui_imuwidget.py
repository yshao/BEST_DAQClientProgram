# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imuwidget.ui'
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

class Ui_IMUWidget(object):
    def setupUi(self, IMUWidget):
        IMUWidget.setObjectName(_fromUtf8("IMUWidget"))
        IMUWidget.resize(565, 467)
        self.gridLayout = QtGui.QGridLayout(IMUWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.inVisualizer = QtGui.QPushButton(IMUWidget)
        self.inVisualizer.setObjectName(_fromUtf8("inVisualizer"))
        self.gridLayout.addWidget(self.inVisualizer, 0, 0, 1, 1)

        self.retranslateUi(IMUWidget)
        QtCore.QMetaObject.connectSlotsByName(IMUWidget)

    def retranslateUi(self, IMUWidget):
        IMUWidget.setWindowTitle(_translate("IMUWidget", "IMUWidget", None))
        self.inVisualizer.setText(_translate("IMUWidget", "Visualizer", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    IMUWidget = QtGui.QWidget()
    ui = Ui_IMUWidget()
    ui.setupUi(IMUWidget)
    IMUWidget.show()
    sys.exit(app.exec_())

