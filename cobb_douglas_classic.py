# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 18:28:15 2020

@author: Mastermind
"""

def fetch_classic(source,  string):
    if source ==  'brown.zip':
        source_frame = pd.read_csv(source,  skiprows=4,  usecols=range(3, 6))
        source_frame.rename(columns = {'Данные по отработанным человеко-часам заимствованы из: Kendrick,  op. cit.,  pp. 311-313,  Table A. 10.':'series', 
                                    'Unnamed: 4':'period', 
                                    'Unnamed: 5':'value'},  inplace=True)
    elif source ==  'cobbdouglas.zip':
        source_frame = pd.read_csv(source,  usecols=range(5, 8))
    elif source ==  'douglas.zip':
        source_frame = pd.read_csv(source,  usecols=range(4, 7))
    elif source ==  'kendrick.zip':
        source_frame = pd.read_csv(source,  usecols=range(4, 7))
    result_frame = source_frame[source_frame.iloc[:,  0] ==  string]
    del source_frame
    result_frame = result_frame[result_frame.columns[[1, 2]]]
    result_frame.columns = result_frame.columns.str.title()
    result_frame.rename(columns = {'Value':string},  inplace=True)
    result_frame.iloc[:,  0] = result_frame.iloc[:,  0].astype(int)
    result_frame.iloc[:,  1] = pd.to_numeric(result_frame.iloc[:,  1],  errors = 'coerce')
    result_frame = result_frame.dropna()
    result_frame = result_frame.sort_values('Period')
    result_frame = result_frame.set_index('Period')
    return result_frame


def fetch_census(source,  string,  index):
    '''Selected Series by U.S. Bureau of the Census
    U.S. Bureau of the Census,  Historical Statistics of the United States,  1789--1945,  Washington,  D.C.,  1949.
    U.S. Bureau of the Census. Historical Statistics of the United States,  Colonial Times to 1970,  Bicentennial Edition. Washington,  D.C.,  1975.'''
    if source ==  'census1975.zip':
        source_frame = pd.read_csv(source,  usecols=range(8, 11),  dtype = {'vector':str,  'period':str,  'value':str})
    else:
        source_frame = pd.read_csv(source,  usecols=range(8, 11))
    source_frame = source_frame[source_frame.iloc[:,  0] ==  string]
    source_frame = source_frame[source_frame.columns[[1, 2]]]
    if source ==  'census1975.zip':
        source_frame.iloc[:,  0] = source_frame.iloc[:,  0].str[:4]
    else:
        pass
    source_frame.iloc[:,  1] = source_frame.iloc[:,  1].astype(float)
    source_frame.columns = source_frame.columns.str.title()
    source_frame.rename(columns = {'Value':string},  inplace=True)
    source_frame.iloc[:,  0] = source_frame.iloc[:,  0].astype(int)
    source_frame = source_frame.sort_values('Period')
    source_frame = source_frame.reset_index(drop = True)
    source_frame = source_frame.groupby('Period').mean()
    if index:
        return source_frame
    else:
        source_frame.reset_index(level = 0,  inplace=True)
        return source_frame


def cobb_douglas_original(source_frame):
    '''Cobb--Douglas Algorithm as per C.W. Cobb,  P.H. Douglas. A Theory of Production,  1928;
    source_frame.index: Period, 
    source_frame.iloc[:,  0]: Capital, 
    source_frame.iloc[:,  1]: Labor, 
    source_frame.iloc[:,  2]: Product
    '''
    def pl(series,  k = 0.25,  b = 1.01):
        return b*series**(-k)
    
    
    def pc(series,  k = 0.25,  b = 1.01):
        return b*series**(1-k)
    
    
    function_dict = {'figure_a':'Chart I Progress in Manufacturing {}$-${} ({} = 100)', 
                    'figure_b':'Chart II Theoretical and Actual Curves of Production {}$-${} ({} = 100)', 
                    'figure_c':'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines = 3 Year Moving Average', 
                    'figure_d':'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}'}
    X = source_frame.iloc[:,  0].div(source_frame.iloc[:,  1])
    Y = source_frame.iloc[:,  2].div(source_frame.iloc[:,  1])
    from numpy.lib.scimath import log
    X = log(X)
    Y = log(Y)
    k,  b = np.polyfit(X,  Y,  1) ## Original: k = 0.25
    b = np.exp(b)
    source_frame['prod_comp'] = b*(source_frame.iloc[:,  0]**k)*(source_frame.iloc[:,  1]**(1-k))
    source_frame['prod_roll'] = source_frame.iloc[:,  2].rolling(window = 3,  center = True).mean()
    source_frame['prod_roll_comp'] = source_frame.iloc[:,  3].rolling(window = 3,  center = True).mean()   
    plt.figure(1)
    plt.semilogy(source_frame.iloc[:,  0],  label = 'Fixed Capital')
    plt.semilogy(source_frame.iloc[:,  1],  label = 'Labor Force')
    plt.semilogy(source_frame.iloc[:,  2],  label = 'Physical Product')
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(function_dict['figure_a'].format(source_frame.index[0], 
                                                source_frame.index[len(source_frame)-1], 
                                                source_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.semilogy(source_frame.iloc[:,  2],  label = 'Actual Product')
    plt.semilogy(source_frame.iloc[:,  3],  label = 'Computed Product,  $P\' = {:, .4f}L^{{{:, .4f}}}C^{{{:, .4f}}}$'.format(b,  1-k,  k))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(function_dict['figure_b'].format(source_frame.index[0], 
                                                source_frame.index[len(source_frame)-1], 
                                                source_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(source_frame.iloc[:,  2].sub(source_frame.iloc[:,  4]), 
              label = 'Deviations of $P$')
    plt.plot(source_frame.iloc[:,  3].sub(source_frame.iloc[:,  5]),  '--', 
              label = 'Deviations of $P\'$')
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(function_dict['figure_c'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(source_frame.iloc[:,  3].div(source_frame.iloc[:,  2])-1)
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(function_dict['figure_d'].format(source_frame.index[0], 
                                                source_frame.index[len(source_frame)-1]))
    plt.grid(True)
    plt.figure(5,  figsize = (5,  8))
    lc = np.arange(0.2,  1.0,  0.005)
    plt.scatter(source_frame.iloc[:,  1].div(source_frame.iloc[:,  0]), 
              source_frame.iloc[:,  2].div(source_frame.iloc[:,  1]))
    plt.scatter(source_frame.iloc[:,  1].div(source_frame.iloc[:,  0]), 
              source_frame.iloc[:,  2].div(source_frame.iloc[:,  0]))
    plt.plot(lc,  pl(lc,  k = k,  b = b),  label = '$\\frac{3}{4}\\frac{P}{L}$')
    plt.plot(lc,  pc(lc,  k = k,  b = b),  label = '$\\frac{1}{4}\\frac{P}{c}$')
    plt.xlabel('$\\frac{L}{C}$')
    plt.ylabel('Indexes')
    plt.title('Relative Final Productivities of Labor and Capital')
    plt.legend()
    plt.grid(True)
    # plt.show()
    return source_frame


def cobb_douglas_preprocessing():
    '''Original Cobb--Douglas Data Preprocessing'''
    semi_frame_a = fetch_classic('cobbdouglas.zip',  'CDT2S4') ## Total Fixed Capital in 1880 dollars (4)
    semi_frame_b = fetch_classic('cobbdouglas.zip',  'CDT3S1') ## Average Number Employed (in thousands)
    semi_frame_c = fetch_census('census1949.zip',  'J0014',  True)
    semi_frame_d = fetch_census('census1949.zip',  'J0013',  True)
    semi_frame_e = fetch_classic('douglas.zip',  'DT24AS01') ## The Revised Index of Physical Production for All Manufacturing In the United States,  1899--1926
    result_frame = pd.concat([semi_frame_a,  semi_frame_b,  semi_frame_c, \
                              semi_frame_d,  semi_frame_e],  axis = 1,  sort = True)
    del semi_frame_a,  semi_frame_b,  semi_frame_c,  semi_frame_d,  semi_frame_e
    result_frame = result_frame.dropna()
    result_frame = result_frame.div(result_frame.iloc[0,  :])
    result_frame = result_frame[result_frame.columns[[0,  1,  2]]]
    return result_frame


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
result_frame = cobb_douglas_original(cobb_douglas_preprocessing())
result_frame["lab_cap"] = result_frame.iloc[:, 1].div(result_frame.iloc[:, 0])
result_frame["lab_pro"] = result_frame.iloc[:, 2].div(result_frame.iloc[:, 1])
result_frame["cap_pro"] = result_frame.iloc[:, 2].div(result_frame.iloc[:, 0])
result_frame = result_frame[result_frame.columns[range(6, 9)]]
result_frame = 100*result_frame
result_frame.set_index("lab_cap",  inplace=True)

# result_frame.dropna(inplace=True)
result_frame.to_csv('cobb_douglas_usa_pro.dat',  sep = " ")
# result_frame = cobb_douglas_preprocessing()
# result_frame.columns = ['capital',  'labor',  'product']
# result_frame = result_frame[result_frame.columns[2]]
# result_frame = 100*result_frame
# result_frame.to_csv('cobb_douglas_usa_pro.dat',  sep = " ")
# result_frame.to_excel("test.xlsx")
print(result_frame)