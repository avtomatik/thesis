# =============================================================================
# Scipy Univariate Spline
# =============================================================================
from scipy.interpolate import UnivariateSpline


def fetchClassic(source, string):
    import pandas as pd
    if source == 'brown.zip':
        source_frame = pd.read_csv(source, skiprows=4, usecols=range(3, 6))
        source_frame.rename(columns = {'Данные по отработанным человеко-часам заимствованы из: Kendrick,  op. cit.,  pp. 311-313,  Table A. 10.':'series', 
                                    'Unnamed: 4':'period', 
                                    'Unnamed: 5':'value'}, inplace=True)
    elif source == 'cobbdouglas.zip':
        source_frame = pd.read_csv(source, usecols=range(5, 8))
    elif source == 'douglas.zip':
        source_frame = pd.read_csv(source, usecols=range(4, 7))
    elif source == 'kendrick.zip':
        source_frame = pd.read_csv(source, usecols=range(4, 7))
    result_frame = source_frame[source_frame.iloc[:, 0] == string]
    del source_frame
    result_frame = result_frame[result_frame.columns[[1, 2]]]
    result_frame.columns = result_frame.columns.str.title()
    result_frame.rename(columns={'Value':string}, inplace=True)
    result_frame.iloc[:, 0] = result_frame.iloc[:, 0].astype(int)
    result_frame.iloc[:, 1] = pd.to_numeric(result_frame.iloc[:, 1], errors='coerce')
    result_frame = result_frame.dropna()
    result_frame = result_frame.sort_values('Period')
    result_frame = result_frame.set_index('Period')
    return result_frame


def fetchCensus(source, string, index):
    '''Selected Series by U.S. Bureau of the Census
    U.S. Bureau of the Census,  Historical Statistics of the United States,  1789--1945,  Washington,  D.C.,  1949.
    U.S. Bureau of the Census. Historical Statistics of the United States,  Colonial Times to 1970,  Bicentennial Edition. Washington,  D.C.,  1975.'''
    import os
    import pandas as pd
    if source == 'census1975.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11), dtype={'vector':str, 'period':str, 'value':str})
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
    source_frame.rename(columns={'Value':string}, inplace=True)
    source_frame.iloc[:, 0] = source_frame.iloc[:, 0].astype(int)
    source_frame = source_frame.sort_values('Period')
    source_frame = source_frame.reset_index(drop=True)
    source_frame = source_frame.groupby('Period').mean()
    if index:
        return source_frame
    else:
        source_frame.to_csv('temporary.txt')
        del source_frame
        result_frame = pd.read_csv('temporary.txt')
        os.unlink('temporary.txt')
        return result_frame


def cobbDouglasPreprocessing():
# =============================================================================
# Original Cobb--Douglas Data Preprocessing
# =============================================================================
    import pandas as pd
    semi_frameA = fetchClassic('cobbdouglas.zip', 'CDT2S4') ## Total Fixed Capital in 1880 dollars (4)
    semi_frameB = fetchClassic('cobbdouglas.zip', 'CDT3S1') ## Average Number Employed (in thousands)
    semi_frameC = fetchCensus('census1949.zip', 'J0014', True)
    semi_frameD = fetchCensus('census1949.zip', 'J0013', True)
    semi_frameE = fetchClassic('douglas.zip', 'DT24AS01') ## The Revised Index of Physical Production for All Manufacturing In the United States,  1899--1926
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE], axis=1, sort=True)
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE
    result_frame = result_frame.dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame


def splineProcedure(source_frame):
    '''
    source_frame.index: Period, 
    source_frame.iloc[:, 0]: Capital, 
    source_frame.iloc[:, 1]: Labor, 
    source_frame.iloc[:, 2]: Product
    '''    
    X = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1]) ##Labor Capital Intensity
    Y = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]) ##Labor Productivity
    X = X.sort_values()
    spl = UnivariateSpline(X, Y)
    import numpy as np
    Z = np.linspace(X.min(), X.max(), len(source_frame)-1)
    import matplotlib.pyplot as plt
    plt.figure()
    plt.scatter(X, Y, label='Original')
    plt.plot(Z, spl(Z))
    plt.title('Labor Capital Intensity & Labor Productivity,  {}$-${}'.format(source_frame.index[0], source_frame.index[len(source_frame)-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    ##print(spl.antiderivative())
    ##print(spl.derivative())
    ##print(spl.derivatives())
    ##print(spl.ext)
    ##print(spl.get_coeffs)
    ##print(spl.get_knots)
    ##print(spl.get_residual)
    ##print(spl.integral)
    ##print(spl.roots)
    ##print(spl.set_smoothing_factor)
    plt.show()


source_frame = cobbDouglasPreprocessing()
splineProcedure(source_frame)