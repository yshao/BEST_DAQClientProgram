from pandas import *
from sqlalchemy import create_engine
from numpy import *

engine2 = create_engine('sqlite:///daq.db')
connection2 = engine2.connect()
resoverall = connection2.execute("SELECT counter, timestamp from rad")

# print resoverall

import pandas as pd
from pandas import DataFrame
df = DataFrame(resoverall.fetchall())
df.columns = resoverall.keys()

print df

dates = pd.date_range('9/1/2014 12:30:00', periods=1441, freq='T')

n = 4
import numpy
print "Random:", numpy.random.uniform()

df1 = DataFrame(numpy.random.randn(n, 2), index=date_range('1/1/2001', periods=n, freq='30S'))
print df1

resampled1 = df1.resample('S')
print "resample at 1S"
print resampled1.head(10)

interp1 = resampled1.interpolate()
print "resample at 1S then interpolate"
print interp1.head(10)

print type(df1[1])

df['timestamp'] = pd.to_datetime(df['timestamp'])

import matplotlib.pyplot as plt

def myplot(df, ilist, clist):
    df1 = df[df['I'].isin(ilist)][clist + ['t', 'I']].set_index('t')
    fig, ax = plt.subplots(len(clist))
    for I, grp in df1.groupby('I'):
        for j, col in enumerate(clist):
            grp[col].plot(ax=ax[j], sharex=True)

myplot(df, [1, 4], ['A', 'B', 'C'])
plt.tight_layout() # cleans up the spacing of the plots


# print DatetimeIndex("9/1/2014 12:30:00")
# array(['2013-05-13 07:45:49', '2013-05-13 07:45:50'], dtype=datetime64[s])

# print interp.tail()

# print df1

resampled=df1.resample('30S')

print "resample at 30S"
print resampled.head(10)

interp = resampled.interpolate()

print interp.head()

print "Sampling"

rng = date_range('1/1/2000 00:00:00', '1/1/2000 00:13:00', freq='min',
                 name='index')
print rng
s = Series(np.random.randn(14), index=rng)

# s = Series(np.random.randn(14), index=counter)
# sre = s.resample('1000', how='mean', )
# ipl = sre.interpolate()

result = s.resample('5min', how='mean', closed='right', label='right')

print result
expected = Series([s[0], s[1:6].mean(), s[6:11].mean(), s[11:].mean()],
                  index=date_range('1/1/2000', periods=4, freq='5min'))

print expected
# assert_series_equal(result, expected)
# self.assertEqual(result.index.name, 'index')

result = s.resample('5min', how='mean', closed='left', label='right')

print result

expected = Series([s[:5].mean(), s[5:10].mean(), s[10:].mean()],
                  index=date_range('1/1/2000 00:05', periods=3,
                                   freq='5min'))
# assert_series_equal(result, expected)
print expected

# s = self.series
result = s.resample('5Min', how='last')

print result
# grouper = TimeGrouper(Minute(5), closed='left', label='left')
# expect = s.groupby(grouper).agg(lambda x: x[-1])
# assert_series_equal(result, expect)