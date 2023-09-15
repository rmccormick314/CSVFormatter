import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

mypath = 'Adam CSVs'

files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
k = 0

dataframe = pd.DataFrame();

for fil in files:
    dataframe = pd.read_csv(mypath+'/'+fil)

    # 5. Delete Lat and Long columns
    # 2. Delete first column
    dataframe = dataframe.drop(dataframe[['system:index', 'latitude', 'longitude']], axis=1)

    # 4. Change name of last two columns to PM2_005 and PM2_007
    dataframe=dataframe.rename(columns = {'rp303_jan12_pm2_005':'pm2_005', 'rp303_jan12_pm2_007':'pm2_007'})

    # 6. Sort - smoothcdl keep only rows with 1 and 2
    dataframe = dataframe.loc[dataframe['SmoothCdl'].isin([1,2])]

    dataframe['SAME VALS'] = dataframe['pm2_005'] + dataframe['pm2_007']

    print(dataframe['SAME VALS'].value_counts())

    # 1. Change order of EVI - 5 to 20
    # 3. Move last two columns to beginning
    new_col_names = ['pm2_005','pm2_007','2classEnsemble','SAME VALS','EVI_5','EVI_6','EVI_7','EVI_8','EVI_9','EVI_10','EVI_11','EVI_12','EVI_13','EVI_14','EVI_15','EVI_16','EVI_17','EVI_18',
    'EVI_19','EVI_20','GFSAD','SmoothCdl','confid','cropland','ensemMask','eviSum1014',
    'eviSum818','evislope810','remapped']

    dataframe=dataframe.reindex(columns=new_col_names)

    dataframe['CDLcompareENSam'] = (dataframe['remapped'] * 10) + dataframe['2classEnsemble']

    print(dataframe)
    print()


    dataframe = dataframe[dataframe['confid'] >= 80] # Select only high-confidence
    final_Results = str(dataframe['CDLcompareENSam'].value_counts())

    with open(str(fil + '.txt'), "w") as text_file:
        text_file.write(final_Results)
    dataframe.to_csv(fil, sep=',', index=False)
