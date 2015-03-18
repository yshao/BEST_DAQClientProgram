# Plot sensor data in raw counts
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import pandas.io.sql as sql

db=sqlite3.connect("../daq.db")

num_pts=100

### plot sensor 1
hsens1=sql.read_sql("SELECT T,Rhi FROM converted1h  LIMIT %s" % num_pts,db)
hsens1=hsens1.interpolate()

ax1 = plt.subplot(6, 2, 1)
plt.title('HPSensor 1')
plt.xlabel('Counter')
plt.ylabel('C1_TEMP')
ax1.plot(hsens1['T'])

ax1 = plt.subplot(6, 2, 2)
plt.xlabel('Counter')
plt.ylabel('C1_H')
ax1.plot(hsens1['Rhi'])

### plot hum sensor 2
hsens2=sql.read_sql("SELECT T,Rhi FROM converted2h  LIMIT %s" % num_pts,db)
hsens2=hsens2.interpolate()

ax1 = plt.subplot(6, 2, 3)
plt.title('HSensor 2')
plt.xlabel('Counter')
plt.ylabel('C2_T')
ax1.plot(hsens2['T'])

ax1 = plt.subplot(6, 2, 4)
plt.xlabel('Counter')
plt.ylabel('C2_H')
ax1.plot(hsens2['RHi'])

### plot sensor 3
hsens3=sql.read_sql("SELECT T,RHi FROM converted3h  LIMIT %s" % num_pts,db)
hsens3=hsens1.interpolate()

ax1 = plt.subplot(6, 2, 5)
plt.title('HSensor 3')
plt.xlabel('Counter')
plt.ylabel('C3_T')
ax1.plot(hsens3['T'])

ax1 = plt.subplot(6, 2, 6)
plt.xlabel('Counter')
plt.ylabel('C3_H')
ax1.plot(hsens3['RHi'])

### plot sensor 4
hsens4=sql.read_sql("SELECT T,RHi FROM converted4h  LIMIT %s" % num_pts,db)
hsens4=hsens4.interpolate()

ax1 = plt.subplot(6, 2, 7)
plt.title('HSensor 4')
plt.xlabel('Counter')
plt.ylabel('C4_T')
ax1.plot(hsens4['T'])

ax1 = plt.subplot(6, 2, 8)
plt.xlabel('Counter')
plt.ylabel('C4_H')
ax1.plot(hsens4['RHi'])

### plot sensor 5
hsens5=sql.read_sql("SELECT T,RHi FROM converted5h  LIMIT %s" % num_pts,db)
hsens5=hsens5.interpolate()

ax1 = plt.subplot(6, 2, 9)
plt.title('HSensor 5')
plt.xlabel('Counter')
plt.ylabel('C5_T')
ax1.plot(hsens5['T'])

ax1 = plt.subplot(6, 2, 10)
plt.xlabel('Counter')
plt.ylabel('C5_P')
ax1.plot(hsens5['RHi'])


### plot sensor 6
hsens6=sql.read_sql("SELECT T,RHi FROM converted6h  LIMIT %s" % num_pts,db)
hsens6=hsens6.interpolate()

ax1 = plt.subplot(6, 2, 11)
plt.title('HSensor 4')
plt.xlabel('Counter')
plt.ylabel('C6_T')
ax1.plot(hsens1['T'])

ax1 = plt.subplot(6, 2, 12)
plt.xlabel('Counter')
plt.ylabel('C6_H')
ax1.plot(hsens1['RHi'])

plt.legend()
plt.show()