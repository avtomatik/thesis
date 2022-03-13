import os
import pandas as pd


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


def fetchMCB(string, index):
    '''Data _frame Fetching from McConnell C.R. & Brue S.L.'''
    source_frame = pd.read_csv('mcConnellBrue.zip', usecols=range(1, 4))
    source_frame = source_frame[source_frame.iloc[:, 0] == string]
    source_frame = source_frame[source_frame.columns[[1, 2]]]
    source_frame.columns = source_frame.columns.str.title()
    source_frame = source_frame.sort_values('Period')
    source_frame = source_frame.reset_index(drop = True)
    if index:
        source_frame = source_frame.set_index('Period')
        return source_frame
    else:
        source_frame.to_csv('temporary.txt', index = False)
        del source_frame
        result_frame = pd.read_csv('temporary.txt')
        os.unlink('temporary.txt')
        return result_frame


def indexswitch(source_frame):
    source_frame.to_csv('temporary.txt')
    del source_frame
    result_frame = pd.read_csv('temporary.txt')
    os.unlink('temporary.txt')
    return result_frame


def periodCentering(source_frame):
    '''
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Series
    '''
    '''Variables Initialised'''
    result_frame = source_frame ##Data_frame for Results
    period = result_frame.iloc[:, 0]
    series = result_frame.iloc[:, 1]
    '''Loop'''
    for i in range(1, 1+len(result_frame)//2):
        period = period.rolling(window = 2).mean()
        series = series.rolling(window = 2).mean()
        periodRoll = period.shift(-(i//2))
        seriesRoll = series.shift(-(i//2))
        seriesFrac = seriesRoll.div(result_frame.iloc[:, 1])
        seriesDiff = (seriesRoll.shift(-2)-seriesRoll).div(2*seriesRoll.shift(-1))
        result_frame = pd.concat([result_frame, periodRoll, seriesRoll, seriesFrac, seriesDiff], axis = 1, sort = True)
    return result_frame


'''A032RC1'''
source_frame = fetchMCB('Национальный доход,  млрд долл. США', False)
result_frame = periodCentering(source_frame)
print(result_frame)
del source_frame, result_frame
source_frame = fetchBEA('dataset USA BEA NipaDataA.txt', 'A032RC')
source_frame = indexswitch(source_frame)
result_frame = periodCentering(source_frame)
print(result_frame)
del source_frame, result_frame