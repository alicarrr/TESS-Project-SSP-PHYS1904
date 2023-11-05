import lightkurve as lk
import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
import Analysis_and_cleaning as ana

def regression(x, y):
    """Function to perform linear regression

    Args:
        x: x values from data
        y: y values from data

    Returns:
        regression: Regression performed
        r_squared: R^2 correlation coefficient 
        regression.coef_: Coefficient of regression line
        regression.intercept_: Intercept of regression line
    """

    # Initialise and perform regression
    regression = LinearRegression()
    regression.fit(x, y)

    # calculate R-squared of regression model
    r_squared = regression.score(x, y)
    
    # Get the coefficients of the regression line
    intercept = regression.intercept_
    slope = regression.coef_[0]

    # Print regression values
    print(f'R^2 = {r_squared}')
    print(f'Intercept = {regression.intercept_}')
    print(f'Slope = {regression.coef_}')

    return regression, r_squared, intercept, slope

# Read csv
data_cleaned = pd.read_csv("exoplanet_cleaned.csv")

# Extract data from cleaned csv file
depth_20_cleaned = data_cleaned['Depth'].to_numpy().T
ratio_cleaned = data_cleaned['Ratio'].to_numpy().T
magnitude_cleaned = data_cleaned['Magnitude'].to_numpy().T
depth_120_cleaned = ratio_cleaned * depth_20_cleaned
data_cleaned['Depth_120'] = depth_120_cleaned

# Linear regression of plot 1
depth_20_reshaped = depth_20_cleaned.reshape(-1, 1)
regression_20_v_120, r_squared_1, intercept_1, slope_1 = regression(depth_20_reshaped, depth_120_cleaned)

# Plot depth of 20 vs 120 with error bars
fig1, ax1 = plt.subplots()

# Plot the regression line
x_regression_1 = np.linspace(0, 0.12, 1000)
y_regression_1 = intercept_1 + slope_1 * x_regression_1
ax1.plot(x_regression_1, y_regression_1, label = f'Regression Line \n R^2 = {r_squared_1:.2f}, \n y = {slope_1:.4f}*x + {intercept_1:.6f}', color = 'red')
sc = plt.scatter(depth_20_cleaned, depth_120_cleaned, c = magnitude_cleaned, cmap = "turbo")
plt.colorbar(sc, label = 'Stellar Magnitude')
# ax1.set_xlim([0, 0.05])
# ax1.set_ylim([0, 0.05])
ax1.set_xlabel('Depth 20s (Fractional Flux)')
ax1.set_ylabel('Depth 120s (Fractional Flux)')
ax1.set_title('Comparison of Depths at Different Cadences')
ax1.grid()
ax1.legend()
fig1.savefig('Plot outputs/p3_depth_vs_depth_before separation.png')
fig1.savefig('Plot outputs/p3_depth_vs_depth_before separation.pdf')

# Linear regression of plot 2
regression_20_v_ratio, r_squared_2, intercept_2, slope_2 = regression(depth_20_reshaped, ratio_cleaned)

# Plot ratio of depth 20s to 120s with error bars
fig2, ax2 = plt.subplots()
# Plot the regression line
x_regression_2 = np.linspace(0, 0.12, 1000)
y_regression_2 = intercept_2 + slope_2 * x_regression_2
ax2.plot(x_regression_2, y_regression_2, label = f'Regression Line \n R^2 = {r_squared_2:.2f}, \n y = {slope_2:.4f}*x + {intercept_2:.2f}', color = 'red')
sc = plt.scatter(depth_20_cleaned, ratio_cleaned, c = magnitude_cleaned, cmap = "turbo")
plt.colorbar(sc, label='Stellar Magnitude')
ax2.set_xlim([0, 0.02])
# ax2.set_ylim([0.2, 1.8])
ax2.set_xlabel('Depth 20s (Fractional Flux)') 
ax2.set_ylabel('Ratio of Depth (120s/20s)')
ax2.set_title('Ratio of Depths (120/20) at Different Depths')
ax2.grid()
ax2.legend()

fig2.savefig('Plot outputs/p2_ratio_vs_depth_before separation.png')
fig2.savefig('Plot outputs/p2_ratio_vs_depth_before separation.pdf')

# Linear regression of plot 3
mag_reshaped = magnitude_cleaned.reshape(-1, 1)
regression_mag_v_ratio, r_squared_3, intercept_3, slope_3 = regression(mag_reshaped, ratio_cleaned)

# Plot stellar magnitude vs. ratio with error bars
fig3, ax3 = plt.subplots()
# Plot the regression line
x_regression_3 = np.linspace(5, 15, 100)
y_regression_3 = intercept_3 + slope_3 * x_regression_3
ax3.plot(x_regression_3, y_regression_3, label = f'Regression Line \n R^2 = {r_squared_3:.2f}, \n y = {slope_3:.4f}*x + {intercept_3:.2f}', color = 'red')
sc = plt.scatter(magnitude_cleaned, ratio_cleaned)
ax3.set_xlabel('Stellar Magnitude')
ax3.set_ylabel('Ratio of Depth (120s/20s)')
ax3.set_title('Ratio of Depths (120/20) at Different Magnitudes')
ax3.grid()
ax3.legend()

fig3.savefig('Plot outputs/p1_magnitude_vs_ratio_before separation.png')
fig3.savefig('Plot outputs/p1_magnitude_vs_ratio_before separation.pdf')

plt.show()