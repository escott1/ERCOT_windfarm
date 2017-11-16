#for testing the system compared to base case, battery system for shifting production

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
ecap = [2] #21 MWh sample storage capacity
totalcash = [] #store total cash for NPV usage later
epow = []

for j in range(len(ecap)):
    store = 0 #current store level in battery
    bank = 0 #$ cash in and out flow
    maxflow = 0
    cond = 0
    capacity = ecap[j]
    soc = []
    for i in range(len(data)):
        print i
        transfer = 0
        #OFF PEAK HOURS
        if data.peak.loc[i] == 0:
    
        #condition 0, energy within 2% deviation is sold at DA rate:
            if np.abs(data.dev.loc[i]) <= 2:
                bank = bank + data.dam.loc[i]*(data.actual.loc[i])
    
            #deviation condition 1, store excess energy if delta is positive
            elif data.delta.loc[i] > 0 and np.abs(data.dev.loc[i]) > 2:
                if store+0.88*data.delta.loc[i] < capacity: #if battery can handle all excess
                
                    #round trip efficiency OF 92% + inverter efficiency of 95% added right at the beginning
                    transfer = 0.88*data.delta.loc[i]
            	    store = store + 0.88*transfer #put all excess into battery
            	    
            	    if transfer>maxflow:
            	        maxflow = transfer
                    bank = bank + data.dam.loc[i]*(data.forecast.loc[i]) #sell forecasted day-ahead at DA
  
                elif store+0.88*data.delta.loc[i] >= capacity: #if battery is nearing full *** do not overcharge
                    remainsell = capacity - store
                    transfer = remainsell
                    
                    if transfer>maxflow:
                        maxflow = transfer

                    store = capacity #set the battery level at the capacity
                    bank = bank + data.dam.loc[i]*(data.forecast.loc[i]) + data.rtm.loc[i]*(data.delta.loc[i]-remainsell) #sell the difference
                    
            #deviation condition 2,pay excess energy at the off-peak rate
            elif data.delta.loc[i] < 0 and np.abs(data.dev.loc[i]) > 2:
                bank = bank + data.dam.loc[i]*(data.forecast.loc[i]) + data.rtm.loc[i]*(data.delta.loc[i]) #pay lacking at LMP 
            
        #PEAK HOURS        
        elif data.peak.loc[i] == 1:

        #condition 0, energy within 2% deviation is sold at DA rate:
            if np.abs(data.dev.loc[i]) <= 2:
                bank = bank + data.dam.loc[i]*(data.actual.loc[i])
    
            #deviation condition 1, sell excess at peak price if delta is positive
            elif data.delta.loc[i] > 0 and np.abs(data.dev.loc[i]) > 2:
                bank = bank + data.dam.loc[i]*(data.forecast.loc[i]) + data.rtm.loc[i]*(data.delta.loc[i]) #sell day-ahead at DA
            
            #deviation condition 2,use stored energy to make difference (if we have the capacity)
            elif data.delta.loc[i] < 0 and np.abs(data.dev.loc[i]) > 2:
            
                #if we have enough battery capacity, use it
                if store - np.abs(data.delta.loc[i]) >= 0.2*capacity:
                    transfer = np.abs(data.delta.loc[i])
                    store = store - np.abs(data.delta.loc[i]) #take out balance from battery
                    
                    if transfer>maxflow:
                        maxflow = transfer
 
                    bank = bank + data.dam.loc[i]*(data.forecast.loc[i]) #sell what we did make at DA
            
                #if we don't have enough battery, use the remainder, do not go under 80% DoD
                #80% DoD is 20% of the total capacity
                elif store - np.abs(data.delta.loc[i]) < 0.2*capacity and store > 0.2*capacity:
                    remainpay = np.abs(data.delta.loc[i]) - 0.2*capacity #take out all battery balance
                    transfer = store-0.2*capacity
                    store = 0.2*capacity
                    
                    if transfer>maxflow:
                        maxflow = transfer
       
                    bank = bank + data.dam[i]*(data.forecast.loc[i]) - data.rtm.loc[i]*remainpay #pay the remainder
                                
                elif store - np.abs(data.delta.loc[i]) < 0.2*capacity and store <= 0.2*capacity and store > 0:
                    store = 0.2*capacity
                    bank = bank + data.dam[i]*(data.forecast.loc[i]) + data.rtm.loc[i]*data.delta.loc[i] #pay the remainder
        soc.append(store/capacity*100)
        if transfer != 0:
            epow.append((transfer,data.dt.loc[i]))
    
    totalcash.append(bank)
    #epow.append(maxflow)

#print totalcash
#print epow
epow = sorted(epow,reverse=True)
epowsort = zip(*epow)
dates = epowsort[1]
transf = epowsort[0]
print transf[0:25]

dates = data['dt']
datesmod = [datetime.strptime(i, '%d/%m/%y  %H:%M') for i in dates]

#sns.set_style("ticks")
#sns.despine()
plt.plot(datesmod[0:960],soc[0:960])
plt.xlabel('Date')
plt.ylabel('SoC %')
plt.title('State of Charge (2MWh Battery) During the First 10 Days Of Model')
sns.plt.show()