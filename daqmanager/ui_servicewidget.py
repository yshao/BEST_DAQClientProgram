# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'servicewidget.ui'
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

class Ui_ServiceWidget(object):
    def setupUi(self, ServiceWidget):
        ServiceWidget.setObjectName(_fromUtf8("ServiceWidget"))
        ServiceWidget.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(ServiceWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.inSetDB = QtGui.QPushButton(ServiceWidget)
        self.inSetDB.setObjectName(_fromUtf8("inSetDB"))
        self.gridLayout.addWidget(self.inSetDB, 0, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(ServiceWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.inExecOutputData = QtGui.QPushButton(ServiceWidget)
        self.inExecOutputData.setObjectName(_fromUtf8("inExecOutputData"))
        self.gridLayout.addWidget(self.inExecOutputData, 2, 2, 1, 1)
        self.inSelectOutDir = QtGui.QPushButton(ServiceWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inSelectOutDir.sizePolicy().hasHeightForWidth())
        self.inSelectOutDir.setSizePolicy(sizePolicy)
        self.inSelectOutDir.setObjectName(_fromUtf8("inSelectOutDir"))
        self.gridLayout.addWidget(self.inSelectOutDir, 1, 0, 1, 1)
        self.inOpenDB = QtGui.QPushButton(ServiceWidget)
        self.inOpenDB.setObjectName(_fromUtf8("inOpenDB"))
        self.gridLayout.addWidget(self.inOpenDB, 0, 2, 1, 1)
        self.inOutputDir = QtGui.QLineEdit(ServiceWidget)
        self.inOutputDir.setObjectName(_fromUtf8("inOutputDir"))
        self.gridLayout.addWidget(self.inOutputDir, 1, 1, 1, 1)
        self.comboBox = QtGui.QComboBox(ServiceWidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox, 1, 2, 1, 1)
        self.progressBar = QtGui.QProgressBar(ServiceWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 3)

        self.retranslateUi(ServiceWidget)
        QtCore.QMetaObject.connectSlotsByName(ServiceWidget)

    def retranslateUi(self, ServiceWidget):
        ServiceWidget.setWindowTitle(_translate("ServiceWidget", "ServiceWidget", None))
        self.inSetDB.setText(_translate("ServiceWidget", "Database", None))
        self.inExecOutputData.setText(_translate("ServiceWidget", "Convert", None))
        self.inSelectOutDir.setText(_translate("ServiceWidget", "Output Dir", None))
        self.inOpenDB.setText(_translate("ServiceWidget", "Open", None))
        self.comboBox.setItemText(0, _translate("ServiceWidget", "Matlab", None))
        self.comboBox.setItemText(1, _translate("ServiceWidget", "CSV", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ServiceWidget = QtGui.QWidget()
    ui = Ui_ServiceWidget()
    ui.setupUi(ServiceWidget)
    ServiceWidget.show()
    sys.exit(app.exec_())

