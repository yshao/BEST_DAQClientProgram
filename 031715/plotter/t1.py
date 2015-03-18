import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import pandas.io.sql as sql

inudb=sqlite3.connect("../inu.db")
encdb=sqlite3.connect("../enc.db")
raddb=sqlite3.connect("../rad.db")

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
c1=sql.read_sql("SELECT counter,packet_len FROM inu  LIMIT 3000",inudb)
c1.astype(float)
c1=c1.interpolate()

time=sql.read_sql("SELECT timestamp FROM inu  LIMIT 3000",inudb)
time.astype(float)

c1A=c1.concat(time)

c2=sql.read_sql("SELECT counter,packet_len FROM enc  LIMIT 3000",encdb)
c2.astype(float)
c2=c2.interpolate()

c3A=sql.read_sql("SELECT counter,packet_len FROM rad  WHERE tailsymb == '::' LIMIT 3000",raddb)
c3A.astype(float)
c3A=c3A.interpolate()

c3B=sql.read_sql("SELECT counter,packet_len FROM rad  WHERE tailsymb == ';;' LIMIT 3000",raddb)
c3B.astype(float)
c3B=c3B.interpolate()

print c1
print c2
print c3A
print c3B

import pandas as pd

c5 = c1A.append(c2).append(c3A).append(c3B)
c5=c5.sort('counter')

db=sqlite3.connect("../daq.db")

sql.to_sql(c5[['counter','packet_len']],'ct',db,flavor='sqlite')

print c5
