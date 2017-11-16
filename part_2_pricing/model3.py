#for testing the system compared to base case, battery system for AS

import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import matplotlib
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

data = pd.read_csv('windmod4.csv',index_col=0)
#column names: date, time, dt, forecast, actual, delta, dev, peak
ecap = [2,6,10,14,18,22,26,30] #21 MWh sample storage capacity
totalcash = [] #store total cash for NPV usage later

for j in range(len(ecap)):
    bank = 0 #$ cash in and out flow
    maxflow = 0
    crate = 0.5
    cond = 0
    captotal = ecap[j]
    capacity = captotal*0.9 #adding in maximum DoD of 80%
    #example, 2MWh capacity, crate of 0.5, delivers 1 MW for 2 hours, 1MW is our commitment
    commit = crate*capacity #into the AS market
    etrans = 0.88*commit*0.25 #energy transfered in each 15min. transaction in AS mkt
    soc = []
    store = 0.2*captotal #current store level in battery
    print capacity    
    for i in range(len(data)):

        daytime = data.dt.loc[i]
        time = daytime.split(' ')[1]
        hour = int(time.split(':')[0])
        
        #STORAGE HOURS
        if hour >= 0 and (hour <= 16 or hour >= 19):
            #commit to down reg market for two hours between 4-6am, reserve this slot in battery
            if hour == 5 or hour == 6:
                bank = bank + data.regdn.loc[i]*commit
                store = store + etrans
                
            #condition 0, energy within 2% deviation is sold at DA rate:
            if np.abs(data.dev.loc[i]) <= 2:
                bank = bank + data.dam.loc[i]*(data.actual.loc[i])

            #deviation condition 1, sell or store excess energy
            elif np.abs(data.dev.loc[i]) > 2:
                bank = bank + data.dam.loc[i]*(data.forecast.loc[i]) + data.rtm.loc[i]*(data.delta.loc[i]) #pay lacking at LMP 

        #NON-STORE HOURS        
        else:
            #commit to up reg market for 1 hours at 1700, battery capacity is guaranteed from down reg
            if hour == 17 or hour == 18:
                bank = bank + data.regup.loc[i]*commit
                store = store - etrans
            
            #condition 0, energy within 2% deviation is sold at DA rate:
            if np.abs(data.dev.loc[i]) <= 2:
                bank = bank + data.dam.loc[i]*(data.actual.loc[i])
  
            #deviation condition 1, sell excess at peak price if delta is positive
            elif np.abs(data.dev.loc[i]) > 2:
                bank = bank + data.dam.loc[i]*(data.forecast.loc[i]) + data.rtm.loc[i]*(data.delta.loc[i]) #sell day-ahead at DA

        soc.append(store/captotal*100)
    print bank
    totalcash.append(bank)

print totalcash

dates = data['dt']
datesmod = [datetime.strptime(i, '%d/%m/%y  %H:%M') for i in dates]
'''
#sns.set_style("ticks")
#sns.despine()
plt.plot(datesmod[0:960],soc[0:960])
plt.xlabel('Date')
plt.ylabel('SoC %')
plt.title('State of Charge (18MWh Battery) During the First 10 Days Of Model')
sns.plt.show()'''