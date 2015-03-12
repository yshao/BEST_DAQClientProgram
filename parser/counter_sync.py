__author__ = 'Ping'

import test.common.sqliteutils
import pandas as pd

# db=DaqDb("daq.db")

def main():
    ""
    "enc""counter"
    "rad""counter"
    "inu"

    "INSERT into COUNTER" "timestamp" ""

    # pd.concat([data, ts]).sort_index().interpolate().reindex(ts.index)


main()


import vincent
import pandas as pd
import random

#Create a date range and populate it with some random data
dates = pd.date_range('4/1/2013 00:00:00', periods=1441, freq='T')
data = [random.randint(20, 100) for x in range(len(dates))]
series = pd.Series(data, index=dates)

#Create a vincent line plot, and add your data. Vincent handles the translation
#of Pandas/Python datetimes to javascript epoch time.
vis = vincent.Line()
vis.tabular_data(series, axis_time='day')

#Add interpolation to make our fake data look nice
vis + ({'value': 'basis'}, 'marks', 0, 'properties', 'enter', 'interpolate')

#Make the visualization a bit wider, and add axis titles
vis.update_vis(width=700, height=300)
vis.axis_label(x_label='Time', y_label='Data')
# vis.to_json(path)