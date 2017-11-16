#Testing the NPV of cashflows for the battery storage system
#Results from Model 3 are input here so we don't re-run the model
import matplotlib.pyplot as plt
import pylab as pl
import seaborn as sns
import numpy as np

rev = [2194591.18, 2379592.15, 2564593.13, 2749594.10,
         2934595.08, 3119596.06, 3304597.03, 3489598.01]

energy = [2,6,10,14,18,22,26,30] #MWhr
#power is easily determined now because I fixed the transactions

#constants--
base = 2102090.69 # base-case revenue (no storage), model 1
cost = 500   #$/kWh (http://www.greenbiz.com/article/crunching-economics-teslas-energy-storage-solution)
dr = 0.10 #assumed a discount rate of 10%

#lifetime depends on how we cycle it, assuming once per day, 5000 cycle life
life = 15 #assumes 1 cycle per day every day

npvs = []
npvmod = []
for i in range(len(rev)):
    print i
    npv = 0 - (cost*energy[i]*1000)
    addcash = rev[i]-base #cash added on top of normal ops
    #npvmod.append(np.npv(0.1,rev[i]))
    
    for j in range(1,life+1):
        npv = npv + (addcash)/((1+dr)**j)
    
    npvs.append(npv)
    print npvs


sns.set_style("ticks")
sns.barplot(energy,npvs,palette="Greens")
sns.despine()
plt.xlabel('Battery Capacity MWh')
plt.ylabel('NPV Over 15 Year Lifetime $')
plt.title('NPV For Various Battery Sizes, Ancillary Service Model')
sns.plt.show()
'''
plt.plot(npvmod,energy)
sns.plt.show()
'''