# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 12:13:55 2020

@author: Mastermind
"""
def fetchClassic(source, string):
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
def fetch(source_frame, string):
    '''Retrieve Yearly Data for BEA Series' Code'''
    source_frame = source_frame[source_frame.iloc[:, 14] == string]
    tables = source_frame.iloc[:, 0].unique()
    tables = pd.Series(tables)
    if len(tables) == 1:
        result_frame = source_frame[source_frame.iloc[:, 0] == tables[0]]
        result_frame = result_frame[result_frame.columns[[15, 17]]]
        result_frame.columns = result_frame.columns.str.title()
        result_frame.rename(columns = {'Value':string}, inplace=True)
        result_frame = result_frame.drop_duplicates()
        result_frame = result_frame.reset_index(drop = True)
        result_frame = result_frame.set_index('Period')
    elif len(tables)> = 2:
        i = 0 ##Counter
        for table in tables:
            current_frame = source_frame[source_frame.iloc[:, 1] == table]
            current_frame = current_frame[current_frame.columns[[15, 17]]]
            print(current_frame)
            result_frame.columns = result_frame.columns.str.title()
            result_frame.rename(columns = {'Value':string}, inplace=True)
            current_frame = current_frame.drop_duplicates()
            current_frame = current_frame.reset_index(drop = True)
            current_frame = current_frame.set_index('Period')
            if i == 0:
                result_frame = current_frame
            elif i> = 1:
                result_frame = pd.concat([current_frame, result_frame], axis = 1, sort = True)
            del current_frame
            i+ = 1
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
def fetchBrown():
    '''Fetch Data from `Reference RU Brown M. 0597_088.pdf`,  Page 193
    Dependent on `fetchClassic`
    Out of Kendrick J.W. Data & Table 2. of `Reference RU Brown M. 0597_088.pdf`'''
    source_frame = pd.read_csv('brown.zip', skiprows=4, usecols=range(3, 6))
    source_frame.rename(columns = {'Данные по отработанным человеко-часам заимствованы из: Kendrick,  op. cit.,  pp. 311-313,  Table A. 10.':'series', 
                        'Unnamed: 4':'period', 
                        'Unnamed: 5':'value'}, inplace=True)
    series = source_frame.iloc[:, 0].sort_values().unique()
    semi_frameA = fetchClassic('brown.zip', series[0])
    semi_frameB = fetchClassic('brown.zip', series[1])
    semi_frameC = fetchClassic('brown.zip', series[2])
    semi_frameD = fetchClassic('brown.zip', series[3])
    semi_frameE = fetchClassic('brown.zip', series[4])
    semi_frameF = fetchClassic('brown.zip', series[5])
    del source_frame, series
    Brown_frame = pd.concat([semi_frameA, semi_frameF, semi_frameC, semi_frameD, semi_frameE, semi_frameB], axis = 1, sort = True)
    Brown_frame.rename(columns = {
                                'Валовой продукт (в млн. долл.,  1929 г.)':'XAA',  ##Gross Domestic Product,  USD 1, 000, 000,  1929 = 100;
                                'Чистый основной капитал (в млн. долл.,  1929 г.)':'XBB',  ##Net Fixed Assets,  USD 1, 000, 000,  1929 = 100;
                                'Используемый основной капитал (в млн. долл.,  1929 г.)':'XCC',  ##Utilized Fixed Assets,  USD 1, 000, 000,  1929 = 100;
                                'Отработанные человеко-часы':'XDD',  ##Actual Man-Hours Worked.
                                'Первая аппроксимация рядов загрузки мощностей,  полученная с помощью метода Уортонской школы':'XEE', 
                                'Вторая аппроксимация рядов загрузки мощностей,  полученная с помощью итеративного процесса':'XFF'
                                }, inplace=True)
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, semi_frameF
    semi_frameA = fetchClassic('kendrick.zip', 'KTA03S07')
    semi_frameB = fetchClassic('kendrick.zip', 'KTA03S08')
    semi_frameC = fetchClassic('kendrick.zip', 'KTA10S08')
    semi_frameD = fetchClassic('kendrick.zip', 'KTA15S07')
    semi_frameE = fetchClassic('kendrick.zip', 'KTA15S08')
    Kendrick_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE], axis = 1, sort = True)
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE
    semi_frameA = Kendrick_frame[20:-2]
    '''Первая аппроксимация рядов загрузки мощностей,  полученная с помощью метода Уортонской школы'''
    semi_frameB = Brown_frame[Brown_frame.columns[[4]]][:-7]
    '''Brown M. Numbers Not Found in Kendrick J.W. For Years Starting From 1954 Inclusive'''
    semi_frameC = Brown_frame[Brown_frame.columns[[0, 1, 2, 3]]][-7:]
    result_frame = pd.concat([semi_frameA, semi_frameB], axis = 1, sort = True)
    result_frame = result_frame.assign(XAA = result_frame.iloc[:, 0]-result_frame.iloc[:, 1], 
                                   XBB = result_frame.iloc[:, 3]+result_frame.iloc[:, 4], 
                                   XCC = result_frame.iloc[:, 5]*(result_frame.iloc[:, 3].rolling(window = 2).mean()+result_frame.iloc[:, 4].rolling(window = 2).mean())/100, 
                                   XDD = result_frame.iloc[:, 2])
    result_frame = result_frame[result_frame.columns[[6, 7, 8, 9]]]
    result_frame = result_frame.dropna()
    result_frame = result_frame.append(semi_frameC)
    result_frame = result_frame.round()
    return result_frame
import os
import pandas as pd
'''Bureau of Economic Analysis'''
#series = ['A006RC1', 'A019RC1', 'A027RC1', 'A030RC1', 'A032RC1', 'A051RC1', 'A052RC1', \
#        'A054RC1', 'A061RC1', 'A065RC1', 'A067RC1', 'A124RC1', 'A191RC1', 'A191RX1', \
#        'A229RC0', 'A229RX0', 'A262RC1', 'A390RC1', 'A392RC1', 'A399RC1', 'A400RC1', \
#        'A4601C0', 'A655RC1', 'A822RC1', 'A929RC1', 'B057RC0', 'B230RC0', 'B394RC1', \
#        'B645RC1', 'DPCERC1', 'W055RC1', 'W056RC1']
#source_frame = pd.read_csv('beanipa20150501.zip')
#source_frame = source_frame[source_frame.iloc[:, 16] == 0] ##Yearly Data
#os.chdir('C:\\Projects')
#for code in series:
#    result_frame = fetch(source_frame, code)
#    result_frame.to_csv('beanipa20150501{}.csv'.format(code))
#    del result_frame
'''Bureau of Labor Statistics'''
#BLSLNU('dataset USA BLS 2015-02-23 ln.data.1.AllData')
#BLSLNU('dataset USA BLS 2017-07-06 ln.data.1.AllData')
#BLSPCUOMFG('dataset USA BLS pc.data.0.Current')
'''FN:Murray Brown
ORG:University at Buffalo;Economics
TITLE:Professor Emeritus,  Retired
EMAIL;PREF;INTERNET:mbrown@buffalo.edu
'''
print(fetchBrown())