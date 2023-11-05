import lightkurve as lk
import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression


# Read csv
data = pd.read_csv("exoplanet_std_uncertainties_outliersremoved.csv")

std_20 = data['20 M/B Std'].to_numpy().T
std_120 = data['120 M Std'].to_numpy().T
mag = data['Magnitude'].to_numpy().T
ratio = std_120/std_20

std_20_reshaped = std_20.reshape(-1,1)

regression_20_v_120 = LinearRegression()

# fit regression model
regression_20_v_120.fit(std_20_reshaped, std_120)

# calculate R-squared of regression model
r_squared_1 = regression_20_v_120.score(std_20_reshaped, std_120)

# Print regression values
print(f'R^2 = {r_squared_1}')
print(f'Intercept = {regression_20_v_120.intercept_}')
print(f'Slope = {regression_20_v_120.coef_}')

# Get the coefficients of the regression line
intercept_1 = regression_20_v_120.intercept_
slope_1 = regression_20_v_120.coef_[0]

# Plot depth of 20 vs 120 with error bars
fig1, ax1 = plt.subplots()
# Add error bars to the scatter plot
# for i in range(len(depth_20)):
#     plt.errorbar(depth_20[i], depth_120[i], xerr=0, yerr=SEM_depth_120, fmt='o', color='black', alpha=0.5)

# Plot the regression line
x_regression_1 = np.linspace(0, 0.12, 1000)
y_regression_1 = intercept_1 + slope_1 * x_regression_1
ax1.plot(x_regression_1, y_regression_1, label = f'Regression Line \n R^2 = {r_squared_1:.2f}, \n y = {slope_1:.4f}*x + {intercept_1:.6f}', color = 'red')

sc = plt.scatter(std_20, std_120, c = mag, cmap = "turbo")
plt.colorbar(sc, label = 'Stellar Magnitude')
ax1.set_xlim([0, 0.009])
ax1.set_ylim([0, 0.02])
ax1.set_xlabel('Standard Deviation in 20s')
ax1.set_ylabel('Standard Deviation in 120s')
ax1.grid()
ax1.legend()




regression_mag_v_ratio = LinearRegression()

# Reshape depth_20 to a 2D array
mag_reshaped = mag.reshape(-1, 1)

# fit regression model
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
fig2, ax3 = plt.subplots()
# # Add error bars to the scatter plot
# for i in range(len(magnitude)):
#     plt.errorbar(magnitude[i], ratio[i], xerr=0, yerr = SEM_ratio, fmt = 'o', color = 'black', alpha = 0.5)

# Plot the regression line
x_regression_3 = np.linspace(5, 15, 100)
y_regression_3 = intercept_3 + slope_3 * x_regression_3
ax3.plot(x_regression_3, y_regression_3, label = f'Regression Line \n R^2 = {r_squared_3:.2f}, \n y = {slope_3:.4f}*x + {intercept_3:.2f}', color = 'red')
sc = plt.scatter(mag, ratio)
# ax3.set_ylim([0.8, 1.2])
ax3.set_xlabel('Stellar Magnitude')
ax3.set_ylabel('Ratio of Standard Deviation (120s/20s)')
ax3.grid()
ax3.legend()


fig1.savefig('p10_20StD_vs_120StD.png')
fig1.savefig('p10_20StD_vs_120StD.pdf')


fig2.savefig('p11_mag_vs_ratio_StD.png')
fig2.savefig('p11_mag_vs_ratio_StD.pdf')


plt.show()


