from pandas import DataFrame
from pandas import *
import numpy

ts = Series(numpy.random.randn(1000), index=date_range('1/1/2000', periods=1000))

ts = ts.cumsum()

ts.plot(style='k--')

rolling_mean(ts, 60).plot(style='k')

df = DataFrame(numpy.random.randn(1000, 4), index=ts.index,
                   columns=['A', 'B', 'C', 'D'])


df = df.cumsum()


rolling_sum(df, 60).plot(subplots=True)


mad = lambda x: np.fabs(x - x.mean()).mean()
rolling_apply(ts, 60, mad).plot(style='k')


ser = Series(numpy.random.randn(10), index=date_range('1/1/2000', periods=10))
rolling_window(ser, 5, 'triang')
rolling_window(ser, 5, 'boxcar')
rolling_mean(ser, 5)
rolling_window(ser, 5, 'gaussian', std=0.1)
rolling_window(ser, 5, 'boxcar')
rolling_window(ser, 5, 'boxcar', center=True)
rolling_mean(ser, 5, center=True)


df2 = df[:20]
rolling_corr(df2, df2['B'], window=5)

covs = rolling_cov(df[['B','C','D']], df[['A','B','C']], 50, pairwise=True)
covs[df.index[-50]]

correls = rolling_corr(df, 50)
correls[df.index[-50]]

correls.ix[:, 'A', 'C'].plot()


rolling_mean(df, window=len(df), min_periods=1)[:5]

expanding_mean(df)[:5]

ts.plot(style='k--')

expanding_mean(ts).plot(style='k')