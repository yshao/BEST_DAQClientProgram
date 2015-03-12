# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotterdialog.ui'
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

class Ui_PlotterDialog(object):
    def setupUi(self, PlotterDialog):
        PlotterDialog.setObjectName(_fromUtf8("PlotterDialog"))
        PlotterDialog.resize(607, 434)
        self.gridLayout = QtGui.QGridLayout(PlotterDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.inUpdate = QtGui.QPushButton(PlotterDialog)
        self.inUpdate.setObjectName(_fromUtf8("inUpdate"))
        self.gridLayout.addWidget(self.inUpdate, 0, 3, 1, 1)
        self.inDataSourceLine = QtGui.QLineEdit(PlotterDialog)
        self.inDataSourceLine.setMinimumSize(QtCore.QSize(489, 21))
        self.inDataSourceLine.setObjectName(_fromUtf8("inDataSourceLine"))
        self.gridLayout.addWidget(self.inDataSourceLine, 0, 0, 1, 1)
        self.inDataSource = QtGui.QPushButton(PlotterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inDataSource.sizePolicy().hasHeightForWidth())
        self.inDataSource.setSizePolicy(sizePolicy)
        self.inDataSource.setMinimumSize(QtCore.QSize(91, 25))
        self.inDataSource.setObjectName(_fromUtf8("inDataSource"))
        self.gridLayout.addWidget(self.inDataSource, 0, 2, 1, 1)
        self.mpl = MplWidget(PlotterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mpl.sizePolicy().hasHeightForWidth())
        self.mpl.setSizePolicy(sizePolicy)
        self.mpl.setObjectName(_fromUtf8("mpl"))
        self.gridLayout.addWidget(self.mpl, 1, 0, 1, 4)
        self.mplactionOpen = QtGui.QAction(PlotterDialog)
        self.mplactionOpen.setIconVisibleInMenu(False)
        self.mplactionOpen.setObjectName(_fromUtf8("mplactionOpen"))
        self.mplactionQuit = QtGui.QAction(PlotterDialog)
        self.mplactionQuit.setObjectName(_fromUtf8("mplactionQuit"))

        self.retranslateUi(PlotterDialog)
        QtCore.QMetaObject.connectSlotsByName(PlotterDialog)

    def retranslateUi(self, PlotterDialog):
        PlotterDialog.setWindowTitle(_translate("PlotterDialog", "Matplotlib In Qt Designer - Count letters frequency in a file", None))
        self.inUpdate.setText(_translate("PlotterDialog", "Update", None))
        self.inDataSourceLine.setText(_translate("PlotterDialog", "C:\\Users\\shand.shand-PC\\Workspace\\best\\daqmanager\\fffff", None))
        self.inDataSource.setText(_translate("PlotterDialog", "Data Source", None))
        self.mplactionOpen.setText(_translate("PlotterDialog", "Open", None))
        self.mplactionQuit.setText(_translate("PlotterDialog", "Quit", None))

from mplwidget import MplWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PlotterDialog = QtGui.QDialog()
    ui = Ui_PlotterDialog()
    ui.setupUi(PlotterDialog)
    PlotterDialog.show()
    sys.exit(app.exec_())

