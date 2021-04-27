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
        self.data = []
        self.bestPortfolios = []
    def findBestPortolio(self):
        alpha0 = np.amin(self.financialdata.meanDailyReturns[0])
        N = 20
        increment = (np.amax(self.financialdata.meanDailyReturns[0]) - np.amin(self.financialdata.meanDailyReturns[0]))/N
        for i in range(N):
            self.__metropolis(alpha0)
            self.__saveRelevantData(alpha0)
            alpha0 += increment
        return self.portfolio


    def __metropolis(self,alpha0):
        currentStep = 0
        steps = 2e4
        triesLimit = 1e3
        tries = 0
        while currentStep < steps:
            kT = steps - currentStep
            proposedPortfolio = self.__proposedPortfolio()
            costDelta = self.__costFunction(alpha0,proposedPortfolio) - self.__costFunction(alpha0,self.portfolio)
            if costDelta < 0:
                self.portfolio = proposedPortfolio
                currentStep += 1
                tries = 0
            else:
                a = np.random.random()
                if np.exp(costDelta/kT) > a:
                    self.portfolio = proposedPortfolio
                    currentStep += 1
                    tries = 0
            tries += 1
            if tries >= triesLimit:
                break 
        return

    def __proposedPortfolio(self):
        #random normalized portfolio
        portfolio = np.random.rand(self.financialdata.quantityOfAssets)
        portfolio = portfolio / np.sum(portfolio)
        return portfolio

    def __costFunction(self,alpha0, portfolio):
        return ( ( portfolio @ self.financialdata.covMatrix @ portfolio ) - self.__shannonEntropy(portfolio) + \
            self.__restrictions(alpha0, portfolio) )

    def __restrictions(self,alpha0, portfolio):
        multiplier = 1e6
        restrictions = multiplier*( alpha0 - (portfolio @ self.financialdata.meanDailyReturns[0]) )
        return abs(restrictions)

    def __shannonEntropy(self,portfolio):
        entropy = 0
        for weight in portfolio:
            entropy -= weight*np.log(weight)
        return entropy

    def __saveRelevantData(self,alpha0):
        self.data.append([alpha0, self.portfolio @ self.financialdata.meanDailyReturns[0], (self.portfolio @ self.financialdata.covMatrix @ self.portfolio), \
            self.__costFunction(alpha0,self.portfolio), self.__shannonEntropy(self.portfolio)])
        self.bestPortfolios.append(self.portfolio)
        return

class MarkowitzOptimization:
    def __init__(self, financialdata):
        self.financialdata = financialdata
        self.portfolio = np.full(financialdata.quantityOfAssets, (1./financialdata.quantityOfAssets), dtype = np.double )
        self.data = []
        self.bestPortfolios = []
    def findBestPortolio(self):
        alpha0 = np.amin(self.financialdata.meanDailyReturns[0])
        N = 20
        increment = (np.amax(self.financialdata.meanDailyReturns[0]) - np.amin(self.financialdata.meanDailyReturns[0]))/N
        for i in range(N):
            self.__metropolis(alpha0)
            self.__saveRelevantData(alpha0)
            alpha0 += increment
        return self.portfolio

    def __metropolis(self,alpha0):
        currentStep = 0
        steps = 5e4
        triesLimit = 1e4
        tries = 0
        while currentStep < steps:
            kT = steps - currentStep
            proposedPortfolio = self.__proposedPortfolio()
            costDelta = self.__costFunction(alpha0,proposedPortfolio) - self.__costFunction(alpha0,self.portfolio)
            if costDelta < 0:
                self.portfolio = proposedPortfolio
                currentStep += 1
                tries = 0
            else:
                a = np.random.random()
                if np.exp(costDelta/kT) > a:
                    self.portfolio = proposedPortfolio
                    currentStep += 1
                    tries = 0
            tries += 1
            if tries >= triesLimit:
                break 
        return

    def __proposedPortfolio(self):
        #random normalized portfolio
        portfolio = np.random.rand(self.financialdata.quantityOfAssets)
        portfolio = portfolio / np.sum(portfolio)
        return portfolio

    def __costFunction(self,alpha0, portfolio):
        return ( ( portfolio @ self.financialdata.covMatrix @ portfolio ) + self.__restrictions(alpha0, portfolio) )

    def __restrictions(self,alpha0, portfolio):
        multiplier = 1e6
        restrictions = multiplier*( alpha0 - (portfolio @ self.financialdata.meanDailyReturns[0]) )
        return abs(restrictions)

    def __saveRelevantData(self,alpha0):
        self.data.append([alpha0, self.portfolio @ self.financialdata.meanDailyReturns[0], (self.portfolio @ self.financialdata.covMatrix @ self.portfolio), \
            self.__costFunction(alpha0,self.portfolio)])
        self.bestPortfolios.append(self.portfolio)
        return



#--------------------------------------------------------#

assets = ['mglu3', 'prio3', 'bpac3', 'tots3', 'wege3']
assets = [asset+'.sa' for asset in assets]
delta = timedelta(days = 720)
startDate = (datetime.today() - delta).isoformat()
endDate = datetime.today().isoformat()

testperiod = FinancialDataForPeriod(assets, startDate, endDate)
'''optimizer = PortfolioOptimization(testperiod)
optimizer.findBestPortolio()
headerData = 'alpha		         actualreturn        	  variance        	   costfunction        	     entropy'
np.savetxt('data3.dat', np.array(optimizer.data), header=headerData)
np.savetxt('bestPortfolio3.dat', np.array(optimizer.bestPortfolios))
'''
headerData = 'alpha		         actualreturn        	  variance        	   costfunction'
markowitzoptimizer = MarkowitzOptimization(testperiod)
markowitzoptimizer.findBestPortolio()
np.savetxt('markowitzdata.dat', np.array(markowitzoptimizer.data), header=headerData)
np.savetxt('markowitzbestportfolio.dat', np.array(markowitzoptimizer.bestPortfolios))
