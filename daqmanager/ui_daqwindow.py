# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'daqwindow.ui'
#
# Created: Sun Oct 19 16:38:47 2014
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

class Ui_DAQManager(object):
    def setupUi(self, DAQManager):
        DAQManager.setObjectName(_fromUtf8("DAQManager"))
        DAQManager.resize(579, 502)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("images/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DAQManager.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(DAQManager)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.outLogBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.outLogBrowser.setObjectName(_fromUtf8("outLogBrowser"))
        self.gridLayout.addWidget(self.outLogBrowser, 1, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        DAQManager.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(DAQManager)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 579, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        DAQManager.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(DAQManager)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        DAQManager.setStatusBar(self.statusbar)
        self.actionNew = QtGui.QAction(DAQManager)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(DAQManager)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.menuConfigEditor = QtGui.QAction(DAQManager)
        self.menuConfigEditor.setObjectName(_fromUtf8("menuConfigEditor"))
        self.menuMotorMonitor = QtGui.QAction(DAQManager)
        self.menuMotorMonitor.setObjectName(_fromUtf8("menuMotorMonitor"))
        self.actionAbout = QtGui.QAction(DAQManager)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuTools.addAction(self.menuConfigEditor)
        self.menuTools.addAction(self.menuMotorMonitor)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(DAQManager)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(DAQManager)

    def retranslateUi(self, DAQManager):
        DAQManager.setWindowTitle(_translate("DAQManager", "DAQManager", None))
        self.menuFile.setTitle(_translate("DAQManager", "File", None))
        self.menuTools.setTitle(_translate("DAQManager", "Tools", None))
        self.menuHelp.setTitle(_translate("DAQManager", "Help", None))
        self.actionNew.setText(_translate("DAQManager", "New", None))
        self.actionOpen.setText(_translate("DAQManager", "Open", None))
        self.menuConfigEditor.setText(_translate("DAQManager", "Config Editor", None))
        self.menuMotorMonitor.setText(_translate("DAQManager", "Motor Monitor", None))
        self.actionAbout.setText(_translate("DAQManager", "About", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DAQManager = QtGui.QMainWindow()
    ui = Ui_DAQManager()
    ui.setupUi(DAQManager)
    DAQManager.show()
    sys.exit(app.exec_())

