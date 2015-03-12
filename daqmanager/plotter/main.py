### plot stacked graph

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates


import datetime as dt


n_pts = 100
dates = [dt.datetime.now() + dt.timedelta(days=i) for i in range(n_pts)]

# counter=db.daq
counter = range(100)
ax1 = plt.subplot(3, 1, 1)
ax1.plot(counter, range(100))
plt.title('Motor')
plt.xlabel('Counter')
plt.ylabel('Raw Encoder')

ax2 = plt.subplot(3, 1, 2, sharex=ax1)
ax2.plot(counter, range(100))
plt.title('CH1')
plt.xlabel('Counter')
plt.ylabel('Volt')

ax3 = plt.subplot(3, 1, 3, sharex=ax1)
ax3.plot(counter, range(100))
plt.title('Sensor')
plt.xlabel('Counter')
plt.ylabel('mBar')

# Now format the x axis. This *MUST* be done after all sharex commands are run.

# put no more than 10 ticks on the date axis.  
ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
# format the date in our own way.
# ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# rotate the labels on both date axes
for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(30)
for label in ax2.xaxis.get_ticklabels():
    label.set_rotation(30)
for label in ax3.xaxis.get_ticklabels():
    label.set_rotation(30)

# tweak the subplot spacing to fit the rotated labels correctly
plt.subplots_adjust(hspace=0.35, bottom=0.125)

plt.show()