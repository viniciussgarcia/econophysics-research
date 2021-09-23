# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas_datareader import data as wb
import math
import os


class KullbackLeibler():
    def __init__(self, n, m):
        self.n=n
        self.m=m
        self.xa=(1+math.sqrt(n/m))**2
        self.xb=(1-math.sqrt(n/m))**2
    
    def compute(self, path):
        relEntr = 0
        #sumexp = 0
        #sumexp2 = 0
        x,y = np.loadtxt(path, usecols=1), np.loadtxt(path, usecols=0)
        y = self.__normalizeDistribution(x,y)
        for i in range(len(x)):
            #sumexp+=(0.016713091922005572)*y[i]
            if (self.xa>x[i]>self.xb or self.xb>x[i]>self.xa):
                #sumexp2+=(0.016713091922005572)*y[i]
                relEntr += y[i]*math.log((y[i]/self.__marchenkopastur(x[i])))
        #print(sumexp)
        #print(sumexp2)
        return relEntr

    def __normalizeDistribution(self, x,y):
        sum = 0
        for i in range(len(x)):
            if (self.xa>x[i]>self.xb or self.xb>x[i]>self.xa):
                sum += y[i]
        return (y/sum)

    def __marchenkopastur(self, x):
        dv = (self.m/self.n) * (1/(2*np.pi)) * math.sqrt((self.xa-x)*(x-self.xb))/x
        return dv

entries=os.listdir('DataTest_N_15_M_20/')
KLcalculator = KullbackLeibler(15,20)
data = {'day':[], 'KL':[]}

for entry in entries:
    if entry[0:12] != 'distribution':
        continue
    path = 'DataTest_N_15_M_20/'+entry
    a = KLcalculator.compute(path)
    data['KL'].append(a)
    data['day'].append(entry[-14:-4])

df = pd.DataFrame(data)
df.to_csv(('normKL.txt'), header=None, index=None, sep=' ', mode='w')



## normalizar a integral da P(x) (dados) para fazer a kullbak leibler DONE
#  https://devblogs.microsoft.com/python/data-science-with-python-in-visual-studio-code/
## plotly para plot
## ver o melhor lambda em tukey lambda. plotar o lambda simultaneamente ao KL