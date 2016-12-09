from pandas import Series, DataFrame
import pandas as pd
import math
import statistics
import time
import numpy as np
import queue as Q
import matplotlib.pyplot as plt

#Calculate distance
#x is the data
#i,j are the index it used to calculate distance (start from 0)
# VarP and VarV are variance of price and volume in these L days
def distance(x,y,i,j,VarP,VarV):
    return math.sqrt(math.pow(x['price'][i]-y['price'][j],2)/VarP+math.pow(x['volume'][i]-y['volume'][j],2)/VarV)

#Determine the smallest D for X,Y with fixed l, (1<l=L<100)
#X is the recent market data we want to benchmark (0 to L)
#Y is the historical data we want to match to (0 to L)
def solveOnlyL(X,Y,L):
    VarP=statistics.variance(X['price'])
    VarV=statistics.variance(X['volume'])
    result={}
    temp=recurse(X,Y,L,L,L-1,L-1,result,VarP,VarV)
    return temp

#Recurse to get the D
#X is current data, Y is historical data
#l is num of data used from X, L is num of data used from Y
#i,j are the current index D(i,j) we are trying to calculate
def recurse(X,Y,l,L,i,j,result,VarP,VarV):
    if ((i==-1)or(j==-1)):
        return float('Inf')
    if (i*100+j) in result:
        return result[i*100+j]
    if ((i==0)and(j==0)):
        return distance(X,Y,i,j,VarP,VarV)
    result[i*100+j]=distance(X,Y,i,j,VarP,VarV)+min(recurse(X,Y,l,L,i,j-1,result,VarP,VarV),recurse(X,Y,l,L,i-1,j,result,VarP,VarV),recurse(X,Y,l,L,i-1,j-1,result,VarP,VarV))
    return result[i*100+j]

def getResult(x,y,l,L,result):
    if (x>=l or y>=L):
        return float('Inf')
    return result[x*100+y]

# Run solve for all the possible historical data period to find the best fits
# X is the data, dateIndex is the date we want to predict its future trend
# result is the output (the best fit perirods)
def match(X,dateIndex,L,result,RunningMeanSize,NumOfBestFitWant,date,dateTable):
    target=X[dateIndex-L+1:dateIndex+1].copy(deep=True)
    target['price']=target['price']/target['price'][L-1]            # standardize price and let the last day to be 1
    size=0
    jump=0
    for x in range(dateIndex-2*L+2)[RunningMeanSize-1:]:
        reference=X[x:x+L].copy(deep=True)
        reference['price']=reference['price']/reference['price'][L-1] # standardize price and let the last day to be 1
        temp=solveOnlyL(target,reference,L)                           #use solveOnlyL to save time
        result.put([-temp ,x])                                        #negative value enables biggest data to stay on top
        size=size+1
        if(size>NumOfBestFitWant):
            result.get()

# Predict next day trend by calling match. Plot volume data
# targetDate is the day we want to predict the future trend
def predict(data,targetDateIndex,L,RunningMeanSize,NumOfBestFitWant,date,dateTable):
    #initializations
    result=Q.PriorityQueue()
    match(data,targetDateIndex,L,result,RunningMeanSize,NumOfBestFitWant,date,dateTable)
    DInverseSum=0
    sum=0

    #pulling results from priority queue
    while not result.empty():
        out=result.get()                                               #get (-D, start date index) pairs from result
        D_=-out[0]                                                     #D, convert negative back
        matchStartDateIndex=out[1]
        matchStartDate=date[out[1]]                                    #convert start date index to actual date
        matchEndDate=date[out[1]+L-1]                                  #convert end date index to actual date
    
        #calculate predicted growth
        sum+=(data['price'][matchStartDateIndex+L]/data['price'][matchStartDateIndex+L-1])/D_
        DInverseSum+=1/D_
        print('D={}, Data Start From {} to {}'.format(round(D_,4),matchStartDate,matchEndDate))
        
    predictGrowth=sum/DInverseSum 
    print('Predict Growth:{}'.format(predictGrowth))
    return predictGrowth

#visualize volume
# data is the data to be plotted,
# start and target are start and end date index
# fig is the figure object
# imgaIndex=1-4
def plotResult(data,start,target,fig,imageIndex):
    fig.add_subplot(2,2,imageIndex)
    data['volume'][start:start+L].plot()
    data['volume'][target:target+L].plot()
