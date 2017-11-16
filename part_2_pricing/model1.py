#BASE SCENARIO, follows algorithm, no battery to store

import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import matplotlib
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import DateFormatter
import seaborn as sns

data = pd.read_csv('windmod4.csv',index_col=0)
#column names: date, time, dt, forecast, actual, delta, dev, peak, prices...

bank = 0 #$ cash in and out flow
dcf = []
day = []
p = 0 # peak net
pp = 0 # paid peak
op = 0 #off peak net
pop = 0 #paid off peak
dates = data['dt']
datesmod = [datetime.strptime(i, '%d/%m/%y  %H:%M') for i in dates]

#the algorithm is split so we could track cashflows during peak and off-peak hrs if wanted
#start of payment strategy
for i in range(len(data)):
    print i
    
    #OFF PEAK HOURS        
    if data.peak.loc[i] == 0:
        #condition 0, energy within 2% deviation is sold at DA rate:
        if np.abs(data.dev.loc[i]) <= 2:
            bank = bank + data.dam.loc[i]*(data.actual.loc[i])
            op = op + data.dam.loc[i]*(data.actual.loc[i])
             
        #deviation condition, sell excess excess
        if data.delta.loc[i] > 0 and np.abs(data.dev.loc[i]) > 2:           
            bank = bank + data.dam.loc[i]*(data.forecast.loc[i]) + data.rtm.loc[i]*(data.delta.loc[i])
            op = op + data.dam.loc[i]*(data.forecast.loc[i]) + data.rtm.loc[i]*(data.delta.loc[i])
        
        #deviation condition, buy lacking energy
        if data.delta.loc[i] < 0 and np.abs(data.dev.loc[i]) > 2:
            bank = bank + data.dam.loc[i]*(data.forecast.loc[i]) + data.rtm.loc[i]*(data.delta.loc[i])
            op = op + data.dam.loc[i]*(data.forecast.loc[i]) + data.rtm.loc[i]*(data.delta.loc[i])
            pop = pop + data.rtm.loc[i]*(data.delta.loc[i])
            
    #PEAK HOURS        
    if data.peak.loc[i] == 1:

    #condition 0, energy within 2% deviation is sold at DA rate:
        if np.abs(data.dev.loc[i]) <= 2:
            bank = bank + data.dam.loc[i]*(data.actual.loc[i])
            p = p + data.dam.loc[i]*(data.actual.loc[i])
            
        #deviation condition, sell excess energy
        if data.delta.loc[i] > 0 and np.abs(data.dev.loc[i]) > 2:
            bank = bank + data.dam.loc[i]*(data.forecast.loc[i]) + data.rtm.loc[i]*(data.delta.loc[i]) 
            p = p + data.dam.loc[i]*(data.forecast.loc[i]) + data.rtm.loc[i]*(data.delta.loc[i]) 
            
        #deviation condition, buy lacking energy    
        if data.delta.loc[i] < 0 and np.abs(data.dev.loc[i]) > 2:
            bank = bank + data.dam.loc[i]*(data.forecast.loc[i]) + data.rtm.loc[i]*(data.delta.loc[i]) 
            p = p + data.dam.loc[i]*(data.forecast.loc[i]) + data.rtm.loc[i]*(data.delta.loc[i])
            pp = pp + data.rtm.loc[i]*(data.delta.loc[i])
            
    if (i+1)%96==0:
        day.append(datesmod[i])
        dcf.append(bank)

#revser = Series(rev)
#revser.to_csv('basecase.csv')

formatter = DateFormatter('%b/%y')
plt.plot(day,dcf)
plt.ylabel('YTD Revenue $')
plt.title('Wind Farm With No Battery Backup')

plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
sns.plt.show()

'''bank cashflow: $2,102,090.69
net from peak: $1,360,070.96
total paid during peak hours: -$321,980.28
from off-peak: $742,019.72
total paid during off-peak hours: -$158,978.15

all else equal if the forecast was perfect, 
could have made: $2,583,049.12
or only 81% of potential due to charges

'''

