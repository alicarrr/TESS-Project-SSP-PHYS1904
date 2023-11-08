import lightkurve as lk
import numpy as np
import csv
from astropy.units import Quantity
import pandas as pd
from astropy.stats import mad_std
import math as mt
#import cleaned datatset
data_i = pd.read_csv("exoplanet_cleaned_with120.csv")
#obtain list of attributes for each system in dataset
toi_list = data_i['System'].iloc[::2]
tic_list = data_i["System"].iloc[1::2]
magnitude_list = data_i['Magnitude'].iloc[::2]
ratio_list = data_i['Ratio'].iloc[::2]
period20_list = data_i['Period'].iloc[::2]
period120_list = data_i['Period'].iloc[1::2]
#fix indexing for newly obtained dataframes
toi_list.reset_index(drop = True, inplace=True)
tic_list.reset_index(drop = True, inplace = True)
magnitude_list.reset_index(drop = True, inplace = True)
ratio_list.reset_index(drop = True, inplace = True)
period20_list.reset_index(drop = True, inplace = True)
period120_list.reset_index(drop = True, inplace = True)

# Uncomment these three lines before running the code (if uncommented data in csv will be overwritten when run)

# f = open("exoplanet_UPD_relative_error.csv", "w")          # Open new file to import exoplanet data into after individual analysis
# f.truncate()                                               # Erase existing data
# f.close()                                                  # Close file

def csvoutput():
    rowcount = 0
    #loop over each system
    for i in range(len(tic_list)):
        #extract values for each system from lists
        tic = int(tic_list[i])
        toi = toi_list[i]
        mag = magnitude_list[i]
        ratio = ratio_list[i]
        period20 = period20_list[i]
        period120 = period120_list[i]
        #create light curve for both cadences
        search_result1 = lk.search_lightcurve('TIC'+str(tic), mission='TESS', exptime=20)
        search_result2 = lk.search_lightcurve('TIC'+str(tic), mission='TESS', exptime=120)
        lc_collection1 = search_result1[0].download()
        lc_collection2 = search_result2[0].download()
        #normalise and remove outliers greater than 3 standard deviations above mean for light curves
        lc1 = lc_collection1.normalize().remove_outliers(sigma_upper = 3, sigma_lower = float('inf'))
        lc2 = lc_collection2.normalize().remove_outliers(sigma_upper = 3, sigma_lower = float('inf'))
        #create period ranges around already found periods
        period1 = np.linspace(period20-2, period20+2, 2000)
        period2 = np.linspace(period120-2, period120+2, 2000)
        try:
            #create periodograms using period ranges
            bls1 = lc1.to_periodogram(method='bls', period = period1, frequency_factor = 500)
            bls2 = lc2.to_periodogram(method='bls', period = period2, frequency_factor = 500)
            #extract transit information
            planet_b_period1 = bls1.period_at_max_power
            planet_b_t01 = bls1.transit_time_at_max_power
            planet_b_dur1 = bls1.duration_at_max_power
            planet_b_depth1 = bls1.depth_at_max_power
            planet_b_period2 = bls2.period_at_max_power
            planet_b_t02 = bls2.transit_time_at_max_power
            planet_b_dur2 = bls2.duration_at_max_power
            planet_b_depth2 = bls2.depth_at_max_power
            #find transit points for both cadences
            planet_b_mask1 = bls1.get_transit_mask(period = planet_b_period1,
                                     transit_time = planet_b_t01 + 0.003,
                                     duration = planet_b_dur1 + planet_b_dur1 * 0.007)
            planet_b_mask2 = bls2.get_transit_mask(period = planet_b_period2,
                                     transit_time = planet_b_t02 + 0.003,
                                     duration = (planet_b_dur2+planet_b_dur2 * 0.007))
            #extract transit points from light curve and make dataframes
            data20 = lc1[planet_b_mask1].to_pandas()
            data120 = lc2[planet_b_mask2].to_pandas()
            #extract flux values for each cadence
            flux20 = data20['flux']
            flux120 = data120['flux']
            flux20 = list(data20['flux'])
            flux120 = list(data120['flux'])
            # how many points in each cadence during transit
            size20 = len(flux20)
            size120 = len(flux120)
            #create cutoof points for ingress and egress 
            p7_20 = mt.ceil(0.07 * size20)
            p7_120 = mt.ceil(0.07 * size120)
            #extract transit bottoms using cutoffs
            transit_20 = []
            for i in range(p7_20, size20 - p7_20):
                transit_20.append(flux20[i])
            transit_120 = []
            for i in range(p7_120, size120 - p7_120):
                transit_120.append(flux120[i])
            #Ffind length of transit bottoms
            size_t20 = len(transit_20)
            size_t120 = len(transit_120)
            #caluclate SEMs of transit bottoms
            sigma20 = np.std(transit_20) / mt.sqrt(size_t20)
            sigma120 = np.std(transit_120) / mt.sqrt(size_t120)
            #calculate relative error of transit bottoms
            relative20 = sigma20/planet_b_depth1
            relative120 = sigma120/planet_b_depth2
            #create headers/row formats and export to csv
            row = [toi, tic, mag, period20, period120, planet_b_depth1, relative20, planet_b_depth2, relative120]
            header = ['TOI', 'TIC', 'Magnitude', '20 Period', '120 Period', '20 Depth', '20 Error', '120 Depth', '120 Error']
            with open("exoplanet_UPD_relative_error.csv", "a", newline = '') as f:
                writer = csv.writer(f)
                if rowcount == 0:
                    writer.writerow(header)
                    rowcount = 1
                    writer.writerow(row)
                else: 
                    writer.writerow(row)

        except ValueError:
            continue

csvoutput()
