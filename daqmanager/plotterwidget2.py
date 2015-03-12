#!/usr/bin/env python

# used to parse files more easily
from __future__ import with_statement

# Numpy module
import numpy as np

# for command-line arguments
import sys

# Qt4 bindings for core Qt functionalities (non-GUI)
from PyQt4 import QtCore
from PyQt4 import QtGui

from ui_plotterdialog import Ui_PlotterDialog

import pandas as pd



class PlotterDialog(QtGui.QDialog):
    ### connects widgets and signals ###
    def __init__(self, parent = None):
        super(PlotterDialog, self).__init__(parent)
        self.ui = Ui_PlotterDialog()
        self.ui.setupUi(self)

        # connect the signals with the slots
        QtCore.QObject.connect(self.ui.inDataSource, QtCore.SIGNAL("clicked()"), self.select_file)
        QtCore.QObject.connect(self.ui.inUpdate, QtCore.SIGNAL("clicked()"), self.update_graph)

    def select_file(self):
        """opens a file select dialog"""
        # open the dialog and get the selected file
        file = QtGui.QFileDialog.getOpenFileName()
        # if a file is selected
        if file:
            # update the lineEdit widget text with the selected filename
            self.ui.inDataSourceLine.setText(file)


    def parse_file(self, filename):
        """Function to parse a text file to extract letters frequencies"""

        # dict initialization
        letters = {}

        # lower-case letter ordinal numbers
        for i in range(97, 122 + 1):
            letters[chr(i)] = 0

        # parse the input file
        with open(filename) as f:
            for line in f:
                for char in line:
                    # counts only letters
                    if ord(char.lower()) in range(97, 122 + 1):
                        letters[char.lower()] += 1

        # compute the ordered list of keys and relative values
        k = sorted(letters.keys())
        v = [letters[ki] for ki in k]

        return k, v

    def update_graph(self):
        """Updates the graph with new letters frequencies"""


        # l, v = self.parse_file(self.ui.inDataSourceLine.text())

        # self.ui.mpl.canvas.ax.clear()
        #
        # self.ui.mpl.canvas.ax.bar(np.arange(len(l))-0.25, v, width=0.5)
        #
        # self.ui.mpl.canvas.ax.set_xlim(xmin=-0.25, xmax=len(l)-0.75)
        #
        # self.ui.mpl.canvas.ax.set_xticks(range(len(l)))
        # self.ui.mpl.canvas.ax.set_xticklabels(l)
        #
        # self.ui.mpl.canvas.ax.get_yaxis().grid(True)

        data1=pd.read_sql("select ch1 from rad",conn)

        randomNumbers = random.sample(range(0, 10), 10)
        canvas=self.ui.mpl.get_canvas()
        fig=Figure()
        canvas.add_plot=fig.add_subplot(121)

        self.ui.mpl.canvas.ax.plot(randomNumbers)

        self.ui.mpl.canvas.draw()


### test
from best.common.sqliteutils import DaqDB
conn=DaqDB("../daq.db").get_connection()

import random
from matplotlib.figure import Figure
# create the GUI application
app = QtGui.QApplication(sys.argv)
# instantiate the main window
dmw = PlotterDialog()
# show it
dmw.show()
# start the Qt main loop execution, exiting from this script
# with the same return code of Qt application
sys.exit(app.exec_())
