# Plot encoder with quadrant info

import pandas as pd
import matplotlib.pyplot as plt
from best.common.sqliteutils import DaqDB

df=pd.DataFrame()
conn=DaqDB("../enc.db")
counter=conn.load_pd_data("SELECt counter FROM enc LIMIT 100")
import sqlite3
import pandas.io.sql as sql

db=sqlite3.connect("../enc.db")

# ch1=conn.load_pd_data("SELECt ch1 FROM rad LIMIT 100")
# ch2=conn.load_pd_data("SELECt ch2 FROM rad LIMIT 100")
# ch3=conn.load_pd_data("SELECt ch3 FROM rad LIMIT 100")
# ch4=conn.load_pd_data("SELECt ch4 FROM rad LIMIT 100")
# ch5=conn.load_pd_data("SELECt ch5 FROM rad LIMIT 100")
# ch6=conn.load_pd_data("SELECt ch6 FROM rad LIMIT 100")

# enc=conn.load_pd_data("SELECT encoder_counter FROM enc LIMIT 100")
mo=sql.read_sql("SELECT counter,encoder_counter,mo1,mo2 FROM enc WHERE mo1 != \"\" LIMIT 3000",db)

# print enc
import numpy as np


mo.ix[mo.mo1 > 0,['mo1']] = 1
mo.ix[mo.mo2 > 0,['mo2']] = 1
mo['mo1']=mo['mo1'].astype(str)
mo['mo2']=mo['mo2'].astype(str)


# mo['qua']

print mo
mo['qua']=mo.apply(lambda row: int(row['mo2']+row['mo1'],2),axis=1)


counter=counter.interpolate()

# print mo

# np.nan_to_num(mo['mo1'])
# np.nan_to_num(mo['mo2'])

# print np.where(mo['mo1'] != np.nan)

# print mo
# mo['quadrant']=np.where(mo['mo1'] != np.nan and mo['mo2'] != np.nan,int(str(mo['mo1'])+str(mo['mo2']),2))

# print mo

# print conn.__dict__.keys()
#

#
# print counter
#
# # counter = range(100)
# ax1 = plt.subplot(1, 1, 1)
# ax1.plot(counter, ch1)
# plt.title('Radiometer')
# plt.xlabel('Counter')
# plt.ylabel('Raw Counts')
#
# # ax1.plot(counter, ch2)
# ax1.plot(counter, ch3)
# ax1.plot(counter, ch4)
# ax1.plot(counter, ch5)
# ax1.plot(counter, ch6)
# plt.legend()
#
# plt.show()


### plot encoder
ax1 = plt.subplot(3, 1, 1)
plt.title('Encoder')
plt.xlabel('Counter')
plt.ylabel('Quadrant Zone')

# ax1.plot(counter, ch2)
ax1.plot(mo['qua'])


ax1 = plt.subplot(3, 1, 2)
plt.title('Encoder')
plt.xlabel('Counter')
plt.ylabel('Encoder raw counter')

# ax1.plot(counter, ch2)
ax1.plot(mo['encoder_counter'])


# ax1 = plt.subplot(3, 1, 3)
# # plt.title('Encoder')
# plt.xlabel('Counter')
# plt.ylabel('SensorP1')

# ax1.plot(counter, ch2)
# ax1.plot(mo['c1_s6'])


### counter ###
# ax1 = plt.subplot(4, 1, 4)
# plt.title('Encoder')
# plt.xlabel('Counter')
# plt.ylabel('Counter')

# ax1.plot(counter, ch2)
# ax1.plot(counter)


# ax1.plot(counter, ch4)
# ax1.plot(counter, ch5)
# ax1.plot(counter, ch6)
plt.legend()
plt.show()


