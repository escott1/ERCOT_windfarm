import pandas as pd
from pandas import DataFrame, Series
import numpy as np

#Start of revision to CASE 1 for Tesla Energy battery sizing challenge
#One of the central improvements will be to add pricing data to the model
#This code will read in several pricing and arrange to match the wind data
#4 sections: 1) day-ahead market 2) real-time market 3) ancillary service 4) combine data


###1) Day-ahead market data prices
damprice = 'ercot_dam_2014_mod.csv'
data = pd.read_table(damprice,sep=',')

p = data['Settlement Point Price']
pmod = []
dam = []

for i in p:
    pmod.append(float(i))

for i in range(len(pmod)/14):
    pave = np.mean(pmod[(14*i):(14*(i+1))]) #average over the 14 min locs
    dam.extend([pave,pave,pave,pave]) #4 values, 15min intervales


###2) Real-time market data price
rtmprice = 'ercot_rtm_2014_mod.csv'
data = pd.read_table(rtmprice,sep=',')

p = data['Settlement Point Price']
pmod = []
rtm = []

for i in p:
    pmod.append(float(i))
    
place = data['Settlement Point Name']
place_assume = 'HB_HUBAVG' #assume our wind farm uses this regions RTM
j = 0

for i in place:
    if i == place_assume:
        rtm.append(pmod[j])
    j = j + 1
    
    
###3) Ancillary-service market: 4 services
ancser = 'ercot_as_2014_mod.csv'
data = pd.read_table(ancser,sep=',')

as1 = data['REGDN'].astype(float)
as2 = data['REGUP'].astype(float)
as3 = data['RRS'].astype(float)
as4 = data['NSPIN'].astype(float)

regdn = []
regup = []
rrs = []
nspin = []

for i in range(len(as1)):
    regdn.extend([as1[i],as1[i],as1[i],as1[i]])
    regup.extend([as2[i],as2[i],as2[i],as2[i]])
    rrs.extend([as3[i],as3[i],as3[i],as3[i]])
    nspin.extend([as4[i],as4[i],as4[i],as4[i]])


###4) Combine all relevant pricing data into data
master = 'windmod3.csv'
data = pd.read_table(master,sep=',',index_col=0)

dam_pd = Series(dam)
dam_pd.name = 'dam'
rtm_pd = Series(rtm)
rtm_pd.name = 'rtm'
regdn_pd = Series(regdn)
regdn_pd.name = 'regdn'
regup_pd = Series(regup)
regup_pd.name = 'regup'
rrs_pd = Series(rrs)
rrs_pd.name = 'rrs'
nspin_pd = Series(nspin)
nspin_pd.name = 'nspin'

data = pd.concat([data,dam_pd,rtm_pd,regdn_pd,regup_pd,rrs_pd,nspin_pd],axis=1)

data.to_csv('windmod4.csv') #windmod4 will have all data from case 1 + PRICING!