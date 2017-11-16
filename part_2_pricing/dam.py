import pandas as pd
from pandas import DataFrame, Series
import numpy as np

damprice = 'ercot_dam_2014_mod.csv'
data = pd.read_table(damprice,sep=',')

p = data['Settlement Point Price']
pint = []
dam = []

for i in p:
    pint.append(float(i))

for i in range(len(pint)/14):
    pave = np.mean(pint[(14*i):(14*(i+1))]) #average over the 14 min locs
    dam.extend([pave,pave,pave,pave]) #4 values, 15min intervales
    
###Day-ahead market data prices are rdy for concatenation

rtmprice = 'ercot_rtm_2014_mod.csv'
data = pd.read_table(rtmprice,sep=',')

p = data['Settlement Point Price']
pint = []
rtm = []

for i in p:
    pint.append(float(i))
    
place = data['Settlement Point Name']
place_assume = 'HB_HUBAVG' #assume our wind farm uses this regions RTM
j = 0

for i in place:
    if i == place_assume:
        rtm.append(p[j])
    j = j + 1

###Real-time market data price almost ready, need to fix length