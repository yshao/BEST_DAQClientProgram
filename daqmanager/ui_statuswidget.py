# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'statuswidget.ui'
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

class Ui_StatusWidget(object):
    def setupUi(self, StatusWidget):
        StatusWidget.setObjectName(_fromUtf8("StatusWidget"))
        StatusWidget.resize(438, 324)
        self.gridLayout = QtGui.QGridLayout(StatusWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_6 = QtGui.QLabel(StatusWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 3, 1, 1)
        self.label_5 = QtGui.QLabel(StatusWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.inScan = QtGui.QPushButton(StatusWidget)
        self.inScan.setObjectName(_fromUtf8("inScan"))
        self.gridLayout.addWidget(self.inScan, 4, 3, 1, 1)
        self.outArchFTP = QtGui.QLabel(StatusWidget)
        self.outArchFTP.setObjectName(_fromUtf8("outArchFTP"))
        self.gridLayout.addWidget(self.outArchFTP, 0, 2, 1, 1)
        self.outRadFTP = QtGui.QLabel(StatusWidget)
        self.outRadFTP.setObjectName(_fromUtf8("outRadFTP"))
        self.gridLayout.addWidget(self.outRadFTP, 2, 2, 1, 1)
        self.label_2 = QtGui.QLabel(StatusWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.outArchIP = QtGui.QLabel(StatusWidget)
        self.outArchIP.setObjectName(_fromUtf8("outArchIP"))
        self.gridLayout.addWidget(self.outArchIP, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(StatusWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.outEncIP = QtGui.QLabel(StatusWidget)
        self.outEncIP.setObjectName(_fromUtf8("outEncIP"))
        self.gridLayout.addWidget(self.outEncIP, 1, 1, 1, 1)
        self.outRadIP = QtGui.QLabel(StatusWidget)
        self.outRadIP.setObjectName(_fromUtf8("outRadIP"))
        self.gridLayout.addWidget(self.outRadIP, 2, 1, 1, 1)
        self.outEncFTP = QtGui.QLabel(StatusWidget)
        self.outEncFTP.setObjectName(_fromUtf8("outEncFTP"))
        self.gridLayout.addWidget(self.outEncFTP, 1, 2, 1, 1)
        self.containerStatus = QtGui.QScrollArea(StatusWidget)
        self.containerStatus.setWidgetResizable(True)
        self.containerStatus.setObjectName(_fromUtf8("containerStatus"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 418, 218))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.containerStatus.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.containerStatus, 3, 0, 1, 4)

        self.retranslateUi(StatusWidget)
        QtCore.QMetaObject.connectSlotsByName(StatusWidget)

    def retranslateUi(self, StatusWidget):
        StatusWidget.setWindowTitle(_translate("StatusWidget", "Status", None))
        self.label_6.setText(_translate("StatusWidget", "TextLabel", None))
        self.label_5.setText(_translate("StatusWidget", "Radiometer 22-30", None))
        self.inScan.setText(_translate("StatusWidget", "Scan", None))
        self.outArchFTP.setText(_translate("StatusWidget", "TextLabel", None))
        self.outRadFTP.setText(_translate("StatusWidget", "TextLabel", None))
        self.label_2.setText(_translate("StatusWidget", "Archival", None))
        self.outArchIP.setText(_translate("StatusWidget", "TextLabel", None))
        self.label_3.setText(_translate("StatusWidget", "Encoder", None))
        self.outEncIP.setText(_translate("StatusWidget", "TextLabel", None))
        self.outRadIP.setText(_translate("StatusWidget", "TextLabel", None))
        self.outEncFTP.setText(_translate("StatusWidget", "TextLabel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    StatusWidget = QtGui.QWidget()
    ui = Ui_StatusWidget()
    ui.setupUi(StatusWidget)
    StatusWidget.show()
    sys.exit(app.exec_())

