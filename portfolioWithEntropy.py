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
        for i in range(10000):
            self.__metropolis()
            alpha0+=0.000001
        return self.portfolio


        return 0

    def __restrictions(alpha0):
        multiplier=100
        restrictions = multiplier*( alpha0 - (self.portfolio @ self.financialdata.meanDailyReturns[0]) )
        return restrictions

    def __shannonEntropy(portfolio):
        entropy = 0
        for weight in portfolio:
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










