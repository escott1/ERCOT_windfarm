import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import matplotlib
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from datetime import datetime

#file of csv with data
file = 'windmod1.csv'

#### switches
plot = 0
export = 1

#read data from csv
data = pd.read_table(file, sep=',')
data = data.replace('#DIV/0!', 0)
data = data.replace('#VALUE!', 0)

dt = [] #to convert to datetime
for i in data.dt:
    daytime = datetime.strptime(i, '%d/%m/%y %H:%M')
    dt.append(daytime)
dates = matplotlib.dates.date2num(dt) #dates are ready for plotting as datenum

#Data columns: date, time, dt, forecast, actual, delta, deviation
#some basic statistics on the energy and deviation data

#print data.forecast.describe()
#print data.actual.describe()
#print data.delta.describe()
#print data.deviation.describe() <--- some messy data here, re-calculate with python and replace

data = data.drop('deviation', 1)
dev = ((data.actual-data.forecast)/data.forecast)*100.0
dev.name = 'dev'
dev = dev.replace('NaN',2)
dev = dev.replace('inf',-2)
dev = dev.replace('-inf',-2)
data = pd.concat([data,dev], axis=1)

#print data.loc[data['dev'].idxmax()] # shows the id of the max deviation scenario
#want to see the number of times the deviations are greater or less than 2%
devgr2 = data[np.abs(data.dev) > 2] #89.5 % of forecast deviate more than 2%

Q1 = -79.99 #from describe
Q3 = -15.97 #from describe
IQR = Q3-Q1
low = Q1-1.5*IQR # -176.02
high = Q3+1.5*IQR #80.06

store = []
for i in dev:
    if i<=low:
        i = low
    if i>=high:
        i = high
    store.append(i)

dev2 = DataFrame(store)
#print dev2.describe() #show new distribution
        
times = data.dt
peak = []

#sorting peak and off peak times into array
for i in times:
    tottime = i.split(' ')[1]
    time = tottime.split(':')
    hr = int(time[0])
    min = int(time[1])
    if hr >= 7 and hr <= 21:
        peak.append(1) #peak
    if hr < 7:
        peak.append(0) #off-peak 
    if hr == 22 and min == 0:
        peak.append(1)
    if hr == 22 and min > 0:
        peak.append(0)
    if hr >22:
        peak.append(0)

peakser = Series(peak)
peakser.name = 'peak'
data = pd.concat([data,peakser],axis=1)
print data.head()

#export the dataframe to 
if export == 1:
    data.to_csv('windmod2.csv')
    print 'dataframe printed to csv'

####PLOTTING, turn on with plot = 1 for basic timeseries plot
if plot == 1:
    fig, ax = plt.subplots()
    ax.plot_date(dates[0:97], data.forecast[0:97], 'b--',label='Forecast Gen.')
    ax.plot_date(dates[0:97], data.actual[0:97],'k:',label='Actual Gen.')
    plt.ylabel('Energy MWh')
    myfmt = mdates.DateFormatter('%d/%m/%y\n%H:%M')
    ax.xaxis.set_major_formatter(myfmt)
    legend = ax.legend(loc='upper center')
    plt.show()
    
#turn on histogram plot with plot = 2
if plot == 2:
    devsort = dev.sort_values() #sort my deviation column
    print devsort[0:5]
    #devsort[len(devsort)] = devsort.iloc[-1]
    #cum_dist = np.linspace(0.,1.,len(devsort))
    #dev_cdf = pd.Series(cum_dist, index=devsort)
    #dev_cdf.plot(drawstyle='steps')
    plt.ylim(-1000,120000)
    plt.xlim(0,36000)
    plt.ylabel('Deviation %')
    plt.xlabel('Count')
    plt.plot(devsort,'.k')
    plt.show()
    
#turn on distribution with plot = 3
if plot == 3:
    num_bins = 50
    devhist = np.array(dev2)
    mu = float(np.mean(dev2))
    sigma = float(np.std(dev2))
    n, bins, patches = plt.hist(devhist, num_bins, normed=1, facecolor='green', alpha=0.5)
    y = mlab.normpdf(bins, mu, sigma)
    plt.ylabel('Probability')
    plt.xlabel('Deviation %')
    plt.plot(bins, y, 'k--')
    plt.show()