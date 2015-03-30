### insert time
import sqlite3
import pandas
from common.env import Env
from common.sqliteutils import DaqDB

import pandas.io.sql as psql
cfg=Env().getConfig()
# local=cfg['local_dir']


# data=db.select_data('select counter from enc')
import pandas.io.sql as sql




# sql.
# dr=pd.Series(dr)

# print dr
# dr.apply(pandas.Series.interpolate)
# dr.interpolate()
# s.interpolate()
# print dr
# print s

### interpolate linear ###
import pandas as pd
import numpy as np
# s = pd.Series([0, 1, np.nan, 3])
#
# print s.interpolate()


# print  map(tuple, aTime.tolist())
### fill a column numpt numpy array ###

# aTime=select counter frm enc
#     cur=con.cursor()
# print cur
# aTime=np.array([1 ,2 ,3])
# aT
# tup= tuple(map(tuple,aTime.tolist()))
# print aTime.tolist()
# tuple
# aTime=['1','2','3']
# print aTime

# con.executemany('UPDATE enc SET counter=?', ((val,) for val in aTime))
# con.execute('update enc set counter=1')
# cur.executemany("UPDATE enc SET counter= ?", map(tuple, aTime.tolist()))
# for v in aTime:
#     print v[0]
# my_data = ({id=1, value='foo'}, {id=2, value='bar'})
# my_data=[[2,0],[2,1],[1,2]]

# for val in my_data:
#     print (val[0],val[1])
# for i,val in enumerate(aTime):
#     print i, val[0]


# print mlist[0:10]
# mlist=[(2,0),(3,1)]



### populate CS frames ###
# local='c:/datasets/buffer'
# bufferp='%s/%s' % (local,'20000101_000203.recI')
# db=DaqDB(bufferp)
#
# con = sqlite3.connect(bufferp)
#
# buffer2p='%s/%s' % (local,'20000101_000203.recI1')
# db2=DaqDB(buffer2p)
#
# con.execute('attach database %s as recI1')
# con.execute('INSERT OR REPLACE INTO rectI1.inu SELECT * FROM db1.inu order by counte')
#
#
# ### same for inu ###
# con = sqlite3.connect(buffer2p)
#
# ### interpolate
# with con:
#     dr = psql.frame_query("SELECT  from inu", con)
#
# # local='c:/datasets/buffer'
# # buffer2p='%s/%s' % (local,'20000101_000203.recI')
# db=DaqDB(bufferp)
#
# #
# s=pd.Series(dr)
# dr.fillna(np.nan)
# #
# dr=dr.interpolate()
# aTime=np.array(dr.interpolate())
# mlist=[(val[0],i+1) for i,val in enumerate(aTime)]
#
# con.executemany('UPDATE inu SET counter=? WHERE rowId=?', mlist)
# con.commit()
#
