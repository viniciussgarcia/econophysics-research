# -*- coding: utf-8 -*-
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
from pandas_datareader import data as wb
from datetime import datetime, timedelta
#from pandas.plotting import lag_plot, autocorrelation_plot, bootstrap_plot

class FinancialDataForPeriod:
    def __init__(self, assets, startDate, endDate ):
        self.assets = assets
        self.quantityOfAssets = len(assets)
        assetsData = {}
        for asset in assets:
        #calculando retornos logaritmicos direto na leitura
            assetsData[asset] = np.log(1 + (wb.DataReader(asset, data_source='yahoo', start=startDate, end=endDate )['Adj Close'].pct_change() ) )
        self.returns = pd.DataFrame(assetsData)
        self.meanDailyReturns = pd.DataFrame(self.returns.mean()).reset_index(drop=True)
        self.meanDailyReturns.index = assets
        self.covMatrix = self.returns.cov()


class PortfolioOptimization:
    def __init__(self, financialdata):
        self.financialdata = financialdata
        self.portfolio = np.full(financialdata.quantityOfAssets, (1./financialdata.quantityOfAssets), dtype = np.double )
    
    def findBestPortolio():
        alpha0=np.amin(self.financialdata.meanDailyReturns[0])
        N=100
        increment = (np.amax(self.financialdata.meanDailyReturns[0]) - np.amin(self.financialdata.meanDailyReturns[0]))/N
        for i in range(N):
            self.__metropolis(alpha0)
            self.__saveRelevantData()
            alpha0+=increment
        return self.portfolio


    def __metropolis(alpha0):
        i = 0
        steps = 1e5
        while i < steps:
            kT = steps - i
            proposedPortfolio = self.__proposedPortfolio()
            costDelta = self.__costFunction(alpha0,proposedPortfolio) - self.__costFunction(alpha0,self.portfolio)
            if costDelta < 0:
                self.portfolio = proposedPortfolio
                i+=1
            else:
                a = np.random.random()
                if np.exp(costDelta/kT) > a:
                    self.portfolio = proposedPortfolio
                    i+=1
        return

    def __proposedPortfolio():
        #random normalized portfolio
        portfolio = np.random.rand(self.financialdata.quantityOfAssets)
        portfolio = portfolio / np.sum(portfolio)
        return portfolio

    def __costFunction(alpha0, portfolio):
        return ( ( portfolio @ self.financialdata.covMatrix @ portfolio ) - self.__shannonEntropy(portfolio) + \
            self.__restrictions(alpha0, portfolio) )

    def __restrictions(alpha0, portfolio):
        multiplier=100
        restrictions = multiplier*( alpha0 - (portfolio @ self.financialdata.meanDailyReturns[0]) )
        return restrictions

    def __shannonEntropy(portfolio):
        entropy = 0
        for weight in portfolio:
            entropy -= weight*np.log(weight)
        return entropy

    def __saveRelevantData():
        return

#--------------------------------------------------------#

assets = ['mglu3', 'prio3', 'bpac3', 'tots3', 'wege3']
assets = [asset+'.sa' for asset in assets]
delta = timedelta(days = 120)
startDate = (datetime.today() - delta).isoformat()
endDate = datetime.today().isoformat()

testperiod = FinancialDataForPeriod(assets, startDate, endDate)
print(testperiod.meanDailyReturns)








