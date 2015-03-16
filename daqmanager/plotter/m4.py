import pandas as pd
import matplotlib.pyplot as plt
from common.sqliteutils import DaqDB

df=pd.DataFrame()
conn=DaqDB("../daq.db")
counter=conn.load_pd_data("SELECt counter FROM rad LIMIT 100")

ch1=conn.load_pd_data("SELECt ch1 FROM rad LIMIT 100")
ch2=conn.load_pd_data("SELECt ch2 FROM rad LIMIT 100")
ch3=conn.load_pd_data("SELECt ch3 FROM rad LIMIT 100")
ch4=conn.load_pd_data("SELECt ch4 FROM rad LIMIT 100")
ch5=conn.load_pd_data("SELECt ch5 FROM rad LIMIT 100")
ch6=conn.load_pd_data("SELECt ch6 FROM rad LIMIT 100")

print conn.__dict__.keys()

counter=counter.interpolate()

print counter

# counter = range(100)
ax1 = plt.subplot(1, 1, 1)
ax1.plot(counter, ch1)
plt.title('Radiometer')
plt.xlabel('Counter')
plt.ylabel('Raw Counts')

# ax1.plot(counter, ch2)
ax1.plot(counter, ch3)
ax1.plot(counter, ch4)
ax1.plot(counter, ch5)
ax1.plot(counter, ch6)
plt.legend()

plt.show()