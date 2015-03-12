import vincent
import pandas as pd
import random

#Create a date range and populate it with some random data
dates = pd.date_range('4/1/2013 00:00:00', periods=1441, freq='T')
data = [random.randint(20, 100) for x in range(len(dates))]
series = pd.Series(data, index=dates)

print series

#Create a vincent line plot, and add your data. Vincent handles the translation
#of Pandas/Python datetimes to javascript epoch time.
# vis = vincent.Line()
vis = vincent.Bar()
vis.tabular_data(series, axis_time='day')

#Add interpolation to make our fake data look nice
vis + ({'value': 'basis'}, 'marks', 0, 'properties', 'enter', 'interpolate')

#Make the visualization a bit wider, and add axis titles
vis.update_vis(width=700, height=300)
vis.axis_label(x_label='Time', y_label='Data')
# vis.to_json(path)


# #Resample to hourly, which can take a lambda function in addition to the
# #standard mean, max, min, etc.
# half_day = series['4/1/2013 00:00:00':'4/1/2013 12:00:00']
# hourly = half_day.resample('H', how=lambda x: x.mean() + random.randint(-30, 40))
#
# #New Area plot
# area = vincent.Area()
# area.tabular_data(hourly, axis_time='hour')
# area + ({'value': 'basis'}, 'marks', 0, 'properties', 'enter', 'interpolate')
# area.update_vis(width=700)
# area.axis_label(x_label='Time (Hourly)', y_label='Data')
# # area.to_json(path)
#
# half_hour = series['4/1/2013 00:00:00':'4/1/2013 00:30:00']
# vis.tabular_data(half_hour, axis_time='minute')
# vis.axis_label(x_label='Time (Minutes)', title='Data vs. Time')
# # vis.to_json(path)