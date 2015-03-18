# Plot sensor data in raw counts
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

sens1=sql.read_sql("SELECT counter,c1_s2,c1_s6 FROM enc  LIMIT 3000",db)
sens2=sql.read_sql("SELECT counter,c2_s2,c2_s6 FROM enc  LIMIT 3000",db)
sens3=sql.read_sql("SELECT counter,c3_s2,c3_s6 FROM enc  LIMIT 3000",db)
sens4=sql.read_sql("SELECT counter,c4_s2,c4_s6 FROM enc  LIMIT 3000",db)
sens5=sql.read_sql("SELECT counter,c5_s2,c5_s6 FROM enc  LIMIT 3000",db)
sens6=sql.read_sql("SELECT counter,c6_s2,c6_s6 FROM enc  LIMIT 3000",db)

# print enc
import numpy as np


sens1=sens1.interpolate()
sens2=sens2.interpolate()
sens3=sens3.interpolate()
sens4=sens4.interpolate()
sens5=sens5.interpolate()
sens6=sens6.interpolate()

# mo.ix[mo.mo1 > 0,['mo1']] = 1
# mo.ix[mo.mo2 > 0,['mo2']] = 1
# mo['mo1']=mo['mo1'].astype(str)
# mo['mo2']=mo['mo2'].astype(str)

# mo['qua']=mo.apply(lambda row: int(row['mo2']+row['mo1'],2),axis=1)


counter=counter.interpolate()


### plot sensor 1
ax1 = plt.subplot(6, 2, 1)
plt.title('Sensor 1')
plt.xlabel('Counter')
plt.ylabel('C1_T')
ax1.plot(sens1['c1_s2'])


ax1 = plt.subplot(6, 2, 2)
plt.xlabel('Counter')
plt.ylabel('C1_P')
ax1.plot(sens1['c1_s6'])

# plt.legend()
# plt.show()

### plot sensor 2
ax1 = plt.subplot(6, 2, 3)
plt.title('Sensor 2')
plt.xlabel('Counter')
plt.ylabel('C2_T')
ax1.plot(sens2['c2_s2'])


ax1 = plt.subplot(6, 2, 4)
plt.xlabel('Counter')
plt.ylabel('C2_P')
ax1.plot(sens2['c2_s6'])

# plt.legend()
# plt.show()



### plot sensor 3
ax1 = plt.subplot(6, 2, 5)
plt.title('Sensor 3')
plt.xlabel('Counter')
plt.ylabel('C3_T')
ax1.plot(sens3['c3_s2'])


ax1 = plt.subplot(6, 2, 6)
plt.xlabel('Counter')
plt.ylabel('C3_P')
ax1.plot(sens3['c3_s6'])

# plt.legend()
# plt.show()


### plot sensor 4
ax1 = plt.subplot(6, 2, 7)
plt.title('Sensor 4')
plt.xlabel('Counter')
plt.ylabel('C4_T')
ax1.plot(sens4['c4_s2'])


ax1 = plt.subplot(6, 2, 8)
plt.xlabel('Counter')
plt.ylabel('C4_P')
ax1.plot(sens4['c4_s6'])

# plt.legend()
# plt.show()


### plot sensor 5
ax1 = plt.subplot(6, 2, 9)
plt.title('Sensor 5')
plt.xlabel('Counter')
plt.ylabel('C5_T')
ax1.plot(sens5['c5_s2'])


ax1 = plt.subplot(6, 2, 10)
plt.xlabel('Counter')
plt.ylabel('C5_P')
ax1.plot(sens5['c5_s6'])

# plt.legend()
# plt.show()


### plot sensor 6
ax1 = plt.subplot(6, 2, 11)
plt.title('Sensor 6')
plt.xlabel('Counter')
plt.ylabel('C6_T')
ax1.plot(sens6['c6_s2'])


ax1 = plt.subplot(6, 2, 12)
plt.xlabel('Counter')
plt.ylabel('C6_P')
ax1.plot(sens6['c6_s6'])


plt.legend()
plt.show()


### plot hum sensor 1
hsens1=sql.read_sql("SELECT counter,c1_s4,c1_s5 FROM enc  LIMIT 3000",db)
hsens1=hsens1.interpolate()

ax1 = plt.subplot(7, 2, 1)
plt.title('HSensor 1')
plt.xlabel('Counter')
plt.ylabel('C1_RH')
ax1.plot(hsens1['c1_s4'])

ax1 = plt.subplot(7, 2, 2)
plt.xlabel('Counter')
plt.ylabel('C1_T')
ax1.plot(hsens1['c1_s5'])

### plot hum sensor 2
hsens2=sql.read_sql("SELECT counter,c2_s4,c2_s5 FROM enc  LIMIT 3000",db)
hsens2=hsens2.interpolate()

ax1 = plt.subplot(7, 2, 3)
plt.title('HSensor 2')
plt.xlabel('Counter')
plt.ylabel('C2_RH')
ax1.plot(hsens2['c2_s4'])

ax1 = plt.subplot(7, 2, 4)
plt.xlabel('Counter')
plt.ylabel('C2_T')
ax1.plot(hsens2['c2_s5'])

### plot hum sensor 3
hsens3=sql.read_sql("SELECT counter,c3_s4,c3_s5 FROM enc  LIMIT 3000",db)
hsens3=hsens3.interpolate()

ax1 = plt.subplot(7, 2, 5)
plt.title('HSensor 3')
plt.xlabel('Counter')
plt.ylabel('C3_RH')
ax1.plot(hsens3['c3_s4'])

ax1 = plt.subplot(7, 2, 6)
plt.xlabel('Counter')
plt.ylabel('C3_T')
ax1.plot(hsens3['c3_s5'])


### plot hum sensor 4
hsens4=sql.read_sql("SELECT counter,c4_s4,c4_s5 FROM enc  LIMIT 3000",db)
hsens4=hsens4.interpolate()

ax1 = plt.subplot(7, 2, 7)
plt.title('HSensor 4')
plt.xlabel('Counter')
plt.ylabel('C4_RH')
ax1.plot(hsens4['c4_s4'])

ax1 = plt.subplot(7, 2, 8)
plt.xlabel('Counter')
plt.ylabel('C4_T')
ax1.plot(hsens4['c4_s5'])


### plot hum sensor 5
hsens5=sql.read_sql("SELECT counter,c5_s4,c5_s5 FROM enc  LIMIT 3000",db)
hsens5=hsens5.interpolate()

ax1 = plt.subplot(7, 2, 9)
plt.title('HSensor 5')
plt.xlabel('Counter')
plt.ylabel('C5_RH')
ax1.plot(hsens5['c5_s4'])

ax1 = plt.subplot(7, 2, 10)
plt.xlabel('Counter')
plt.ylabel('C5_T')
ax1.plot(hsens5['c5_s5'])

### plot hum sensor 6
hsens6=sql.read_sql("SELECT counter,c6_s4,c6_s5 FROM enc  LIMIT 3000",db)
hsens6=hsens6.interpolate()

ax1 = plt.subplot(7, 2, 11)
plt.title('HSensor 6')
plt.xlabel('Counter')
plt.ylabel('C6_RH')
ax1.plot(hsens6['c6_s4'])

ax1 = plt.subplot(7, 2, 12)
plt.xlabel('Counter')
plt.ylabel('C6_T')
ax1.plot(hsens6['c6_s5'])

### plot hum sensor 6
hsens8=sql.read_sql("SELECT counter,c8_s4,c8_s5 FROM enc  LIMIT 3000",db)
hsens8=hsens8.interpolate()

ax1 = plt.subplot(7, 2, 13)
plt.title('HSensor 8')
plt.xlabel('Counter')
plt.ylabel('C8_RH')
ax1.plot(hsens8['c8_s4'])

ax1 = plt.subplot(7, 2, 14)
plt.xlabel('Counter')
plt.ylabel('C8_T')
ax1.plot(hsens8['c8_s5'])


plt.legend()
plt.show()