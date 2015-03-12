# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testdatawidget.ui'
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

class Ui_TestDataWidget(object):
    def setupUi(self, TestDataWidget):
        TestDataWidget.setObjectName(_fromUtf8("TestDataWidget"))
        TestDataWidget.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(TestDataWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.inGetData = QtGui.QPushButton(TestDataWidget)
        self.inGetData.setObjectName(_fromUtf8("inGetData"))
        self.verticalLayout.addWidget(self.inGetData)
        self.inDecode = QtGui.QPushButton(TestDataWidget)
        self.inDecode.setObjectName(_fromUtf8("inDecode"))
        self.verticalLayout.addWidget(self.inDecode)
        self.inConvert = QtGui.QPushButton(TestDataWidget)
        self.inConvert.setObjectName(_fromUtf8("inConvert"))
        self.verticalLayout.addWidget(self.inConvert)
        self.inPlot = QtGui.QPushButton(TestDataWidget)
        self.inPlot.setObjectName(_fromUtf8("inPlot"))
        self.verticalLayout.addWidget(self.inPlot)
        self.outText = QtGui.QLabel(TestDataWidget)
        self.outText.setObjectName(_fromUtf8("outText"))
        self.verticalLayout.addWidget(self.outText)
        self.outLogBrowser = QtGui.QTextBrowser(TestDataWidget)
        self.outLogBrowser.setObjectName(_fromUtf8("outLogBrowser"))
        self.verticalLayout.addWidget(self.outLogBrowser)
        self.outPBar = QtGui.QProgressBar(TestDataWidget)
        self.outPBar.setProperty("value", 24)
        self.outPBar.setObjectName(_fromUtf8("outPBar"))
        self.verticalLayout.addWidget(self.outPBar)

        self.retranslateUi(TestDataWidget)
        QtCore.QMetaObject.connectSlotsByName(TestDataWidget)

    def retranslateUi(self, TestDataWidget):
        TestDataWidget.setWindowTitle(_translate("TestDataWidget", "Test Data Widget", None))
        self.inGetData.setText(_translate("TestDataWidget", "GetData", None))
        self.inDecode.setText(_translate("TestDataWidget", "Decode", None))
        self.inConvert.setText(_translate("TestDataWidget", "Convert", None))
        self.inPlot.setText(_translate("TestDataWidget", "Plot", None))
        self.outText.setText(_translate("TestDataWidget", "TextLabel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TestDataWidget = QtGui.QWidget()
    ui = Ui_TestDataWidget()
    ui.setupUi(TestDataWidget)
    TestDataWidget.show()
    sys.exit(app.exec_())

