# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas_datareader import data as wb
from datetime import datetime, timedelta
import math
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

class PortfolioGenerator:
    def __init__(self, financialdata):
        self.financialdata = financialdata
        self.portfolio = np.full(financialdata.quantityOfAssets, (1./financialdata.quantityOfAssets), dtype = np.double )
        self.output = {'retorno':[], 'cost':[],'stddev':[], 'entropy':[]}
        for asset in self.financialdata.assets:
            self.output[asset]=[]

    def generatePortolios(self, N, x):
        self.x=x
        print(self.x)
        np.random.seed(123)
        for i in range(N):
            self.__generateRandomPortfolio()
            self.__saveRelevantData()
        self.output=pd.DataFrame(data=self.output)
        self.output.sort_values(by=['retorno'],inplace=True)
        return self.output

    def getOutput(self):
        return self.output

    def __generateRandomPortfolio(self):
        #random normalized portfolio
        portfolio = np.random.rand(self.financialdata.quantityOfAssets)
        self.portfolio = portfolio / np.sum(portfolio)
        return

    def __costFunction(self):
        return ( self.x*( self.portfolio @ self.financialdata.covMatrix @ self.portfolio ) - (1-self.x)*self.__shannonEntropy(self.portfolio) )

    def __shannonEntropy(self,portfolio):
        entropy = 0
        for weight in portfolio:
            entropy -= weight*np.log(weight)
        return entropy

    def __saveRelevantData(self):
        self.output['retorno'].append(self.portfolio @ self.financialdata.meanDailyReturns[0])
        self.output['stddev'].append(math.sqrt(self.portfolio @ self.financialdata.covMatrix @ self.portfolio))
        self.output['cost'].append(self.__costFunction())
        self.output['entropy'].append(self.__shannonEntropy(self.portfolio))
        for i in range(self.financialdata.quantityOfAssets):
            self.output[self.financialdata.assets[i]].append(self.portfolio[i])
        return

class FrontierCalculator:
    def __init__(self, generator, N, x):
        self.generator = generator
        self.data = self.generator.generatePortolios(N,x)
        self.frontier = pd.DataFrame({'retorno':[], 'cost':[]})

    def findFrontier(self, numberOfSteps):
        maxReturn, minReturn = self.data['retorno'].max() , self.data['retorno'].min()
        stepSize = (maxReturn - minReturn)/numberOfSteps
        for step in range(numberOfSteps):
            referenceReturn = minReturn+(step)*stepSize
            filteredData = self.data.query('retorno >= @referenceReturn &  retorno < (@referenceReturn + @stepSize)')
            minCost = filteredData['cost'].min()
            if pd.isnull(minCost):
                continue
            self.frontier=self.frontier.append(filteredData[filteredData.cost == minCost])
        return self.frontier

#--------------------------------------------------------------#
assets = ['mglu3', 'prio3', 'bpac3', 'tots3', 'wege3']
assets = [asset+'.sa' for asset in assets]
delta = timedelta(days = 720)
startDate = (datetime.today() - delta).isoformat()
endDate = datetime.today().isoformat()
testperiod = FinancialDataForPeriod(assets, startDate, endDate)

xvalues = [0, 0.1, 0.5, 0.9, 0.99, 0.999, 0.9999, 1]
#xvalues = [0, 0.995]

for xvalue in xvalues:
    headerdata=''
    generator = PortfolioGenerator(testperiod)
    frontierCalculator = FrontierCalculator(generator, int(1E5), xvalue)
    frontier = frontierCalculator.findFrontier(100)
    for column in frontier.columns:
        headerdata += column+' '
    np.savetxt('filteredmontecarlodata'+str(xvalue)+'.dat', frontier.values, header=headerdata)
    np.savetxt('montecarlodata'+str(xvalue)+'.dat', generator.getOutput().values, header=headerdata)
#plt.xlabel('Lagrangiano')
#plt.ylabel('Retorno esperado')
#plt.scatter(frontier['cost'], frontier['retorno'], alpha=0.5)
#plt.savefig('test'++'.jpg')
#plt.show()