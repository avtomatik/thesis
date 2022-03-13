# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 21:17:48 2020

@author: Mastermind
"""
import pandas as pd
import matplotlib.pyplot as plt


def beaFetch(zpfl, wrkbk, wrksht, start, finish, line):
    """Data _frame Fetching from Bureau of Economic Analysis Zip Archives"""
    """
    zpfl: Name of Zip Archive, 
    wrkbk: Name of Excel File within Zip Archive, 
    wrksht: Name of Worksheet within Excel File within Zip Archive, 
    boundary: 4+<Period_Finish>-<Period_Start>, 
    line: Line"""
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
    """Selected Series by U.S. Bureau of the Census
    U.S. Bureau of the Census,  Historical Statistics of the United States,  1789--1945,  Washington,  D.C.,  1949.
    U.S. Bureau of the Census. Historical Statistics of the United States,  Colonial Times to 1970,  Bicentennial Edition. Washington,  D.C.,  1975."""
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


def FRBIP():
    """Indexed Manufacturing Series: FRB G17 IP,  AIPMA_SA_IX,  1919--2018"""
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


def FRBMS():
    """Indexed Money Stock Measures (H.6) Series:
    https://www.federalreserve.gov/datadownload/Download.aspx?rel = h6&series = 5398d8d1734b19f731aba3105eb36d47&filetype = csv&label = include&layout = seriescolumn&from = 01/01/1959&to = 12/31/2018"""
    import pandas as pd
    source_frame = pd.read_csv('dataset USA FRB_H6.csv', skiprows=5, usecols=range(2))
    source_frame.columns = source_frame.columns.to_series().replace({'[ .:;@_]':''}, regex = True)
    source_frame['Period'], source_frame['Mnth'] = source_frame['TimePeriod'].str.split('-').str
    source_frame = source_frame[source_frame.columns[[2, 1]]]
    source_frame = source_frame.groupby('Period').mean()
    source_frame.to_csv('temporary.txt')
    del source_frame
    result_frame = pd.read_csv('temporary.txt')
    import os
    os.unlink('temporary.txt')
    result_frame = result_frame.set_index('Period')
    return result_frame


def fetchBEA(source, string):
    """`dataset USA BEA NipaDataA.txt`: U.S. Bureau of Economic Analysis
    Archived: https://www.bea.gov/National/FAweb/Details/Index.html
    https://www.bea.gov//national/FA2004/DownSS2.asp,  Accessed May 26,  2018"""
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


def FRBCU():
    """Indexed Capacity Utilization Series: CAPUTL.B50001.A,  1967--2012
    CAPUTL.B50001.A Fetching"""
    import os
    import pandas as pd
    source_frame = pd.read_csv('dataset USA FRB_G17_All_Annual 2013-06-23.csv', skiprows=1, usecols=range(5, 100))
    source_frame = source_frame.T
    source_frame.to_csv('temporary.txt')
    del source_frame
    source_frame = pd.read_csv('temporary.txt', skiprows=1)
    os.unlink('temporary.txt')
    source_frame.columns = source_frame.columns.to_series().replace({'[ .:;@_]':''}, regex = True)
    result_frame = source_frame[['SeriesName', 'CAPUTLB50001A']]
    del source_frame
    result_frame = result_frame.dropna()
    result_frame = result_frame.reset_index(drop = True)
    result_frame.rename(columns = {'SeriesName':'Period'}, inplace=True)
    result_frame.iloc[:, 0] = result_frame.iloc[:, 0].astype(int)
    result_frame = result_frame.set_index('Period')
    return result_frame


def archivedBEALabor():
    import pandas as pd
    """Labor Series: H4313C0,  1929--1948"""
    semi_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section6ALL_Hist.xls', '60500A Ann', 1929, 1948, 14)
    """Labor Series: J4313C0,  1948--1969"""
    semi_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section6ALL_Hist.xls', '60500B Ann', 1948, 1969, 13)
    """Labor Series: J4313C0,  1969--1987"""
    semi_frameC = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section6all_xls.xls', '60500B Ann', 1969, 1987, 13)
    """Labor Series: A4313C0,  1987--2000"""
    semi_frameD = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section6all_xls.xls', '60500C Ann', 1987, 2000, 13)
    """Labor Series: N4313C0,  1998--2011"""
    semi_frameE = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section6all_xls.xls', '60500D Ann', 1998, 2011, 13)
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE], axis = 1, sort = True)
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE
    result_frame = result_frame.mean(1)
    result_frame = result_frame.to_frame(name = 'Labor')
    return result_frame


def archivedDataCombined():
    """Version: 02 December 2013"""
    import pandas as pd
    """Nominal Investment Series: A006RC1,  1929--1969"""
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1968, 7)
    """Nominal Investment Series: A006RC1,  1969--2012"""
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 7)
    semi_frameA = sub_frameA.append(sub_frameB)
    del sub_frameA, sub_frameB
    """Implicit Price Deflator Series: A006RD3,  1929--1969"""
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10109 Ann', 1929, 1969, 7)
    """Implicit Price Deflator Series: A006RD3,  1969--2012"""
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10109 Ann', 1969, 2012, 7)
    semi_frameB = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    """Gross private domestic investment -- Nonresidential: A008RC1,  1929--1969"""
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 9)
    """Gross private domestic investment -- Nonresidential: A008RC1,  1969--2012"""
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 9)
    semi_frameC = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    """Implicit Price Deflator -- Gross private domestic investment -- Nonresidential: A008RD3,  1929--1969"""
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10109 Ann', 1929, 1969, 9)
    """Implicit Price Deflator -- Gross private domestic investment -- Nonresidential: A008RD3,  1969--2012"""
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10109 Ann', 1969, 2012, 9)
    semi_frameD = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    """Nominal National income Series: A032RC1,  1929--1969"""
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10705 Ann', 1929, 1969, 16)
    """Nominal National income Series: A032RC1,  1969--2011"""
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10705 Ann', 1969, 2011, 16)
    semi_frameE = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    """Gross Domestic Product,  2005 = 100: B191RA3,  1929--1969"""
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10103 Ann', 1929, 1969, 1)
    """Gross Domestic Product,  2005 = 100: B191RA3,  1969--2012"""
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10103 Ann', 1969, 2012, 1)
    semi_frameF = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    """Nominal Nominal Gross Domestic Product Series: A191RC1,  1929--1969"""
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 1)
    """Nominal Nominal Gross Domestic Product Series: A191RC1,  1969--2012"""
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 1)
    semi_frameG = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    """Real Gross Domestic Product Series,  2005 = 100: A191RX1,  1929--1969"""
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10106 Ann', 1929, 1969, 1)
    """Real Gross Domestic Product Series,  2005 = 100: A191RX1,  1969--2012"""
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10106 Ann', 1969, 2012, 1)
    semi_frameH = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB    
    """Labor Series"""
    semi_frameI = archivedBEALabor()
    """Gross Domestic Investment,  W170RC1,  1929--1969"""
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section5ALL_Hist.xls', '50100 Ann', 1929, 1968, 22)
    """Gross Domestic Investment,  W170RC1,  1969--2012"""
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section5all_xls.xls', '50100 Ann', 1969, 2012, 22)
    semi_frameJ = sub_frameA.append(sub_frameB)
    del sub_frameA, sub_frameB
    """Gross Domestic Investment,  W170RX1,  1967--1969"""
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section5ALL_Hist.xls', '50206 Ann', 1967, 1969, 1)
    """Gross Domestic Investment,  W170RX1,  1969--2011"""
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section5all_xls.xls', '50206 Ann', 1969, 2011, 1)
    semi_frameK = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    """Fixed Assets Series: K160491,  1951--1969"""
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section5ALL_Hist.xls', '50900 Ann', 1951, 1969, 49)
    """Fixed Assets Series: K160491,  1969--2011"""
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section5all_xls.xls', '50900 Ann', 1969, 2011, 49)
    semi_frameL = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    semi_frameM = fetchBEA('beanipa20131202sfat.zip', 'i3ptotl1es00')
    semi_frameN = fetchBEA('beanipa20131202sfat.zip', 'icptotl1es00')
    semi_frameO = fetchBEA('beanipa20131202sfat.zip', 'k1ptotl1es00')
    semi_frameP = fetchBEA('beanipa20131202sfat.zip', 'k3ptotl1es00')
    semi_frameQ = fetchBEA('beanipa20131202sfat.zip', 'kcptotl1es00')
    semi_frameR = pd.read_csv('dataset USA 0022M1.txt')
    semi_frameR.columns = semi_frameR.columns.str.title()
    semi_frameR = semi_frameR.set_index('Period')
    semi_frameS = fetchCensus('census1975.zip', 'X0414', True)
    semi_frameT = FRBMS()
    semi_frameU = pd.read_csv('dataset USA 0025PR.txt')
    semi_frameU.columns = semi_frameU.columns.str.title()
    semi_frameU = semi_frameU.set_index('Period')
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                           semi_frameF, semi_frameG, semi_frameH, semi_frameI, semi_frameJ, \
                           semi_frameK, semi_frameL, semi_frameM, semi_frameN, semi_frameO, \
                           semi_frameP, semi_frameQ, semi_frameR, semi_frameS, semi_frameT, \
                           semi_frameU], axis = 1, sort = True)
    return result_frame


def dataCombined():
    """Most Up-To-Date Version"""
    """US BEA Fixed Assets Series Tests"""
    """Item 1.1"""
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    """Item 1.2"""
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    """Item 1.3"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    """Item 1.4: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    """Item 1.5"""
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    """Item 2.1: Don't Use,  Use Item 1.1 Instead"""
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    """Item 2.2: Don't Use,  Use Item 1.2 Instead"""
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    """Item 2.3: Don't Use,  Use Item 1.3 Instead"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    """Item 2.4"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    """Item 2.5: Don't Use,  Use Item 1.5 Instead"""
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    """Item 3.1: Don't Use,  Use Item 1.1 Instead"""
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    """Item 3.2: Don't Use,  Use Item 1.2 Instead"""
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    """Item 3.3: Don't Use,  Use Item 1.3 Instead"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    """Item 3.4: Don't Use,  Use Item 2.4 Instead"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    """Item 3.5: Don't Use,  Use Item 1.5 Instead"""
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    """Item 4.1: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    """Item 4.2: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    """Item 4.3: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    """Item 4.4: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    """Item 4.5: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    """Item 5.1: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    """Item 5.2: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    """Item 5.3: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    """Item 5.4: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    """Item 5.5: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    """Item 6.1: Don't Use,  Use Item 1.1 Instead"""
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    """Item 6.2: Don't Use,  Use Item 1.2 Instead"""
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    """Item 6.3: Don't Use,  Use Item 1.3 Instead"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    """Item 6.4: Don't Use,  Use Item 2.4 Instead"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    """Item 6.5: Don't Use,  Use Item 1.5 Instead"""
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    """Item 7.1: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    """Item 7.2: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    """Item 7.3: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    """Item 7.4: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    """Item 7.5: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    """Item 8.1: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    """Item 8.2: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    """Item 8.3: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    """Item 8.4: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    """Item 8.5: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    """Item 9.1: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    """Item 9.2: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    """Item 9.3: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    """Item 9.4: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    """Item 9.5: Don't Use"""
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    import pandas as pd
    semi_frameA = fetchBEA('dataset USA BEA NipaDataA.txt', 'A006RC')
    semi_frameB = fetchBEA('dataset USA BEA NipaDataA.txt', 'A006RD')
    semi_frameC = fetchBEA('dataset USA BEA NipaDataA.txt', 'A008RC')
    semi_frameD = fetchBEA('dataset USA BEA NipaDataA.txt', 'A008RD')
    semi_frameE = fetchBEA('dataset USA BEA NipaDataA.txt', 'A032RC')
    semi_frameF = fetchBEA('dataset USA BEA NipaDataA.txt', 'A191RA')
    semi_frameG = fetchBEA('dataset USA BEA NipaDataA.txt', 'A191RC')
    semi_frameH = fetchBEA('dataset USA BEA NipaDataA.txt', 'A191RX')
    sub_frameA = fetchBEA('dataset USA BEA NipaDataA.txt', 'H4313C')
    sub_frameB = fetchBEA('dataset USA BEA NipaDataA.txt', 'J4313C')
    sub_frameC = fetchBEA('dataset USA BEA NipaDataA.txt', 'A4313C')
    sub_frameD = fetchBEA('dataset USA BEA NipaDataA.txt', 'N4313C')
    semi_frameI = pd.concat([sub_frameA, sub_frameB, sub_frameC, sub_frameD], axis = 1, sort = True)
    del sub_frameA, sub_frameB, sub_frameC, sub_frameD
    semi_frameI = semi_frameI.mean(1)
    semi_frameI = semi_frameI.to_frame(name = 'Labor')
    semi_frameJ = fetchBEA('dataset USA BEA NipaDataA.txt', 'W170RC')
    semi_frameK = fetchBEA('dataset USA BEA NipaDataA.txt', 'W170RX')
    """Fixed Assets Series: K100701,  1951--1969"""
    sub_frameA = beaFetch(None, 'dataset USA BEA Release 2015-03-02 Section5ALL_Hist.xls', '51000 Ann', 1951, 1969, 70)
    """Fixed Assets Series: K100701,  1969--2013"""
    sub_frameB = beaFetch(None, 'dataset USA BEA Release 2015-03-02 Section5all_xls.xls', '51000 Ann', 1969, 2013, 70)
    semi_frameL = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    """Investment in Fixed Assets,  Private,  i3ptotl1es000,  1901--2016"""
    semi_frameM = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section1ALL_xls.xls', '105 Ann', 1901, 2016, 3)
    """Chain-Type Quantity Index for Investment in Fixed Assets,  Private,  icptotl1es000,  1901--2016"""    
    semi_frameN = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section1ALL_xls.xls', '106 Ann', 1901, 2016, 3)
    """Current-Cost Net Stock of Fixed Assets,  Private,  k1ptotl1es000,  1925--2016"""    
    semi_frameO = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section1ALL_xls.xls', '101 Ann', 1925, 2016, 3)
    """Historical-Cost Net Stock of Private Fixed Assets,  Private Fixed Assets,  k3ptotl1es000,  1925--2016"""
    semi_frameP = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section2ALL_xls.xls', '203 Ann', 1925, 2016, 1)
    """Chain-Type Quantity Indexes for Net Stock of Fixed Assets,  Private,  kcptotl1es000,  1925--2016"""
    semi_frameQ = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section1ALL_xls.xls', '102 Ann', 1925, 2016, 3)
    semi_frameR = FRBMS()
    semi_frameS = FRBMS()
    semi_frameT = FRBMS()
    semi_frameU = pd.read_csv('dataset USA 0025PR.txt')
    semi_frameU.columns = semi_frameU.columns.str.title()
    semi_frameU = semi_frameU.set_index('Period')
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                           semi_frameF, semi_frameG, semi_frameH, semi_frameI, semi_frameJ, \
                           semi_frameK, semi_frameL, semi_frameM, semi_frameN, semi_frameO, \
                           semi_frameP, semi_frameQ, semi_frameR, semi_frameS, semi_frameT, \
                           semi_frameU], axis = 1, sort = True)
    return result_frame


def indexswitch(source_frame):
    import os
    import pandas as pd
    source_frame.to_csv('temporary.txt')
    del source_frame
    result_frame = pd.read_csv('temporary.txt')
    os.unlink('temporary.txt')
    return result_frame


def preprocessingA(source_frame):
    source_frame = source_frame[source_frame.columns[[0, 4, 6, 7]]]
    source_frame = source_frame.dropna()
    source_frame = source_frame.div(source_frame.iloc[0, :])
    source_frame = indexswitch(source_frame)
    return source_frame


def preprocessingB(source_frame):
    source_frame = source_frame[source_frame.columns[[0, 6, 7, 20]]]
    source_frame = source_frame.dropna()
    source_frame = indexswitch(source_frame)
    return source_frame


def preprocessingC(source_frame):
    import pandas as pd
    source_frameProduction = source_frame[source_frame.columns[[0, 6, 7]]]
    source_frameProduction = source_frameProduction.dropna()
    source_frameProduction = source_frameProduction.div(source_frameProduction.iloc[0, :])
    source_frameMoney = source_frame.iloc[:, 18:20]    
    source_frameMoney = source_frameMoney.mean(1)
    source_frameMoney = pd.Data_frame(source_frameMoney, columns = ['M1']) ##Convert Series to Dataframe
    source_frameMoney = source_frameMoney.dropna()
    source_frameMoney = source_frameMoney.div(source_frameMoney.iloc[0, :])
    result_frame = pd.concat([source_frameProduction, source_frameMoney], axis = 1)
    result_frame = result_frame.dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    result_frame = indexswitch(result_frame)
    return result_frame


def preprocessingD(source_frame):
    source_frame = source_frame[source_frame.columns[[0, 1, 2, 3, 7]]]
    source_frame = source_frame.dropna()
    source_frame = indexswitch(source_frame)
    return source_frame


def dataFetchPlottingA(source_frame):
    """
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Gross Domestic Investment, 
    source_frame.iloc[:, 2]: National Income, 
    source_frame.iloc[:, 3]: Nominal Gross Domestic Product, 
    source_frame.iloc[:, 4]: Real Gross Domestic Product
    """
    """`Real` Investment"""
    source_frame['inv'] = source_frame.iloc[:, 1]*source_frame.iloc[:, 4].div(source_frame.iloc[:, 3])
    """`Real` Production"""
    source_frame['prd'] = source_frame.iloc[:, 2]*source_frame.iloc[:, 4].div(source_frame.iloc[:, 3])
    import matplotlib.pyplot as plt
    plt.figure()
    plt.title('Gross Private Domestic Investment & National Income,  %d$-$%d' %(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame.iloc[:, 0])-1, 0]))
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 5], label = 'Gross Private Domestic Investment')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 6], label = 'National Income')
    plt.xlabel('Period')
    plt.ylabel('Index')
    source_frame.iloc[:, 0] = (source_frame.iloc[:, 0].shift(-1)+source_frame.iloc[:, 0])/2
    X = (source_frame.iloc[:, 5].shift(-1)+source_frame.iloc[:, 5])/2
    Y = (source_frame.iloc[:, 6].shift(-1)+source_frame.iloc[:, 6])/2
    plt.plot(source_frame.iloc[:, 0], X, '--', source_frame.iloc[:, 0], Y, '--')
    plt.grid()
    plt.legend()
    plt.show()


def dataFetchPlottingB(source_frame):
    """
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Gross Domestic Investment, 
    source_frame.iloc[:, 2]: Nominal Gross Domestic Product, 
    source_frame.iloc[:, 3]: Real Gross Domestic Product, 
    source_frame.iloc[:, 4]: Prime Rate
    """
    """`Real` Investment"""
    source_frame['inv'] = source_frame.iloc[:, 1]*source_frame.iloc[:, 3].div(source_frame.iloc[:, 2])
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(source_frame.iloc[:, 4], source_frame.iloc[:, 5])
    plt.title('Gross Private Domestic Investment,  A006RC,  %d$-$%d' %(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame.iloc[:, 0])-1, 0]))
    plt.xlabel('Percentage')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.show()


def dataFetchPlottingC(source_frame):
    """
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Gross Domestic Investment, 
    source_frame.iloc[:, 2]: Nominal Gross Domestic Product, 
    source_frame.iloc[:, 3]: Real Gross Domestic Product, 
    source_frame.iloc[:, 4]: M1
    """
    """`Real` Investment"""
    source_frame['inv'] = source_frame.iloc[:, 1]*source_frame.iloc[:, 3].div(source_frame.iloc[:, 2])
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 3], label = 'Real Gross Domestic Product')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 5], label = '`Real` Gross Domestic Investment')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 4], label = 'Money Supply')
    plt.title('Indexes,  %d$-$%d' %(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame.iloc[:, 0])-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.legend()
    plt.grid(True)
    plt.show()


def dataFetchPlottingD(source_frame):
    """
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Gross Domestic Investment, 
    source_frame.iloc[:, 2]: Gross Domestic Investment Price Index, 
    source_frame.iloc[:, 3]: Fixed Investment, 
    source_frame.iloc[:, 4]: Fixed Investment Price Index, 
    source_frame.iloc[:, 5]: Real Gross Domestic Product
    """
    i = len(source_frame.iloc[:, 0])-1
    while abs(source_frame.iloc[i, 2]-100)>0.1:
        i- = 1
        base = i ##Basic Year
    """Real Investment,  Billions"""
    source_frame['inv'] = source_frame.iloc[base, 1]*source_frame.iloc[:, 2].div(100*1000)
    """Real Fixed Investment,  Billions"""
    source_frame['fnv'] = source_frame.iloc[base, 3]*source_frame.iloc[:, 4].div(100*1000)
    source_frame.iloc[:, 5] = source_frame.iloc[:, 5].div(1000)
    import matplotlib.pyplot as plt
    plt.figure(1)
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 6], label = 'Real Gross Private Domestic Investment $GPDI$')
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 7], color = 'red', label = 'Real Gross Private Fixed Investment,  Nonresidential $GPFI(n)$')
    plt.title('Real Indexes,  %d = 100,  %d$-$%d' %(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[len(source_frame.iloc[:, 0])-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars')
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 5])
    plt.title('Real Gross Domestic Product $GDP$,  %d = 100,  %d$-$%d' %(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[len(source_frame.iloc[:, 0])-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.figure(3)
    plt.plot(source_frame.iloc[:, 6], source_frame.iloc[:, 5])
    plt.title('$GPDI$ & $GPFI(n)$,  %d = 100,  %d$-$%d' %(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[len(source_frame.iloc[:, 0])-1, 0]))
    plt.xlabel('Billions of Dollars')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.figure(4)
    plt.plot(source_frame.iloc[:, 7], source_frame.iloc[:, 5])
    plt.title('$GPFI(n)$ & $GDP$,  %d = 100,  %d$-$%d' %(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[len(source_frame.iloc[:, 0])-1, 0]))
    plt.xlabel('Billions of Dollars')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.show()


def preprocessingE(source_frame):
    """Works on Result of `archivedDataCombined`"""
    """`Real` Investment"""
    source_frame['inv'] = source_frame.iloc[:, 0]*source_frame.iloc[:, 7].div(source_frame.iloc[:, 6])
    """`Real` Capital"""
    source_frame['cap'] = source_frame.iloc[:, 11]*source_frame.iloc[:, 7].div(source_frame.iloc[:, 6])
    """Nominal DataSet"""
    nominal_frame = source_frame[source_frame.columns[[0, 6, 11]]].dropna()
    """`Real` DataSet"""
    real_frame = source_frame[source_frame.columns[[21, 7, 22]]].dropna()
    return nominal_frame, real_frame


def plottingE(source_frame):
    """
    source_frame.iloc[:, 0]: Investment, 
    source_frame.iloc[:, 1]: Production, 
    source_frame.iloc[:, 2]: Capital
    """
    """Investment to Production Ratio"""
    source_frame['S'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])
    """Fixed Assets Turnover Ratio"""
    source_frame['L'] = source_frame.iloc[:, 1].div(source_frame.iloc[:, 2])
    import scipy as sp
    QS = sp.polyfit(source_frame.iloc[:, 0], source_frame.iloc[:, 1], 1)
    QL = sp.polyfit(source_frame.iloc[:, 1], source_frame.iloc[:, 2], 1)
    source_frame['RS'] = QS[1]+QS[0]*source_frame.iloc[:, 0]
    source_frame['RL'] = QL[1]+QL[0]*source_frame.iloc[:, 2]
    import matplotlib.pyplot as plt
    plt.figure()
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 1])
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 5])
    plt.title('Investment to Production Ratio,  %d$-$%d' %(source_frame.index[0], source_frame.index[len(source_frame)-1]))
    plt.xlabel('Investment,  Billions of Dollars')
    plt.ylabel('Gross Domestic Product,  Billions of Dollars')
    plt.grid(True)
    plt.legend(['$P(I)$', '$\\hat P(I) = %.4f+%.4f I$' %(QS[1], QS[0])])
    print(source_frame.iloc[:, 3].describe())
    print(QS)
    print(source_frame.iloc[:, 4].describe())
    print(QL)    
    plt.show()


def preprocessingF(testing_frame):
    """testing_frame: Test _frame"""
    import pandas as pd    
    """Control _frame"""
    control_frame = pd.read_csv('dataset USA Reference RU Kurenkov Yu.V..csv')
    control_frame = control_frame.set_index('Period')    
    """Data Fetch"""
    """Production"""
    semi_frameAA = control_frame[control_frame.columns[[0]]]
    semi_frameAB = testing_frame[testing_frame.columns[[7]]].dropna()
    semi_frameAC = FRBIP()
    result_frameA = pd.concat([semi_frameAA, semi_frameAB, semi_frameAC], axis = 1, sort = True)
    result_frameA = result_frameA.div(result_frameA.iloc[31, :]/100)
    """Labor"""
    semi_frameBA = control_frame[control_frame.columns[[1]]]
    semi_frameBB = testing_frame[testing_frame.columns[[8]]].dropna()
    result_frameB = pd.concat([semi_frameBA, semi_frameBB], axis = 1, sort = True)
    """Capital"""
    semi_frameCA = control_frame[control_frame.columns[[2]]]
    semi_frameCB = testing_frame[testing_frame.columns[[11]]].dropna()
    result_frameC = pd.concat([semi_frameCA, semi_frameCB], axis = 1, sort = True)
    result_frameC = result_frameC.div(result_frameC.iloc[1, :]/100)
    """Capacity Utilization"""
    semi_frameDA = control_frame[control_frame.columns[[3]]]
    semi_frameDB = FRBCU()
    result_frameD = pd.concat([semi_frameDA, semi_frameDB], axis = 1, sort = True)
    return result_frameA, result_frameB, result_frameC, result_frameD


def plottingF(source_frameA, source_frameB, source_frameC, source_frameD):
    """
    source_frameA: Production _frame, 
    source_frameB: Labor _frame, 
    source_frameC: Capital _frame, 
    source_frameD: Capacity Utilization _frame, 
    baseA = 31, 
    baseC = 1"""
    """Plotting"""
    fig, axs = plt.subplots(4, 1)
    axs[0].plot(source_frameA.index, source_frameA.iloc[:, 0], label = 'Kurenkov Data,  %d = 100' %(source_frameA.index[31]))
    axs[0].plot(source_frameA.index, source_frameA.iloc[:, 1], label = 'BEA Data,  %d = 100' %(source_frameA.index[31]))
    axs[0].plot(source_frameA.index, source_frameA.iloc[:, 2], label = 'FRB Data,  %d = 100' %(source_frameA.index[31]))
    axs[0].set_title('Production')
    axs[0].set_xlabel('Period')
    axs[0].set_ylabel('Percentage')
    axs[0].legend()
    axs[0].grid(True)
    axs[1].plot(source_frameB.index, source_frameB.iloc[:, 0], label = 'Kurenkov Data')
    axs[1].plot(source_frameB.index, source_frameB.iloc[:, 1], label = 'BEA Data')
    axs[1].set_title('Labor')
    axs[1].set_xlabel('Period')
    axs[1].set_ylabel('Thousands of Persons')
    axs[1].legend()
    axs[1].grid(True)
    """Revised Capital"""
    axs[2].plot(source_frameC.index, source_frameC.iloc[:, 0], label = 'Kurenkov Data,  %d = 100' %(source_frameC.index[1]))
    axs[2].plot(source_frameC.index, source_frameC.iloc[:, 1], label = 'BEA Data,  %d = 100' %(source_frameC.index[1]))
    axs[2].set_title('Capital')
    axs[2].set_xlabel('Period')
    axs[2].set_ylabel('Percentage')
    axs[2].legend()
    axs[2].grid(True)
    axs[3].plot(source_frameD.index, source_frameD.iloc[:, 0], label = 'Kurenkov Data')
    axs[3].plot(source_frameD.index, source_frameD.iloc[:, 1], label = 'FRB Data')
    axs[3].set_title('Capacity Utilization')
    axs[3].set_xlabel('Period')
    axs[3].set_ylabel('Percentage')
    axs[3].legend()
    axs[3].grid(True)
    fig.set_size_inches(10., 20.)
    ##fig.savefig('view.pdf', format = 'pdf', dpi = 900)


source_frameA = archivedDataCombined()
source_frameB = dataCombined()
"""Project: Initial Version Dated: 05 October 2012"""
result_frameAB = preprocessingA(source_frameA)
result_frameAC = preprocessingA(source_frameB)
dataFetchPlottingA(result_frameAB)
dataFetchPlottingA(result_frameAC)
"""Project: Initial Version Dated: 23 November 2012"""
result_frameBB = preprocessingB(source_frameA)
result_frameBC = preprocessingB(source_frameB)
dataFetchPlottingB(result_frameBB)
dataFetchPlottingB(result_frameBC)
"""Project: Initial Version Dated: 16 June 2013"""
result_frameCB = preprocessingC(source_frameA)
result_frameCC = preprocessingC(source_frameB)
dataFetchPlottingC(result_frameCB)
dataFetchPlottingC(result_frameCC)
"""Project: Initial Version Dated: 15 June 2015"""
result_frameD = preprocessingD(source_frameB)
dataFetchPlottingD(result_frameD)
"""Project: Initial Version Dated: 17 February 2013"""
result_frameEA, result_frameEB = preprocessingE(source_frameA)
plottingE(result_frameEA)
plottingE(result_frameEB)
"""Project: BEA Data Compared with Kurenkov Yu.V. Data"""
result_frameFA, result_frameFB, result_frameFC, result_frameFD = preprocessingF(source_frameA)
plottingF(result_frameFA, result_frameFB, result_frameFC, result_frameFD)