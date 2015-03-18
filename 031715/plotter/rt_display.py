

# class DecodeTask:
#     signal=QSignals
#
#     def __init__(self):
#
#     def start():
#         #decode 3000 frames:
#
#         send signal to display
#
#
#     def
#
#
# FRAME_INTERVAL=3000
#
# class PlotterTask:
#     def __init__(self):
#         self.db=DataFrame.select("converted",FRAME_INTERVAL)
#         self.count=0
#
#     def update_graph(self):
#         self.count=count


import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates


import datetime as dt


n_pts = 10
dates = [dt.datetime.now() + dt.timedelta(days=i) for i in range(n_pts)]

ax1 = plt.subplot(121)
ax1.plot(dates, range(10))

ax2 = plt.subplot(123, sharex=ax1)
ax2.plot(dates, range(10))

# ax3 = plt.subplot(123, sharex=ax1)
# ax3.plot(dates, range(10))

# Now format the x axis. This *MUST* be done after all sharex commands are run.

# put no more than 10 ticks on the date axis.
ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
# format the date in our own way.
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# rotate the labels on both date axes
for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(30)
for label in ax2.xaxis.get_ticklabels():
    label.set_rotation(30)
# for label in ax3.xaxis.get_ticklabels():
#     label.set_rotation(30)


# tweak the subplot spacing to fit the rotated labels correctly
plt.subplots_adjust(hspace=0.35, bottom=0.125)

plt.show()


import matplotlib.pyplot as plt

plt.subplot(111)
plt.title("Radiometer")
plt.subplot(211)
plt.title("Sensor")
plt.subplot(311)
plt.title("Encoder")

plt.show()


# parse_enc(file)
# # get filename
#
#
# parse_inu(file)
#
# parse_rad(file)



