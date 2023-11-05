import lightkurve as lk
import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
import Analysis_and_cleaning as ana


"""
    Function to plot summary graphs and perform regression for analysis of multiple systems

    Sample output for one graph regression:
    R^2 = 0.07078999294886457
    Intercept = 0.050703077190033904
    Slope = [-1.25046581]
"""


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



# Read csvs to perform plotting
data_relative_error = pd.read_csv("exoplanet_UPD_relative_error.csv")               # CSV containing relative error calculations
data_uncertainty = pd.read_csv("exoplanet_std_uncertainties_outliersremoved.csv")   # CSV including data without outliers
data_cleaned_before = pd.read_csv("exoplanet_cleaned.csv")                                 # Cleaned data before fitering
data_after = pd.read_csv("exoplanet_cleaned_big.csv") # Cleaned data after filtering
# Extract parameters from each database

# Relative error database
depth_20_relative = data_relative_error['20 Depth'].to_numpy().T
magnitude_relative = data_relative_error['Magnitude'].to_numpy().T
depth_120_relative = data_relative_error['120 Depth'].to_numpy().T
error_20_relative = data_relative_error['20 Error'].to_numpy().T
error_120_relative = data_relative_error['120 Error'].to_numpy().T
error_ratio = error_120_relative / error_20_relative

# Uncertainty database 
# Calculate standard deviation for 20 and 120 second data
std_20 = data_uncertainty['20 M/B Std'].to_numpy().T
std_120 = data_uncertainty['120 M Std'].to_numpy().T
std_mag = data_uncertainty['Magnitude'].to_numpy().T
# Ratio of depth standard deviations
std_ratio = std_120 / std_20

# Extract data from cleaned csv file before filtering
depth_20_cleaned_before = data_cleaned_before['Depth'].to_numpy().T
ratio_cleaned_before = data_cleaned_before['Ratio'].to_numpy().T
magnitude_cleaned_before = data_cleaned_before['Magnitude'].to_numpy().T
depth_120_cleaned_before = ratio_cleaned_before * depth_20_cleaned_before
data_cleaned_before['Depth_120'] = depth_120_cleaned_before

# Extract data from cleaned csv file after filtering
depth_20_after = data_after['Depth'].to_numpy().T
ratio_after = data_after['Ratio'].to_numpy().T
magnitude_after = data_after['Magnitude'].to_numpy().T
depth_120_after = ratio_after * depth_20_after
data_after['Depth_120'] = depth_120_after

# Reshape data for use in regression 

depth_120_relative_reshaped = depth_120_relative.reshape(-1, 1)
depth_20_relative_reshaped = depth_20_relative.reshape(-1, 1)
mag_relative_reshaped = magnitude_relative.reshape(-1, 1)

std_20_reshaped = std_20.reshape(-1,1) 
std_mag_reshaped = std_mag.reshape(-1, 1)

depth_20_before_reshaped = depth_20_cleaned_before.reshape(-1, 1)
mag_before_reshaped = magnitude_cleaned_before.reshape(-1, 1)

depth_20_after_reshaped = depth_20_after.reshape(-1, 1)
mag_after_reshaped = magnitude_after.reshape(-1, 1)

# Perform linear regression between required variables
print('Linear regression for a range of variables (in order of plotting)')
regression_20_v_120_relative, r_squared_1, intercept_1, slope_1 = regression(depth_120_relative_reshaped, error_120_relative)
regression_20_v_ratio_relative, r_squared_2, intercept_2, slope_2 = regression(depth_20_relative_reshaped, error_20_relative)
regression_mag_v_ratio_relative, r_squared_3, intercept_3, slope_3 = regression(mag_relative_reshaped, error_120_relative)
regression_20_v_120_std, r_squared_4, intercept_4, slope_4 = regression(std_20_reshaped, std_120)
regression_mag_v_ratio_std, r_squared_5, intercept_5, slope_5 = regression(std_mag_reshaped, std_ratio)
regression_20_v_120_before, r_squared_6, intercept_6, slope_6 = regression(depth_20_before_reshaped, depth_120_cleaned_before)
regression_20_v_ratio_before, r_squared_7, intercept_7, slope_7 = regression(depth_20_before_reshaped, ratio_cleaned_before)
regression_mag_v_ratio_before, r_squared_8, intercept_8, slope_8 = regression(mag_before_reshaped, ratio_cleaned_before)
regression_20_v_120_after, r_squared_9, intercept_9, slope_9 = regression(depth_20_after_reshaped, depth_120_after)
regression_20_v_ratio_after, r_squared_10, intercept_10, slope_10 = regression(depth_20_after_reshaped, ratio_after)
regression_mag_v_ratio_after, r_squared_11, intercept_11, slope_11 = regression(mag_after_reshaped, ratio_after)


# Use analysis_and_cleaning file to clean data and calculate error measures

# Before Separation
print('Printing results for data before separation to reduce errors')
median_ratio_before, mean_ratio_before, stdev_ratio_before, count_ratio_before, SEM_ratio_before = ana.analysis(data_cleaned_before, 'Ratio')
median_depth_20_before, mean_depth_20_before, stdev_depth_20_before, count_depth_20_before, SEM_depth_20_before = ana.analysis(data_cleaned_before, 'Depth')
median_depth_120_before, mean_depth_120_before, stdev_depth_120_before, count_depth_120_before, SEM_depth_120_before = ana.analysis(data_cleaned_before, 'Depth_120')
median_mag_before, mean_mag_before, stdev_mag_before, count_mag_before, SEM_mag_before = ana.analysis(data_cleaned_before, 'Magnitude')
print('-------------------------------------------------------------')

# After separation
print('Printing results for data after separation to reduce errors')
median_ratio_after, mean_ratio_after, stdev_ratio_after, count_ratio_after, SEM_ratio_after = ana.analysis(data_after, 'Ratio')
median_depth_20_after, mean_depth_20_after, stdev_depth_20_after, count_depth_20_after, SEM_depth_20_after = ana.analysis(data_after, 'Depth')
median_depth_120_after, mean_depth_120_after, stdev_depth_120_after, count_depth_120_after, SEM_depth_120_after = ana.analysis(data_after, 'Depth_120')
median_mag_after, mean_mag_after, stdev_mag_after, count_mag_after, SEM_mag_after = ana.analysis(data_after, 'Magnitude')
print('-------------------------------------------------------------')

# Relative error plots 

# Plot depth of 20 vs 120
fig1, ax1 = plt.subplots()
# Plot the regression line
x_regression_1 = np.linspace(0, 0.04, 500)
y_regression_1 = intercept_1 + slope_1 * x_regression_1
ax1.plot(x_regression_1, y_regression_1, label = f'Regression Line \n R^2 = {r_squared_1:.2f}, \n y = {slope_1:.4f}*x + {intercept_1:.6f}', color = 'red')
sc = plt.scatter(depth_120_relative, error_120_relative, c = magnitude_relative, cmap = "turbo")
plt.colorbar(sc, label = 'Stellar Magnitude')
ax1.set_xlim([0, 0.025])
ax1.set_ylim([0, 0.3])
ax1.set_xlabel('Depth of 120s (Fractional Flux)')
ax1.set_ylabel('Relative Error of 120s Transit')
ax1.grid()
ax1.legend()
fig1.savefig('Plot outputs/newp7_120error.png')
fig1.savefig('Plot outputs/newp7_120error.pdf')

# Plot ratio of depth 20s to 120s
fig2, ax2 = plt.subplots()
# Plot the regression line
x_regression_2 = np.linspace(0, 0.04, 500)
y_regression_2 = intercept_2 + slope_2 * x_regression_2
ax2.plot(x_regression_2, y_regression_2, label = f'Regression Line \n R^2 = {r_squared_2:.2f}, \n y = {slope_2:.4f}*x + {intercept_2:.2f}', color = 'red')
sc = plt.scatter(depth_20_relative, error_20_relative, c = magnitude_relative, cmap = "turbo")
plt.colorbar(sc, label='Stellar Magnitude')
ax2.set_xlim([0, 0.025])
ax2.set_ylim([0, 0.3])
ax2.set_xlabel('Depth of 20s (Fractional Flux)') 
ax2.set_ylabel('Relative Error of 20s Transit')
ax2.grid()
ax2.legend()
fig2.savefig('Plot outputs/newp8_20error.png')
fig2.savefig('Plot outputs/newp8_20error.pdf')

# Plot stellar magnitude vs. ratio with error bars
fig3, ax3 = plt.subplots()
# Plot the regression line
x_regression_3 = np.linspace(5, 15, 100)
y_regression_3 = intercept_3 + slope_3 * x_regression_3
ax3.plot(x_regression_3, y_regression_3, label = f'Regression Line \n R^2 = {r_squared_3:.2f}, \n y = {slope_3:.4f}*x + {intercept_3:.2f}', color = 'red')
sc = plt.scatter(magnitude_relative, error_120_relative)
ax3.set_xlabel('Plot outputs/Stellar Magnitude')
ax3.set_ylabel('Plot outputs/Relative Error of 120s Transit')
ax3.grid()
ax3.legend()
fig3.savefig('Plot outputs/newp9_mag_vs_120error.png')
fig3.savefig('Plot outputs/newp9_mag_vs_120error.pdf')


# Plots of uncertainties and standard deviation

# Plot depth of 20 vs 120 
fig4, ax4 = plt.subplots()
# Plot the regression line
x_regression_4 = np.linspace(0, 0.12, 1000)
y_regression_4 = intercept_4 + slope_4 * x_regression_4
ax4.plot(x_regression_4, y_regression_4, label = f'Regression Line \n R^2 = {r_squared_4:.2f}, \n y = {slope_4:.4f}*x + {intercept_4:.6f}', color = 'red')
sc = plt.scatter(std_20, std_120, c = std_mag, cmap = "turbo")
plt.colorbar(sc, label = 'Stellar Magnitude')
ax4.set_xlim([0, 0.009])
ax4.set_ylim([0, 0.02])
ax4.set_xlabel('Standard Deviation in 20s')
ax4.set_ylabel('Standard Deviation in 120s')
ax4.grid()
ax4.legend()
fig4.savefig('Plot outputs/p10_20StD_vs_120StD.png')
fig4.savefig('Plot outputs/p10_20StD_vs_120StD.pdf')

# Plot stellar magnitude vs. ratio with error bars
fig5, ax5 = plt.subplots()
# Plot the regression line
x_regression_5 = np.linspace(5, 15, 100)
y_regression_5 = intercept_5 + slope_5 * x_regression_5
ax5.plot(x_regression_5, y_regression_5, label = f'Regression Line \n R^2 = {r_squared_5:.2f}, \n y = {slope_5:.4f}*x + {intercept_5:.2f}', color = 'red')
sc = plt.scatter(std_mag, std_ratio)
ax5.set_xlabel('Stellar Magnitude')
ax5.set_ylabel('Ratio of Standard Deviation (120s/20s)')
ax5.grid()
ax5.legend()
fig5.savefig('Plot outputs/p11_mag_vs_ratio_StD.png')
fig5.savefig('Plot outputs/p11_mag_vs_ratio_StD.pdf')

# Summary plots before separation

# Plot depth of 20 vs 120
fig6, ax6 = plt.subplots()
# Plot the regression line
x_regression_6 = np.linspace(0, 0.12, 1000)
y_regression_6 = intercept_6 + slope_6 * x_regression_6
ax6.plot(x_regression_6, y_regression_6, label = f'Regression Line \n R^2 = {r_squared_6:.2f}, \n y = {slope_6:.4f}*x + {intercept_6:.6f}', color = 'red')
sc = plt.scatter(depth_20_cleaned_before, depth_120_cleaned_before, c = magnitude_cleaned_before, cmap = "turbo")
plt.colorbar(sc, label = 'Stellar Magnitude')
ax6.set_xlabel('Depth 20s (Fractional Flux)')
ax6.set_ylabel('Depth 120s (Fractional Flux)')
ax6.set_title('Comparison of Depths at Different Cadences')
ax6.grid()
ax6.legend()
fig6.savefig('Plot outputs/p3_depth_vs_depth_before separation.png')
fig6.savefig('Plot outputs/p3_depth_vs_depth_before separation.pdf')

# Plot ratio of depth 20s to 120s against 20s depth
fig7, ax7 = plt.subplots()
# Plot the regression line
x_regression_7 = np.linspace(0, 0.12, 1000)
y_regression_7 = intercept_7 + slope_7 * x_regression_7
ax7.plot(x_regression_7, y_regression_7, label = f'Regression Line \n R^2 = {r_squared_7:.2f}, \n y = {slope_7:.4f}*x + {intercept_7:.2f}', color = 'red')
sc = plt.scatter(depth_20_cleaned_before, ratio_cleaned_before, c = magnitude_cleaned_before, cmap = "turbo")
plt.colorbar(sc, label='Stellar Magnitude')
ax7.set_xlim([0, 0.02])
# ax7.set_ylim([0.7, 1.8])
ax7.set_xlabel('Depth 20s (Fractional Flux)') 
ax7.set_ylabel('Ratio of Depth (120s/20s)')
ax7.set_title('Ratio of Depths (120/20) at Different Depths')
ax7.grid()
ax7.legend()
fig7.savefig('Plot outputs/p2_ratio_vs_depth_before separation.png')
fig7.savefig('Plot outputs/p2_ratio_vs_depth_before separation.pdf')

# Plot stellar magnitude vs. ratio
fig8, ax8 = plt.subplots()
# Plot the regression line
x_regression_8 = np.linspace(5, 15, 100)
y_regression_8 = intercept_8 + slope_8 * x_regression_8
ax8.plot(x_regression_8, y_regression_8, label = f'Regression Line \n R^2 = {r_squared_8:.2f}, \n y = {slope_8:.4f}*x + {intercept_8:.2f}', color = 'red')
sc = plt.scatter(magnitude_cleaned_before, ratio_cleaned_before)
ax8.set_xlabel('Stellar Magnitude')
ax8.set_ylabel('Ratio of Depth (120s/20s)')
ax8.set_title('Ratio of Depths (120/20) at Different Magnitudes')
ax8.grid()
ax8.legend()
fig8.savefig('Plot outputs/p1_magnitude_vs_ratio_before separation.png')
fig8.savefig('Plot outputs/p1_magnitude_vs_ratio_before separation.pdf')

# Summary plots after separation (depth > 0.005)

# Plot depth of 20 vs 120 
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

# Plot ratio of depth 20s to 120s
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

# Plot stellar magnitude vs. ratio
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