import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
from random import random

#genearte layout
app = QtGui.QApplication([])
win = pg.GraphicsWindow()
p1 = win.addPlot(row=1, col=0)
p2 = win.addPlot(row=2, col=0)
p3 = win.addPlot(row=3, col=0)
p4 = win.addPlot(row=4, col=0)
region = pg.LinearRegionItem()
region.setZValue(10)
p4.addItem(region)

#create numpy arrays
#make the numbers large to show that the xrange shows data from 10000 to all the way 0
data1 = 10000 + 3000 * np.random.random(size=10000)
data2 = 15000 + 3000 * np.random.random(size=10000)

p1.plot(data1, pen="r")
p2.plot(data2, pen="g")
p3.plot(data1, pen="w")
p4.plot(data2, pen="w")

for window in [p1, p2, p3]:
    window.setMouseEnabled(y=False)

def update():
    rgn = region.getRegion()
    for window, data in [(p1, data1), (p2, data2), (p3, data1)]:
        window.setXRange(*rgn, padding=0)
        window.setYRange(data[rgn[0]:rgn[1]+1].min(), data[rgn[0]:rgn[1]+1].max())
    
def updateRegion(window, viewRange):
    rgn = viewRange[0]
    region.setRegion(rgn)
region.sigRegionChanged.connect(update)
region.setRegion([1000, 2000])
for window in [p1, p2, p3]:
    window.sigRangeChanged.connect(updateRegion)

app.exec_()