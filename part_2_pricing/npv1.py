#Testing the NPV of cashflows for the battery storage system
#Results from Model 2 are input here so we don't re-run the model
import matplotlib.pyplot as plt
import pylab as pl
import seaborn as sns
import numpy as np

rev = [2107039.15, 2120588.44, 2132301.06, 2138915.38, 
        2147069.29, 2154022.02, 2161254.77, 2166354.47]

energy = [2,6,10,14,18,22,26,30] #MWhr
power = [1.6, 3.96395, 3.963951, 3.96395, 3.96395, 3.96395, 3.96395, 3.96395]

#constants--
base = 2102090.69 # base-case revenue (no storage)
cost = 250 #$/kWh (http://www.greenbiz.com/article/crunching-economics-teslas-energy-storage-solution)
dr = 0.1 #assumed a discount rate of 10%

#lifetime depends on how we cycle it, assuming once per day, 5000 cycle life
life = 15 #assumes 1 cycle per day every day

npvs = []

for i in range(len(rev)):
    npv = 0 - (cost*energy[i]*1000)
    addcash = rev[i]-base #cash added on top of normal ops

    for j in range(1,life+1):
        npv = npv + (addcash)/((1+dr)**i)
    
    npvs.append(npv)


sns.set_style("ticks")
sns.barplot(energy,npvs,palette="Reds")
sns.despine()
plt.xlabel('Battery Capacity MWh')
plt.ylabel('NPV Over 15 Year Lifetime $')
plt.title('NPV For Various Battery Sizes, Production Shift Model')
sns.plt.show()
