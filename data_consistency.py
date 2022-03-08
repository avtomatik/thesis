# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 20:39:06 2020

@author: Mastermind
"""

def beaFetch(zpfl, wrkbk, wrksht, start, finish, line):
    """Data _frame Fetching from Bureau of Economic Analysis Zip Archives"""
    """
    zpfl: Name of Zip Archive, 
    wrkbk: Name of Excel File within Zip Archive, 
    wrksht: Name of Worksheet within Excel File within Zip Archive, 
    boundary: 4+<Period_Finish>-<Period_Start>, 
    line: Line"""
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
def fetchCANSIMQ(source, vector, index):
    '''Data _frame Fetching from Quarterly Data within CANSIM Zip Archives
    Should Be [x 7 columns]
    index == True -- indexed by `Period`;
    index == False -- not indexed by `Period`'''
    source_frame = pd.read_csv('dataset CAN {}-eng.zip'.format(source))
    source_frame = source_frame[source_frame.Vector == vector]
    if source == '02820011':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '02820012':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '03790031':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '03800068':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    else:
        source_frame = source_frame[source_frame.columns[[0, 6]]] ##Should Be [x 7 columns]
    source_frame.rename(columns = {'Value':vector}, inplace=True)
    source_frame['Period'], source_frame['Q'] = source_frame.iloc[:, 0].str.split('/').str
    source_frame = source_frame[source_frame.columns[[2, 1]]]
    source_frame.iloc[:, 0] = source_frame.iloc[:, 0].astype(int)
    source_frame.iloc[:, 1] = pd.to_numeric(source_frame.iloc[:, 1])
    if (source == '03800084' and vector == 'v62306938'):
        source_frame = source_frame.groupby('Period').sum()
    elif (source == '03790031' and vector == 'v65201536'):
        source_frame = source_frame.groupby('Period').mean()
    elif (source == '03790031' and vector == 'v65201809'):
        source_frame = source_frame.groupby('Period').sum()
    else:
        source_frame = source_frame.groupby('Period').mean()
    if index:
        return source_frame
    else:
        source_frame.to_csv('temporary.txt')
        del source_frame
        result_frame = pd.read_csv('temporary.txt')
        os.unlink('temporary.txt')
        return result_frame
def fetchCANSIM(source, vector, index):
    '''Data _frame Fetching from CANSIM Zip Archives
    Should Be [x 7 columns]
    index == True -- indexed by `Period`;
    index == False -- not indexed by `Period`'''
    source_frame = pd.read_csv('dataset CAN {}-eng.zip'.format(source))
    source_frame = source_frame[source_frame.Vector == vector]
    if source == '03800106':
        source_frame = source_frame[source_frame.columns[[0, 5]]]
    elif source == '03800566':
        source_frame = source_frame[source_frame.columns[[0, 5]]]
    elif source == '02820011':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '02820012':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '03790031':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '03800068':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    else:
        source_frame = source_frame[source_frame.columns[[0, 6]]] ##Should Be [x 7 columns]
    source_frame.rename(columns = {'Ref_Date':'Period', 'Value':vector}, inplace=True)
    source_frame.iloc[:, 1] = pd.to_numeric(source_frame.iloc[:, 1])
    source_frame.to_csv('dataset CAN {} {}.csv'.format(source, vector), index = False)
    if index:
        source_frame = source_frame.set_index('Period')
        os.unlink('dataset CAN {} {}.csv'.format(source, vector))
        return source_frame
    else:
        del source_frame
        result_frame = pd.read_csv('dataset CAN {} {}.csv'.format(source, vector))
        os.unlink('dataset CAN {} {}.csv'.format(source, vector))
        return result_frame
def fetchCANSIMGroupA(source, row):
    source_frame = pd.read_csv('dataset CAN cansim{}.csv'.format(source), skiprows=row)
    if source == '7931814471809016759':
        source_frame.columns = source_frame.columns.to_series().replace({'[.:;@_]':''}, regex = True)
        source_frame['Q1 2014'] = source_frame['Q1 2014'].str.replace(';', '')
    else:
        pass
    source_frame = source_frame.T
    source_frame.to_csv('temporary.txt')
    del source_frame
    source_frame = pd.read_csv('temporary.txt', skiprows=1)
    os.unlink('temporary.txt')
    source_frame['qrtr'], source_frame['Period'] = source_frame.iloc[:, 0].str.split(' ').str
    source_frame = source_frame.groupby('Period').mean()
    return source_frame
def fetchCANSIMGroupB(source, row):
    source_frame = pd.read_csv('dataset CAN cansim{}.csv'.format(source), skiprows=row)
    source_frame['mnth'], source_frame['Period'] = source_frame.iloc[:, 0].str.split('-').str
    result_frame = source_frame.groupby('Period').mean()
    del source_frame
    return result_frame
def BLSLNU(source):
    '''LNU04000000: Bureau of Labor Statistics Unemployment Rate'''
    string = 'LNU04000000'
    source_frame = pd.read_csv(source, sep = '\t', low_memory = False)
    source_frame = source_frame[source_frame.iloc[:, 0].str.contains(string)]
    source_frame = source_frame[source_frame.iloc[:, 2] == 'M13']
    result_frame = source_frame[source_frame.columns[[1, 3]]]
    result_frame.rename(columns = {'year':'period'}, inplace=True)
    result_frame.columns = result_frame.columns.str.title()
    result_frame.rename(columns = {'Value':string}, inplace=True)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].astype(float)
    return result_frame
def BLSPCUOMFG(source):
    '''PCUOMFG--OMFG--: Bureau of Labor Statistics Producer Price Index Manufacturing'''
    string = 'PCUOMFG--OMFG--'
    source_frame = pd.read_csv(source, sep = '\t', low_memory = False)
    source_frame = source_frame[source_frame.iloc[:, 0].str.contains(string)]
    source_frame = source_frame[source_frame.iloc[:, 2] == 'M13']
    result_frame = source_frame[source_frame.columns[[1, 3]]]
    result_frame.rename(columns = {'year':'period'}, inplace=True)
    result_frame.columns = result_frame.columns.str.title()
    result_frame.rename(columns = {'Value':string}, inplace=True)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].astype(float)
    return result_frame
def archivedCombinedCapitalTest():
    '''Data Test'''
    '''Nominal Investment Series: A006RC1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 7)
    '''Nominal Gross Domestic Product Series: A191RC1,  1929--1969'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 1)
    control_frame = pd.concat([sub_frameA, sub_frameB], axis = 1, sort = True)
    del sub_frameA, sub_frameB
    '''Nominal Investment Series: A006RC1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 7)
    '''Nominal Gross Domestic Product Series: A191RC1,  1929--1969'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 1)
    test_frame = pd.concat([sub_frameA, sub_frameB], axis = 1, sort = True)
    del sub_frameA, sub_frameB
    if control_frame.equals(test_frame):
        print('Series `A006RC1` & `A191RC1` @ Worksheet `10105 Ann` Equals Series `A006RC1` & `A191RC1` @ Worksheet `10505 Ann` for Period 1929--1969')
    else:
        print('Data Varies from Worksheet `10105 Ann` to Worksheet `10505 Ann`')
    del control_frame, test_frame
    '''Nominal Investment Series: A006RC1,  1969--2012'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 7)
    '''Nominal Gross Domestic Product Series: A191RC1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 1)
    control_frame = pd.concat([sub_frameA, sub_frameB], axis = 1, sort = True)
    del sub_frameA, sub_frameB
    '''Nominal Investment Series: A006RC1,  1969--2012'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 7)
    '''Nominal Gross Domestic Product Series: A191RC1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 1)
    test_frame = pd.concat([sub_frameA, sub_frameB], axis = 1, sort = True)
    del sub_frameA, sub_frameB
    if control_frame.equals(test_frame):
        print('Series `A006RC1` & `A191RC1` @ Worksheet `10105 Ann` Equals Series `A006RC1` & `A191RC1` @ Worksheet `10505 Ann` for Period 1969--2012')
    else:
        print('Data Varies from Worksheet `10105 Ann` to Worksheet `10505 Ann`')
    del control_frame, test_frame
def fetchBEA(source, string):
    '''`dataset USA BEA NipaDataA.txt`: U.S. Bureau of Economic Analysis
    Archived: https://www.bea.gov/National/FAweb/Details/Index.html
    https://www.bea.gov//national/FA2004/DownSS2.asp,  Accessed May 26,  2018'''
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
    os.unlink('temporary.txt')
    result_frame = result_frame.set_index('Period')
    if source == 'beanipa20170823sfat.zip':
        result_frame = result_frame.round(3)
    else:
        pass
    result_frame = result_frame.drop_duplicates()
    return result_frame
def lookup(source_frame):
    for i in range(len(source_frame.columns)):
        print(source_frame.columns[i])
        series = source_frame.iloc[:, i].sort_values().unique()
        print(series)
        del series
def retrieval(string):
    source_frame = pd.read_csv('beanipa20150501.zip')
    source_frame = source_frame[source_frame.iloc[:, 0].str.contains('Table 3.17. Selected Government Current and Capital Expenditures by Function')]
    source_frame = source_frame[source_frame.iloc[:, 7].str.contains(string)]
    lookup(source_frame)
def testProcedure(codes):
    semi_frameA = fetchBEA('beanipa20150501.zip', codes[0])
    semi_frameB = fetchBEA('beanipa20150501.zip', codes[1])
    semi_frameC = fetchBEA('beanipa20150501.zip', codes[2])
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC], axis = 1, sort = True)
    del semi_frameA, semi_frameB, semi_frameC
    result_frame['test'] = result_frame.iloc[:, 0]-result_frame.iloc[:, 1]-result_frame.iloc[:, 2]
    result_frame.iloc[:, 3].plot(grid = True)
def fetchbeasfat(string):
    """Retrieve Historical Manufacturing Series from BEA SFAT CSV File"""
    source_frame = pd.read_csv('beanipa20170823sfat.zip', low_memory = False)
    source_frame = source_frame[source_frame.iloc[:, 0].str.contains('Historical')]
    source_frame = source_frame[source_frame.iloc[:, 6].str.contains('Manufacturing')]
    source_frame = source_frame[source_frame.iloc[:, 8] == string]
    tables = source_frame.iloc[:, 0].unique()
    tables = pd.Series(tables)
    if len(tables) == 1:
        result_frame = source_frame[source_frame.iloc[:, 0] == tables[0]]
        result_frame = result_frame[result_frame.columns[[9, 10]]]
        result_frame.columns = result_frame.columns.str.title()
        result_frame.rename(columns = {'Value':string}, inplace=True)
        result_frame = result_frame.reset_index(drop = True)
        result_frame = result_frame.set_index('Period')
    elif len(tables)> = 2:
        i = 0
        for table in tables:
            current_frame = source_frame[source_frame.iloc[:, 0] == table]
            current_frame = current_frame[current_frame.columns[[9, 10]]]
            current_frame.columns = current_frame.columns.str.title()
            current_frame.rename(columns = {'Value':string}, inplace=True)            
            current_frame = current_frame.reset_index(drop = True)
            current_frame = current_frame.set_index('Period')
            if i == 0:
                result_frame = current_frame
            elif i> = 1:
                result_frame = pd.concat([result_frame, current_frame], axis = 1, sort = True)
            del current_frame
            i+ = 1
    return result_frame
def subTestA(source_frame):
    source_frame['delta_sm'] = source_frame.iloc[:, 0]-source_frame.iloc[:, 3]-source_frame.iloc[:, 4]-source_frame.iloc[:, 5]
    source_frame.dropna(inplace=True)
    from pandas.plotting import autocorrelation_plot
    autocorrelation_plot(source_frame.iloc[:, 7])
def subTestB(source_frame):
#    source_frame['delta_eq'] = source_frame.iloc[:, 0]-source_frame.iloc[:, 6]
    source_frame['delta_eq'] = 2*(source_frame.iloc[:, 0]-source_frame.iloc[:, 6]).div(source_frame.iloc[:, 0]+source_frame.iloc[:, 6])
    source_frame.dropna(inplace=True)
    source_frame.iloc[:, 7].plot(grid = True)
def fetchbeasfatSeries():    
    """Earlier Version of `k3n31gd1es000`"""
    control_frame = pd.read_csv('beanipaUnknownsfatk3n31gd1es000.zip')
    controlHeader = control_frame.iloc[:, 8].unique().tolist()[0]
    control_frame = control_frame[control_frame.columns[[9, 10]]]
    control_frame.columns = control_frame.columns.str.title()
    control_frame.rename(columns = {'Value':controlHeader}, inplace=True)
    control_frame = control_frame.reset_index(drop = True)
    control_frame = control_frame.set_index('Period')
    semi_frameA = fetchbeasfat('k3n31gd1es000')
    semi_frameB = fetchbeasfat('k3n31gd1eq000')
    semi_frameC = fetchbeasfat('k3n31gd1ip000')
    semi_frameD = fetchbeasfat('k3n31gd1st000')
    test_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD], axis = 1, sort = True)
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD
    result_frame = pd.concat([test_frame, control_frame], axis = 1, sort = True)
    return result_frame
def plotCanadaTest(control, test):
    plt.figure()
    control.plot(logy = True)
    test.plot(logy = True)
    plt.title('Discrepancy')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.show()
def plot_nber(source, method):
    source_frame = pd.read_csv(source)
    if method == 'mean':
        source_frame = source_frame.groupby('year').mean()
        title = 'Mean NBER-CES'
    elif method == 'sum':
        source_frame = source_frame.groupby('year').sum()
        title = 'Sum NBER-CES'
    else:
        return
    if 'sic' in source:
        source_frame.drop(['sic'], axis = 1, inplace=True)
    elif 'naics' in source:
        source_frame.drop(['naics'], axis = 1, inplace=True)
    else:
        return
    series = source_frame.columns
    plt.figure()
    for i in range(len(series)):
        plt.plot(source_frame.iloc[:, i], label = series[i])
        plt.title(title)
        plt.xlabel('Period')
        plt.ylabel('Dimension')
        plt.grid(True)
        plt.legend()
        plt.show()
def dataConsistencyTestA():
    '''Project I: Canada Gross Domestic Product Data Comparison'''
    print(__doc__)
    '''Expenditure-Based Gross Domestic Product Series Used'''
    '''Income-Based Gross Domestic Product Series Not Used'''
    '''Series A Equals Series D,  However,  Series D Is Preferred Over Series A As It Is Yearly: v62307282 - 380-0066 Price indexes,  gross domestic product; Canada; Implicit price indexes; Gross domestic product at market prices (quarterly,  1961-03-01 to 2017-09-01)'''
    semi_frameA = fetchCANSIMQ('03800066', 'v62307282', True)
    '''Series B Equals Both Series C & Series E,  However,  Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306896 - 380-0084 Gross domestic product at 2007 constant prices,  expenditure-based; Canada; Seasonally adjusted at annual rates; Gross domestic product at market prices (x 1, 000, 000) (quarterly,  1961-03-01 to 2017-09-01)'''
    semi_frameB = fetchCANSIMQ('03800084', 'v62306896', True)
    '''Series C Equals Both Series B & Series E,  However,  Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306938 - 380-0084 Gross domestic product at 2007 constant prices,  expenditure-based; Canada; Unadjusted; Gross domestic product at market prices (x 1, 000, 000) (quarterly,  1961-03-01 to 2017-09-01)'''
    semi_frameC = fetchCANSIMQ('03800084', 'v62306938', True)
    '''Series D Equals Series A,  However,  Series D Is Preferred Over Series A As It Is Yearly: v62471023 - 380-0102 Gross domestic product indexes; Canada; Implicit price indexes; Gross domestic product at market prices (annual,  1961 to 2016)'''
    semi_frameD = fetchCANSIM('03800102', 'v62471023', True)
    '''Series E Equals Both Series B & Series C,  However,  Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62471340 - 380-0106 Gross domestic product at 2007 constant prices,  expenditure-based; Canada; Gross domestic product at market prices (x 1, 000, 000) (annual,  1961 to 2016)'''
    semi_frameE = fetchCANSIM('03800106', 'v62471340', True)
    semi_frameF = fetchCANSIM('03800518', 'v96411770', True)
    semi_frameG = fetchCANSIM('03800566', 'v96391932', True)
    semi_frameH = fetchCANSIM('03800567', 'v96730304', True)
    semi_frameI = fetchCANSIM('03800567', 'v96730338', True)
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                           semi_frameF, semi_frameG, semi_frameH, semi_frameI], axis = 1, sort = True)
    result_frame = result_frame.dropna()
    SERA = result_frame.iloc[:, 0].div(result_frame.iloc[0, 0])
    SERB = result_frame.iloc[:, 4].div(result_frame.iloc[0, 4])
    SERC = result_frame.iloc[:, 5].div(result_frame.iloc[0, 5])
    SERD = result_frame.iloc[:, 7].div(result_frame.iloc[:, 6].div(result_frame.iloc[:, 5]/100))
    SERE = result_frame.iloc[:, 8].div(result_frame.iloc[0, 8])
    '''Option 1'''
    plotCanadaTest(SERA, SERC)
    '''Option 2'''
    plotCanadaTest(SERD, SERE)
    '''Option 3'''
    plotCanadaTest(SERB, SERE)
    '''Option 4'''
    plotCanadaTest(SERE.div(SERB), SERC)
def dataConsistencyTestB():
    '''Project II: USA Fixed Assets Data Comparison'''
    print(__doc__)
    """Fixed Assets Series: k1ntotl1si000,  1925--2016"""
    semi_frameA = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section2ALL_xls.xls', '201 Ann', 1925, 2016, 48)
    """Fixed Assets Series: kcntotl1si000,  1925--2016"""
    semi_frameB = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section2ALL_xls.xls', '202 Ann', 1925, 2016, 48)
    """Not Used: Fixed Assets: k3ntotl1si000,  1925--2016,  Table 2.3. Historical-Cost Net Stock of Private Fixed Assets,  Equipment,  Structures,  and Intellectual Property Products by Type"""
    semi_frameC = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section2ALL_xls.xls', '203 Ann', 1925, 2016, 48)
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC], axis = 1, sort = True)
    del semi_frameA, semi_frameB, semi_frameC
    print(result_frame)
def dataConsistencyTestC():
    '''Project III: USA BLS Unemployment Rate & Producer Price Index Manufacturing'''
    print(__doc__)
    '''LNU04000000: Bureau of Labor Statistics Unemployment Rate'''
    print(BLSLNU('dataset USA BLS 2015-02-23 ln.data.1.AllData'))
    '''LNU04000000: Bureau of Labor Statistics Unemployment Rate'''
    print(BLSLNU('dataset USA BLS 2017-07-06 ln.data.1.AllData'))
    '''PCUOMFG--OMFG--: Bureau of Labor Statistics Producer Price Index Manufacturing'''
    print(BLSPCUOMFG('dataset USA BLS pc.data.0.Current'))
def dataConsistencyTestD():
    '''Project IV: USA Macroeconomic & Fixed Assets Data Tests'''
    print(__doc__)
    """Macroeconomic Data Tests"""
    """Tested: `A051RC1`! = `A052RC1`+`A262RC1`"""
    testProcedure(['A051RC1', 'A052RC1', 'A262RC1'])
    """Tested: `Government` = `Federal`+`State and local`"""
    testProcedure(['A822RC1', 'A823RC1', 'A829RC1'])
    testProcedure(['A955RC1', 'A957RC1', 'A991RC1'])
    """Tested: `Federal` = `National defense`+`Nondefense`"""
    testProcedure(['A823RC1', 'A824RC1', 'A825RC1'])
    testProcedure(['A957RC1', 'A997RC1', 'A542RC1'])
    """Fixed Assets Data Tests"""
    result_frame = fetchbeasfatSeries()
    """Tested: `k3n31gd1es000` = `k3n31gd1eq000`+`k3n31gd1ip000`+`k3n31gd1st000`"""
#    subTestA(result_frame)
    """Comparison of `k3n31gd1es000` out of control_frame with `k3n31gd1es000` out of test_frame"""
#    subTestB(result_frame)
    """Future Project: Test Ratio of Manufacturing Fixed Assets to Overall Fixed Assets"""
    """To Do"""
def dataConsistencyTestE():
    '''Project V: USA NBER Data Plotting'''
    print(__doc__)
    plot_nber('dataset USA NBER-CES MID sic5811.csv', 'mean')
    plot_nber('dataset USA NBER-CES MID sic5811.csv', 'sum')
    plot_nber('dataset USA NBER-CES MID naics5811.csv', 'mean')
    plot_nber('dataset USA NBER-CES MID naics5811.csv', 'sum')
import os
import pandas as pd
import matplotlib.pyplot as plt
dataConsistencyTestA()
dataConsistencyTestB()
dataConsistencyTestC()
#dataConsistencyTestD()
dataConsistencyTestE()