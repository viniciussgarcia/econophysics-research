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
        N=1000
        increment = (np.amax(self.financialdata.meanDailyReturns[0]) - np.amin(self.financialdata.meanDailyReturns[0]))/N
        for i in range(N):
            self.__metropolis(alpha0)
            self.__saveRelevantData()
            alpha0+=increment
        return self.portfolio


    def __metropolis(alpha0):
        i = 0
        while i < 1000:
            proposedPortfolio = self.__proposedPortfolio()
            costDelta = self.__costFunction(alpha0,proposedPortfolio) - self.__costFunction(alpha0,self.portfolio)
            if costDelta < 0:
                self.portfolio = proposedPortfolio
                i+=1
            else:
                a = np.random.random()
                if np.exp(costDelta) > a:
                    self.portfolio = proposedPortfolio
                    i+=1
        return 0    

    def __proposedPortfolio():
        portfolio = self.portfolio
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
        for weight in self.portfolio:
            entropy -= weight*np.log(weight)
        return entropy

assets = ['mglu3', 'prio3', 'bpac3', 'tots3', 'wege3']
assets = [asset+'.sa' for asset in assets]
delta = timedelta(days = 120)
startDate = (datetime.today() - delta).isoformat()
endDate = datetime.today().isoformat()

testperiod = FinancialDataForPeriod(assets, startDate, endDate)
print(testperiod.meanDailyReturns)





'''
class MetropolisAlgorithm:
    def __init__(self, covmatrix):

        self.covmatrix = covmatrix

    def __costFunction( ):
        return 0

    def metropolis( weights ):
        self.weights = weights
        self.__costFunction( )
        for weight in self.weights:
            weight += 1


'''










