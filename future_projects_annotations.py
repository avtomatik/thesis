##D:\archiveProjectUSACobbDouglasOptions.py
from datafetch import beaFetch
from datafetch import beaFetch
from datafetch import FRBCU
def preprocessingDXDY(start, stop, period, capital, labor, product):
    period = period[start:stop].reset_index(drop = True)
    capital = capital[start:stop].reset_index(drop = True)
    labor = labor[start:stop].reset_index(drop = True)
    product = product[start:stop].reset_index(drop = True)
    labor = labor/labor[0]
    X = capital/labor ##Labor Capital Intensity
    Y = product/labor ##Labor Productivity
    DX = X/X.shift(1) ##Labor Capital Intensity Increment
    DY = Y/Y.shift(1) ##Labor Productivity Increment
    return X, Y, DX, DY
def procedureA(X, Y, DX, DY):
    import matplotlib.pyplot as plt
    '''Scenario I'''
    ##plt.figure(1)
    ####plt.plot(X, Y, '--', X, Y, '+') # Description Here
    ####plt.xlabel('Labor Capital Intensity') ##To Do: Add Annotations
    ####plt.ylabel('Labor Productivity') ##To Do: Add Annotations
    ##plt.plot(DX, DY, '--', DX, DY, '+') # Description Here
    ##plt.xlabel('Labor Capital Intensity Increment') ##To Do: Add Annotations
    ##plt.ylabel('Labor Productivity Increment') ##To Do: Add Annotations
    ##plt.show()
    '''Scenario II'''
    fig = plt.figure()
    ##plt.plot(X, Y, '--', X, Y, '+') # Description Here
    ##plt.xlabel('Labor Capital Intensity') ##To Do: Add Annotations
    ##plt.ylabel('Labor Productivity') ##To Do: Add Annotations
    plt.plot(DX, DY, '--', DX, DY, '+') # Description Here
    plt.xlabel('Labor Capital Intensity Increment') ##To Do: Add Annotations
    plt.ylabel('Labor Productivity Increment') ##To Do: Add Annotations
    ax = fig.add_subplot(111)
##    for i in range(0, 90, 5):
##        ax.annotate(period[i], (DX[i], DY[i]))
    plt.grid()
    ##result_frame = pd.concat([period, capital, labor, product, X, Y, DX, DY], axis = 1, sort = False)
    ##result_frame.to_csv('dataset USA Cobb-Douglas Modern Dataset-Out.csv', index = False)
    plt.show()
def procedureB(X, Y, DX, DY):
    import matplotlib.pyplot as plt
    '''Scenario I'''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(X, Y)
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
##    for i in range(4, 90, 5):
##        ax.annotate(period[i], (X[i], Y[i]))
    plt.grid()
    plt.show()
    '''Scenario II'''
    ##plt.figure()
    ##plt.plot(X, Y, 'o', X, Y, '-')
    ##plt.xlabel('Labor Capital Intensity')
    ##plt.ylabel('Labor Productivity')
    ##plt.show()
'''To Do: Revise Dataset'''
import os
os.chdir('D:')
import pandas as pd
from datafetch import archivedCommonFetch
frame = archivedCommonFetch()
T = frame.iloc[:, 0]
d = frame.iloc[:, 8]/frame.iloc[:, 7] ##Deflator,  2009 = 100
C11 = frame.iloc[:, 4]*d ##Fixed Assets,  K160491
C12 = frame.iloc[:, 2]*d ##Fixed Assets,  k3n31gd1es000
C21 = frame.iloc[:, 1]*frame.iloc[:, 10]
C22 = frame.iloc[:, 1]*frame.iloc[:, 11]/frame.iloc[:, 9]
C23 = frame.iloc[:, 2]*frame.iloc[:, 10]
C24 = frame.iloc[:, 2]*frame.iloc[:, 11]/frame.iloc[:, 9]
L = frame.iloc[:, 5]
P11 = d*frame.iloc[:, 6] ##Production
P12 = 100*d*frame.iloc[:, 6]/frame.iloc[:, 12] ##Production Maximum
P21 = frame.iloc[:, 9]*frame.iloc[:, 10]
P22 = frame.iloc[:, 11]
P23 = frame.iloc[:, 13]*frame.iloc[:, 10]
P24 = frame.iloc[:, 13]*frame.iloc[:, 11]/frame.iloc[:, 9]
##'''Option 1'''
##X1, X2, X3, X4 = preprocessingDXDY(42, 87, T, C11, L, P11)
##'''Option 2'''
##X1, X2, X3, X4 = preprocessingDXDY(42, 87, T, C11, L, P12)
##'''Option 3'''
X1, X2, X3, X4 = preprocessingDXDY(42, 87, T, C12, L, P11)
##'''Option 4'''
##X1, X2, X3, X4 = preprocessingDXDY(42, 87, T, C12, L, P12)
'''To Do: test `k1ntotl1si000`'''
##'''Option 1'''
##X1, X2, X3, X4 = preprocessingDXDY(4, 88, T, C21, L, P21)
##'''Option 2'''
##X1, X2, X3, X4 = preprocessingDXDY(4, 88, T, C22, L, P22)
##'''Option 3'''
##X1, X2, X3, X4 = preprocessingDXDY(4, 88, T, C21, L, P23)
##'''Option 4'''
##X1, X2, X3, X4 = preprocessingDXDY(4, 88, T, C22, L, P24)
##'''Option 5'''
##X1, X2, X3, X4 = preprocessingDXDY(4, 88, T, C23, L, P21)
##'''Option 6'''
##X1, X2, X3, X4 = preprocessingDXDY(4, 88, T, C24, L, P22)
##'''Option 7'''
##X1, X2, X3, X4 = preprocessingDXDY(4, 88, T, C23, L, P23)
##'''Option 8'''
##X1, X2, X3, X4 = preprocessingDXDY(4, 88, T, C24, L, P24)
procedureA(X1, X2, X3, X4)
##procedureB(X1, X2, X3, X4)
"""Update from `project.py`"""
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
    result_frame.rename(columns = {'Value':string}, inplace=True)
    result_frame.iloc[:, 0] = result_frame.iloc[:, 0].astype(int)
    result_frame.iloc[:, 1] = pd.to_numeric(result_frame.iloc[:, 1], errors = 'coerce')
    result_frame = result_frame.dropna()
    result_frame = result_frame.sort_values('Period')
    result_frame = result_frame.set_index('Period')
    return result_frame
def beaFetch(zpfl, wrkbk, wrksht, start, finish, line):
    '''Data _frame Fetching from Bureau of Economic Analysis Zip Archives'''
    '''
    zpfl: Name of Zip Archive, 
    wrkbk: Name of Excel File within Zip Archive, 
    wrksht: Name of Worksheet within Excel File within Zip Archive, 
    boundary: 4+<Period_Finish>-<Period_Start>, 
    line: Line'''
    import os
    import pandas as pd
    boundary = 4-start+finish
    if zpfl == None:
        xl = pd.ExcelFile(wrkbk)
    else:
        import zipfile
        zf = zipfile.ZipFile(zpfl, 'r')
        xl = pd.ExcelFile(zf.open(wrkbk))
        del zf
    source_frame = pd.read_excel(xl, wrksht, usecols=range(2, boundary), skiprows=7)
    source_frame.dropna(inplace=True)
    source_frame = source_frame.T
    source_frame.to_csv('temporary.txt')
    del xl, source_frame
    result_frame = pd.read_csv('temporary.txt', usecols=[0, line], skiprows=1)
    os.unlink('temporary.txt')
    result_frame.columns = result_frame.columns.to_series().replace({'^Unnamed: \d':'Period'}, regex = True)
    result_frame = result_frame.set_index('Period')
    return result_frame
def fetchCensus(source, string, index):
    '''Selected Series by U.S. Bureau of the Census
    U.S. Bureau of the Census,  Historical Statistics of the United States,  1789--1945,  Washington,  D.C.,  1949.
    U.S. Bureau of the Census. Historical Statistics of the United States,  Colonial Times to 1970,  Bicentennial Edition. Washington,  D.C.,  1975.'''
    import os
    import pandas as pd
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
def fetchCapital():
    """Series Not Used - `k3ntotl1si000`"""
    import pandas as pd
    semi_frameA = fetchClassic('cobbdouglas.zip', 'CDT2S1') ##Annual Increase in Terms of Cost Price (1)
    semi_frameB = fetchClassic('cobbdouglas.zip', 'CDT2S3') ##Annual Increase in Terms of 1880 dollars (3)
    semi_frameC = fetchClassic('cobbdouglas.zip', 'CDT2S4') ##Total Fixed Capital in 1880 dollars (4)
    """Fixed Assets: k1n31gd1es000,  1925--2016,  Table 4.1. Current-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization"""
    semi_frameD = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '401 Ann', 1925, 2016, 9)
    """Not Used: Fixed Assets: k3n31gd1es000,  1925--2016,  Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization"""
    semi_frameE = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '403 Ann', 1925, 2016, 9)
    semi_frameF = fetchCensus('census1975.zip', 'P0107', True)
    semi_frameG = fetchCensus('census1975.zip', 'P0110', True)
    semi_frameH = fetchCensus('census1975.zip', 'P0119', True)
    """Kendrick J.W.,  Productivity Trends in the United States,  Page 320"""
    semi_frameI = fetchClassic('kendrick.zip', 'KTA15S08')
    """Douglas P.H.,  Theory of Wages,  Page 332"""
    semi_frameJ = fetchClassic('douglas.zip', 'DT63AS01')
    """FRB Data"""
    semi_frameK = FRBFA()
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                           semi_frameF, semi_frameG, semi_frameH, semi_frameI, semi_frameJ, \
                           semi_frameK], axis = 1, sort = True)
    return result_frame
def FRBFA():
    '''Returns _frame of Manufacturing Fixed Assets Series,  Billion USD:
        _frame.iloc[:, 0]: Nominal;
        _frame.iloc[:, 1]: Real
    '''
    import os
    import pandas as pd
    source_frame = pd.read_csv('dataset USA FRB invest_capital.csv', skiprows=4, skipfooter = 688, engine = 'python')
    source_frame = source_frame.T
    source_frame.to_csv('temporary.txt')
    del source_frame
    source_frame = pd.read_csv('temporary.txt', skiprows=1)
    os.unlink('temporary.txt')
    source_frame.columns = source_frame.columns.to_series().replace({'Manufacturing':'Period'})
    source_frame = source_frame.set_index('Period')
    source_frame['nominal_frb'] = source_frame.iloc[:, 1]*source_frame.iloc[:, 2].div(1000*source_frame.iloc[:, 0])+source_frame.iloc[:, 4]*source_frame.iloc[:, 5].div(1000*source_frame.iloc[:, 3])
    source_frame['real_frb'] = source_frame.iloc[:, 2].div(1000)+source_frame.iloc[:, 5].div(1000)
    result_frame = source_frame[source_frame.columns[[6, 7]]]
    return result_frame
def FRBFADEF():
    """Returns _frame of Deflator for Manufacturing Fixed Assets Series,  Index:
        _frame.iloc[:, 0]: Deflator
    """
    import os
    import pandas as pd
    source_frame = pd.read_csv('dataset USA FRB invest_capital.csv', skiprows=4, skipfooter = 688, engine = 'python')
    source_frame = source_frame.T
    source_frame.to_csv('temporary.txt')
    del source_frame
    source_frame = pd.read_csv('temporary.txt', skiprows=1)
    os.unlink('temporary.txt')
    source_frame.columns = source_frame.columns.to_series().replace({'Manufacturing':'Period'})
    source_frame = source_frame.set_index('Period')
    source_frame['fa_def_frb'] = (source_frame.iloc[:, 1]+source_frame.iloc[:, 4]).div(source_frame.iloc[:, 0]+source_frame.iloc[:, 3])
    result_frame = source_frame[source_frame.columns[[6]]]
    return result_frame
def pricesInverseSingle(frame):
    '''Intent: Returns Prices Icrement Series from Cumulative Deflator Series;
    source: pandas Data_frame'''
    import pandas as pd
    D = frame.iloc[:, 0].div(frame.iloc[:, 0].shift(1))-1
    return D
def processing(frame, col):
    interim_frame = frame[frame.columns[[col]]]
    interim_frame = interim_frame.dropna()
    result_frame = pricesInverseSingle(interim_frame)
    result_frame = result_frame.dropna()
    return result_frame
def fetchBEA(source, string):
    '''`dataset USA BEA NipaDataA.txt`: U.S. Bureau of Economic Analysis
    Archived: https://www.bea.gov/National/FAweb/Details/Index.html
    https://www.bea.gov//national/FA2004/DownSS2.asp,  Accessed May 26,  2018'''
    import pandas as pd
    if source == 'beanipa20131202.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
    elif source == 'beanipa20150302section5.zip': ##Not Used
        source_frame = pd.read_csv(source, usecols=range(8, 11))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
    elif source == 'beanipa20150501.zip':
        source_frame = pd.read_csv(source, usecols=range(14, 18))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
        source_frame = source_frame[source_frame.iloc[:, 2] == 0]
        source_frame = source_frame[source_frame.columns[[0, 1, 3]]]
    elif source == 'dataset USA BEA NipaDataA.txt':
        source_frame = pd.read_csv(source, thousands = ', ')
        source_frame.rename(columns = {'Value':string}, inplace=True)
    elif source == 'beanipa20131202sfat.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
    elif source == 'beanipa20170823sfat.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
    else:
        pass
    result_frame = source_frame[source_frame.iloc[:, 0] == string]
    del source_frame
    result_frame = result_frame[result_frame.columns[[1, 2]]]
    result_frame = result_frame.reset_index(drop = True)
    result_frame = result_frame.set_index('Period')
    result_frame.to_csv('temporary.txt')
    del result_frame
    result_frame = pd.read_csv('temporary.txt')
    import os
    os.unlink('temporary.txt')
    result_frame = result_frame.set_index('Period')
    if source == 'beanipa20170823sfat.zip':
        result_frame = result_frame.round(3)
    else:
        pass
    result_frame = result_frame.drop_duplicates()
    return result_frame
def FRBIP():
    '''Indexed Manufacturing Series: FRB G17 IP,  AIPMA_SA_IX,  1919--2018'''
    import pandas as pd
    source_frame = pd.read_csv('dataset USA FRB US3_IP 2018-09-02.csv', skiprows=7)
    source_frame.columns = source_frame.columns.to_series().replace({'[ .:;@_]':''}, regex = True)
    source_frame['Period'], source_frame['Mnth'] = source_frame['Unnamed0'].str.split('-').str
    source_frame = source_frame.groupby('Period').mean()
    source_frame.to_csv('temporary.txt')
    del source_frame
    result_frame = pd.read_csv('temporary.txt', usecols=[0, 3])
    import os
    os.unlink('temporary.txt')
    result_frame = result_frame.set_index('Period')
    return result_frame
def fetchINFCF():
    '''Retrieve Yearly Price Rates from `infcf16652007.zip`'''
    import os
    import pandas as pd
    os.chdir('D:')
    source_frame = pd.read_csv('infcf16652007.zip', usecols=range(4, 7))
    series = source_frame.iloc[:, 0].unique()
    i = 0
    for ser in series:
        current_frame = source_frame[source_frame.iloc[:, 0] == ser]
        current_frame = current_frame[current_frame.columns[[1, 2]]]
        current_frame.columns = current_frame.columns.str.title()
        current_frame.rename(columns = {'Value':ser}, inplace=True)
        current_frame = current_frame.set_index('Period')
        current_frame.iloc[:, 0] = current_frame.iloc[:, 0].rdiv(1)
        current_frame = -pricesInverseSingle(current_frame) ## Put "-" Is the Only Way to Comply with the Rest of Study
        if i == 0:
            result_frame = current_frame
        elif i> = 1:
            result_frame = pd.concat([result_frame, current_frame], axis = 1, sort = True)
        del current_frame
        i+ = 1
    result_frame = result_frame[result_frame.columns[range(14)]]
    result_frame['cpiu_fused'] = result_frame.mean(1)
    result_frame = result_frame[result_frame.columns[[14]]]
    return result_frame
def cobbDouglasCapitalDeflator():
    """Fixed Assets Deflator,  2009 = 100"""
    import pandas as pd
    import scipy as sp
    base = 84 ## 2009 = 100
    """Combine L2,  L15,  E7,  E23,  E40,  E68 & P107/P110"""
    """Bureau of Labor Statistics
    Data Not Used As It Covers Only Years of 1998--2017"""
    """Results:
    fetchCensus('census1949.zip', 'L0036', True) Offset with fetchCensus('census1975.zip', 'E0183', True)
    fetchCensus('census1949.zip', 'L0038', True) Offset with fetchCensus('census1975.zip', 'E0184', True)
    fetchCensus('census1949.zip', 'L0039', True) Offset with fetchCensus('census1975.zip', 'E0185', True)
    fetchCensus('census1975.zip', 'E0052', True) Offset With fetchCensus('census1949.zip', 'L0002', True)"""
    """Cost-Of-Living Indexes"
    "E183: Federal Reserve Bank,  1913 = 100"
    "E184: Burgess,  1913 = 100"
    "E185: Douglas,  1890-99 = 100"""
    sub_frameA = fetchClassic('cobbdouglas.zip', 'CDT2S1')
    sub_frameB = fetchClassic('cobbdouglas.zip', 'CDT2S3')
    sub_frameC = fetchCensus('census1949.zip', 'L0001', True)
    sub_frameD = fetchCensus('census1949.zip', 'L0002', True)
    sub_frameE = fetchCensus('census1949.zip', 'L0015', True)
    sub_frameF = fetchCensus('census1949.zip', 'L0037', True)
    sub_frameG = fetchCensus('census1975.zip', 'E0007', True)
    sub_frameH = fetchCensus('census1975.zip', 'E0008', True)
    sub_frameI = fetchCensus('census1975.zip', 'E0009', True)
    sub_frameJ = fetchCensus('census1975.zip', 'E0023', True)
    sub_frameK = fetchCensus('census1975.zip', 'E0040', True)
    sub_frameL = fetchCensus('census1975.zip', 'E0068', True)
    sub_frameM = fetchCensus('census1975.zip', 'E0183', True)
    sub_frameN = fetchCensus('census1975.zip', 'E0184', True)
    sub_frameO = fetchCensus('census1975.zip', 'E0185', True)
    sub_frameP = fetchCensus('census1975.zip', 'E0186', True)
    sub_frameQ = fetchCensus('census1975.zip', 'P0107', True)
    sub_frameR = fetchCensus('census1975.zip', 'P0110', True)
    sub_frameS = FRBFADEF()
    sub_frameQ = sub_frameQ[22:]
    sub_frameR = sub_frameR[22:]
    basis_frame = pd.concat([sub_frameA, sub_frameB, sub_frameC, sub_frameD, sub_frameE, \
                          sub_frameF, sub_frameG, sub_frameH, sub_frameI, sub_frameJ, \
                          sub_frameK, sub_frameL, sub_frameM, sub_frameN, sub_frameO, \
                          sub_frameP, sub_frameQ, sub_frameR, sub_frameS], axis = 1, sort = True)
    del sub_frameA, sub_frameB, sub_frameC, sub_frameD, sub_frameE, sub_frameF, sub_frameG, \
        sub_frameH, sub_frameI, sub_frameJ, sub_frameK, sub_frameL, sub_frameM, sub_frameN, \
        sub_frameO, sub_frameP, sub_frameQ, sub_frameR, sub_frameS
    basis_frame['fa_def_cd'] = basis_frame.iloc[:, 0].div(basis_frame.iloc[:, 1])
    basis_frame['fa_def_cn'] = basis_frame.iloc[:, 16].div(basis_frame.iloc[:, 17])
    """Cobb--Douglas"""
    semi_frameA = processing(basis_frame, 19)
    """Bureau of Economic Analysis"""
    """Fixed Assets: k1n31gd1es000,  1925--2016,  Table 4.1. Current-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization"""
    sub_frameA = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '401 Ann', 1925, 2016, 9)
    """Fixed Assets: kcn31gd1es000,  1925--2016,  Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization"""
    sub_frameB = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '402 Ann', 1925, 2016, 9)
    """Not Used: Not Used: Fixed Assets: k3n31gd1es000,  1925--2016,  Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization"""
    sub_frameC = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '403 Ann', 1925, 2016, 9)
    """Not Used: Fixed Assets: k3ntotl1si000,  1925--2016,  Table 2.3. Historical-Cost Net Stock of Private Fixed Assets,  Equipment,  Structures,  and Intellectual Property Products by Type"""
    sub_frameD = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section2ALL_xls.xls', '203 Ann', 1925, 2016, 48)
    """Not Used: mcn31gd1es000,  1925--2016,  Table 4.5. Chain-Type Quantity Indexes for Depreciation of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization"""
    sub_frameE = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '405 Ann', 1925, 2016, 9)
    """Not Used: mcntotl1si000,  1925--2016,  Table 2.5. Chain-Type Quantity Indexes for Depreciation of Private Fixed Assets,  Equipment,  Structures,  and Intellectual Property Products by Type"""
    sub_frameF = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section2ALL_xls.xls', '205 Ann', 1925, 2016, 48)
    """Real Values"""
    semi_frameB = pd.concat([sub_frameA, sub_frameB], axis = 1, sort = True)
    del sub_frameA, sub_frameB, sub_frameC, sub_frameD, sub_frameE, sub_frameF
    semi_frameB['ppi_bea'] = 100*semi_frameB.iloc[:, 0].div(semi_frameB.iloc[base, 0]*semi_frameB.iloc[:, 1])
    semi_frameB.iloc[:, 2] = processing(semi_frameB, 2)
    semi_frameB = semi_frameB[semi_frameB.columns[[2]]]
    """Bureau of the Census"""
    """Correlation Test:
    `kendall_frame = result_frame.corr(method = 'kendall')`
    `pearson_frame = result_frame.corr(method = 'pearson')`
    `spearman_frame = result_frame.corr(method = 'spearman')`
    Correlation Test Result: kendall & pearson & spearman: L2,  L15,  E7,  E23,  E40,  E68"""
    sub_frameA = processing(basis_frame, 3)
    sub_frameB = processing(basis_frame, 4)
    sub_frameC = processing(basis_frame, 6)
    sub_frameD = processing(basis_frame, 9)
    sub_frameE = processing(basis_frame, 10)
    sub_frameF = processing(basis_frame, 11)
    sub_frameG = processing(basis_frame, 20)
    semi_frameC = pd.concat([sub_frameA, sub_frameB, sub_frameC, sub_frameD, sub_frameE, \
                          sub_frameF, sub_frameG], axis = 1, sort = True)
    del sub_frameA, sub_frameB, sub_frameC, sub_frameD, sub_frameE, sub_frameF, sub_frameG
    semi_frameC['ppi_census_fused'] = semi_frameC.mean(1)
    semi_frameC = semi_frameC[semi_frameC.columns[[7]]]
    """Federal Reserve"""
    semi_frameD = processing(basis_frame, 18)
    """Robert C. Sahr,  2007"""
    semi_frameE = fetchINFCF()
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE], axis = 1, sort = True)
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE
    result_frame = result_frame[128:]
    result_frame['def_cum_bea'] = sp.cumprod(1+result_frame.iloc[:, 1])
    result_frame['def_cum_cen'] = sp.cumprod(1+result_frame.iloc[:, 2])
    result_frame['def_cum_frb'] = sp.cumprod(1+result_frame.iloc[:, 3])
    result_frame['def_cum_sah'] = sp.cumprod(1+result_frame.iloc[:, 4])
    result_frame.iloc[:, 5] = result_frame.iloc[:, 5].div(result_frame.iloc[177, 5]) ##1970
    result_frame.iloc[:, 6] = result_frame.iloc[:, 6].div(result_frame.iloc[177, 6]) ##1970
    result_frame.iloc[:, 7] = result_frame.iloc[:, 7].div(result_frame.iloc[177, 7]) ##1970
    result_frame.iloc[:, 8] = result_frame.iloc[:, 8].div(result_frame.iloc[177, 8]) ##1970
    result_frame['def_cum_com'] = result_frame.iloc[:, [5, 6, 7]].mean(1)
    result_frame['fa_def_com'] = processing(result_frame, 9)
    result_frame.iloc[:, 9] = result_frame.iloc[:, 9].div(result_frame.iloc[216, 9]) ##2009
    result_frame = result_frame[result_frame.columns[[9]]]
    result_frame.dropna(inplace=True)
    return result_frame
def cobbDouglasCapitalExtension():
    """Existing Capital Dataset"""
    source_frame = fetchCapital()
    """Convert Capital Series into Current (Historical) Prices"""
    source_frame['nominal_cbb_dg'] = source_frame.iloc[:, 0]*source_frame.iloc[:, 2].div(1000*source_frame.iloc[:, 1])
    source_frame['nominal_census'] = source_frame.iloc[:, 5]*source_frame.iloc[:, 7].div(source_frame.iloc[:, 6])
    source_frame['nominal_dougls'] = source_frame.iloc[:, 0]*source_frame.iloc[:, 9].div(1000*source_frame.iloc[:, 1])
    source_frame['nominal_kndrck'] = source_frame.iloc[:, 5]*source_frame.iloc[:, 8].div(1000*source_frame.iloc[:, 6])
    source_frame.iloc[:, 15] = source_frame.iloc[66, 6]*source_frame.iloc[:, 15].div(source_frame.iloc[66, 5])
    """Douglas P.H. -- Kendrick J.W. (Blended) Series"""
    source_frame['nominal_doug_kndrck'] = source_frame.iloc[:, 14:16].mean(1)
    """Cobb C.W.,  Douglas P.H. -- FRB (Blended) Series"""
    source_frame['nominal_cbb_dg_frb'] = source_frame.iloc[:, [12, 10]].mean(1)
    """Capital Structure Series: `Cobb C.W.,  Douglas P.H. -- FRB (Blended) Series` to `Douglas P.H. -- Kendrick J.W. (Blended) Series`"""
    source_frame['struct_ratio'] = source_frame.iloc[:, 17].div(source_frame.iloc[:, 16])
    """Filling the Gaps within Capital Structure Series"""
    source_frame.iloc[6:36, 18].fillna(source_frame.iloc[36, 18], inplace=True)
    source_frame.iloc[36:, 18].fillna(0.275, inplace=True)
    """Patch Series `Douglas P.H. -- Kendrick J.W. (Blended) Series` Multiplied by `Capital Structure Series`"""
    source_frame['nominal_patch'] = source_frame.iloc[:, 16]*source_frame.iloc[:, 18]
    """`Cobb C.W.,  Douglas P.H. -- FRB (Blended) Series` Patched with `Patch Series`"""
    source_frame['nominal_extended'] = source_frame.iloc[:, [17, 19]].mean(1)
    source_frame = source_frame[source_frame.columns[[20]]]
    source_frame.dropna(inplace=True)
    return source_frame
def cobbDouglasLaborExtension():
    """Manufacturing Laborers` Series Comparison
    semi_frameA: Cobb C.W.,  Douglas P.H. Labor Series
    semi_frameB: Census Bureau 1949,  D69
    semi_frameC: Census Bureau 1949,  J4
    semi_frameD: Census Bureau 1975,  D130
    semi_frameE: Census Bureau 1975,  P5
    semi_frameF: Census Bureau 1975,  P62
    semi_frameG: Bureau of Economic Analysis,  H4313C & J4313C & A4313C & N4313C
    semi_frameH: J.W. Kendrick,  Productivity Trends in the United States,  Table D-II,  `Persons Engaged` Column,  pp. 465--466
    semi_frameI: Yu.V. Kurenkov
    Bureau of Labor Statistics
    Federal Reserve Board"""
    import pandas as pd
    semi_frameA = fetchClassic('cobbdouglas.zip', 'CDT3S1') ## Average Number Employed (in thousands)
    semi_frameB = fetchCensus('census1949.zip', 'D0069', True)
    semi_frameC = fetchCensus('census1949.zip', 'J0004', True)
    semi_frameD = fetchCensus('census1975.zip', 'D0130', True)
    semi_frameE = fetchCensus('census1975.zip', 'P0005', True)
    semi_frameF = fetchCensus('census1975.zip', 'P0062', True)
    sub_frameA = fetchBEA('dataset USA BEA NipaDataA.txt', 'H4313C')
    sub_frameB = fetchBEA('dataset USA BEA NipaDataA.txt', 'J4313C')
    sub_frameC = fetchBEA('dataset USA BEA NipaDataA.txt', 'A4313C')
    sub_frameD = fetchBEA('dataset USA BEA NipaDataA.txt', 'N4313C')
    semi_frameG = pd.concat([sub_frameA, sub_frameB, sub_frameC, sub_frameD], axis = 1, sort = True)
    del sub_frameA, sub_frameB, sub_frameC, sub_frameD
    semi_frameG = semi_frameG.mean(1)
    semi_frameG = semi_frameG.to_frame(name = 'BEA')
    semi_frameH = fetchClassic('kendrick.zip', 'KTD02S02')
    semi_frameI = pd.read_csv('dataset USA Reference RU Kurenkov Yu.V..csv', usecols=[0, 2])
    semi_frameI = semi_frameI.set_index('Period')
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                           semi_frameF, semi_frameG, semi_frameH, semi_frameI], axis = 1, sort = True)
    result_frame['kendrick'] = result_frame.iloc[14, 0]*result_frame.iloc[:, 7].div(result_frame.iloc[14, 7])
    result_frame['labor'] = result_frame.iloc[:, [0, 1, 3, 6, 8, 9]].mean(1)
    result_frame = result_frame[result_frame.columns[[10]]]
    result_frame.dropna(inplace=True)
    result_frame = result_frame[2:]
    return result_frame
def cobbDouglasProductExtension():
    import pandas as pd
    base = [109, 149] ##1899,  1939
    """Bureau of the Census,  1949,  Page 179,  J13: National Bureau of Economic Research Index of Physical Output,  All Manufacturing Industries."""
    semi_frameA = fetchCensus('census1949.zip', 'J0013', True)
    """Bureau of the Census,  1949,  Page 179,  J14: Warren M. Persons,  Index of Physical Production of Manufacturing"""
    semi_frameB = fetchCensus('census1949.zip', 'J0014', True)
    """Bureau of the Census,  1975,  Page 667,  P17: Edwin Frickey Index of Manufacturing Production"""
    semi_frameC = fetchCensus('census1975.zip', 'P0017', True)
    """The Revised Index of Physical Production for All Manufacturing In the United States,  1899--1926"""
    semi_frameD = fetchClassic('douglas.zip', 'DT24AS01')
    """Federal Reserve,  AIPMASAIX"""
    semi_frameE = FRBIP()
    """Joseph H. Davis Production Index"""
    semi_frameF = pd.read_excel('dataset USA Davis J.H. ip-total.xls', skiprows=4)
    semi_frameF.columns = ['Period', 'davis_index']
    semi_frameF = semi_frameF.set_index('Period')
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, semi_frameF], axis = 1, sort = True)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].div(result_frame.iloc[base[0], 1]/100)
    result_frame.iloc[:, 5] = result_frame.iloc[:, 5].div(result_frame.iloc[base[0], 5]/100)
    result_frame['fused_classic'] = result_frame.iloc[:, [0, 1, 2, 3, 5]].mean(1)
    result_frame.iloc[:, 4] = result_frame.iloc[:, 4].div(result_frame.iloc[base[1], 4]/100)
    result_frame.iloc[:, 6] = result_frame.iloc[:, 6].div(result_frame.iloc[base[1], 6]/100)
    result_frame['fused'] = result_frame.iloc[:, [4, 6]].mean(1)
    result_frame = result_frame[result_frame.columns[[7]]]
    return result_frame
def datasetVersionC():
    """Data Fetch"""
    import pandas as pd
    """Data Fetch for Capital"""
    capital_frameA = cobbDouglasCapitalExtension()
    """Data Fetch for Capital Deflator"""
    capital_frameB = cobbDouglasCapitalDeflator()
    capital_frame = pd.concat([capital_frameA, capital_frameB], axis = 1, sort = True)
    capital_frame.dropna(inplace=True)
    capital_frame['capital_real'] = capital_frame.iloc[:, 0].div(capital_frame.iloc[:, 1])
    """Data Fetch for Labor"""
    labor_frame = cobbDouglasLaborExtension()
    """Data Fetch for Product"""
    product_frame = cobbDouglasProductExtension()
    result_frame = pd.concat([capital_frame.iloc[:, 2], labor_frame, product_frame], axis = 1, sort = True).dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame
def service(source_frame):
    """
    source_frame.iloc[:, 0]: Capital Series;
    source_frame.iloc[:, 1]: Labor Series;
    source_frame.iloc[:, 2]: Product Series
    """
    source_frame['labcap'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])                 ##Labor Capital Intensity
    source_frame['labprd'] = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1])                 ##Labor Productivity
    source_frame['labcap_inc'] = source_frame.iloc[:, 3].div(source_frame.iloc[:, 3].shift(1))    ##Labor Capital Intensity Increment
    source_frame['labprd_inc'] = source_frame.iloc[:, 4].div(source_frame.iloc[:, 4].shift(1))    ##Labor Productivity Increment
    source_frame = source_frame[source_frame.columns[[3, 4, 5, 6]]]
    return source_frame
def increment_plot(frame):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2, 1) ##fig, axs = plt.subplots()
    axs[0].plot(frame.iloc[:, 0], frame.iloc[:, 1], label = 'Description Here')
    axs[0].set_xlabel('Labor Capital Intensity')
    axs[0].set_ylabel('Labor Productivity')
    axs[0].set_title('Description')
    axs[0].legend()
    axs[0].grid(True)
    axs[1].plot(frame.iloc[:, 2], frame.iloc[:, 3], label = 'Description Here')
    axs[1].set_xlabel('Labor Capital Intensity Increment')
    axs[1].set_ylabel('Labor Productivity Increment')
    axs[1].set_title('Description')
    axs[1].grid(True)
    axs[1].legend()
    for i in range(3, len(frame), 5):
        axs[1].annotate(frame.index[i], (frame.iloc[i, 2], frame.iloc[i, 3]))
#    import os
#    os.chdir('C:\\Projects')
#    plt.tight_layout()
#    fig.set_size_inches(10., 25.)
#    fig.savefig('nameFigure1.pdf', format = 'pdf', dpi = 900)
    plt.show()
source_frame = service(datasetVersionC())
increment_plot(source_frame)