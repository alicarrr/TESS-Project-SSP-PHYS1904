import lightkurve as lk
import numpy as np
import csv
from astropy.units import Quantity
import pandas as pd
from astropy.stats import mad_std

# File with functions to perform all error analysis for a given data set. 
# It also filters the dataframe to separate for depths above and below 0.005


def cleaning(dataframe):
    """Function to clean an input dataframe of outliers 4 standard deviation from the median

    Args:
        dataframe: dataframe inputted that analysis will be performed on
    Returns:
        new: cleaned dataframe with outliers removed
    """
    stdev = dataframe['Ratio'].std()
    count = 0
    indexlist = []
    for index, row in dataframe.iterrows():
        if abs(dataframe['Ratio'].median() - row.iloc[8]) >= 4 * stdev:
            count += 1
            indexlist.append(index)
            indexlist.append(index+1)
    new = dataframe.copy().drop(indexlist)
    print(f"Number of entries removed: {count}")
    return(new)           


def analysis(dataframe, column):
    """_summary_

    Args:
        dataframe: dataframe inputted that analysis will be performed on
        column: column title from dataframe that analysis is performed on

    Returns:
        median:     Median of dataset
        mean:       Mean of dataset
        stdev:      Standard deviation of dataset
        count:      Number of items in dataset
        sem:        Standard error of the mean of the dataset
    """
    median = dataframe[column].median()     # Calculate median
    mean = dataframe[column].mean()         # Calculate mean
    stdev = dataframe[column].std()         # Calculate standard deviation
    count = dataframe[column].count()       # Count number of items in list
    countsqrt = np.sqrt(count)
    sem = stdev / countsqrt                 # Calculate standard error of the mean (SEM)

    # Print required analysis
    print('Median +/- SEM:', str(median), "+/-", str(sem))
    print('Mean +/- StDev:', mean, '+/-' , stdev)
    print('MadStd:', mad_std(dataframe[column]))

    return median, mean, stdev, count, sem


def outliers(dataframe):
    """Performs outlier rejection on inputted dataframe

    Args:
        dataframe: dataframe inputted that analysis will be performed on
    Returns:
        new: cleaned dataframe with outliers removed
    """
    new = cleaning(dataframe)
    i = 0
    while i < 5:
        new = cleaning(new)
        i += 1
    return(new)


def separation(dataframe):
    """Function to filter for depths greater than 0.005

    Args:
        dataframe: input dataframe to have depth values filtered

    Returns:
        new_big: dataframe containing values with depth < 0.005
        new_sml: dataframe containing values with depth < 0.005
    """
    indexlist_big = []
    indexlist_sml = []
    
    for index, row in dataframe.iterrows():
            if index % 2 != 0:
                continue
            elif row.loc['Depth'] >= 0.005 and (index % 2) == 0:
                indexlist_big.append(index)
                indexlist_big.append(index + 1)
            elif row.loc['Depth'] < 0.005 and (index % 2) == 0:
                indexlist_sml.append(index)
                indexlist_sml.append(index + 1)
    new_big = dataframe.copy().drop(indexlist_sml)
    new_sml = dataframe.copy().drop(indexlist_big)
    return(new_big, new_sml)
    

# Import uncleaned data before outlier rejection has been performed
dataset = pd.read_csv("exoplanetdata_alldata_nocleaning.csv", index_col = False)
dataset_20sec = dataset.iloc[::2]
stdev = dataset_20sec['Ratio'].std()

# Remove outliers from original data
new = outliers(dataset)
new.to_csv('exoplanet_cleaned_with120.csv', index = False)

# Split data into depths larger than 0.005 (new_big) and less than 0.005 (new_sml)
new_big, new_sml = separation(dataset)

# Perform outlier rejection on separated files
new_big = outliers(new_big)
new_sml = outliers(new_sml)

# Convert each to csv
new_big.to_csv('exoplanet_cleaned_big_with120.csv', index = False)
new_sml.to_csv('exoplanet_cleaned_sml_with120.csv', index = False)

# Compute data analysis for the ratio input in each dataframe including above and below depth of 0.005 and all data
analysis(new,'Ratio')
analysis(new_sml,'Ratio')
analysis(new_big,'Ratio')