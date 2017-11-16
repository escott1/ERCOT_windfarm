#plot the base-case scenario of NO STORAGE
#want to see price sensitivity

import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from datetime import datetime

revs = pd.read_csv('basecase.csv',index_col=0,header=None)
pp = np.array([50,100,150]) #peak-price list
op = np.array([-5,5,15]) #off-peak price list
X, Y = np.meshgrid(pp, op)
revplot = np.array(revs)
print revplot
Z = revplot.reshape(X.shape)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
