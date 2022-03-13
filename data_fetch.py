# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 12:13:55 2020

@author: Mastermind
"""
import pandas as pd


def fetch_classic(file_name: str, series_id: str) -> pd.DataFrame:
# =============================================================================
# Data Fetch Procedure for Enumerated Classical Datasets
# =============================================================================
    if file_name == 'brown.zip':
        data_frame = pd.read_csv(file_name, skiprows=4, usecols=range(3, 6))
        data_frame.rename(columns={'Данные по отработанным человеко-часам заимствованы из: Kendrick,  op. cit.,  pp. 311-313,  Table A. 10.':'series', 
                                    'Unnamed: 4':'period', 
                                    'Unnamed: 5':'value'}, inplace=True)
    elif file_name == 'cobbdouglas.zip':
        data_frame = pd.read_csv(file_name, usecols=range(5, 8))
    elif file_name == 'douglas.zip':
        data_frame = pd.read_csv(file_name, usecols=range(4, 7))
    elif file_name == 'kendrick.zip':
        data_frame = pd.read_csv(file_name, usecols=range(4, 7))
    result_frame = data_frame[data_frame.iloc[:, 0] == series_id]
    del data_frame
    result_frame = result_frame[result_frame.columns[[1, 2]]]
    result_frame.columns = result_frame.columns.str.title()
    result_frame.rename(columns={'Value':series_id}, inplace=True)
    result_frame.iloc[:, 0] = result_frame.iloc[:, 0].astype(int)
    result_frame.iloc[:, 1] = pd.to_numeric(result_frame.iloc[:, 1], errors='coerce')
    result_frame = result_frame.dropna()
    result_frame = result_frame.sort_values('Period')
    result_frame = result_frame.set_index('Period')
    return result_frame


def fetch(data_frame, series_id):
# =============================================================================
# Retrieve Yearly Data for BEA Series' Code
# =============================================================================
    data_frame = data_frame[data_frame.iloc[:, 14] == series_id]
    tables = data_frame.iloc[:, 0].unique()
    tables = pd.Series(tables)
    if len(tables) == 1:
        result_frame = data_frame[data_frame.iloc[:, 0] == tables[0]]
        result_frame = result_frame[result_frame.columns[[15, 17]]]
        result_frame.columns = result_frame.columns.str.title()
        result_frame.rename(columns={'Value':series_id}, inplace=True)
        result_frame = result_frame.drop_duplicates()
        result_frame = result_frame.reset_index(drop=True)
        result_frame = result_frame.set_index('Period')
    elif len(tables) >= 2:
        i = 0 ##Counter
        for table in tables:
            current_frame = data_frame[data_frame.iloc[:, 1] == table]
            current_frame = current_frame[current_frame.columns[[15, 17]]]
            print(current_frame)
            result_frame.columns = result_frame.columns.str.title()
            result_frame.rename(columns={'Value':series_id}, inplace=True)
            current_frame = current_frame.drop_duplicates()
            current_frame = current_frame.reset_index(drop=True)
            current_frame = current_frame.set_index('Period')
            if i == 0:
                result_frame = current_frame
            elif i >= 1:
                result_frame = pd.concat([current_frame, result_frame], axis=1, sort=True)
            del current_frame
            i += 1
    return result_frame


def BLSLNU(file_name):
# =============================================================================
# LNU04000000: Bureau of Labor Statistics Unemployment Rate
# =============================================================================
    series_id = 'LNU04000000'
    data_frame = pd.read_csv(file_name, sep='\t', low_memory=False)
    data_frame = data_frame[data_frame.iloc[:, 0].str.contains(series_id)]
    data_frame = data_frame[data_frame.iloc[:, 2] == 'M13']
    result_frame = data_frame[data_frame.columns[[1, 3]]]
    result_frame.rename(columns={'year':'period'}, inplace=True)
    result_frame.columns = result_frame.columns.str.title()
    result_frame.rename(columns={'Value':series_id}, inplace=True)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].astype(float)
    return result_frame


def BLSPCUOMFG(file_name):
# =============================================================================
# PCUOMFG--OMFG--: Bureau of Labor Statistics Producer Price Index Manufacturing
# =============================================================================
    series_id = 'PCUOMFG--OMFG--'
    data_frame = pd.read_csv(file_name, sep='\t', low_memory=False)
    data_frame = data_frame[data_frame.iloc[:, 0].str.contains(series_id)]
    data_frame = data_frame[data_frame.iloc[:, 2] == 'M13']
    result_frame = data_frame[data_frame.columns[[1, 3]]]
    result_frame.rename(columns={'year':'period'}, inplace=True)
    result_frame.columns = result_frame.columns.str.title()
    result_frame.rename(columns={'Value':series_id}, inplace=True)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].astype(float)
    return result_frame


def fetch_brown():
# =============================================================================
# Fetch Data from `Reference RU Brown M. 0597_088.pdf`,  Page 193
# Dependent on `fetch_classic`
# Out of Kendrick J.W. Data & Table 2. of `Reference RU Brown M. 0597_088.pdf`
# =============================================================================
    data_frame = pd.read_csv('brown.zip', skiprows=4, usecols=range(3, 6))
    data_frame.rename(columns={'Данные по отработанным человеко-часам заимствованы из: Kendrick,  op. cit.,  pp. 311-313,  Table A. 10.':'series', 
                        'Unnamed: 4':'period', 
                        'Unnamed: 5':'value'}, inplace=True)
    series = data_frame.iloc[:, 0].sort_values().unique()
    semi_frame_A = fetch_classic('brown.zip', series[0])
    semi_frame_B = fetch_classic('brown.zip', series[1])
    semi_frame_C = fetch_classic('brown.zip', series[2])
    semi_frame_D = fetch_classic('brown.zip', series[3])
    semi_frame_E = fetch_classic('brown.zip', series[4])
    semi_frame_F = fetch_classic('brown.zip', series[5])
    del data_frame, series
    Brown_frame = pd.concat([semi_frame_A, semi_frame_F, semi_frame_C, semi_frame_D, semi_frame_E, semi_frame_B], axis=1, sort=True)
    Brown_frame.rename(columns={
                                'Валовой продукт (в млн. долл.,  1929 г.)':'XAA',  ##Gross Domestic Product,  USD 1, 000, 000,  1929=100;
                                'Чистый основной капитал (в млн. долл.,  1929 г.)':'XBB',  ##Net Fixed Assets,  USD 1, 000, 000,  1929=100;
                                'Используемый основной капитал (в млн. долл.,  1929 г.)':'XCC',  ##Utilized Fixed Assets,  USD 1, 000, 000,  1929=100;
                                'Отработанные человеко-часы':'XDD',  ##Actual Man-Hours Worked.
                                'Первая аппроксимация рядов загрузки мощностей,  полученная с помощью метода Уортонской школы':'XEE', 
                                'Вторая аппроксимация рядов загрузки мощностей,  полученная с помощью итеративного процесса':'XFF'
                                }, inplace=True)
    del semi_frame_A, semi_frame_B, semi_frame_C, semi_frame_D, semi_frame_E, semi_frame_F
    semi_frame_A = fetch_classic('kendrick.zip', 'KTA03S07')
    semi_frame_B = fetch_classic('kendrick.zip', 'KTA03S08')
    semi_frame_C = fetch_classic('kendrick.zip', 'KTA10S08')
    semi_frame_D = fetch_classic('kendrick.zip', 'KTA15S07')
    semi_frame_E = fetch_classic('kendrick.zip', 'KTA15S08')
    Kendrick_frame = pd.concat([semi_frame_A, semi_frame_B, semi_frame_C, semi_frame_D, semi_frame_E], axis=1, sort=True)
    del semi_frame_A, semi_frame_B, semi_frame_C, semi_frame_D, semi_frame_E
    semi_frame_A = Kendrick_frame[20:-2]
# =============================================================================
# Первая аппроксимация рядов загрузки мощностей,  полученная с помощью метода Уортонской школы
# =============================================================================
    semi_frame_B = Brown_frame[Brown_frame.columns[[4]]][:-7]
# =============================================================================
# Brown M. Numbers Not Found in Kendrick J.W. For Years Starting From 1954 Inclusive
# =============================================================================
    semi_frame_C = Brown_frame[Brown_frame.columns[[0, 1, 2, 3]]][-7:]
    result_frame = pd.concat([semi_frame_A, semi_frame_B], axis=1, sort=True)
    result_frame = result_frame.assign(XAA = result_frame.iloc[:, 0]-result_frame.iloc[:, 1], 
                                   XBB = result_frame.iloc[:, 3]+result_frame.iloc[:, 4], 
                                   XCC = result_frame.iloc[:, 5]*(result_frame.iloc[:, 3].rolling(window = 2).mean()+result_frame.iloc[:, 4].rolling(window=2).mean())/100, 
                                   XDD = result_frame.iloc[:, 2])
    result_frame = result_frame[result_frame.columns[[6, 7, 8, 9]]]
    result_frame = result_frame.dropna()
    result_frame = result_frame.append(semi_frame_C)
    result_frame = result_frame.round()
    return result_frame


# =============================================================================
# Bureau of Economic Analysis
# =============================================================================
series = ('A006RC1', 'A019RC1', 'A027RC1', 'A030RC1', 'A032RC1',
          'A051RC1', 'A052RC1', 'A054RC1', 'A061RC1', 'A065RC1',
          'A067RC1', 'A124RC1', 'A191RC1', 'A191RX1', 'A229RC0',
          'A229RX0', 'A262RC1', 'A390RC1', 'A392RC1', 'A399RC1',
          'A400RC1', 'A4601C0', 'A655RC1', 'A822RC1', 'A929RC1',
          'B057RC0', 'B230RC0', 'B394RC1', 'B645RC1', 'DPCERC1',
          'W055RC1', 'W056RC1',)
# data_frame = pd.read_csv('beanipa20150501.zip')
# data_frame = data_frame[data_frame.iloc[:, 16] == 0] ##Yearly Data
# os.chdir('C:\\Projects')
# for series_id in series:
#     result_frame = fetch(data_frame, series_id)
#     result_frame.to_csv('beanipa20150501{}.csv'.format(series_id))
#     del result_frame
# =============================================================================
# Bureau of Labor Statistics
# =============================================================================
# BLSLNU('dataset USA BLS 2015-02-23 ln.data.1.AllData')
# BLSLNU('dataset USA BLS 2017-07-06 ln.data.1.AllData')
# BLSPCUOMFG('dataset USA BLS pc.data.0.Current')
# =============================================================================
# FN:Murray Brown
# ORG:University at Buffalo;Economics
# TITLE:Professor Emeritus,  Retired
# EMAIL;PREF;INTERNET:mbrown@buffalo.edu
# =============================================================================
print(fetch_brown())
