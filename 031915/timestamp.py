import numpy as np
import sqlite3

conn = sqlite3.connect('test.db')

cur = conn.cursor()

cur.execute('select * from table1')
# Out[5]: <sqlite3.Cursor object at 0xa3142c0>

CS=np.array(cur.fetchall())
import sqlite3 as db

# db.fetchall()
# import esutil

### INT: aTime ###
aTime=np.array()

aDiff=aTime[np.where()]

aCS=np.array(range(0.255))

aCSCounter=np.vstack(aCS)

### slide timestamp counter into aCS counter
for i in aDiff:
  st=aDiff[i]
  end=aDiff[i+1]
  aCSSub=aDiff[st:end]
  # for

aCSCounter=np.vstack((aCSCounter,aCSSub))
 

###

indices = np.arange(features.shape[0])
feature_indices = F(l)

features.flat[indices, feature_indices] = 1



