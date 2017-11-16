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

DA = 36 #$20/MWh day-ahead rate is always the same
PP = 41 #$100/MWh real-time PEAK PRICE
OP = 25 #$50/MWh real-time OFF PEAK PRICE
store = 0 #current store level in battery
bank = 0 #$ cash in and out flow
capacity = 50 #21 MWh sample storage capacity

for i in range(len(data)):
    #OFF PEAK HOURS
    if data.peak.loc[i] == 0:
    
    #condition 0, energy within 2% deviation is sold at DA rate:
        if np.abs(data.dev.loc[i]) <= 2:
            bank = bank + DA*(data.actual.loc[i])
    
        #deviation condition 1, store excess energy if delta is positive
        elif data.delta.loc[i] > 0 and np.abs(data.dev.loc[i]) > 2:
            if store+data.delta.loc[i] < capacity: #if battery can handle all excess
            	store = store + data.delta.loc[i] #put all excess into battery
                bank = bank + DA*(data.forecast.loc[i]) #sell forecasted day-ahead at DA

            elif store+data.delta.loc[i] > capacity: #if battery is nearing full
                remainsell = capacity - store 
                store = capacity
                bank = bank + DA*(data.forecast.loc[i]) + OP*(data.delta.loc[i]-remainsell) #sell the difference
            
        #deviation condition 2,pay excess energy at the off-peak rate
        elif data.delta.loc[i] < 0 and np.abs(data.dev.loc[i]) > 2:
            bank = bank + DA*(data.forecast.loc[i]) + OP*(data.delta.loc[i]) #pay lacking at LMP
            
    #PEAK HOURS        
    elif data.peak.loc[i] == 1:

    #condition 0, energy within 2% deviation is sold at DA rate:
        if np.abs(data.dev.loc[i]) <= 2:
            bank = bank + DA*(data.actual.loc[i])
    
        #deviation condition 1, sell excess at peak price if delta is positive
        elif data.delta.loc[i] > 0 and np.abs(data.dev.loc[i]) > 2:
            bank = bank + DA*(data.forecast.loc[i]) + PP*(data.delta.loc[i]) #sell day-ahead at DA
            
        #deviation condition 2,use stored energy to make difference (if we have the capacity)
        elif data.delta.loc[i] < 0 and np.abs(data.dev.loc[i]) > 2:
            #if we have enough battery capacity, use it
            if store - np.abs(data.delta.loc[i]) > 0:
                store = store - np.abs(data.delta.loc[i]) #take out balance from battery
                bank = bank + DA*(data.forecast.loc[i]) #sell what we did make at DA
            
            #if we don't have enough battery, use the remainder:
            elif store - np.abs(data.delta.loc[i]) < 0:
                remainpay = np.abs(data.delta.loc[i]) - store #take out all battery balance
                store = 0
                bank = bank + DA*(data.forecast.loc[i]) + PP*remainpay #pay the remainder

print bank
