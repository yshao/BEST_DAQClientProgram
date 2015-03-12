# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'daqwidget.ui'
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

class Ui_DAQWidget(object):
    def setupUi(self, DAQWidget):
        DAQWidget.setObjectName(_fromUtf8("DAQWidget"))
        DAQWidget.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(DAQWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(DAQWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 6, 1, 1, 1)
        self.label_4 = QtGui.QLabel(DAQWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 5, 1, 1, 1)
        self.inSetRawDir = QtGui.QPushButton(DAQWidget)
        self.inSetRawDir.setObjectName(_fromUtf8("inSetRawDir"))
        self.gridLayout.addWidget(self.inSetRawDir, 0, 1, 1, 1)
        self.inDataFolder = QtGui.QLineEdit(DAQWidget)
        self.inDataFolder.setObjectName(_fromUtf8("inDataFolder"))
        self.gridLayout.addWidget(self.inDataFolder, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(DAQWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.inInterval = QtGui.QLineEdit(DAQWidget)
        self.inInterval.setObjectName(_fromUtf8("inInterval"))
        self.gridLayout.addWidget(self.inInterval, 1, 3, 1, 1)
        self.outFtpSyncPBar = QtGui.QProgressBar(DAQWidget)
        self.outFtpSyncPBar.setProperty("value", 24)
        self.outFtpSyncPBar.setObjectName(_fromUtf8("outFtpSyncPBar"))
        self.gridLayout.addWidget(self.outFtpSyncPBar, 5, 2, 1, 3)
        self.outDecodePBar = QtGui.QProgressBar(DAQWidget)
        self.outDecodePBar.setProperty("value", 24)
        self.outDecodePBar.setObjectName(_fromUtf8("outDecodePBar"))
        self.gridLayout.addWidget(self.outDecodePBar, 6, 2, 1, 3)
        self.inOpenFolder = QtGui.QPushButton(DAQWidget)
        self.inOpenFolder.setObjectName(_fromUtf8("inOpenFolder"))
        self.gridLayout.addWidget(self.inOpenFolder, 1, 4, 1, 1)
        self.outSize = QtGui.QLabel(DAQWidget)
        self.outSize.setObjectName(_fromUtf8("outSize"))
        self.gridLayout.addWidget(self.outSize, 0, 4, 1, 1)
        self.inDecode = QtGui.QCheckBox(DAQWidget)
        self.inDecode.setObjectName(_fromUtf8("inDecode"))
        self.gridLayout.addWidget(self.inDecode, 2, 4, 1, 1)
        self.inFtpSync = QtGui.QCheckBox(DAQWidget)
        self.inFtpSync.setObjectName(_fromUtf8("inFtpSync"))
        self.gridLayout.addWidget(self.inFtpSync, 2, 3, 1, 1)

        self.retranslateUi(DAQWidget)
        QtCore.QMetaObject.connectSlotsByName(DAQWidget)

    def retranslateUi(self, DAQWidget):
        DAQWidget.setWindowTitle(_translate("DAQWidget", "DAQWidget", None))
        self.label.setText(_translate("DAQWidget", "Decode", None))
        self.label_4.setText(_translate("DAQWidget", "FTP sync", None))
        self.inSetRawDir.setText(_translate("DAQWidget", "Raw Dir", None))
        self.inDataFolder.setText(_translate("DAQWidget", "N:/data/test_station/Demo/Data", None))
        self.label_2.setText(_translate("DAQWidget", "Interval:", None))
        self.inInterval.setText(_translate("DAQWidget", "1", None))
        self.inOpenFolder.setText(_translate("DAQWidget", "Open", None))
        self.outSize.setText(_translate("DAQWidget", "Size", None))
        self.inDecode.setText(_translate("DAQWidget", "Enable Decoding", None))
        self.inFtpSync.setText(_translate("DAQWidget", "Enable FTP Sync", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DAQWidget = QtGui.QWidget()
    ui = Ui_DAQWidget()
    ui.setupUi(DAQWidget)
    DAQWidget.show()
    sys.exit(app.exec_())

