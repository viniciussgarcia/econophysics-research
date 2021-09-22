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
    df['date'], df['hour'] = df['time'].str.split(' ', 1).str
    print(ticker)
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
        self.data = (self.__filterData(assetsData)).dropna()
#        self.DOS = 

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

class Simulation:
    @staticmethod
    def calculate(day):
        print('Simulation running...')
        sampleSize = 15
        samplesQty = 300
        assetsQty = len(day.data.columns)
        eta = 1e-3
        c = sampleSize/assetsQty
        ea = 6 #((1+np.sqrt(c))**2)*1.2
        eb = 0 #((1-np.sqrt(c))**2)*1.2
        #esp = np.linspace(eb,ea,540)
        esp = np.linspace(eb,ea,360)

        DOS = []
        for it in range(samplesQty):
            R = day.data.sample(n=sampleSize, replace=True)
            H = R.corr()
            gsp = []
            for e in esp:
                G = np.linalg.inv((e+1j*eta)*np.eye(assetsQty)-H)
                gsp.append(-(1.0/(assetsQty*np.pi))*np.trace(G.imag))
            DOS.append(gsp)
        DOS = np.average(DOS,axis=0)
        return {'probability' : DOS, 'epsilon' : esp}

def save_data(period):
    #counter=0
    for day in period.days:
        df = pd.DataFrame( Simulation.calculate(day) )
        df.to_csv(('DataTest_N_15_M_20/distribution'+day.date+'.csv'), header=None, index=None, sep=' ', mode='w')
        #df.to_csv(('DataTest/distribution'+day.date+'.csv'), header=None, index=None, sep=' ', mode='w')
        #distribution = Simulation.calculate(day)
        #plt.plot(distribution['epsilon'],distribution['probability'],'.',color='gray')
        #plt.show() 
        #counter +=1

def save_raw_data(period):
    for day in period.days:
        df = day.data
        df.to_csv(('DATA/'+day.date+'.csv'), header=True, index=True, sep=' ', mode='w')

for year in [1,2]:
    for month in [1,2,3,4,5,6,7,8,9,10,11,12]:
        timeSlice = 'year'+str(year)+'month'+str(month)
        print(timeSlice)
        period = Period(getAssets(), timeSlice=timeSlice)
        save_raw_data(period)