import lightkurve as lk
import numpy as np
import csv
from astropy.units import Quantity
import pandas as pd
from astropy.stats import mad_std
#import cleaned dataset
data_i = pd.read_csv("exoplanet_cleaned_with120.csv")
#obtain list of attributes for each system in dataset
toi_list = data_i['System'].iloc[::2]
tic_list = data_i["System"].iloc[1::2]
magnitude_list = data_i['Magnitude'].iloc[::2]
ratio_list = data_i['Ratio'].iloc[::2]
period20_list = data_i['Period'].iloc[::2]
period120_list = data_i['Period'].iloc[1::2]
#fix indexing for newly obtained dataframes
toi_list.reset_index(drop = True, inplace = True)
tic_list.reset_index(drop = True, inplace = True)
magnitude_list.reset_index(drop = True, inplace = True)
ratio_list.reset_index(drop = True, inplace = True)
period20_list.reset_index(drop = True, inplace = True)
period120_list.reset_index(drop = True, inplace = True)
#output option, insert output file here
f = open("", "w")
f.truncate()
f.close()

def csvoutput():
    rowcount = 0
    #loop over each system
    for i in range(len(tic_list)):
        #obtain data from each system
        tic = int(tic_list[i])
        toi = toi_list[i]
        mag = magnitude_list[i]
        ratio = ratio_list[i]
        period20 = period20_list[i]
        period120 = period120_list[i]
        #obtain light curves for each system        
        search_result1 = lk.search_lightcurve('TIC' + str(tic), mission = 'TESS', exptime = 20)
        search_result2 = lk.search_lightcurve('TIC' + str(tic), mission = 'TESS', exptime = 120)
        #match sectors and light curves for 20 and 120 second data        
        lc_collection1 = search_result1[0].download()
        lc_collection2 = search_result2[0].download()
        #nornmalise and remove outliers 3 standard deviations above the mean            
        lc1 = lc_collection1.normalize().remove_outliers(sigma_upper = 3, sigma_lower = float('inf'))
        lc2 = lc_collection2.normalize().remove_outliers(sigma_upper = 3, sigma_lower = float('inf'))
        #create a small array of periods around already found periods
        period1 = np.linspace(period20 - 1.5, period20 + 1.5, 5000)
        period2 = np.linspace(period120 - 1.5, period120 + 1.5, 5000)
        try:
            #create periodogram for each cadence using period ranges
            bls1 = lc1.to_periodogram(method = 'bls', period = period1, frequency_factor = 500)
            bls2 = lc2.to_periodogram(method = 'bls', period = period2, frequency_factor = 500)
            #extract data from peridogram
            planet_b_period1 = bls1.period_at_max_power
            planet_b_t01 = bls1.transit_time_at_max_power
            planet_b_dur1 = bls1.duration_at_max_power
            planet_b_depth1 = bls1.depth_at_max_power

            planet_b_period2 = bls2.period_at_max_power
            planet_b_t02 = bls2.transit_time_at_max_power
            planet_b_dur2 = bls2.duration_at_max_power
            planet_b_depth2 = bls2.depth_at_max_power
            #create mask for transits
            planet_b_mask1 = bls1.get_transit_mask(period = planet_b_period1,
                                    transit_time = planet_b_t01,
                                    duration = planet_b_dur1)
            planet_b_mask2 = bls2.get_transit_mask(period = planet_b_period2,
                                                transit_time = planet_b_t02,
                                                duration = (planet_b_dur2 + planet_b_dur2 * 0.12))
            #create dataframe of all flux values for both cadences and calculate standard deviations in flux
            x = lc1.to_pandas()
            y = lc2.to_pandas()
            x_std = x['flux'].std()
            y_std = y['flux'].std()
            #create light curves without transits
            masked_lc1 = lc1[~planet_b_mask1]
            masked_lc2 = lc2[~planet_b_mask2]
            #creates dataframe without transit for 120 second and calculate standard deviation in flux
            masked_y = masked_lc2.to_pandas()
            maskedy_std = masked_y['flux'].std()


            #bin 20 second cadence to 120 second cadence
            lc_binned1=lc1.bin(binsize = 6)
            #create new periodogram for binned 20 second data      
            bls3 = lc_binned1.to_periodogram(method = 'bls', period = period1, frequency_factor = 500);
            #get parameters 
            planet_binned_period1 = bls3.period_at_max_power
            planet_binned_t01 = bls3.transit_time_at_max_power
            planet_binned_dur1 = bls3.duration_at_max_power
            planet_binned_depth1 = bls3.depth_at_max_power
            #create mask for binned 20second data
            planet_b_mask_binned = bls3.get_transit_mask(period = planet_binned_period1,
                                                transit_time = planet_binned_t01,
                                                duration = planet_binned_dur1)
            #create binned light curve without transit and calculate standard deviation
            masked_binned_lc1 = lc_binned1[~planet_b_mask_binned]
            masked_binned = masked_binned_lc1.to_pandas()
            masked_binned_std = masked_binned['flux'].std()
            #export to csv and create header row/row format
            row = [toi, tic, mag, planet_b_period1, planet_b_period2, planet_b_depth1, planet_b_depth2, x_std, y_std, masked_binned_std, maskedy_std]
            header = ['TOI', 'TIC', 'Magnitude', '20 Period', '120 Period', '20 Depth', '120 Depth', '20 Std', '120 Std', '20 M/B Std', '120 M Std']
            with open("exoplanet_std_uncertainties_outliersremoved", "a", newline = '') as f:
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

