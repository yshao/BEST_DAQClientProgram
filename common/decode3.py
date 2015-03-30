import sqlite3
import pandas.io.sql as psql
import shutil
from common.sqliteutils import DaqDB

local='c:/datasets/buffer'

name='20000101_000203'
buffer2p='%s/%s' % (local,'20000101_000203.recI1')
### same for inu ###
con = sqlite3.connect(buffer2p)

### interpolate
import numpy as np
import pandas as pd

with con:
    dr = psql.frame_query("SELECT counter  from inu", con)

# local='c:/datasets/buffer'
# buffer2p='%s/%s' % (local,'20000101_000203.recI')
# db=DaqDB(bufferp)

#
s=pd.Series(dr)
dr.fillna(np.nan)
aTime=np.array(dr.interpolate())
mlist=[(val[0],i+1) for i,val in enumerate(aTime)]
#
print mlist[0:100]
con.executemany('UPDATE inu SET counter=? WHERE rowId=?', mlist)
con.commit()