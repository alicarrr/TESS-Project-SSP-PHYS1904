# TESS-Project-SSP-PHYS1904
All code and outputted CSVs for Physics SSP Project on Exploring Transiting Exoplanets with NASA’s TESS Mission. The nasa_toi_alldata is a CSV file downloaded from https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=TOI which includes TOI data for all project candidates. This is the base data used in the following files for exoplanet analysis.

## Each code file is summarised and implemented in the order here:
1. **IterationTOI.py**: this iterates over all inputted TOIs from *'nasa_toi_alldata.csv'* and outputs to the *'exoplanetdata_alldata_nocleaning.csv'* file which contains all TOIs analysed before outlier rejection is performed.

2. **Analysis_and_cleaning.py**: This takes *'exoplanetdata_alldata_nocleaning.csv'* as an input where outlier rejection is performed and the data is separated into the following csv files:
    - *'exoplanet_cleaned_with_120.csv'*: includes all data cleaned with outliers removed
    - *'exoplanet_cleaned_sml_with120'*: includes cleaned data under depths of 0.005
    - *'exoplanet_cleaned_big_with120'*: includes cleaned data over depths of 0.005

3. **transit_relative_errors.py**: This takes the cleaned data and finds the relative error for each system, outputting these errors to the csv file *'exoplanet_UPD_relative_error.csv'* which also includes the variables from the original cleaned data.

4. **uncertainty_measurements_iteration.py**: *'exoplanet_cleaned_with_120.csv'* is input into this file and the standard deviation for each TOI is calculated and output in a csv file *'exoplanet_std_uncertainties_outliersremoved'* which also includes all the original variables from the cleaned csv file.

5. **SummaryPlots.py**: The data obtained from each of these analysis methods is used in the 'SummaryPlots.py' file which produces plots to describe the trends between all systems analysed. The Analysis_and_cleaning.py file is called in this summary to output the required analysis of data sets including mean, median, SEM, etc.
