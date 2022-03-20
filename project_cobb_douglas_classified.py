#-*- coding: utf-8 -*-
"""
Created on Wed Feb  5 22:19:02 2020
@author: Mastermind
"""


def fetch_usa_bea_labor():
    '''Labor Series: H4313C0, 1929--1948'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    semi_frame_a = fetch_usa_bea(file_name, 'Section6ALL_Hist.xls', '60500A Ann', 'H4313C0')
    '''Labor Series: J4313C0, 1948--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    semi_frame_b = fetch_usa_bea(file_name, 'Section6ALL_Hist.xls', '60500B Ann', 'J4313C0')
    '''Labor Series: J4313C0, 1969--1987'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    semi_frame_c = fetch_usa_bea(file_name, 'Section6all_xls.xls', '60500B Ann', 'J4313C0')
    '''Labor Series: A4313C0, 1987--2000'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    semi_frame_d = fetch_usa_bea(file_name, 'Section6all_xls.xls', '60500C Ann', 'A4313C0')
    '''Labor Series: N4313C0, 1998--2011'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    semi_frame_e = fetch_usa_bea(file_name, 'Section6all_xls.xls', '60500D Ann', 'N4313C0')
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e], axis=1, sort=True)

    result_frame = result_frame.mean(1)
    result_frame = result_frame.to_frame(name='Labor')
    return result_frame


def fetch_usa_frb_cu():
    '''Indexed Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
    CAPUTL.B50001.A Fetching'''
    file_name = 'dataset_usa_FRB_G17_All_Annual 2013-06-23.csv'
    series_id = 'CAPUTLB50001A'
    data_frame = pd.read_csv(file_name, skiprows=1, usecols=range(5, 100))
    data_frame.columns = ['period', *data_frame.columns[1:]]
    data_frame.iloc[:,0] = data_frame.iloc[:,0].str.replace(r"[,@\'?\.$%_]",
                                                            '',
                                                            regex=True)
    data_frame = data_frame.set_index(data_frame.columns[0]).transpose()
    data_frame.index = pd.to_numeric(data_frame.index, downcast='integer')
    return data_frame.loc[:, [series_id]].dropna()


def get_dataset_version_a():
    """Returns  result_frame_a: Capital, Labor, Product;
                result_frame_b: Capital, Labor, Product Adjusted to Capacity Utilisation"""
    '''Data Fetch Archived'''
    '''Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_a = fetch_usa_bea(file_name, 'Section4ALL_xls.xls', '402 Ann', 'kcn31gd1es000')
    """Labor"""
    semi_frame_b = fetch_usa_bea_labor()
    '''Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10106 Ann', 'A191RX1')
    """Real Gross Domestic Product Series, 2005=100: A191RX1, 1969--2012"""
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10106 Ann', 'A191RX1')
    semi_frame_c = sub_frame_a.append(sub_frame_b).drop_duplicates()
    '''Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012'''
    semi_frame_d = fetch_usa_frb_cu()
    result_frame_a = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c], axis=1, sort=True).dropna()
    result_frame_b = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d], axis=1, sort=True).dropna()

    result_frame_b.iloc[:, 2] = result_frame_b.iloc[:, 2].div(result_frame_b.iloc[:, 3]/100)
    result_frame_b = result_frame_b[result_frame_b.columns[[0, 1, 2]]]
    result_frame_a = result_frame_a.div(result_frame_a.iloc[0, :])
    result_frame_b = result_frame_b.div(result_frame_b.iloc[0, :])
    return result_frame_a, result_frame_b


def get_dataset_version_b():
    """Returns  result_frame_a: Capital, Labor, Product;
                result_frame_b: Capital, Labor, Product;
                result_frame_c: Capital, Labor, Product Adjusted to Capacity Utilisation"""
    base = 38 # # 1967=100
    '''Data Fetch Revised'''
    '''Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_a = fetch_usa_bea(file_name, 'Section4ALL_xls.xls', '402 Ann', 'kcn31gd1es000')
    """Labor"""
    semi_frame_b = fetch_usa_bea_labor()
    '''Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018'''
    semi_frame_c = fetch_usa_frb_ip()
    '''Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012'''
    semi_frame_d = fetch_usa_frb_cu()
    result_frame_a = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c], axis=1, sort=True).dropna()
    result_frame_b = result_frame_a[base:]
    result_frame_c = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d], axis=1, sort=True).dropna()
    result_frame_c.iloc[:, 2] = result_frame_c.iloc[:, 2].div(result_frame_c.iloc[:, 3]/100)
    result_frame_c = result_frame_c[result_frame_c.columns[[0, 1, 2]]]
    result_frame_a = result_frame_a.div(result_frame_a.iloc[0, :])
    result_frame_b = result_frame_b.div(result_frame_b.iloc[0, :])
    result_frame_c = result_frame_c.div(result_frame_c.iloc[0, :])
    return result_frame_a, result_frame_b, result_frame_c


def bln_to_mln(data_frame, column):
    '''Convert Series in Billions of Dollars to Series in Millions of Dollars'''
    data_frame.iloc[:, column] = 1000*data_frame.iloc[:, column]
    return data_frame


def fetch_capital_purchases():
    file_name = 'dataset_usa_cobb-douglas.zip'
    semi_frame_a = fetch_classic(file_name, 'CDT2S1') # Nominal
    file_name = 'dataset_usa_cobb-douglas.zip'
    semi_frame_b = fetch_classic(file_name, 'CDT2S3') # # 1880=100
    file_name = 'dataset_douglas.zip'
    semi_frame_c = fetch_classic(file_name, 'DT63AS01') # # 1880=100
    file_name = 'dataset_douglas.zip'
    semi_frame_d = fetch_classic(file_name, 'DT63AS02') # # Do Not Use
    file_name = 'dataset_douglas.zip'
    semi_frame_e = fetch_classic(file_name, 'DT63AS03') # # Do Not Use
    file_name = 'dataset_usa_census1949.zip'
    semi_frame_f = fetch_census(file_name, 'J0149') # Nominal
    file_name = 'dataset_usa_census1949.zip'
    semi_frame_g = fetch_census(file_name, 'J0150') # Nominal
    file_name = 'dataset_usa_census1949.zip'
    semi_frame_h = fetch_census(file_name, 'J0151') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_i = fetch_census(file_name, 'P0107') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_j = fetch_census(file_name, 'P0108') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_k = fetch_census(file_name, 'P0109') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_l = fetch_census(file_name, 'P0110') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_m = fetch_census(file_name, 'P0111') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_n = fetch_census(file_name, 'P0112') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_o = fetch_census(file_name, 'P0113') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_p = fetch_census(file_name, 'P0114') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_q = fetch_census(file_name, 'P0115') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_r = fetch_census(file_name, 'P0116') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_s = fetch_census(file_name, 'P0117') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_t = fetch_census(file_name, 'P0118') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_u = fetch_census(file_name, 'P0119') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_v = fetch_census(file_name, 'P0120') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_w = fetch_census(file_name, 'P0121') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_x = fetch_census(file_name, 'P0122') # 1958=100
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e, \
                           semi_frame_f, semi_frame_g, semi_frame_h, semi_frame_i, semi_frame_j, \
                           semi_frame_k, semi_frame_l, semi_frame_m, semi_frame_n, semi_frame_o, \
                           semi_frame_p, semi_frame_q, semi_frame_r, semi_frame_s, semi_frame_t, \
                           semi_frame_u, semi_frame_v, semi_frame_w, semi_frame_x], axis=1, sort=True)
    result_frame = result_frame[12:]
    for i in range(8, 24):
        result_frame = bln_to_mln(result_frame, i)
    result_frame['total'] = result_frame.iloc[:, [0, 5, 8]].mean(1)
    result_frame['structures'] = result_frame.iloc[:, [6, 9]].mean(1)
    result_frame['equipment'] = result_frame.iloc[:, [7, 10]].mean(1)
    result_frame.iloc[:, 24] = signal.wiener(result_frame.iloc[:, 24]).round()
    result_frame.iloc[:, 25] = signal.wiener(result_frame.iloc[:, 25]).round()
    result_frame.iloc[:, 26] = signal.wiener(result_frame.iloc[:, 26]).round()
    return result_frame


def plot_capital_purchases(source_frame):
    plt.figure()
    plt.semilogy(source_frame.index, source_frame.iloc[:, 0], linewidth = 3, label='$s^{2;1}_{Cobb-Douglas}$')
    plt.semilogy(source_frame.index, source_frame.iloc[:, 24], label='Total')
    plt.semilogy(source_frame.index, source_frame.iloc[:, 25], label='Structures')
    plt.semilogy(source_frame.index, source_frame.iloc[:, 26], label='Equipment')
    plt.title('Fixed Assets Purchases')
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.legend()
    plt.grid(True)
    plt.show()


def cobb_douglas_alternative(source_frame):
    '''Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    source_frame.index: Period,
    source_frame.iloc[:, 0]: Capital,
    source_frame.iloc[:, 1]: Labor,
    source_frame.iloc[:, 2]: Product,
    source_frame.iloc[:, 3]: Alternative Product
    '''
    figures_dict = {'figure_a':'Chart I Progress in Manufacturing %d$-$%d (%d=100)',
                'figure_b':'Chart II Theoretical and Actual Curves of Production %d$-$%d (%d=100)',
                'figure_c':'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines = 3 Year Moving Average',
                'figure_d':'Chart IV Percentage Deviations of Computed from Actual Product %d$-$%d'}
    X = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])
    Y = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1])
    X = np.log(X)
    Y = np.log(Y)
    f1p = np.polyfit(X, Y, 1)
    a1, a0 = f1p # # Original: a1 = 0.25
    a0 = np.exp(a0)
    PP = a0*(source_frame.iloc[:, 1]**(1-a1))*(source_frame.iloc[:, 0]**a1)
    PR = source_frame.iloc[:, 2].rolling(window=3, center=True).mean()
    PPR = PP.rolling(window=3, center=True).mean()
    YX = source_frame.iloc[:, 3].div(source_frame.iloc[:, 1])
    YX = np.log(YX)
    f1px = np.polyfit(X, YX, 1)
    B01, B00 = f1px # # Original: a1 = 0.25
    B00 = np.exp(B00)
    PPX = B00*(source_frame.iloc[:, 1]**(1-B01))*(source_frame.iloc[:, 0]**B01)
    PRX = source_frame.iloc[:, 3].rolling(window=3, center=True).mean()
    PPRX = PPX.rolling(window=3, center=True).mean()
    plt.figure(1)
    plt.plot(source_frame.index, source_frame.iloc[:, 0], label='Fixed Capital')
    plt.plot(source_frame.index, source_frame.iloc[:, 1], label='Labor Force')
    plt.plot(source_frame.index, source_frame.iloc[:, 2], label='Physical Product')
    plt.plot(source_frame.index, source_frame.iloc[:, 3], label='Physical Product, Alternative')
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(figures_dict['figure_a'] %(source_frame.index[0], source_frame.index[-1], source_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(source_frame.index, source_frame.iloc[:, 3], label='Actual Product')
    plt.plot(source_frame.index, PPX, label='Computed Product, $P\' = %fL^{%f}C^{%f}$' %(B00, 1-B01, B01))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(figures_dict['figure_b'] %(source_frame.index[0], source_frame.index[-1], source_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(source_frame.index, source_frame.iloc[:, 3]-PRX, label='Deviations of $P$')
    plt.plot(source_frame.index, PPX-PPRX, '--', label='Deviations of $P\'$')
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(figures_dict['figure_c'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(source_frame.index, PPX.div(source_frame.iloc[:, 3])-1)
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(figures_dict['figure_d'] %(source_frame.index[0], source_frame.index[-1]))
    plt.grid(True)
    plt.show()


def procedure(source_frame):
    '''Cobb-Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928'''
    '''Scipy Signal Median Filter, Non-Linear Low-Pass Filter'''
    X = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])
    Y = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1])

    X = signal.medfilt(X)
    Y = signal.medfilt(Y)
    X = np.log(X)
    Y = np.log(Y)
    f1p = np.polyfit(X, Y, 1)
    A01, A00 = f1p # # Original: A01 = 0.25
    A00 = np.exp(A00)
    PP = A00*(source_frame.iloc[:, 1]**(1-A01))*(source_frame.iloc[:, 0]**A01)
    PR = source_frame.iloc[:, 2].rolling(window=3, center=True).mean()
    PPR = PP.rolling(window=3, center=True).mean()
    plt.figure(1)
    plt.plot(source_frame.iloc[:, 0], label='Fixed Capital')
    plt.plot(source_frame.iloc[:, 1], label='Labor Force')
    plt.plot(source_frame.iloc[:, 2], label='Physical Product')
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title('Chart I Progress in Manufacturing %d$-$%d (%d=100)' %(source_frame.index[0], source_frame.index[-1], source_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(source_frame.iloc[:, 2], label='Actual Product')
    plt.plot(source_frame.index, PP, label='Computed Product, $P\' = %fL^{%f}C^{%f}$' %(A00, 1-A01, A01))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title('Chart II Theoretical and Actual Curves of Production %d$-$%d (%d=100)' %(source_frame.index[0], source_frame.index[-1], source_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(source_frame.iloc[:, 2]-PR, label='Deviations of $P$')
    plt.plot(source_frame.index, PP-PPR, '--', label='Deviations of $P\'$')
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title('Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines = 3 Year Moving Average')
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(source_frame.index, PP.div(source_frame.iloc[:, 2])-1)
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title('Chart IV Percentage Deviations of Computed from Actual Product %d$-$%d' %(source_frame.index[0], source_frame.index[-1]))
    plt.grid(True)
    plt.show()


def procedure_numbers(data_frame):
    '''
    data_frame.index: Period,
    data_frame.iloc[:, 0]: Capital,
    data_frame.iloc[:, 1]: Labor,
    data_frame.iloc[:, 2]: Product
    '''
    data_frame.reset_index(level=0, inplace=True)
    T = data_frame.iloc[:, 0]
    X = data_frame.iloc[:, 1].div(data_frame.iloc[:, 2]) # # Labor Capital Intensity
    Y = data_frame.iloc[:, 3].div(data_frame.iloc[:, 2]) # # Labor Productivity
    YP1P0 = np.array([1.0, 1.0])
    def func(T, A1, A0):
        return A1*T**A0


    numbers, matrix = optimization.curve_fit(func, X, Y, YP1P0)
    print('Factor: {:,.4f}; Index: {:,.4f}'.format(numbers[0], numbers[1]))


print(__doc__)
"""Project I. Classified"""
source_frame = get_dataset_cobb_douglas()
result_frame_a = source_frame.iloc[:,range(4)]
result_frame_b = source_frame[source_frame.columns[[0, 1, 2, 4]]]
cobb_douglas_alternative(result_frame_a)
cobb_douglas_alternative(result_frame_b)

result_frame_a = source_frame[source_frame.columns[[0, 1, 2]]]
result_frame_b = source_frame[source_frame.columns[[0, 1, 3]]]
result_frame_c = source_frame[source_frame.columns[[0, 1, 4]]]
result_frame_d, result_frame_e = get_dataset_version_a()
result_frame_f, result_frame_g, result_frame_h = get_dataset_version_b()
result_frame_i = dataset_version_c()
procedure_numbers(result_frame_a)
procedure_numbers(result_frame_b)
procedure_numbers(result_frame_c)
procedure_numbers(result_frame_d)
procedure_numbers(result_frame_e)
procedure_numbers(result_frame_f)
procedure_numbers(result_frame_g)
procedure_numbers(result_frame_h)
procedure_numbers(result_frame_i)
procedure_numbers(result_frame_a)
procedure_numbers(result_frame_b)
procedure_numbers(result_frame_c)
"""    No Capacity Utilization Adjustment"""
procedure_numbers(result_frame_d)
"""    Capacity Utilization Adjustment"""
procedure_numbers(result_frame_e)
"""    Option: 1929--2013, No Capacity Utilization Adjustment"""
procedure_numbers(result_frame_f)
"""    Option: 1967--2013, No Capacity Utilization Adjustment"""
procedure_numbers(result_frame_g)
"""    Option: 1967--2012, Capacity Utilization Adjustment"""
procedure_numbers(result_frame_h)
procedure_numbers(result_frame_i)
"""Project II. Scipy Signal Median Filter, Non-Linear Low-Pass Filter"""
procedure(result_frame_a)
procedure(result_frame_b)
procedure(result_frame_c)
procedure(result_frame_d)
procedure(result_frame_e)
procedure(result_frame_f)
procedure(result_frame_g)
procedure(result_frame_h)
procedure(result_frame_i)
procedure(result_frame_a)
procedure(result_frame_b)
procedure(result_frame_c)
"""Project III. Scipy Signal Wiener Filter"""
purchases_frame = fetch_capital_purchases()
plot_capital_purchases(purchases_frame)