import lightkurve as lk
import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
import Analysis_and_cleaning as ana

# Read csv
data_after = pd.read_csv("exoplanet_cleaned_big.csv")

depth_20_after = data_after['Depth'].to_numpy().T
ratio_after = data_after['Ratio'].to_numpy().T
magnitude_after = data_after['Magnitude'].to_numpy().T
depth_120_after = ratio_after * depth_20_after
data_after['Depth_120'] = depth_120_after

# Calculate error measures
median_ratio_after, mean_ratio_after, stdev_ratio_after, count_ratio_after, SEM_ratio_after = ana.analysis(data_after, 'Ratio')
median_depth_20_after, mean_depth_20_after, stdev_depth_20_after, count_depth_20_after, SEM_depth_20_after = ana.analysis(data_after, 'Depth')
median_depth_120_after, mean_depth_120_after, stdev_depth_120_after, count_depth_120_after, SEM_depth_120_after = ana.analysis(data_after, 'Depth_120')
median_mag_after, mean_mag_after, stdev_mag_after, count_mag_after, SEM_mag_after = ana.analysis(data_after, 'Magnitude')

# Linear regression of plot 1
# Reshape depth_20_after to a 2D array
depth_20_after_reshaped = depth_20_after.reshape(-1, 1)

# initiate linear regression model
regression_20_v_120_after = LinearRegression()

# fit regression model
regression_20_v_120_after.fit(depth_20_after_reshaped, depth_120_after)

# calculate R-squared of regression model
r_squared_9 = regression_20_v_120_after.score(depth_20_after_reshaped, depth_120_after)

# Print regression values
print(f'R^2 = {r_squared_9}')
print(f'Intercept = {regression_20_v_120_after.intercept_}')
print(f'Slope = {regression_20_v_120_after.coef_}')

# Get the coefficients of the regression line
intercept_9 = regression_20_v_120_after.intercept_
slope_9 = regression_20_v_120_after.coef_[0]

# Plot depth of 20 vs 120 with error bars
fig9, ax9 = plt.subplots()
# Plot the regression line
x_regression_9 = np.linspace(0, 0.12, 1000)
y_regression_9 = intercept_9 + slope_9 * x_regression_9
ax9.plot(x_regression_9, y_regression_9, label = f'Regression Line \n R^2 = {r_squared_9:.2f}, \n y = {slope_9:.4f}*x + {intercept_9:.6f}', color = 'red')
sc = plt.scatter(depth_20_after, depth_120_after, c = magnitude_after, cmap = "turbo")
plt.colorbar(sc, label = 'Stellar Magnitude')
ax9.set_xlim([0, 0.05])
ax9.set_ylim([0, 0.05])
ax9.set_xlabel('Depth 20s (Fractional Flux)')
ax9.set_ylabel('Depth 120s (Fractional Flux)')
ax9.grid()
ax9.legend()
fig9.savefig('Plot outputs/p4_magnitude_vs_ratio_after separation.png')
fig9.savefig('Plot outputs/p4_magnitude_vs_ratio_after separation.pdf')

# Linear regression of plot 2

# initiate linear regression model
regression_20_v_ratio_after = LinearRegression()

# fit regression model
regression_20_v_ratio_after.fit(depth_20_after_reshaped, ratio_after)

# calculate R-squared of regression model
r_squared_10 = regression_20_v_ratio_after.score(depth_20_after_reshaped, ratio_after)

# Print regression values
print(f'R^2 plot 2 = {r_squared_10}')
print(f'Intercept plot 2 = {regression_20_v_ratio_after.intercept_}')
print(f'Slope plot 2 = {regression_20_v_ratio_after.coef_}')

# Get the coefficients of the regression line
intercept_10 = regression_20_v_ratio_after.intercept_
slope_10 = regression_20_v_ratio_after.coef_[0]


# Plot ratio of depth 20s to 120s with error bars
fig10, ax10 = plt.subplots()
# Plot the regression line
x_regression_10 = np.linspace(0, 0.12, 1000)
y_regression_10 = intercept_10 + slope_10 * x_regression_10
ax10.plot(x_regression_10, y_regression_10, label = f'Regression Line \n R^2 = {r_squared_10:.2f}, \n y = {slope_10:.4f}*x + {intercept_10:.2f}', color = 'red')
sc = plt.scatter(depth_20_after, ratio_after, c = magnitude_after, cmap = "turbo")
plt.colorbar(sc, label='Stellar Magnitude')
ax10.set_xlim([0.0049, 0.05])
# ax10.set_ylim([0.2, 1.8])
ax10.set_xlabel('Depth 20s (Fractional Flux)') 
ax10.set_ylabel('Ratio of Depths (120s/20s)')
ax10.grid()
ax10.legend()
fig10.savefig('Plot outputs/p5_ratio_vs_depth_after separation.png')
fig10.savefig('Plot outputs/p5_ratio_vs_depth_after separation.pdf')

# Linear regression of plot 3
# initiate linear regression model
regression_mag_v_ratio_after = LinearRegression()

# Reshape depth_20_after to a 2D array
mag_after_reshaped = magnitude_after.reshape(-1, 1)

# fit regression model
regression_mag_v_ratio_after.fit(mag_after_reshaped, ratio_after)

# calculate R-squared of regression model
r_squared_11 = regression_mag_v_ratio_after.score(mag_after_reshaped, ratio_after)

# Print regression values
print(f'R^2 plot 3 = {r_squared_11}')
print(f'Intercept plot 3 = {regression_mag_v_ratio_after.intercept_}')
print(f'Slope plot 3 = {regression_mag_v_ratio_after.coef_}')

# Get the coefficients of the regression line
intercept_11 = regression_mag_v_ratio_after.intercept_
slope_11 = regression_mag_v_ratio_after.coef_[0]


# Plot stellar magnitude vs. ratio with error bars
fig11, ax11 = plt.subplots()
# Plot the regression line
x_regression_11 = np.linspace(5, 15, 100)
y_regression_11 = intercept_11 + slope_11 * x_regression_11
ax11.plot(x_regression_11, y_regression_11, label = f'Regression Line \n R^2 = {r_squared_11:.2f}, \n y = {slope_11:.4f}*x + {intercept_11:.2f}', color = 'red')
sc = plt.scatter(magnitude_after, ratio_after)
# ax11.set_ylim([0.8, 1.2])
ax11.set_xlabel('Stellar Magnitude')
ax11.set_ylabel('Ratio of Depths (120s/20s)')
ax11.grid()
ax11.legend()
fig11.savefig('Plot outputs/p6_depth_vs_depth_after separation.png')
fig11.savefig('Plot outputs/p6_depth_vs_depth_after separation.pdf')

plt.show()




