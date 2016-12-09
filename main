import simulation as sim

from pandas import Series, DataFrame
import pandas as pd
import math
import statistics
import time
import numpy as np
import queue as Q
import matplotlib.pyplot as plt

%matplotlib inline

#Import data from csv
rawdata0=pd.read_csv('_if00.csv',index_col='date',keep_default_na=True)
rawdata1=pd.read_csv('_if01.csv',index_col='date',keep_default_na=True)

#Parameters
L=10
numofentry=len(rawdata0['close'])
RunningMeanSize=50
NumOfBestFitWant=4

# Calculate runningMean 
# x is data, N is the running mean window size
def runningMean(x, N):
    return np.convolve(x, np.ones((N,))/N,mode='valid')

# Process raw data
# 1. Add up volumes of two serires of data
# 2. Make dataTable to convert date to index and vice versa
# 3. Calculate volumes/runningMean
# 4. Syntesize all data to data
# Not include: 1. Standardization of price. 2. Divide price and volume by its STD
    # They are done in each match below
price=rawdata0['close']
volume=rawdata0['volume']+rawdata1['volume']

date=rawdata0.index.values
dateTable=pd.Series(range(numofentry),date)
mean=runningMean(volume, RunningMeanSize)
for a in range(RunningMeanSize-1):
  mean=np.insert(mean, 0, 0)
pdmean=pd.Series(mean,index=date)
volume=volume/pdmean

data = DataFrame({'price':price,'volume':volume})
data.to_csv('ProcessedData.csv')

startingDate='8/22/16'
endDate='9/22/16'
initialAsset=100000
sim.run(data,startingDate,endDate,initialAsset,RunningMeanSize,NumOfBestFitWant,date,dateTable,L)
