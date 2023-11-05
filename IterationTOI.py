import lightkurve as lk
import numpy as np
import csv
from astropy.units import Quantity
import pandas as pd
from astropy.stats import mad_std

# File to iterate over a range of TOI inputs and perform transit analysis on these. 
# This was adapted from the Jupyter notebook provided. 

# NOTE: make sure the CSV file "exoplanetdata_alldata_nocleaning.csv" is empty before running, this code takes a long time to 
# run and will overwrite an existing file with the name provided if the data for it already exists

# Pull database from NASA of project candidates and their properties
nasa = pd.read_csv("nasa_toi_alldata.csv")
# Extract TOI and TIC ID from database
toi_list = nasa["toi"]
tic_list = nasa["tid"]

# Make empty dataframe
data = {}
 
# Uncomment these three lines before running the code (if uncommented data in csv will be overwritten when run)

# f = open("exoplanetdata_alldata_nocleaning.csv", "w")      # Open new file to import exoplanet data into after individual analysis
# f.truncate()                                               # Erase existing data
# f.close()                                                  # Close file

def csvoutput():
    """
        Function to produce light curves and transit model for each inputted TOI and TIC pair 
        and writes these results to an output CSV file which can then have analysis performed on it.
    """
    rowcount = 0

    for i in range(len(tic_list)):
        tic = tic_list[i]
        toi = toi_list[i]

        for index, row in nasa.iterrows():
            if row['tid'] == tic and row['toi'] == toi:
                mag = row["Mag"]
                period_nasa = row["Period"]
                type = row['type']
            else:
                continue
        
        search_result1 = lk.search_lightcurve('TIC' + str(tic), mission = 'TESS', exptime = 20)
        search_result2 = lk.search_lightcurve('TIC' + str(tic), mission = 'TESS', exptime = 120)
    
        search_result2mis = search_result2.mission
        
        if len(search_result1) == 0:
            continue
        else:
            search_result1mis = search_result1.mission[0]
        
            for i  in range(len(search_result2)):
                if search_result2mis[i] == search_result1mis:
                    lc_collection1 = search_result1[0].download()
                    lc_collection2 = search_result2[i].download()
                else:
                    continue

            lc1 = lc_collection1.normalize().remove_outliers(sigma_upper = 3, sigma_lower = float('inf'))
            lc2 = lc_collection2.normalize().remove_outliers(sigma_upper = 3, sigma_lower = float('inf'))

            period1 = np.linspace(0.5, 20, 10000)
            period2 = np.linspace(0.5, 20, 10000)
            bls1 = lc1.to_periodogram(method = 'bls', period=period1, frequency_factor = 500);
            bls2 = lc2.to_periodogram(method = 'bls', period=period2, frequency_factor = 500);
            

            if (period_nasa - 1) <= round((bls1.period_at_max_power).value) <= (period_nasa + 1) or (period_nasa - 1) <= round((bls2.period_at_max_power).value) <= (period_nasa + 1) and period_nasa < 25:
                try:
                    if (period_nasa - 2) <= round((bls1.period_at_max_power).value) <= (period_nasa + 2) and period_nasa < 20:
                        period2 = np.linspace(0.5, bls1.period_at_max_power.value * 1.5 , 10000)

                    elif (period_nasa - 2) <= round((bls2.period_at_max_power).value) <= (period_nasa + 2) and period_nasa < 20:
                        period1 = np.linspace(0.5, bls2.period_at_max_power.value * 1.5 , 10000)

                except ValueError:
                    continue

                bls1 = lc1.to_periodogram(method='bls', period = period1, frequency_factor = 500);
                bls2 = lc2.to_periodogram(method='bls', period = period2, frequency_factor = 500);

                planet_b_period1 = bls1.period_at_max_power
                planet_b_t01 = bls1.transit_time_at_max_power
                planet_b_dur1 = bls1.duration_at_max_power
                planet_b_depth1 = bls1.depth_at_max_power

                planet_b_period2 = bls2.period_at_max_power
                planet_b_t02 = bls2.transit_time_at_max_power
                planet_b_dur2 = bls2.duration_at_max_power
                planet_b_depth2 = bls2.depth_at_max_power

                data[tic,toi] = {"20sec":{"Period":planet_b_period1,"Time": planet_b_t01,"Duration": planet_b_dur1,"Depth": planet_b_depth1}, "120sec" : {"Period":planet_b_period2,"Time": planet_b_t02,"Duration": planet_b_dur2,"Depth": planet_b_depth2}}

                x=list(data[tic,toi]["20sec"].keys())
                l0=x.insert(0, "System")
                l1=x.insert(1, "Format")
                l2=x.insert(2, "Magnitude")
                l3=x.append("Ratio")
                l4=x.insert(2, "Type")

                ratio = (data[tic,toi]["120sec"]["Depth"].value) / (data[tic,toi]["20sec"]["Depth"].value)

                row20 = [toi,"20sec", type, mag , data[tic,toi]["20sec"]["Period"].value, data[tic,toi]["20sec"]["Time"].value, data[tic,toi]["20sec"]["Duration"].value, data[tic,toi]["20sec"]["Depth"].value, ratio]
                row120 = [tic,"120sec"," ", "" , data[tic,toi]["120sec"]["Period"].value, data[tic,toi]["120sec"]["Time"].value, data[tic,toi]["120sec"]["Duration"].value, data[tic,toi]["120sec"]["Depth"].value, ""]

                with open("exoplanetdata_alldata_nocleaning.csv", "a", newline = '') as f:
                    writer = csv.writer(f)
                    if rowcount == 0:
                        writer.writerow(x)
                        rowcount = 1
                        writer.writerow(row20)
                        writer.writerow(row120)
                    else: 
                        writer.writerow(row20)
                        writer.writerow(row120)
            else:
                continue

csvoutput()