from timeseries import *
d1 = datetime.datetime(2010,1,1)
d2 = datetime.datetime(2011,1,1)
fd = FinancialData('MT.PA', d1, d2)

t1 = TimeSeries(fd.data.low, time=fd.data.date)
event1 = Event(datetime.datetime(2010, 11, 8), "event1", t1.data[10], "ev1")
event2 = Event(datetime.datetime(2010, 12, 8), "event2", t1.data[32], "ev2")
t1.events.addevent(event1)
t1.events.addevent(event2)

t1.plot()
t2 = t1.gettsbetweenevents('ev1', 'ev2')
t2.plot('xg-', keep=True)  # to not erase the previous plot