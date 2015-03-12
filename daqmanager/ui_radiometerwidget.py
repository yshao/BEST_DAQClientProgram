# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'radiometerwidget.ui'
#
# Created: Mon Sep 22 13:00:48 2014
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

class Ui_RadiometerWidget(object):
    def setupUi(self, RadiometerWidget):
        RadiometerWidget.setObjectName(_fromUtf8("RadiometerWidget"))
        RadiometerWidget.resize(400, 300)

        self.retranslateUi(RadiometerWidget)
        QtCore.QMetaObject.connectSlotsByName(RadiometerWidget)

    def retranslateUi(self, RadiometerWidget):
        RadiometerWidget.setWindowTitle(_translate("RadiometerWidget", "RadiometerWidget", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RadiometerWidget = QtGui.QWidget()
    ui = Ui_RadiometerWidget()
    ui.setupUi(RadiometerWidget)
    RadiometerWidget.show()
    sys.exit(app.exec_())

