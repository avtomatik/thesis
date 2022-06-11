# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 22:19:02 2020
@author: Mastermind
"""


def get_data_usa_bea_labor_mfg():
    # =========================================================================
    # Manufacturing Labor Series: H4313C0, 1929--1948
    # Manufacturing Labor Series: J4313C0, 1948--1969
    # Manufacturing Labor Series: J4313C0, 1969--1987
    # Manufacturing Labor Series: A4313C0, 1987--2000
    # Manufacturing Labor Series: N4313C0, 1998--2011
    # =========================================================================
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section6ALL_Hist.xls',
        'Section6ALL_Hist.xls',
        'Section6all_xls.xls',
        'Section6all_xls.xls',
        'Section6all_xls.xls',
    )
    SH_NAMES = (
        '60500A Ann',
        '60500B Ann',
        '60500B Ann',
        '60500C Ann',
        '60500D Ann',
    )
    SERIES_IDS = (
        'H4313C0',
        'J4313C0',
        'J4313C0',
        'A4313C0',
        'N4313C0',
    )
    data_frame = pd.concat(
        [
            extract_usa_bea(archive_name, wb, sh, _id)
            for archive_name, wb, sh, _id in zip(ARCHIVE_NAMES, WB_NAMES, SH_NAMES, SERIES_IDS)
        ],
        axis=1,
        sort=True)
    data_frame['mfg_labor'] = data_frame.mean(axis=1)
    return data_frame.iloc[:, [-1]].dropna(axis=0)


def get_dataset_usa_frb_cu():
    '''Indexed Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
    CAPUTL.B50001.A Fetching'''
    file_name = 'dataset_usa_FRB_G17_All_Annual 2013-06-23.csv'
    series_id = 'CAPUTLB50001A'
    data_frame = pd.read_csv(file_name, skiprows=1, usecols=range(5, 100))
    data_frame.columns = ['period', *data_frame.columns[1:]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].str.replace(r"[,@\'?\.$%_]",
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
    semi_frame_a = fetch_usa_bea(
        file_name, 'Section4ALL_xls.xls', '402 Ann', 'kcn31gd1es000')
    """Labor"""
    semi_frame_b = get_dataset_usa_bea_labor()
    '''Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(
        file_name, 'Section1ALL_Hist.xls', '10106 Ann', 'A191RX1')
    """Real Gross Domestic Product Series, 2005=100: A191RX1, 1969--2012"""
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(
        file_name, 'Section1all_xls.xls', '10106 Ann', 'A191RX1')
    semi_frame_c = sub_frame_a.append(sub_frame_b).drop_duplicates()
    '''Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012'''
    semi_frame_d = get_dataset_usa_frb_cu()
    result_frame_a = pd.concat(
        [semi_frame_a, semi_frame_b, semi_frame_c], axis=1, sort=True).dropna()
    result_frame_b = pd.concat(
        [semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d], axis=1, sort=True).dropna()

    result_frame_b.iloc[:, 2] = result_frame_b.iloc[:, 2].div(
        result_frame_b.iloc[:, 3]).mul(100)
    result_frame_b = result_frame_b.iloc[:, [0, 1, 2]]
    result_frame_a = result_frame_a.div(result_frame_a.iloc[0, :])
    result_frame_b = result_frame_b.div(result_frame_b.iloc[0, :])
    return result_frame_a, result_frame_b


def get_dataset_version_b():
    """Returns  result_frame_a: Capital, Labor, Product;
                result_frame_b: Capital, Labor, Product;
                result_frame_c: Capital, Labor, Product Adjusted to Capacity Utilisation"""
    '''Data Fetch Revised'''
    # =============================================================================
    # Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
    # =============================================================================
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_a = fetch_usa_bea(
        FILE_NAME, 'Section4ALL_xls.xls', '402 Ann', 'kcn31gd1es000')
    # =============================================================================
    # Labor
    # =============================================================================
    semi_frame_b = get_dataset_usa_bea_labor()
    # =============================================================================
    # Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018
    # =============================================================================
    semi_frame_c = get_dataset_usa_frb_ip()
    # =============================================================================
    # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
    # =============================================================================
    semi_frame_d = get_dataset_usa_frb_cu()
    result_frame_a = pd.concat(
        [semi_frame_a, semi_frame_b, semi_frame_c], axis=1, sort=True).dropna()
    result_frame_b = result_frame_a[result_frame_a.index.get_loc(1967):]
    result_frame_c = pd.concat(
        [semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d], axis=1, sort=True).dropna()
    result_frame_c.iloc[:, 2] = result_frame_c.iloc[:, 2].div(
        result_frame_c.iloc[:, 3]).mul(100)
    result_frame_c = result_frame_c.iloc[:, [0, 1, 2]]
    result_frame_a = result_frame_a.div(result_frame_a.iloc[0, :])
    result_frame_b = result_frame_b.div(result_frame_b.iloc[0, :])
    result_frame_c = result_frame_c.div(result_frame_c.iloc[0, :])
    return result_frame_a, result_frame_b, result_frame_c


def get_dataset_capital_purchases():
    FILE_NAMES = (
        # =====================================================================
        # CDT2S1: Nominal; CDT2S3: 1880=100;
        # =====================================================================
        'dataset_usa_cobb-douglas.zip',
        # =====================================================================
        # DT63AS01: 1880=100; DT63AS02: Do Not Use; DT63AS03: Do Not Use;
        # =====================================================================
        'dataset_douglas.zip',)
    SERIES_IDS = ('CDT2S1', 'CDT2S3', 'DT63AS01', 'DT63AS02', 'DT63AS03',)
    _args = [tuple(((FILE_NAMES[0], FILE_NAMES[1])[series_id.startswith(
        'DT')], series_id,)) for series_id in SERIES_IDS]
    _data_frame = pd.concat(
        [fetch_classic(*arg) for arg in _args],
        axis=1,
        sort=True)

    FILE_NAMES = (
        # =====================================================================
        # Nominal Series, USD Millions
        # =====================================================================
        'dataset_usa_census1949.zip',
        # =====================================================================
        # P0107, P0108, P0109, P0113, P0114, P0115 -- Nominal Series, USD Billions
        # P0110, P0111, P0112, P0116, P0117, P0118, P0119, P0120, P0121, P0122 -- Real Series, 1958=100, USD Billions
        # =====================================================================
        'dataset_usa_census1975.zip',)
    SERIES_IDS = (
        'J0149', 'J0150', 'J0151', 'P0107', 'P0108', 'P0109', 'P0110',
        'P0111', 'P0112', 'P0113', 'P0114', 'P0115', 'P0116', 'P0117',
        'P0118', 'P0119', 'P0120', 'P0121', 'P0122',
    )
    _args = [(tuple((FILE_NAMES[0], series_id, 1,)), tuple((FILE_NAMES[1], series_id, 1000,)))[
        series_id.startswith('P')] for series_id in SERIES_IDS]
    data_frame_ = pd.concat(
        [fetch_census(*_[:2]).mul(_[-1]) for _ in _args],
        axis=1,
        sort=True)
    data_frame = pd.concat([_data_frame, data_frame_], axis=1, sort=True)
    data_frame = data_frame[data_frame.index.get_loc(1875):]
    data_frame['total'] = data_frame.loc[:, [
        'CDT2S1', 'J0149', 'P0107']].mean(1)
    data_frame['struc'] = data_frame.loc[:, ['J0150', 'P0108']].mean(1)
    data_frame['equip'] = data_frame.loc[:, ['J0151', 'P0109']].mean(1)
    data_frame.iloc[:, -3] = signal.wiener(data_frame.iloc[:, -3]).round()
    data_frame.iloc[:, -2] = signal.wiener(data_frame.iloc[:, -2]).round()
    data_frame.iloc[:, -1] = signal.wiener(data_frame.iloc[:, -1]).round()
    return data_frame


def plot_capital_purchases(source_frame):
    plt.figure()
    plt.semilogy(source_frame.iloc[:, 0], linewidth=3,
                 label='$s^{2;1}_{Cobb-Douglas}$')
    plt.semilogy(source_frame.iloc[:, 24], label='Total')
    plt.semilogy(source_frame.iloc[:, 25], label='Structures')
    plt.semilogy(source_frame.iloc[:, 26], label='Equipment')
    plt.title('Fixed Assets Purchases')
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_cobb_douglas_alternative(data_frame):
    '''Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    data_frame.index: Period,
    data_frame.iloc[:, 0]: Capital,
    data_frame.iloc[:, 1]: Labor,
    data_frame.iloc[:, 2]: Product,
    data_frame.iloc[:, 3]: Alternative Product
    '''
    FIGURES = {
        'fig_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
        'fig_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
        'fig_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fig_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
    }
    X = data_frame.iloc[:, 0].div(data_frame.iloc[:, 1])
    Y = data_frame.iloc[:, 2].div(data_frame.iloc[:, 1])
    X = np.log(X)
    Y = np.log(Y)
# =============================================================================
# Original: k=0.25
# =============================================================================
    k, b = np.polyfit(X, Y, 1)
    b = np.exp(b)
    PP = b*(data_frame.iloc[:, 1]**(1-k))*(data_frame.iloc[:, 0]**k)
    PR = data_frame.iloc[:, 2].rolling(window=3, center=True).mean()
    PPR = PP.rolling(window=3, center=True).mean()
    YX = data_frame.iloc[:, 3].div(data_frame.iloc[:, 1])
    YX = np.log(YX)
# =============================================================================
# Original: k=0.25
# =============================================================================
    _k, _b = np.polyfit(X, YX, 1)
    _b = np.exp(_b)
    p_p_x = _b*(data_frame.iloc[:, 1]**(1-_k))*(data_frame.iloc[:, 0]**_k)
    p_r_x = data_frame.iloc[:, 3].rolling(window=3, center=True).mean()
    PPRX = PPX.rolling(window=3, center=True).mean()
    plt.figure(1)
    plt.plot(data_frame.iloc[:, 0], label='Fixed Capital')
    plt.plot(data_frame.iloc[:, 1], label='Labor Force')
    plt.plot(data_frame.iloc[:, 2], label='Physical Product')
    plt.plot(data_frame.iloc[:, 3], label='Physical Product, Alternative')
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(FIGURES['fig_a'].format(data_frame.index[0],
                                      data_frame.index[-1],
                                      data_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(data_frame.iloc[:, 3], label='Actual Product')
    plt.plot(
        PPX, label='Computed Product, $P\' = %fL^{%f}C^{%f}$' % (_b, 1-_k, _k))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(FIGURES['fig_b'].format(data_frame.index[0],
                                      data_frame.index[-1],
                                      data_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(data_frame.iloc[:, 3].sub(PR)X, label='Deviations of $P$')
    plt.plot(PPX-PPRX, '--', label='Deviations of $P\'$')
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(FIGURES['fig_c'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(PPX.div(data_frame.iloc[:, 3]).sub(1))
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(FIGURES['fig_d'].format(data_frame.index[0],
                                      data_frame.index[-1]))
    plt.grid(True)
    plt.show()


def procedure(data_frame):
    '''Cobb-Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928'''
    '''Scipy Signal Median Filter, Non-Linear Low-Pass Filter'''
    X = data_frame.iloc[:, 0].div(data_frame.iloc[:, 1])
    Y = data_frame.iloc[:, 2].div(data_frame.iloc[:, 1])

    X = signal.medfilt(X)
    Y = signal.medfilt(Y)
    X = np.log(X)
    Y = np.log(Y)
# =============================================================================
# Original: k=0.25
# =============================================================================
    k, b = np.polyfit(X, Y, 1)
    b = np.exp(b)
    PP = b*(data_frame.iloc[:, 1]**(1-k))*(data_frame.iloc[:, 0]**k)
    PR = data_frame.iloc[:, 2].rolling(window=3, center=True).mean()
    PPR = PP.rolling(window=3, center=True).mean()
    plt.figure(1)
    plt.plot(data_frame.iloc[:, 0], label='Fixed Capital')
    plt.plot(data_frame.iloc[:, 1], label='Labor Force')
    plt.plot(data_frame.iloc[:, 2], label='Physical Product')
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title('Chart I Progress in Manufacturing %d$-$%d (%d=100)' % (data_frame.index[0],
                                                                      data_frame.index[-1],
                                                                      data_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(data_frame.iloc[:, 2], label='Actual Product')
    plt.plot(
        PP, label='Computed Product, $P\' = %fL^{%f}C^{%f}$' % (b, 1-k, k))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title('Chart II Theoretical and Actual Curves of Production %d$-$%d (%d=100)' % (data_frame.index[0],
                                                                                         data_frame.index[-1],
                                                                                         data_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(data_frame.iloc[:, 2].sub(PR), label='Deviations of $P$')
    plt.plot(PP.sub(PPR), '--', label='Deviations of $P\'$')
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title('Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines = 3 Year Moving Average')
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(PP.div(data_frame.iloc[:, 2]).sub(1))
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title('Chart IV Percentage Deviations of Computed from Actual Product %d$-$%d' % (data_frame.index[0],
                                                                                          data_frame.index[-1]))
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
    X = data_frame.iloc[:, 1].div(
        data_frame.iloc[:, 2])  # Labor Capital Intensity
    Y = data_frame.iloc[:, 3].div(data_frame.iloc[:, 2])  # Labor Productivity
    YP_1P_0 = np.array([1.0, 1.0])

    def func(T, A_1, A_0):
        return A_1*T**A_0

    numbers, matrix = optimization.curve_fit(func, X, Y, YP_1P_0)
    print('Factor: {:,.4f}; Index: {:,.4f}'.format(numbers[0], numbers[1]))


print(__doc__)
# =============================================================================
# Project I. Classified
# =============================================================================
source_frame = get_dataset_cobb_douglas()
result_frame_a = source_frame.iloc[:, range(4)]
result_frame_b = source_frame.iloc[:, [0, 1, 2, 4]]
plot_cobb_douglas_alternative(result_frame_a)
plot_cobb_douglas_alternative(result_frame_b)

result_frame_a = source_frame.iloc[:, [0, 1, 2]]
result_frame_b = source_frame.iloc[:, [0, 1, 3]]
result_frame_c = source_frame.iloc[:, [0, 1, 4]]
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
# =============================================================================
# No Capacity Utilization Adjustment
# =============================================================================
procedure_numbers(result_frame_d)
# =============================================================================
# Capacity Utilization Adjustment
# =============================================================================
procedure_numbers(result_frame_e)
# =============================================================================
# Option: 1929--2013, No Capacity Utilization Adjustment
# =============================================================================
procedure_numbers(result_frame_f)
# =============================================================================
# Option: 1967--2013, No Capacity Utilization Adjustment
# =============================================================================
procedure_numbers(result_frame_g)
# =============================================================================
# Option: 1967--2012, Capacity Utilization Adjustment
# =============================================================================
procedure_numbers(result_frame_h)
procedure_numbers(result_frame_i)
# =============================================================================
# Project II. Scipy Signal Median Filter, Non-Linear Low-Pass Filter
# =============================================================================
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
# =============================================================================
# Project III. Scipy Signal Wiener Filter
# =============================================================================
purchases_frame = get_dataset_capital_purchases()
plot_capital_purchases(purchases_frame)
