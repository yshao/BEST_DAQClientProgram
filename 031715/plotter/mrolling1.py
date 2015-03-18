# Plot sensor data in raw counts
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import pandas.io.sql as sql

db=sqlite3.connect("../daq.db")

### plot sensor 1
hsens1=sql.read_sql("SELECT TEMP,P FROM converted1  LIMIT 3000",db)
hsens1=hsens1.interpolate()

ax1 = plt.subplot(6, 2, 1)
plt.title('PSensor 1')
plt.xlabel('Counter')
plt.ylabel('C1_T')
ax1.plot(hsens1['TEMP'])

ax1 = plt.subplot(6, 2, 2)
plt.xlabel('Counter')
plt.ylabel('C1_P')
ax1.plot(hsens1['P'])

### plot hum sensor 2
hsens2=sql.read_sql("SELECT TEMP,P FROM converted2  LIMIT 3000",db)
hsens2=hsens2.interpolate()

ax1 = plt.subplot(6, 2, 3)
plt.title('PSensor 2')
plt.xlabel('Counter')
plt.ylabel('C2_T')
ax1.plot(hsens2['TEMP'])

ax1 = plt.subplot(6, 2, 4)
plt.xlabel('Counter')
plt.ylabel('C2_P')
ax1.plot(hsens2['P'])

### plot sensor 3
hsens1=sql.read_sql("SELECT TEMP,P FROM converted3  LIMIT 3000",db)
hsens1=hsens1.interpolate()

ax1 = plt.subplot(6, 2, 5)
plt.title('PSensor 3')
plt.xlabel('Counter')
plt.ylabel('C3_T')
ax1.plot(hsens1['TEMP'])

ax1 = plt.subplot(6, 2, 6)
plt.xlabel('Counter')
plt.ylabel('C3_P')
ax1.plot(hsens1['P'])

### plot sensor 4
hsens1=sql.read_sql("SELECT TEMP,P FROM converted4  LIMIT 3000",db)
hsens1=hsens1.interpolate()

ax1 = plt.subplot(6, 2, 7)
plt.title('PSensor 4')
plt.xlabel('Counter')
plt.ylabel('C4_T')
ax1.plot(hsens1['TEMP'])

ax1 = plt.subplot(6, 2, 8)
plt.xlabel('Counter')
plt.ylabel('C4_P')
ax1.plot(hsens1['P'])

### plot sensor 5
hsens1=sql.read_sql("SELECT TEMP,P FROM converted5  LIMIT 3000",db)
hsens1=hsens1.interpolate()

pd.rolling_window(hsens1,10)

ax1 = plt.subplot(6, 2, 9)
plt.title('PSensor 5')
plt.xlabel('Counter')
plt.ylabel('C5_T')
ax1.plot(hsens1['TEMP'])


ax1 = plt.subplot(6, 2, 10)
plt.xlabel('Counter')
plt.ylabel('C5_P')
ax1.plot(hsens1['P'])

h1r=pd.rolling_window(hsens1,10,1)
print h1r


### plot sensor 6
hsens1=sql.read_sql("SELECT TEMP,P FROM converted6  LIMIT 3000",db)
hsens1=hsens1.interpolate()

ax1 = plt.subplot(6, 2, 11)
plt.title('PSensor 4')
plt.xlabel('Counter')
plt.ylabel('C6_T')
ax1.plot(hsens1['TEMP'])

ax1 = plt.subplot(6, 2, 12)
plt.xlabel('Counter')
plt.ylabel('C6_P')
ax1.plot(hsens1['P'])

plt.legend()
plt.show()