import lightkurve as lk
import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression


# Read csv
data = pd.read_csv("exoplanet_UPD_relative_error.csv")

depth_20 = data['20 Depth'].to_numpy().T
magnitude = data['Magnitude'].to_numpy().T
depth_120 = data['120 Depth'].to_numpy().T
error_20 = data['20 Error'].to_numpy().T
error_120 = data['120 Error'].to_numpy().T
ratio = error_120/error_20
# Calculate error measures


# Linear regression of plot 1
# Reshape depth_20 to a 2D array
depth_120_reshaped = depth_120.reshape(-1, 1)

# initiate linear regression model
regression_20_v_120 = LinearRegression()

# fit regression model
regression_20_v_120.fit(depth_120_reshaped, error_120)

# calculate R-squared of regression model
r_squared_1 = regression_20_v_120.score(depth_120_reshaped, error_120)

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
x_regression_1 = np.linspace(0, 0.04, 500)
y_regression_1 = intercept_1 + slope_1 * x_regression_1
ax1.plot(x_regression_1, y_regression_1, label = f'Regression Line \n R^2 = {r_squared_1:.2f}, \n y = {slope_1:.4f}*x + {intercept_1:.6f}', color = 'red')

sc = plt.scatter(depth_120, error_120, c = magnitude, cmap = "turbo")
plt.colorbar(sc, label = 'Stellar Magnitude')
ax1.set_xlim([0, 0.025])
ax1.set_ylim([0, 0.3])
ax1.set_xlabel('Depth of 120s (Fractional Flux)')
ax1.set_ylabel('Relative Error of 120s Transit')
ax1.grid()
ax1.legend()

# Linear regression of plot 2

# initiate linear regression model
regression_20_v_ratio = LinearRegression()

depth_20_reshaped = depth_20.reshape(-1, 1)
# fit regression model
regression_20_v_ratio.fit(depth_20_reshaped, error_20)

# calculate R-squared of regression model
r_squared_2 = regression_20_v_ratio.score(depth_20_reshaped, error_20)

# Print regression values
print(f'R^2 plot 2 = {r_squared_2}')
print(f'Intercept plot 2 = {regression_20_v_ratio.intercept_}')
print(f'Slope plot 2 = {regression_20_v_ratio.coef_}')

# Get the coefficients of the regression line
intercept_2 = regression_20_v_ratio.intercept_
slope_2 = regression_20_v_ratio.coef_[0]


# Plot ratio of depth 20s to 120s with error bars
fig2, ax2 = plt.subplots()
# # Add error bars to the scatter plot
# for i in range(len(depth_20)):
#     plt.errorbar(depth_20[i], ratio[i], xerr = 0, yerr = SEM_ratio, fmt = 'o', color = 'black', alpha = 0.5)
# Plot the regression line
x_regression_2 = np.linspace(0, 0.04, 500)
y_regression_2 = intercept_2 + slope_2 * x_regression_2
ax2.plot(x_regression_2, y_regression_2, label = f'Regression Line \n R^2 = {r_squared_2:.2f}, \n y = {slope_2:.4f}*x + {intercept_2:.2f}', color = 'red')
sc = plt.scatter(depth_20, error_20, c = magnitude, cmap = "turbo")
plt.colorbar(sc, label='Stellar Magnitude')
ax2.set_xlim([0, 0.025])
ax2.set_ylim([0, 0.3])
ax2.set_xlabel('Depth of 20s (Fractional Flux)') 
ax2.set_ylabel('Relative Error of 20s Transit')
ax2.grid()
ax2.legend()

# Linear regression of plot 3
# initiate linear regression model
regression_mag_v_ratio = LinearRegression()

# Reshape depth_20 to a 2D array
mag_reshaped = magnitude.reshape(-1, 1)

# fit regression model
regression_mag_v_ratio.fit(mag_reshaped, error_120)

# calculate R-squared of regression model
r_squared_3 = regression_mag_v_ratio.score(mag_reshaped, error_120)

# Print regression values
print(f'R^2 plot 3 = {r_squared_3}')
print(f'Intercept plot 3 = {regression_mag_v_ratio.intercept_}')
print(f'Slope plot 3 = {regression_mag_v_ratio.coef_}')

# Get the coefficients of the regression line
intercept_3 = regression_mag_v_ratio.intercept_
slope_3 = regression_mag_v_ratio.coef_[0]


# Plot stellar magnitude vs. ratio with error bars
fig3, ax3 = plt.subplots()
# # Add error bars to the scatter plot
# for i in range(len(magnitude)):
#     plt.errorbar(magnitude[i], ratio[i], xerr=0, yerr = SEM_ratio, fmt = 'o', color = 'black', alpha = 0.5)

# Plot the regression line
x_regression_3 = np.linspace(5, 15, 100)
y_regression_3 = intercept_3 + slope_3 * x_regression_3
ax3.plot(x_regression_3, y_regression_3, label = f'Regression Line \n R^2 = {r_squared_3:.2f}, \n y = {slope_3:.4f}*x + {intercept_3:.2f}', color = 'red')
sc = plt.scatter(magnitude, error_120)
# ax3.set_ylim([0, 7])
ax3.set_xlabel('Stellar Magnitude')
ax3.set_ylabel('Relative Error of 120s Transit')
ax3.grid()
ax3.legend()


fig1.savefig('newp7_120error.png')
fig1.savefig('newp7_120error.pdf')


fig2.savefig('newp8_20error.png')
fig2.savefig('newp8_20error.pdf')

fig3.savefig('newp9_mag_vs_120error.png')
fig3.savefig('newp9_mag_vs_120error.pdf')

plt.show()




