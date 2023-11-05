# TESS-Project-SSP-PHYS1904
All code and outputted CSVs for Physics SSP Project on Exploring Transiting Exoplanets with NASA’s TESS Mission. The nasa_toi_alldata is a CSV file downloaded from https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=TOI which includes TOI data for all project candidates. This is the base data used in the following files for exoplanet analysis.

## Each code file is summarised as:


## It runs in the order described here:
1. **IterationTOI.py**: this iterates over all inputted TOIs from *'nasa_toi_alldata.csv'* and outputs to the 'exoplanetdata_alldata_nocleaning.csv' file.
2. **transit_relative_errors.py**: This *'exoplanetdata_alldata_nocleaning'* is input into the 'transit_relative_errors.py' file which performs cleaning and separation (outputs cleaned, cleaned big and cleaned sml)
3. **uncertainty_measurements_iteration.py** and **transit_relative_errors.py**: *'exoplanet_cleaned_with_120'* is input into the uncertainty_measurements_iteration.py and transit_relative_errors.py files separately
4. **SummaryPlots.py**: The data obtained from each of these analysis methods is used in the 'SummaryPlots.py' file which produces plots to describe the trends between all systems analysed.
