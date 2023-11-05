import lightkurve as lk
import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

"""
File to find and plot summaries for standard deviation of magnitude and depths and output R^2, 
intercepts, and slope of each plot.

Sample output:
R^2 = 0.9691173752199179
Intercept = -8.153950026992514e-06
Slope = [1.02946281]
R^2 plot 3 = 0.056904892087765835
Intercept plot 3 = 1.2219522028586687
Slope plot 3 = [-0.01777121]
"""

# Read csv including data without outliers
data_uncertainty = pd.read_csv("exoplanet_std_uncertainties_outliersremoved.csv")

# Calculate standard deviation for 20 and 120 second data
std_20 = data_uncertainty['20 M/B Std'].to_numpy().T
std_120 = data_uncertainty['120 M Std'].to_numpy().T
mag = data_uncertainty['Magnitude'].to_numpy().T

# Ratio of depth standard deviations
ratio = std_120 / std_20

std_20_reshaped = std_20.reshape(-1,1)

# Linear regression of two depths
regression_20_v_120 = LinearRegression()
regression_20_v_120.fit(std_20_reshaped, std_120)

# calculate R-squared of regression model
r_squared_4 = regression_20_v_120.score(std_20_reshaped, std_120)

# Print regression values
print(f'R^2 = {r_squared_4}')
print(f'Intercept = {regression_20_v_120.intercept_}')
print(f'Slope = {regression_20_v_120.coef_}')

# Get the coefficients of the regression line
intercept_4 = regression_20_v_120.intercept_
slope_4 = regression_20_v_120.coef_[0]

# Plot depth of 20 vs 120 
fig4, ax4 = plt.subplots()
# Plot the regression line
x_regression_4 = np.linspace(0, 0.12, 1000)
y_regression_4 = intercept_4 + slope_4 * x_regression_1
ax4.plot(x_regression_4, y_regression_4, label = f'Regression Line \n R^2 = {r_squared_4:.2f}, \n y = {slope_4:.4f}*x + {intercept_4:.6f}', color = 'red')
sc = plt.scatter(std_20, std_120, c = mag, cmap = "turbo")
plt.colorbar(sc, label = 'Stellar Magnitude')
ax4.set_xlim([0, 0.009])
ax4.set_ylim([0, 0.02])
ax4.set_xlabel('Standard Deviation in 20s')
ax4.set_ylabel('Standard Deviation in 120s')
ax4.grid()
ax4.legend()

regression_mag_v_ratio = LinearRegression()
mag_reshaped = mag.reshape(-1, 1)
regression_mag_v_ratio.fit(mag_reshaped, ratio)

# calculate R-squared of regression model
r_squared_3 = regression_mag_v_ratio.score(mag_reshaped, ratio)

# Print regression values
print(f'R^2 plot 3 = {r_squared_3}')
print(f'Intercept plot 3 = {regression_mag_v_ratio.intercept_}')
print(f'Slope plot 3 = {regression_mag_v_ratio.coef_}')

# Get the coefficients of the regression line
intercept_3 = regression_mag_v_ratio.intercept_
slope_3 = regression_mag_v_ratio.coef_[0]


# Plot stellar magnitude vs. ratio with error bars
fig5, ax5 = plt.subplots()
# Plot the regression line
x_regression_3 = np.linspace(5, 15, 100)
y_regression_3 = intercept_3 + slope_3 * x_regression_3
ax5.plot(x_regression_3, y_regression_3, label = f'Regression Line \n R^2 = {r_squared_3:.2f}, \n y = {slope_3:.4f}*x + {intercept_3:.2f}', color = 'red')
sc = plt.scatter(mag, ratio)
ax5.set_xlabel('Stellar Magnitude')
ax5.set_ylabel('Ratio of Standard Deviation (120s/20s)')
ax5.grid()
ax5.legend()


fig4.savefig('Plot outputs/p10_20StD_vs_120StD.png')
fig4.savefig('Plot outputs/p10_20StD_vs_120StD.pdf')


fig5.savefig('Plot outputs/p11_mag_vs_ratio_StD.png')
fig5.savefig('Plot outputs/p11_mag_vs_ratio_StD.pdf')

plt.show()