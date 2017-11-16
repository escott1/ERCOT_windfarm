import numpy as np 
from pandas import DataFrame, Series
import pandas as pd
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.dates import DateFormatter

import seaborn as sns

#INPUT FILE NAME FOR PROFILE:
file = 'windmod4.csv'

data = pd.read_csv(file, index_col=0)
delta = data['delta']
dam = data['dam']
rtm = data['rtm']
regdn = data['regdn']
regup = data['regup']
rrs = data['rrs']
nspin = data['nspin']
peak = data['peak']
actual = data['actual']

enp = np.array(regup)
e = np.reshape(enp, (-1, 96))

dates = data['dt']
datesmod = [datetime.strptime(i, '%d/%m/%y  %H:%M') for i in dates]
dtlist = []
hours = []
val = 0
for i in data['dt']:
    if val%96 == 0:
        dtlist.append(i.split(' ')[0])
    val += 1
    if val < 97:
        hours.append(i.split(' ')[1]) 

p = [] #peak sum
op = [] #off-peak sum
for i in range(len(peak)):
    if peak[i] == 1:
        p.append(rtm[i])
    elif peak[i] == 0:
        op.append(rtm[i])


df = DataFrame(e, index=dtlist, columns=hours)

cmap = mpl.colors.ListedColormap(sns.color_palette("coolwarm", 25))
sns.heatmap(df,yticklabels=85,xticklabels=16,linewidth=0,vmax=50)
plt.ylabel('Date')
plt.xlabel('Hour')
plt.title('UP REGULATION ERCOT Ancillary Service, $/MWh')
sns.plt.show()


'''
formatter = DateFormatter('%b/%y')

f, axarr = plt.subplots(2, sharex=True)

axarr[0].plot(datesmod,dam,'k-',linewidth=0.8)
axarr[0].set_title('Day Ahead (DAM) and Real-Time Market (RTM) Pricing, ERCOT')
axarr[0].set_ylabel('DAM $/MWh')
axarr[0].grid(True)
axarr[1].plot(datesmod,rtm,'r-',linewidth=0.8)
axarr[1].set_ylabel('RTM $/MWh')
axarr[1].set_ylim(-10,1400)
axarr[1].grid(True)
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
f.autofmt_xdate()

plt.show()'''