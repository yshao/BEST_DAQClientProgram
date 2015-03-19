import pandas as pd
from pandas.lib import to_datetime
from common.env import Env

idx = pd.date_range('09-01-2013', '09-30-2013')

s = pd.Series({'09-02-2013': 2,
               '09-03-2013': 10,
               '09-06-2013': 5,
               '09-07-2013': 1})
s.index = pd.DatetimeIndex(s.index)

s = s.reindex(idx, fill_value=0)
# print(s)
#
# s = pd.Series({})
#
# s.reindex('CS',fill_value=0)




homepath=Env().getParam()['HOME']
# homepath=cfg.getpath('HOME')

import pandas.io.sql as psql
import sqlite3 as lite
buf='daqmanager/inu.db'
bufferp='%s/%s'%(homepath,buf)
print bufferp
con = lite.connect(bufferp)
with con:
    sql = "SELECT CS,counter FROM inu where CS >= 0"
    df = psql.frame_query(sql, con)
    print df.shape




import numpy as np
def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

nd=np.array(df)
# print nd
mnd=moving_average(nd[0])
# print df['counter'].reindex(df['CS'])

# df.apply(pd.pandas.Series.interpolate)
# print df[(np.abs(df) > 200).any(1)]
# print df
# print df.ix[2]
# a=df.ix[:,1].values
# print a
# print to_datetime(a)
# print df['counter'].fillna('')
# print df.interpolate()

# print mnd.shape

def get_gaps(series):
    """
    @param series: a continuous time series of data with the index's freq set
    @return: a series where the index is the start of gaps, and the values are
         the ends
    """
    missing = series.isnull()
    different_from_last = missing.diff()

    # any row not missing while the last was is a gap end
    gap_ends = series[~missing & different_from_last].index

    # count the start as different from the last
    different_from_last[0] = True

    # any row missing while the last wasn't is a gap start
    gap_starts = series[missing & different_from_last].index

    # check and remedy if series ends with missing data
    if len(gap_starts) > len(gap_ends):
         gap_ends = gap_ends.append(series.index[-1:] + series.index.freq)

    return pd.Series(index=gap_starts, data=gap_ends)

# print get_gaps(df)
# print df.T.unstack()
# print df.isnull()

# print pd.DataFrame(range(0,255))

p=pd.DataFrame(range(0,255))
nn=np.array(range(0,255))
nd=np.array(df['CS'])
nt=np.array(df['counter'])
# ar=np.array(df)
# for a in ar:
# #     if ar[a] != ar
# for i in nd:
#     ""
#     if nd[i] - p.ix[i,0] > 1):
#     elif nd[i] - p.ix[i,0] < 0):
#     else:

# df['gap']=np.where(df['CS'])
# print nd
ndiff =np.diff(nd)
# nn=np.array(range(0,255))
# for r in ndiff:
#     s=nn(r)
#     i=ndiff[r]
    # np.array(range(s,s+diff))

ndd=np.where(ndiff < 0)
mpad=ndd[0].shape[0]
nnm=np.array([])
for i in range(0,mpad):
    nnm=np.hstack([nnm,nn])
print nnm.shape
# for r in nd:
#     i=nd[r]
#     data=nt[r]
#     nd[i,1]=data

