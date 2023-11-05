import lightkurve as lk
import numpy as np
import csv
from astropy.units import Quantity
import pandas as pd
from astropy.stats import mad_std
import matplotlib.pyplot as plt

data= pd.read_csv("exoplanet_cleaned.csv",index_col=False)
ratio = data["Ratio"]
depth = data['Depth']

plt.figure(1)
plt.scatter(depth,ratio)
plt.figure(2)
plt.scatter(depth,ratio*depth)

plt.show()