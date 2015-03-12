# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visbar.ui'
#
# Created: Wed Sep 10 12:29:11 2014
#      by: PyQt4 UI code generator 4.11
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

class Ui_PlotDialog(object):
    def setupUi(self, PlotDialog):
        PlotDialog.setObjectName(_fromUtf8("PlotDialog"))
        PlotDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(PlotDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.outPBar = QtGui.QProgressBar(PlotDialog)
        self.outPBar.setProperty("value", 24)
        self.outPBar.setObjectName(_fromUtf8("outPBar"))
        self.verticalLayout.addWidget(self.outPBar)
        self.inPlot = QtGui.QPushButton(PlotDialog)
        self.inPlot.setObjectName(_fromUtf8("inPlot"))
        self.verticalLayout.addWidget(self.inPlot)
        self.outLogBrowser = QtGui.QTextBrowser(PlotDialog)
        self.outLogBrowser.setObjectName(_fromUtf8("outLogBrowser"))
        self.verticalLayout.addWidget(self.outLogBrowser)

        self.retranslateUi(PlotDialog)
        QtCore.QMetaObject.connectSlotsByName(PlotDialog)

    def retranslateUi(self, PlotDialog):
        PlotDialog.setWindowTitle(_translate("PlotDialog", "Plot", None))
        self.inPlot.setText(_translate("PlotDialog", "Plot", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PlotDialog = QtGui.QDialog()
    ui = Ui_PlotDialog()
    ui.setupUi(PlotDialog)
    PlotDialog.show()
    sys.exit(app.exec_())

