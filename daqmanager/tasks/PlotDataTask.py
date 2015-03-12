### service for refreshing data ###
class PlotDataTask():
    def __init__(self):
        ""

    def check_update(self):
        ""

    def refresh(self):
        ""




### test plot with matplot ###
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from best.daqmanager.plotterwidget import PlotterWidget

dataframe = pd.DataFrame({'Col': np.random.uniform(size=1000)})
plt.scatter(dataframe.index, dataframe['Col'])

plt.show()

### test with plotterwidget
db=DaqDB("")

plotter=PlotterWidget(db)


plotter.show()
### refresh thread based on new records found within parameter

# new_count='select count(*) from %s' % self.widget.table

# if new_count > count:
#     plot.refresh()
plotter.refresh()

plotter.update_plot()