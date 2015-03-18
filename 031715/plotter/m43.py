import pandas as pd
import matplotlib.pyplot as plt
from best.common.sqliteutils import DaqDB
import sqlite3
import pandas.io.sql as sql

db=sqlite3.connect("../inu.db")

class Plotter():
    def __init__(self):
        ""
    
    def set_labels(self,title,xLabel,yLabel):
        plt.title(title)
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.legend()
    
    def plot_data(self,query,num_dr):
        acc=sql.read_sql(query + " LIMIT %s" % num_dr,db)
        acc=acc.interpolate()
        
        for i in self.row*self.col:
            ax1 = plt.subplot(self.row, self.col, i)
            ax1.plot(acc['c1_s4'])
            

        plt.show()
    
    def set_dim(self,row,col):
        ""
        self.row=row
        self.col=col
        

        

### plot acc sensor
acc=sql.read_sql("SELECT counter,accX,accY,accZ FROM inu  LIMIT 3000",db)
acc=acc.interpolate()

print acc

ax1 = plt.subplot(3, 3, 1)
plt.title('Acc')
plt.xlabel('Counter')
plt.ylabel('accX')
ax1.plot(acc['accx'])

ax1 = plt.subplot(3, 3, 2)
plt.xlabel('Counter')
plt.ylabel('accY')
ax1.plot(acc['accy'])

ax1 = plt.subplot(3, 3, 3)
plt.xlabel('Counter')
plt.ylabel('accZ')
ax1.plot(acc['accz'])

### plot gyro sensor
gyr=sql.read_sql("SELECT counter,gyrX,gyrY,gyrZ FROM inu  LIMIT 3000",db)
gyr=gyr.interpolate()

ax1 = plt.subplot(3, 3, 4)
plt.title('Gyro')

plt.xlabel('Counter')
plt.ylabel('gyrX')
ax1.plot(gyr['gyrx'])

ax1 = plt.subplot(3, 3, 5)
plt.xlabel('Counter')
plt.ylabel('gyry')
ax1.plot(gyr['gyry'])

ax1 = plt.subplot(3, 3, 6)
plt.xlabel('Counter')
plt.ylabel('gyrz')
ax1.plot(gyr['gyrz'])

### plot mag sensor
mag=sql.read_sql("SELECT counter,magX,magY,magZ FROM inu  LIMIT 3000",db)
mag=mag.interpolate()

ax1 = plt.subplot(3, 3, 7)
plt.title('Mag')
plt.xlabel('Counter')
plt.ylabel('magX')
ax1.plot(mag['magx'])

ax1 = plt.subplot(3, 3, 8)
plt.xlabel('Counter')
plt.ylabel('magY')
ax1.plot(mag['magy'])

ax1 = plt.subplot(3, 3, 9)
plt.xlabel('Counter')
plt.ylabel('magZ')
ax1.plot(mag['magz'])


plt.legend()
plt.show()