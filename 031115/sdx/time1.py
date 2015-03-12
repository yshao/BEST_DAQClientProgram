import os
import csv
from math import *
from random import *

name_file='Bastia.txt'
path='C:/Users/gensolle/Desktop/These/DEV/Modeles_energetiques/eolien/%s' % name_file
f = open(path)
reader = csv.reader(f, delimiter=" ")
for cpt in range(10):
    print reader.next()



speed = []
f = open(path)
reader = csv.reader(f, delimiter=" ")
for line in reader:
   if line[2] == '':
      speed.append('nan')
   else:
      speed.append(line[2])


import pandas as pd
from dateutil.parser import parse

#creating the index for the time serie
dates = pd.date_range(parse('1/1/2006',dayfirst=True), parse('23/12/2012 21h00',dayfirst=True),freq='3h')

#creating the actual time serie with a 3 hours frequency
timeserie = pd.Series([float(nb) for nb in speed], index = dates)

#If the frequency is not convenient, there are methods to resample
timeserie = timeserie.resample('H', fill_method = 'ffill')  #hourly time serie from a '3h' time serie
Daily_timeserie = timeserie.resample('D', how = 'mean')     #daily time serie from a hourly time serie

#Interpolation for non informed entries
timeserie = timeserie.interpolate() 
Daily_timeserie = Daily_timeserie.interpolate() 

#Converting wind speed data from km/h to m/
timeserie = timeserie.apply(lambda x:ceil(float(x)*10/36))
Daily_timeserie = Daily_timeserie.apply(lambda x:ceil(float(x)*10/36))


import matplotlib.pyplot as plt
timeserie.resample('M',how='mean').plot(label='observed data monthly resampled')
plt.xlabel('time')
plt.ylabel('Wind Speed (m/s)')
plt.legend()


Daily_timeserie['01/01/07':'31/03/07'].plot(label='obserded data daily resampled')
plt.xlabel('time')
plt.ylabel('Wind Speed (m/s)')
plt.legend()
plt.show()



import statsmodels.tsa.stattools
import numpy as np

auto_correlation = np.apply_along_axis(lambda x: statsmodels.tsa.stattools.acf(x), 0, timeserie)
plt.plot(range(len(auto_correlation)),auto_correlation, label = 'autocorrelation of observed wind speed')
plt.xlabel('lags (hours)')
plt.ylabel('Autocorrelation')
plt.legend()

