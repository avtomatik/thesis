# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 20:45:44 2019

@author: Mastermind
"""
def fetchCensus(source, string, index):
    '''Selected Series by U.S. Bureau of the Census
    U.S. Bureau of the Census,  Historical Statistics of the United States,  1789--1945,  Washington,  D.C.,  1949.
    U.S. Bureau of the Census. Historical Statistics of the United States,  Colonial Times to 1970,  Bicentennial Edition. Washington,  D.C.,  1975.'''
    if source == 'census1975.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11), dtype = {'vector':str, 'period':str, 'value':str})
    else:
        source_frame = pd.read_csv(source, usecols=range(8, 11))
    source_frame = source_frame[source_frame.iloc[:, 0] == string]
    source_frame = source_frame[source_frame.columns[[1, 2]]]
    if source == 'census1975.zip':
        source_frame.iloc[:, 0] = source_frame.iloc[:, 0].str[:4]
    else:
        pass
    source_frame.iloc[:, 1] = source_frame.iloc[:, 1].astype(float)
    source_frame.columns = source_frame.columns.str.title()
    source_frame.rename(columns = {'Value':string}, inplace=True)
    source_frame.iloc[:, 0] = source_frame.iloc[:, 0].astype(int)
    source_frame = source_frame.sort_values('Period')
    source_frame = source_frame.reset_index(drop = True)
    source_frame = source_frame.groupby('Period').mean()
    if index:
        return source_frame
    else:
        source_frame.to_csv('temporary.txt')
        del source_frame
        result_frame = pd.read_csv('temporary.txt')
        os.unlink('temporary.txt')
        return result_frame
def plotRMF(source_frame):
    """
    source_frame.iloc[:, 0]: Period;
    source_frame.iloc[:, 1]: Series
    Rolling Mean Filter"""
    plt.figure(1)
    plt.title('Moving Average {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    source_frame['sma'] = source_frame.iloc[:, 1].rolling(window = 1, center = True).mean()
    plt.scatter(source_frame.iloc[:, 0], source_frame.iloc[:, 2], label = '$Y$')
    """Smoothed Series Calculation"""
    for i in range(1, len(source_frame)//2):
        source_frame.iloc[:, 2] = source_frame.iloc[:, 1].rolling(window = 1+i, center = True).mean()
        if i%2 == 0:
            plt.plot(0.5+source_frame.iloc[:, 0], source_frame.iloc[:, 2], label = '$\\bar Y_{m = %d}$' %(i, ))
        else:
            plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 2], label = '$\\bar Y_{m = %d}$' %(i, ))
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Moving Average Deviations {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Deviations ($\\delta$),  Percent')
    source_frame['del'] = (source_frame.iloc[:, 1].rolling(window = 1, center = True).mean().shift(-1)-source_frame.iloc[:, 1].rolling(window = 1, center = True).mean()).div(source_frame.iloc[:, 1].rolling(window = 1, center = True).mean())
    plt.scatter(source_frame.iloc[:, 0], source_frame.iloc[:, 3], label = '$\\delta(Y)$')
    """Deviations Calculation"""
    for i in range(1, len(source_frame)//2):
        source_frame.iloc[:, 3] = (source_frame.iloc[:, 1].rolling(window = 1+i, center = True).mean().shift(-1)-source_frame.iloc[:, 1].rolling(window = 1+i, center = True).mean()).div(source_frame.iloc[:, 1].rolling(window = 1+i, center = True).mean())
        if i%2 == 0:
            plt.plot(0.5+source_frame.iloc[:, 0], source_frame.iloc[:, 3], label = '$\\delta(\\bar Y_{m = %d})$' %(i, ))
        else:
            plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 3], label = '$\\delta(\\bar Y_{m = %d})$' %(i, ))

    plt.grid(True)
    plt.legend()
    plt.show()
def plotGrowthElasticity(source_frame):
    '''Growth Elasticity Plotting
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Series
    '''    
    resultList = [] ##Create List Results
    for i in range(len(source_frame)-3):
        '''
        `Period`: Period,  Centered
        `ValueA`: Value,  Centered
        `ValueB`: Value,  Growth Rate
        `ValueC`: Value,  Elasticity
        '''
        resultList.append({'Period': (source_frame.iloc[1+i, 0]+source_frame.iloc[2+i, 0])/2, \
                           'ValueA': (source_frame.iloc[1+i, 1]+source_frame.iloc[2+i, 1])/2, \
                           'ValueB': (source_frame.iloc[2+i, 1]-source_frame.iloc[i, 1])/(source_frame.iloc[i, 1]+source_frame.iloc[1+i, 1]), \
                           'ValueC': (source_frame.iloc[2+i, 1]+source_frame.iloc[3+i, 1]-source_frame.iloc[i, 1]-source_frame.iloc[1+i, 1])/(source_frame.iloc[i, 1]+source_frame.iloc[1+i, 1]+source_frame.iloc[2+i, 1]+source_frame.iloc[3+i, 1])})
    result_frame = pd.Data_frame(resultList) ##Convert List to Dataframe
    del resultList
    result_frame = result_frame.set_index('Period')
    plt.figure()
    result_frame.iloc[:, 1].plot(label = 'Growth Rate')
    result_frame.iloc[:, 2].plot(label = 'Elasticity Rate')
    plt.title('Growth & Elasticity Rates')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.show()
import os
import pandas as pd
import matplotlib.pyplot as plt
source_frame = fetchCensus('census1949.zip', 'J0014', False)
plotGrowthElasticity(source_frame)
plotRMF(source_frame)