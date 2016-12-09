import matchingAlgo as MA

from pandas import Series, DataFrame
import pandas as pd
import math
import statistics
import time
import numpy as np
import queue as Q
import matplotlib.pyplot as plt

def run(data,startingDate,endDate,asset,RunningMeanSize,NumOfBestFitWant,date,dateTable,L):
    start_time = time.time()                                         # timer
    startDateIndex=dateTable[startingDate]
    endDateIndex=dateTable[endDate]
    temp=startDateIndex
    profit=0
    rate=0
    while (temp<endDateIndex):
        predictGrowth=round(MA.predict(data,temp,L,RunningMeanSize,NumOfBestFitWant,date,dateTable),3)
        if ((predictGrowth)>1.0):
            rate=simulate(data,temp,1)
            print('Buy. Actual Rate:{}'.format(rate))
        else:
            print('No Act.')
        profit+=rate*asset
        temp=temp+1
    print("--- %s seconds ---" % (time.time() - start_time))        # print timer
    return profit

#position=1  buy
#position=-1 sell
#take care of the boundary!!
def simulate(data,dateIndex,position):
    p1=data['price'][dateIndex]
    p2=data['price'][dateIndex+1]
    return (p2-p1)/p1
