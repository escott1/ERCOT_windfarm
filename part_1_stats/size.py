#for testing the system compared to base case, input variables

import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import matplotlib
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from datetime import datetime

data = pd.read_csv('windmod2.csv',index_col=0)
#column names: date, time, dt, forecast, actual, delta, dev, peak
#recall deviation distribution: mean is -24.97% as a first guess, I'd want to cover all deficits below
#96 readings in a day (4 per hour)

DA = 15 #$20/MWh day-ahead rate is always the same
PP = 200 #$100/MWh real-time PEAK PRICE
OP = 20 #$50/MWh real-time OFF PEAK PRICE
bank = 0

edef = [] #energy deficits

for i in range(len(data)):
    #concerned about peak
    if data.peak.loc[i] == 1 and data.delta.loc[i]<0:
        edef.append(data.delta.loc[i])
    if data.peak.loc[i] == 0 or data.delta.loc[i]>=0:
        edef.append(0)

daydef = [] #bin the deficits per day, sum every 96 values and store
for i in range(0,365):
    eday = i
    energy = 0
    for j in range(0,96):
        energy = energy + edef[j+(96*eday)] #store the deficit for each day
    daydef.append(energy)

# print len(daydef) #check, should be 365
day_df = Series(daydef)
print day_df.describe()

num_bins = 45
devhist = np.array(day_df)
mu = float(np.mean(day_df))
sigma = float(np.std(day_df))
n, bins, patches = plt.hist(devhist, num_bins, facecolor='green', alpha=0.5)
y = mlab.normpdf(bins, mu, sigma)
plt.ylabel('Count')
plt.xlabel('Total Peak Energy Deficit (MWh) For a Given Day')
plt.plot(bins, y, 'k--')
plt.show()
