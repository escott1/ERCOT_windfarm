#BASE SCENARIO, follows algorithm, no battery to store

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

DA = 10 #$10/MWh day-ahead rate is always the same
PPl = [200] #peak-price list
OPl = [20] #off-peak price list
bank = 0 #$ cash in and out flow
#rev = [] #made list to start testing out sensitivities

for j in range(0,len(PPl)):
    PP = PPl[j] #set peak price
    print PP

    for k in range(0,len(OPl)):
        OP = OPl[k] #set off-peak price
        
        #start of payment strategy
        for i in range(len(data)):
            print i
            #OFF PEAK HOURS
            
            if data.peak.loc[i] == 0:
             #condition 0, energy within 2% deviation is sold at DA rate:
                if np.abs(data.dev.loc[i]) <= 2:
                    bank = bank + DA*(data.actual.loc[i])
             
             #deviation condition 1, sell excess energy if delta is positive
                if data.delta.loc[i] > 0 and np.abs(data.dev.loc[i]) > 2:
                    bank = bank + DA*(data.forecast.loc[i]) + OP*(data.delta.loc[i]) #sell forecasted day-ahead at DA
             
             #deviation condition 2,pay excess energy at the off-peak rate
                if data.delta.loc[i] < 0 and np.abs(data.dev.loc[i]) > 2:
                    bank = bank + DA*(data.forecast.loc[i]) + OP*(data.delta.loc[i]) #pay lacking at LMP
            
            #PEAK HOURS        
            if data.peak.loc[i] == 1:

            #condition 0, energy within 2% deviation is sold at DA rate:
                if np.abs(data.dev.loc[i]) <= 2:
                    bank = bank + DA*(data.actual.loc[i])
    
                #deviation condition 1, sell excess at peak price if delta is positive
                if data.delta.loc[i] > 0 and np.abs(data.dev.loc[i]) > 2:
                    bank = bank + DA*(data.forecast.loc[i]) + PP*(data.delta.loc[i]) 
            
                #deviation condition 2, pay what we lack in gen.
                if data.delta.loc[i] < 0 and np.abs(data.dev.loc[i]) > 2:
                    bank = bank + DA*(data.forecast.loc[i]) + PP*(data.delta.loc[i]) 
#        rev.append(bank)

#revser = Series(rev)
#revser.to_csv('basecase.csv')
print bank

