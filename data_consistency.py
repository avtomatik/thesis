#-*- coding: utf-8 -*-
"""
Created on Wed Mar  4 20:39:06 2020

@author: Mastermind
"""

# =============================================================================
# TODO: Refactor
# =============================================================================
def fetch_usa_bea(archive_name, wb_name, sh_name, series_id):
# =============================================================================
# Data Frame Fetching from Bureau of Economic Analysis Zip Archives
# =============================================================================
# =============================================================================
# archive_name: Name of Zip Archive,
# wb_name: Name of Excel File within Zip Archive,
# sh_name: Name of Worksheet within Excel File within Zip Archive,
# series_id: Series ID
# =============================================================================
# =============================================================================
#     TODO: Eliminate Duplicate
# =============================================================================
    if not archive_name == None:
        with pd.ExcelFile(ZipFile(archive_name, 'r').open(wb_name)) as xl_file:
# =============================================================================
#             Duplicate
# =============================================================================
# =============================================================================
#             Load
# =============================================================================
            data_frame = pd.read_excel(xl_file, sh_name, skiprows=7)
# =============================================================================
#             Re-Load
# =============================================================================
            data_frame = pd.read_excel(xl_file,
                                       sh_name,
                                       usecols=range(2, data_frame.shape[1]),
                                       skiprows=7)
    else:
        with pd.ExcelFile(wb_name) as xl_file:
# =============================================================================
#             Duplicate
# =============================================================================
# =============================================================================
#             Load
# =============================================================================
            data_frame = pd.read_excel(xl_file, sh_name, skiprows=7)
# =============================================================================
#             Re-Load
# =============================================================================
            data_frame = pd.read_excel(xl_file,
                                       sh_name,
                                       usecols=range(2, data_frame.shape[1]),
                                       skiprows=7)
    data_frame.dropna(inplace=True)
    data_frame.columns = ['period', *data_frame.columns[1:]]
    data_frame = data_frame.set_index(data_frame.columns[0]).transpose()
    return data_frame.loc[:, [series_id]]


def fetch_can_quarterly(file_name, vector):
# =============================================================================
# Data Frame Fetching from Quarterly Data within CANSIM Zip Archives
# Should Be [x 7 columns]
# =============================================================================
    data_frame = pd.read_csv(f'dataset_can_{file_name}-eng.zip')
    data_frame = data_frame[data_frame.Vector == vector]
    if file_name == '02820011':
        data_frame = data_frame[data_frame.columns[[0, 7]]]
    elif file_name == '02820012':
        data_frame = data_frame[data_frame.columns[[0, 7]]]
    elif file_name == '03790031':
        data_frame = data_frame[data_frame.columns[[0, 7]]]
    elif file_name == '03800068':
        data_frame = data_frame[data_frame.columns[[0, 7]]]
    else:
        data_frame = data_frame[data_frame.columns[[0, 6]]] # # Should Be [x 7 columns]
    data_frame.rename(columns={'Value':vector}, inplace=True)
    data_frame['Period'], data_frame['Q'] = data_frame.iloc[:, 0].str.split('/').str
    data_frame = data_frame[data_frame.columns[[2, 1]]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].astype(int)
    data_frame.iloc[:, 1] = pd.to_numeric(data_frame.iloc[:, 1])
    if (file_name == '03800084' and vector == 'v62306938'):
        data_frame = data_frame.groupby('Period').sum()
    elif (file_name == '03790031' and vector == 'v65201536'):
        data_frame = data_frame.groupby('Period').mean()
    elif (file_name == '03790031' and vector == 'v65201809'):
        data_frame = data_frame.groupby('Period').sum()
    else:
        data_frame = data_frame.groupby('Period').mean()
    return data_frame


def fetch_can_annually(file_id, series_id):
# =============================================================================
# Data Frame Fetching from CANSIM Zip Archives
# =============================================================================
    usecols = {
        '02820012': (5, 7,),
        '03800102': (4, 6,),
        '03800106': (3, 5,),
        '03800518': (4, 6,),
        '03800566': (3, 5,),
        '03800567': (4, 6,),
        }
    data_frame = pd.read_csv(f'dataset_can_{file_id}-eng.zip',
                              usecols=[0, *usecols[file_id]])
    data_frame = data_frame[data_frame.iloc[:, 1] == series_id].iloc[:,[0, 2]]
    data_frame.columns = [data_frame.columns[0].upper(), series_id]
    data_frame.set_index(data_frame.columns[0], inplace=True)
    data_frame.iloc[:, 0] = pd.to_numeric(data_frame.iloc[:, 0])
    return data_frame


def fetch_can_group_a(file_id, skiprows):
# =============================================================================
# Not Used Anywhere
# =============================================================================
    data_frame = pd.read_csv(f'dataset_can_cansim{file_id}.csv',
                              skiprows=skiprows)
    if file_id == '7931814471809016759':
        data_frame.columns = [column[:7] for column in data_frame.columns]
        data_frame.iloc[:, -1] = pd.to_numeric(data_frame.iloc[:, -1].str.replace(';', ''))
    data_frame = data_frame.set_index(data_frame.columns[0]).transpose()
    data_frame.reset_index(inplace=True)
    data_frame[['quarter',
                'period',]] = data_frame.iloc[:, 0].str.split(expand=True)
    data_frame.set_index(data_frame.columns[0], inplace=True)
    return data_frame.groupby(data_frame.columns[-1]).mean()


def fetch_can_group_b(file_id, skiprows):
# =============================================================================
# Not Used Anywhere
# =============================================================================
    data_frame = pd.read_csv(f'dataset_can_cansim{file_id}.csv',
                             skiprows=skiprows)
    data_frame[['month',
                'period',]] = data_frame.iloc[:, 0].str.split('-', expand=True)
    return data_frame.groupby(data_frame.columns[-1]).mean()


def fetch_usa_bls_lnu(file_name):
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


def fetch_usa_bls_ppi(file_name):
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


def test_capital_combined_archived():
    '''Data Test'''
    '''Nominal Investment Series: A006RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A006RC1')
    '''Nominal Gross Domestic Product Series: A191RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
    control_frame = pd.concat([sub_frame_a, sub_frame_b], axis=1, sort=True)

    '''Nominal Investment Series: A006RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A006RC1')
    '''Nominal Gross Domestic Product Series: A191RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
    test_frame = pd.concat([sub_frame_a, sub_frame_b], axis=1, sort=True)

    if control_frame.equals(test_frame):
        print('Series `A006RC1` & `A191RC1` @ Worksheet `10105 Ann` Equals Series `A006RC1` & `A191RC1` @ Worksheet `10505 Ann` for Period 1929--1969')
    else:
        print('Data Varies from Worksheet `10105 Ann` to Worksheet `10505 Ann`')

    '''Nominal Investment Series: A006RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10105 Ann', 'A006RC1')
    '''Nominal Gross Domestic Product Series: A191RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
    control_frame = pd.concat([sub_frame_a, sub_frame_b], axis=1, sort=True)

    '''Nominal Investment Series: A006RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10105 Ann', 'A006RC1')
    '''Nominal Gross Domestic Product Series: A191RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
    test_frame = pd.concat([sub_frame_a, sub_frame_b], axis=1, sort=True)

    if control_frame.equals(test_frame):
        print('Series `A006RC1` & `A191RC1` @ Worksheet `10105 Ann` Equals Series `A006RC1` & `A191RC1` @ Worksheet `10505 Ann` for Period 1969--2012')
    else:
        print('Data Varies from Worksheet `10105 Ann` to Worksheet `10505 Ann`')


def fetch_bea_usa(file_name, series_id):
# =============================================================================
# TODO: Replace with Other Fetch Procedures and Eliminate These Databases
# =============================================================================
# =============================================================================
# `dataset_usa_bea_nipadataa.txt`: U.S. Bureau of Economic Analysis
# Archived: https://www.bea.gov/National/FAweb/Details/Index.html
# https://www.bea.gov//national/FA2004/DownSS2.asp, Accessed May 26, 2018
# =============================================================================
    if file_name == 'dataset_usa_bea-nipa-2015-05-01.zip':
        data_frame = pd.read_csv(file_name, usecols=range(14, 18))
        data_frame = data_frame[data_frame.iloc[:, 2] == int(0)].iloc[:,[0, 1, 3]]
    elif file_name == 'dataset_usa_bea_nipadataa.txt':
        data_frame = pd.read_csv(file_name, thousands=',')
    else:
        pass
    result_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:,[1, 2]]
    result_frame.columns = [result_frame.columns[0].lower(), series_id]
    result_frame.drop_duplicates(inplace=True)
    result_frame.set_index(result_frame.columns[0], inplace=True, verify_integrity=True)
    return result_frame


def lookup(data_frame):
    for i, series_id in enumerate(data_frame.columns):
        series = data_frame.iloc[:, i].sort_values().unique()
        print('{:*^50}'.format(series_id))
        print(series)


def retrieval(series_id):
    file_name = 'dataset_usa_bea-nipa-2015-05-01.zip'
    data_frame = pd.read_csv(file_name)
    data_frame = data_frame[data_frame.iloc[:, 0].str.contains('Table 3.17. Selected Government Current and Capital Expenditures by Function')]
    data_frame = data_frame[data_frame.iloc[:, 7].str.contains(series_id)]
    lookup(data_frame)


def test_procedure(series_ids: tuple) -> None:
    file_name = 'dataset_usa_bea-nipa-2015-05-01.zip'
    df = pd.concat(
        [fetch_bea_usa(file_name, series_id) for series_id in series_ids],
        axis=1,
        sort=True)
    df['diff_abs'] = df.iloc[:, 0].sub(df.iloc[:, 1]).sub(df.iloc[:, 2])
    df.iloc[:, [-1]].dropna().plot(grid=True)


def test_sub_a(data_frame):
    data_frame['delta_sm'] = data_frame.iloc[:, 0]-data_frame.iloc[:, 3]-data_frame.iloc[:, 4]-data_frame.iloc[:, 5]
    data_frame.dropna(inplace=True)
    autocorrelation_plot(data_frame.iloc[:, 7])


def test_sub_b(data_frame):
#    data_frame['delta_eq'] = data_frame.iloc[:, 0]-data_frame.iloc[:, 6]
    data_frame['delta_eq'] = 2*(data_frame.iloc[:, 0]-data_frame.iloc[:, 6]).div(data_frame.iloc[:, 0] + data_frame.iloc[:, 6])
    data_frame.dropna(inplace=True)
    data_frame.iloc[:, 7].plot(grid=True)


def fetch_usa_bea_sfat_series():
# =============================================================================
# Earlier Version of `k3n31gd1es000`
# =============================================================================
    file_name = 'dataset_usa_bea-nipa-selected.zip'
    control_frame = pd.read_csv(file_name)
    control_header = control_frame.iloc[:, 8].unique().tolist()[0]
    control_frame = control_frame[control_frame.columns[[9, 10]]]
    control_frame.columns = control_frame.columns.str.title()
    control_frame.rename(columns={'Value':control_header}, inplace=True)
    control_frame = control_frame.reset_index(drop=True)
    control_frame = control_frame.set_index('Period')
    """Fixed Assets Series: k3n31gd1es000, 1925--2016"""
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_a = fetch_usa_bea_single(file_name, 'Section4ALL_xls.xls', '403 Ann', 'k3n31gd1es000')
    """Fixed Assets Series: k3n31gd1eq000, 1925--2016"""
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_b = fetch_usa_bea_single(file_name, 'Section4ALL_xls.xls', '403 Ann', 'k3n31gd1eq000')
    """Fixed Assets Series: k3n31gd1ip000, 1925--2016"""
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_c = fetch_usa_bea_single(file_name, 'Section4ALL_xls.xls', '403 Ann', 'k3n31gd1ip000')
    """Fixed Assets Series: k3n31gd1st000, 1925--2016"""
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_d = fetch_usa_bea_single(file_name, 'Section4ALL_xls.xls', '403 Ann', 'k3n31gd1st000')
    test_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d], axis=1, sort=True)

    result_frame = pd.concat([test_frame, control_frame], axis=1, sort=True)
    return result_frame


def plot_can_test(control, test):
    plt.figure()
    control.plot(logy=True)
    test.plot(logy=True)
    plt.title('Discrepancy')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.show()


def plot_usa_nber(file_name, method):
    data_frame = pd.read_csv(file_name)
    if method == 'mean':
        data_frame = data_frame.groupby('year').mean()
        title = 'Mean NBER-CES'
    elif method == 'sum':
        data_frame = data_frame.groupby('year').sum()
        title = 'Sum NBER-CES'
    else:
        return
    if 'sic' in file_name:
        data_frame.drop(['sic'], axis=1, inplace=True)
    elif 'naics' in file_name:
        data_frame.drop(['naics'], axis=1, inplace=True)
    else:
        return
    plt.figure()
    for i, series_id in enumerate(data_frame.columns):
        plt.plot(data_frame.iloc[:, i], label=series_id)
        plt.title(title)
        plt.xlabel('Period')
        plt.ylabel('Dimension')
        plt.grid(True)
        plt.legend()
        plt.show()


def test_data_consistency_a():
    '''Project I: Canada Gross Domestic Product Data Comparison'''
    print(__doc__)
    '''Expenditure-Based Gross Domestic Product Series Used'''
    '''Income-Based Gross Domestic Product Series Not Used'''
    '''Series A Equals Series D, However, Series D Is Preferred Over Series A As It Is Yearly: v62307282 - 380-0066 Price indexes, gross domestic product; Canada; Implicit price indexes; Gross domestic product at market prices (quarterly, 1961-03-01 to 2017-09-01)'''
    semi_frame_a = fetch_can_quarterly('03800066', 'v62307282')
    '''Series B Equals Both Series C & Series E, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306896 - 380-0084 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Seasonally adjusted at annual rates; Gross domestic product at market prices (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)'''
    semi_frame_b = fetch_can_quarterly('03800084', 'v62306896')
    '''Series C Equals Both Series B & Series E, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306938 - 380-0084 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Unadjusted; Gross domestic product at market prices (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)'''
    semi_frame_c = fetch_can_quarterly('03800084', 'v62306938')
    '''Series D Equals Series A, However, Series D Is Preferred Over Series A As It Is Yearly: v62471023 - 380-0102 Gross domestic product indexes; Canada; Implicit price indexes; Gross domestic product at market prices (annual, 1961 to 2016)'''
    semi_frame_d = fetch_can_annually('03800102', 'v62471023')
    '''Series E Equals Both Series B & Series C, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62471340 - 380-0106 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Gross domestic product at market prices (x 1,000,000) (annual, 1961 to 2016)'''
    semi_frame_e = fetch_can_annually('03800106', 'v62471340')
    semi_frame_f = fetch_can_annually('03800518', 'v96411770')
    semi_frame_g = fetch_can_annually('03800566', 'v96391932')
    semi_frame_h = fetch_can_annually('03800567', 'v96730304')
    semi_frame_i = fetch_can_annually('03800567', 'v96730338')
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e, \
                           semi_frame_f, semi_frame_g, semi_frame_h, semi_frame_i], axis=1, sort=True)
    result_frame = result_frame.dropna()
    SERA = result_frame.iloc[:, 0].div(result_frame.iloc[0, 0])
    SERB = result_frame.iloc[:, 4].div(result_frame.iloc[0, 4])
    SERC = result_frame.iloc[:, 5].div(result_frame.iloc[0, 5])
    SERD = result_frame.iloc[:, 7].div(result_frame.iloc[:, 6].div(result_frame.iloc[:, 5]/100))
    SERE = result_frame.iloc[:, 8].div(result_frame.iloc[0, 8])
    '''Option 1'''
    plot_can_test(SERA, SERC)
    '''Option 2'''
    plot_can_test(SERD, SERE)
    '''Option 3'''
    plot_can_test(SERB, SERE)
    '''Option 4'''
    plot_can_test(SERE.div(SERB), SERC)


def test_data_consistency_b():
    '''Project II: USA Fixed Assets Data Comparison'''
    print(__doc__)
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    """Fixed Assets Series: k1ntotl1si000, 1925--2016"""
    semi_frame_a = fetch_usa_bea(file_name, 'Section2ALL_xls.xls', '201 Ann', 'k1ntotl1si000')
    """Fixed Assets Series: kcntotl1si000, 1925--2016"""
    semi_frame_b = fetch_usa_bea(file_name, 'Section2ALL_xls.xls', '202 Ann', 'kcntotl1si000')
    """Not Used: Fixed Assets: k3ntotl1si000, 1925--2016, Table 2.3. Historical-Cost Net Stock of Private Fixed Assets, Equipment, Structures, and Intellectual Property Products by Type"""
    semi_frame_c = fetch_usa_bea(file_name, 'Section2ALL_xls.xls', '203 Ann', 'k3ntotl1si000')
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c], axis=1, sort=True)

    print(result_frame)


def test_data_consistency_c():
    '''Project III: USA BLS Unemployment Rate & Producer Price Index Manufacturing'''
    print(__doc__)
    '''LNU04000000: Bureau of Labor Statistics Unemployment Rate'''
    print(fetch_usa_bls_lnu('dataset USA BLS 2015-02-23 ln.data.1.AllData'))
    '''LNU04000000: Bureau of Labor Statistics Unemployment Rate'''
    print(fetch_usa_bls_lnu('dataset USA BLS 2017-07-06 ln.data.1.AllData'))
    '''PCUOMFG--OMFG--: Bureau of Labor Statistics Producer Price Index Manufacturing'''
    print(fetch_usa_bls_ppi('dataset USA BLS pc.data.0.Current'))


def test_data_consistency_d():
    '''Project IV: USA Macroeconomic & Fixed Assets Data Tests'''
    print(__doc__)
    """Macroeconomic Data Tests"""
# =============================================================================
#     Tested: `A051RC1` != `A052RC1` + `A262RC1`
# =============================================================================
    series_ids = ('A051RC1', 'A052RC1', 'A262RC1',)
    test_procedure(series_ids)
# =============================================================================
#     Tested: `Government` = `Federal` + `State and local`
# =============================================================================
    series_ids = ('A822RC1', 'A823RC1', 'A829RC1',)
    test_procedure(series_ids)
    series_ids = ('A955RC1', 'A957RC1', 'A991RC1',)
    test_procedure(series_ids)
# =============================================================================
#     Tested: `Federal` = `National defense` + `Nondefense`
# =============================================================================
    series_ids = ('A823RC1', 'A824RC1', 'A825RC1',)
    test_procedure(series_ids)
    series_ids = ('A957RC1', 'A997RC1', 'A542RC1',)
    test_procedure(series_ids)
    """Fixed Assets Data Tests"""
    result_frame = fetch_usa_bea_sfat_series()
    """Tested: `k3n31gd1es000` = `k3n31gd1eq000` + `k3n31gd1ip000` + `k3n31gd1st000`"""
#    test_sub_a(result_frame)
    """Comparison of `k3n31gd1es000` out of control_frame with `k3n31gd1es000` out of test_frame"""
#    test_sub_b(result_frame)
    """Future Project: Test Ratio of Manufacturing Fixed Assets to Overall Fixed Assets"""
    """To Do"""


def test_data_consistency_e():
    '''Project V: USA NBER Data Plotting'''
    print(__doc__)
    plot_usa_nber('dataset USA NBER-CES MID sic5811.csv', 'mean')
    plot_usa_nber('dataset USA NBER-CES MID sic5811.csv', 'sum')
    plot_usa_nber('dataset USA NBER-CES MID naics5811.csv', 'mean')
    plot_usa_nber('dataset USA NBER-CES MID naics5811.csv', 'sum')


test_data_consistency_a()
test_data_consistency_b()
test_data_consistency_c()
# test_data_consistency_d()
test_data_consistency_e()