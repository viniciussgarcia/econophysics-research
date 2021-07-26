# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas_datareader import data as wb
import math
import time

def getAssets():
    path='symbols.csv'
    file = open(path, 'r')
    data = file.read().split('\n')
    return data

def getTimeSeriesIntraday(interval, ticker, timeSlice, apiKey='K565YCHGP2BN7YV1'):
    df = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol='+ticker+'&interval='+interval+'&slice='+timeSlice+'&apikey='+apiKey+'&datatype=csv&outputsize=full')
    print(ticker)
    df['date'], df['hour'] = df['time'].str.split(' ', 1).str
    df.drop(columns = ['time', 'open', 'high', 'low'], inplace=True)
    df['return'] = np.log(1 + df['close'].pct_change() )
    return df

class Period:
    def __init__(self, assets, interval='1min', timeSlice = 'year1month1'):
        self.interval = interval
        self.assets = assets
        self.timeSlice = timeSlice
        self.assetsData = {}
        self.__fillAssetsData()
        self.days = []
        self.__buildDays()

    
    def __buildDays(self):
        dates = self.assetsData[self.assets[0]].date.unique()
        for date in dates:
            day = Day(date, self.assetsData)
            self.days.append(day)
    
    def __fillAssetsData(self):
        counter = 0
        start_time = time.time()
        for asset in self.assets:
            counter+=1
            if counter == 70:
                counter = 1
                if (time.time() - start_time) <= 1:
                    time.sleep(1-(time.time()-start_time))
                start_time = time.time()
            self.assetsData[asset] = getTimeSeriesIntraday(self.interval, asset, self.timeSlice)
            


class Day:
    def __init__(self, date, assetsData):
        self.date = date
        self.filteredData = self.__filterData(assetsData)
        self.corrMatrix = self.filteredData.corr()
        #self.entropy = self.__calculateEntropy()

    def __calculateEntropy(self):
        distribution = PlemeljSokhotski.calculate(self.corrMatrix)
        entropy = ShannonEntropy.calculate(distribution)
        return entropy
    
    def __filterData(self, assetsData):
        filteredData = pd.DataFrame()
        for asset in assetsData.keys():
            assetData = assetsData[asset]
            df = assetData[assetData['date'] == str(self.date)]
            df.set_index('hour', inplace=True)
            returns = pd.Series(data=df['return'])
            mean = returns.mean(skipna=True)
            meansquared = (returns**2).mean()
            filteredData[asset] = (returns - mean)/math.sqrt(meansquared-(mean**2))
        return filteredData

class ShannonEntropy:
    @staticmethod
    def calculate(distribution):
        entropy = 0
        for probability in distribution['probabilities']:
            entropy -= probability*np.log(probability)
        return entropy

class PlemeljSokhotski:
    @staticmethod
    def calculate(corrMatrix):
        N = corrMatrix.shape[0]
        distribution = { 'epsilon': np.arange(0, 10, 0.01), 'probability':[] }
        
        I = np.identity(N)
        for e in distribution['epsilon']:
            G = np.linalg.inv((e+0.001j)*I - corrMatrix)
            ro = (-1/(N*np.pi))*np.imag(np.trace(G))
            distribution['probability'].append(ro)
        return distribution




testperiod = Period(getAssets())

counter=0
for day in testperiod.days:
    if counter >=2 :
        break
    df = pd.DataFrame( PlemeljSokhotski.calculate(day.corrMatrix) )
    df.to_csv(('distributiontest'+day.date+'.csv'), header=None, index=None, sep=' ', mode='w')
    counter +=1