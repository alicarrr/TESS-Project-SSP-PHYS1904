import lightkurve as lk
import numpy as np
import csv
from astropy.units import Quantity
import pandas as pd
from astropy.stats import mad_std

"""
    File with functions to perform all error analysis for a given data set.

"""


def cleaning(dataframe):
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
    median = dataframe[column].median()
    mean = dataframe[column].mean()
    stdev = dataframe[column].std()
    count = dataframe[column].count()
    countsqrt = np.sqrt(count)
    sem = stdev/countsqrt
    print('Median +/- SEM:',str(median), "+/-", str(sem))
    print('Mean +/- StDev:', mean, '+/-' , stdev)
    print('MadStd:', mad_std(dataframe[column]))

    return median, mean, stdev, count, sem


def outliers(dataframe):
    new = cleaning(dataframe)
    i = 0
    while i < 5:
        new = cleaning(new)
        i += 1
    return(new)


def separation(dataframe):
    indexlist_big = []
    indexlist_sml = []
    for index, row in dataframe.iterrows():
            if index % 2 != 0:
                continue
            elif row.loc['Depth'] >= 0.005 and (index % 2) == 0:
                indexlist_big.append(index)
                indexlist_big.append(index+1)
            elif row.loc['Depth'] < 0.005 and (index % 2) == 0:
                indexlist_sml.append(index)
                indexlist_sml.append(index+1)
    new_big = dataframe.copy().drop(indexlist_sml)
    new_sml = dataframe.copy().drop(indexlist_big)
    return(new_big,new_sml)
    

dataset = pd.read_csv("exoplanetdata_alldata_nocleaning.csv", index_col = False)
dataset_20sec = dataset.iloc[::2]
stdev = dataset_20sec['Ratio'].std()

new = outliers(dataset)
new.to_csv('exoplanet_cleaned_with120.csv', index = False)
        
new_big, new_sml = separation(dataset)
new_big = outliers(new_big)
new_sml = outliers(new_sml)


new_big.to_csv('exoplanet_cleaned_big_with120.csv', index = False)
new_sml.to_csv('exoplanet_cleaned_sml_with120.csv', index = False)

analysis(new,'Ratio')
analysis(new_sml,'Ratio')
analysis(new_big,'Ratio')