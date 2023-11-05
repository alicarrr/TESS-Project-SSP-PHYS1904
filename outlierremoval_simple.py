import pandas as pd
import numpy as np 


dataset = pd.read_csv('exoplanetdata_std_individuals.csv')

dataset['Ratio'] = dataset['120 M Std']/dataset['20 M/B Std']

stdev = dataset['Ratio'].std()


def cleaning(dataframe):
    count = 0
    indexlist = []
    for index, row in dataframe.iterrows():
        if abs(dataframe['Ratio'].median() - row.loc['Ratio']) >= 3 * stdev:
            count += 1
            indexlist.append(index)
    new = dataframe.copy().drop(indexlist)
    print(f"Number of entries removed: {count}")
    return(new)       




def outliers(dataframe):
    new = cleaning(dataframe)
    i = 0
    while i < 5:
        new = cleaning(new)
        i += 1
    return(new)

new = outliers(dataset)

new.to_csv('exoplanet_std_uncertainties_outliersremoved.csv', index = False)