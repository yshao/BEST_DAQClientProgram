### populate CS frames ###
import os
import sqlite3
import pandas.io.sql as psql
import shutil
from common.sqliteutils import DaqDB

local='c:/datasets/buffer'
bufferp='%s/%s' % (local,'20000101_000203.recI')
db=DaqDB(bufferp)

con = sqlite3.connect(bufferp)

name='20000101_000203'
buffer2p='%s/%s' % (local,'20000101_000203.recI1')
db2=DaqDB(buffer2p)

recp='%s/%s' % ('c:/datasets/buffer','%s.recI' % name)
# os.remove('../enc.db')
# shutil.copy('../daq.db','../enc.db')
try:
    os.remove(buffer2p)
except:
    pass

shutil.copy('daq.db',buffer2p)


con.execute("attach database '%s' as recI1" % buffer2p)
con.execute("attach database '%s' as db1" % bufferp)
res=con.execute('select * from recI1.calib').fetchall()
# res=con.fetchall()
for s in res:
    print s

sql_con="select * from db1.inu where counter < (select counter from inu where rowid =(select max(rowid) from inu)) order by file_pos"

res=con.execute("insert into recI1.inu %s" % sql_con).fetchall()
# res=con.fetchall()
print len(res)
for s in res:
    print s


res=con.execute("select * from recI1.calib").fetchall()
# res=con.fetchall()
print len(res)
for s in res:
    print s

print "AREA"
res=con.execute(" SELECT * FROM recI1.inu where CS != '' limit 100").fetchall()
print len(res)
for s in res:
    print s

con.commit()
### same for inu ###
con = sqlite3.connect(buffer2p)

### interpolate
import numpy as np
import pandas as pd

with con:
    dr = psql.frame_query("SELECT *  from inu", con)

# local='c:/datasets/buffer'
# buffer2p='%s/%s' % (local,'20000101_000203.recI')
db=DaqDB(bufferp)

#
# s=pd.Series(dr)
# dr.fillna(np.nan)
# #
# dr=dr.interpolate()
# aTime=np.array(dr.interpolate())
# mlist=[(val[0],i+1) for i,val in enumerate(aTime)]
#
# con.executemany('UPDATE inu SET counter=? WHERE rowId=?', mlist)
# con.commit()

