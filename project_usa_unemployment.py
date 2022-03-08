# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 23:12:03 2019

@author: Mastermind
"""

def fetchCensus(source, string, index):
    '''Selected Series by U.S. Bureau of the Census
    U.S. Bureau of the Census,  Historical Statistics of the United States,  1789--1945,  Washington,  D.C.,  1949.
    U.S. Bureau of the Census. Historical Statistics of the United States,  Colonial Times to 1970,  Bicentennial Edition. Washington,  D.C.,  1975.'''
    import os
    import pandas as pd
    if source =='census1975.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11), dtype = {'vector':str, 'period':str, 'value':str})
    else:
        source_frame = pd.read_csv(source, usecols=range(8, 11))
    source_frame = source_frame[source_frame.iloc[:, 0] ==string]
    source_frame = source_frame[source_frame.columns[[1, 2]]]
    if source =='census1975.zip':
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
def BLSLNU(source):
    '''LNU04000000: Bureau of Labor Statistics Unemployment Rate'''
    string = 'LNU04000000'
    import pandas as pd
    source_frame = pd.read_csv(source, sep = '\t', low_memory = False)
    source_frame = source_frame[source_frame.iloc[:, 0].str.contains(string)]
    source_frame = source_frame[source_frame.iloc[:, 2] =='M13']
    result_frame = source_frame[source_frame.columns[[1, 3]]]
    result_frame.rename(columns = {'year':'period'}, inplace=True)
    result_frame.columns = result_frame.columns.str.title()
    result_frame.rename(columns = {'Value':string}, inplace=True)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].astype(float)
    result_frame = result_frame.set_index('Period')
    return result_frame
import os
import pandas as pd
import matplotlib.pyplot as plt
os.chdir('D:')
semi_frameA = fetchCensus('census1975.zip', 'D0086', True)
semi_frameB = BLSLNU('dataset USA BLS 2017-07-06 ln.data.1.AllData')
result_frame = pd.concat([semi_frameA, semi_frameB], axis = 1, sort = True)
del semi_frameA, semi_frameB
result_frame.plot(title = 'US Unemployment,  {}$-${}'.format(result_frame.index[0], result_frame.index[len(result_frame)-1]), grid = True)
os.chdir('C:\\Projects')
plt.savefig('unemployment.pdf', format = 'pdf', dpi = 900)
#result_frame['fused'] = result_frame.mean(1)
#from pandas.plotting import autocorrelation_plot
#autocorrelation_plot(result_frame.iloc[:, 2])
#plt.grid(True)
#os.chdir('C:\\Projects')
#plt.savefig('unemployment.pdf', format = 'pdf', dpi = 900)