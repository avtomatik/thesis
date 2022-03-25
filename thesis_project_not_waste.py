#-*- coding: utf-8 -*-
"""
Created on Fri Nov  8 23:41:12 2019

@author: Mastermind
"""

# =============================================================================
# Section5ALL_Hist
# =============================================================================
# =============================================================================
# www.bea.gov/histdata/Releases/GDP_and_PI/2012/Q1/Second_May-31-2012/Section5ALL_Hist.xls
# =============================================================================
# =============================================================================
# Metadata: `Section5ALL_Hist.xls`@[`dataset_usa_bea-release-2010-08-05 Section5ALL_Hist.xls` Offsets `dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip`]'''
# =============================================================================
# '''Fixed Assets Series: K160021, 1951--1969'''
# file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
# sub_frame_a = fetch_usa_bea_single(file_name, 'Section5ALL_Hist.xls', '50900 Ann', 'K160021')
def cobb_douglas_original(frame):
    '''Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    frame.index: Period,
    frame.iloc[:, 0]: Capital,
    frame.iloc[:, 1]: Labor,
    frame.iloc[:, 2]: Product
    '''
    figures_dict = {'figure_a':'Chart I Progress in Manufacturing %d$-$%d (%d=100)',
                  'figure_b':'Chart II Theoretical and Actual Curves of Production %d$-$%d (%d=100)',
                  'figure_c':'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines = 3 Year Moving Average',
                  'figure_d':'Chart IV Percentage Deviations of Computed from Actual Product %d$-$%d'}
    X = frame.iloc[:, 0].div(frame.iloc[:, 1])
    Y = frame.iloc[:, 2].div(frame.iloc[:, 1])

    X = sp.log(X)
    Y = sp.log(Y)
    f1p = sp.polyfit(X, Y, 1)
    a1, a0 = f1p # # Original: a1 = 0.25
    a0 = sp.exp(a0)
    PP = a0*(frame.iloc[:, 1]**(1-a1))*(frame.iloc[:, 0]**a1)
    PR = frame.iloc[:, 2].rolling(window=3, center=True).mean()
    PPR = PP.rolling(window=3, center=True).mean()

    fig, axs = plt.subplots(4, 1)
    axs[0].plot(frame.index, frame.iloc[:, 0], label='Fixed Capital')
    axs[0].plot(frame.index, frame.iloc[:, 1], label='Labor Force')
    axs[0].plot(frame.index, frame.iloc[:, 2], label='Physical Product')
    axs[0].set_xlabel('Period')
    axs[0].set_ylabel('Indexes')
    axs[0].set_title(figures_dict['figure_a'] %(frame.index[0], frame.index[frame.shape[0]-1], frame.index[0]))
    axs[0].legend()
    axs[0].grid(True)
    axs[1].plot(frame.index, frame.iloc[:, 2], label='Actual Product')
    axs[1].plot(frame.index, PP, label='Computed Product, $P\' = %fL^{%f}C^{%f}$' %(a0, 1-a1, a1))
    axs[1].set_xlabel('Period')
    axs[1].set_ylabel('Production')
    axs[1].set_title(figures_dict['figure_b'] %(frame.index[0], frame.index[frame.shape[0]-1], frame.index[0]))
    axs[1].legend()
    axs[1].grid(True)
    axs[2].plot(frame.index, frame.iloc[:, 2]-PR, label='Deviations of $P$')
    axs[2].plot(frame.index, PP-PPR, '--', label='Deviations of $P\'$')
    axs[2].set_xlabel('Period')
    axs[2].set_ylabel('Percentage Deviation')
    axs[2].set_title(figures_dict['figure_c'])
    axs[2].legend()
    axs[2].grid(True)
    axs[3].plot(frame.index, PP.div(frame.iloc[:, 2])-1)
    axs[3].set_xlabel('Period')
    axs[3].set_ylabel('Percentage Deviation')
    axs[3].set_title(figures_dict['figure_d'] %(frame.index[0], frame.index[frame.shape[0]-1]))
    axs[3].grid(True)
    plt.tight_layout()
    plt.savefig('view.pdf', format = 'pdf', dpi = 900)
    plt.show()


def plot_kzf_b(source_frame):
    """Kolmogorov--Zurbenko Filter
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Series"""


    """DataFrame for Kolmogorov--Zurbenko Filter Results"""
    result_frame_a = source_frame
    """DataFrame for Kolmogorov--Zurbenko Filter Residuals"""
    result_frame_b = pd.concat([source_frame.iloc[:, 0], source_frame.iloc[:, 0].rolling(window=2).mean()], axis=1, sort=False)
    result_frame_b = pd.concat([result_frame_b, (source_frame.iloc[:, 1]-source_frame.iloc[:, 1].shift(1)).div(source_frame.iloc[:, 1].shift(1))], axis=1, sort=False)
    series = source_frame.iloc[:, 1]
    for i in range(1, 1 + source_frame.shape[0]//2):
        series = series.rolling(window=2).mean()
        skz = series.shift(-(i//2))
        result_frame_a = pd.concat([result_frame_a, skz], axis=1, sort=False)
        if i%2 ==0:
            result_frame_b = pd.concat([result_frame_b, (skz-skz.shift(1)).div(skz.shift(1))], axis=1, sort=False)
        else:
            result_frame_b = pd.concat([result_frame_b, (skz.shift(-1)-skz).div(skz)], axis=1, sort=False)
    plt.figure(1)
    plt.title('Kolmogorov$-$Zurbenko Filter')
    plt.xlabel('Period')
    plt.ylabel('Measure')
    plt.scatter(result_frame_a.iloc[:, 0], result_frame_a.iloc[:, 1], label='Original Series')
    for i in range(2, 1 + source_frame.shape[0]//2):
        if i%2 ==0:
            plt.plot(result_frame_a.iloc[:, 0].rolling(window=2).mean(), result_frame_a.iloc[:, i], label='$KZF(\\lambda = {})$'.format(i-1))
        else:
            plt.plot(result_frame_a.iloc[:, 0], result_frame_a.iloc[:, i], label='$KZF(\\lambda = {})$'.format(i-1))
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Kolmogorov$-$Zurbenko Filter Residuals')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(result_frame_b.iloc[:, 1], result_frame_b.iloc[:, 2], label='Residuals')
    for i in range(3, 2 + source_frame.shape[0]//2):
        if i%2 ==0:
            plt.plot(result_frame_b.iloc[:, 1], result_frame_b.iloc[:, i], label='$\\delta KZF(\\lambda = {})$'.format(i-1))
        else:
            plt.plot(result_frame_b.iloc[:, 0], result_frame_b.iloc[:, i], label='$\\delta KZF(\\lambda = {})$'.format(i-1))
    plt.grid(True)
    plt.legend()
    plt.show()


def data_fetch_usa_xlsm():
    '''Indexed'''


    '''Nominal Investment Series: A006RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A006RC1')
    '''Nominal Investment Series: A006RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10105 Ann', 'A006RC1')
    semi_frame_a = sub_frame_a.append(sub_frame_b)

    '''Nominal National income Series: A032RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10705 Ann', 'A032RC1')
    '''Nominal National income Series: A032RC1, 1969--2011'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10705 Ann', 'A032RC1')
    semi_frame_b = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Nominal Nominal Gross Domestic Product Series: A191RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
    '''Nominal Nominal Gross Domestic Product Series: A191RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
    semi_frame_c = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10106 Ann', 'A191RX1')
    '''Real Gross Domestic Product Series, 2005=100: A191RX1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10106 Ann', 'A191RX1')
    semi_frame_d = sub_frame_a.append(sub_frame_b).drop_duplicates()

    file_name = 'dataset_usa_0025_p_r.txt'
    semi_frame_e = pd.read_csv(file_name)
    semi_frame_e.columns = semi_frame_e.columns.str.title()
    semi_frame_e = semi_frame_e.set_index('Period')
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e], axis=1, sort=True).dropna(how='all')
    return result_frame


# # '''https://stackoverflow.com/questions/32788526/python-scipy-kolmogorov-zurbenko-filter'''


# # def kz(series, window, iterations):
# #    """KZ filter implementation
# #    series is a pandas series
# #    window is the filter window m in the units of the data (m = 1 + 2q)
# #    iterations is the number of times the moving average is evaluated
# #    """
# #    z = series.copy()
# #    for i in range(iterations):
# #        z = pd.rolling_mean(z, window=window, min_periods = 1, center=True)
# #    return z
    # # plt.savefig('NBER-CESmean.pdf', format = 'pdf', dpi = 900)
    # # plt.savefig('NBER-CESsum.pdf', format = 'pdf', dpi = 900)
# os.chdir('/media/alexander/321B-6A94')
# plt.figure(1).savefig('figure_1.pdf')
# plt.figure(2).savefig('figure_2.pdf')
# plt.figure(3).savefig('figure_3.pdf')
# plt.figure(4).savefig('figure_4.pdf')
'''Gross fixed capital formation Data Block'''
'''Not Clear: v62143969 - 380-0068 Gross fixed capital formation; Canada; Chained (2007) dollars; Seasonally adjusted at annual rates; Industrial\
machinery and equipment (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)'''
'''Not Clear: v62143990 - 380-0068 Gross fixed capital formation; Canada; Chained (2007) dollars; Seasonally adjusted at annual rates; Industrial\
machinery and equipment (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)'''
# # fetch_can_quarterly('03800068', 'v62143969')
# # fetch_can_quarterly('03800068', 'v62143990')
# # fetch_can_group_b('5245628780870031920', 3)
# # fetch_can_group_a('7931814471809016759', 241)
# # fetch_can_group_a('8448814858763853126', 81)
'''Not Clear'''
file_name = 'dataset_can_cansim-{}-eng-{}.csv'.format(0310003, 7591839622055840674)
# # frame = pd.read_csv(file_name, skiprows=3)
# #
'''Unallocated'''
'''Fixed Assets Series: k3n31gd1es000, 1947--2011'''
file_name = 'dataset_usa_bea-sfat-release-2012-08-15-SectionAll_xls.zip'
semi_frame_c = fetch_usa_bea_single(file_name, 'Section3ALL_xls.xls', '303ES Ann', 'k3n31gd1es000')
# =============================================================================
# Nominal Gross Domestic Product Series: A191RC1, 1929--1969
# =============================================================================
file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip'
sub_frame_a = fetch_usa_bea_single(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
# =============================================================================
# Nominal Gross Domestic Product Series: A191RC1, 1969--2014
# =============================================================================
file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip'
sub_frame_b = fetch_usa_bea_single(file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
semi_frame_d = sub_frame_a.append(sub_frame_b).drop_duplicates()

semi_frame_d = semi_frame_d.set_index('Period')


def dataset_canada():
    '''Number 1. CANSIM Table 282-0012 Labour Force Survey Estimates (LFS), employment by class of worker, North American Industry Classification\
    System (NAICS) and sex'''
    '''Number 2. CANSIM Table 03790031'''
    '''Title: Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS)'''
    '''Measure: monthly (dollars x 1,000,000)'''
    '''Number 3. CANSIM Table 03800068'''
    '''Title: Gross fixed capital formation'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 4. CANSIM Table 031-0004: Flows and stocks of fixed non-residential capital, total all industries, by asset, provinces and territories, \
    annual (dollars x 1,000,000)'''
    '''Number 5. CANSIM Table 03790028'''
    '''Title: Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS), provinces and territories'''
    '''Measure: annual (percentage share)'''
    '''Number 6. CANSIM Table 03800001'''
    '''Title: Gross domestic product (GDP), income-based, *Terminated*'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 7. CANSIM Table 03800002'''
    '''Title: Gross domestic product (GDP), expenditure-based, *Terminated*'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 8. CANSIM Table 03800063'''
    '''Title: Gross domestic product, income-based'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 9. CANSIM Table 03800064'''
    '''Title: Gross domestic product, expenditure-based'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 10. CANSIM Table 03800069'''
    '''Title: Investment in inventories'''
    '''Measure: quarterly (dollars unless otherwise noted)'''
    '''---'''
    '''1.0. Labor Block: `v2523012`, Preferred Over `v3437501` Which Is Quarterly'''
    '''`v2523012` - 282-0012 Labour Force Survey Estimates (LFS), employment by class of worker, North American Industry Classification System (NAICS)\
    and sex; Canada; Total employed, all class of workers; Manufacturing; Both sexes (x 1,000) (annual, 1987 to 2017)'''
    labor = fetch_can_annually('02820012', 'v2523012')
    '''1.1. Labor Block, Alternative Option Not Used'''
    '''`v3437501` - 282-0011 Labour Force Survey estimates (LFS), employment by class of worker, North American Industry Classification System (NAICS)\
    and sex, unadjusted for seasonality; Canada; Total employed, all classes of workers; Manufacturing; Both sexes (x 1,000) (monthly, 1987-01-01 to\
    2017-12-01)'''
    # # fetch_can_quarterly('02820011', 'v3437501')
    '''2.i. Fixed Assets Block: `Industrial buildings`, `Industrial machinery` for `Newfoundland and Labrador`, `Prince Edward Island`, `Nova Scotia`, `New Brunswick`, \
    `Quebec`, `Ontario`, `Manitoba`, `Saskatchewan`, `Alberta`, `British Columbia`, `Yukon`, `Northwest Territories`, `Nunavut`'''
    '''2.0. 2007 constant prices'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1,000,000): `v43975603`, `v43977683`, `v43978099`, `v43978515`, `v43978931`, `v43979347`, `v43979763`, `v43980179`, `v43980595`, \
    `v43976019`, `v43976435`, `v43976851`, `v43977267`'''
    '''Industrial machinery (x 1,000,000): `v43975594`, `v43977674`, `v43978090`, `v43978506`, `v43978922`, `v43979338`, `v43979754`, `v43980170`, `v43980586`, \
    `v43976010`, `v43976426`, `v43976842`, `v43977258`'''
    S = ('v43975603', 'v43977683', 'v43978099', 'v43978515', 'v43978931', 'v43979347', 'v43979763', 'v43980179', 'v43980595', 'v43976019', 'v43976435', 'v43976851', \
       'v43977267', 'v43975594', 'v43977674', 'v43978090', 'v43978506', 'v43978922', 'v43979338', 'v43979754', 'v43980170', 'v43980586', 'v43976010', 'v43976426', \
       'v43976842', 'v43977258')
    '''2.1. Fixed Assets Block, Alternative Option Not Used'''
    '''2.1.1. Chained (2007) dollars'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1,000,000): `v43980803`, `v43981843`, `v43982051`, `v43982259`, `v43982467`, `v43982675`, `v43982883`, `v43983091`, `v43983299`, \
    `v43981011`, `v43981219`, `v43981427`, `v43981635`'''
    '''Industrial machinery (x 1,000,000): `v43980794`, `v43981834`, `v43982042`, `v43982250`, `v43982458`, `v43982666`, `v43982874`, `v43983082`, `v43983290`, \
    `v43981002`, `v43981210`, `v43981418`, `v43981626`'''
    # # AS1 = ('v43980803', 'v43981843', 'v43982051', 'v43982259', 'v43982467', 'v43982675', 'v43982883', 'v43983091', 'v43983299', 'v43981011', 'v43981219', 'v43981427', \
    # #     'v43981635', 'v43980794', 'v43981834', 'v43982042', 'v43982250', 'v43982458', 'v43982666', 'v43982874', 'v43983082', 'v43983290', 'v43981002', 'v43981210', \
    # #     'v43981418', 'v43981626')
    '''2.1.2. Current prices'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1,000,000): `v43975395`, `v43977475`, `v43977891`, `v43978307`, `v43978723`, `v43979139`, `v43979555`, `v43979971`, `v43980387`, \
    `v43975811`, `v43976227`, `v43976643`, `v43977059`'''
    '''Industrial machinery (x 1,000,000): `v43975386`, `v43977466`, `v43977882`, `v43978298`, `v43978714`, `v43979130`, `v43979546`, `v43979962`, `v43980378`, \
    `v43975802`, `v43976218`, `v43976634`, `v43977050`'''
    # # AS2 = ('v43975395', 'v43977475', 'v43977891', 'v43978307', 'v43978723', 'v43979139', 'v43979555', 'v43979971', 'v43980387', 'v43975811', 'v43976227', 'v43976643', \
    # #     'v43977059', 'v43975386', 'v43977466', 'v43977882', 'v43978298', 'v43978714', 'v43979130', 'v43979546', 'v43979962', 'v43980378', 'v43975802', 'v43976218', \
    # #     'v43976634', 'v43977050')
    capital = fetch_can_fixed_assets(fetch_can_capital_query_archived())
    '''3.i. Production Block: `v65201809`, Preferred Over `v65201536` Which Is Quarterly'''
    '''3.0. Production Block: `v65201809`'''
    '''`v65201809` - 379-0031 Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS); Canada; Trading-day\
    adjusted; 2007 constant prices; Manufacturing (x 1,000,000) (monthly, 1997-01-01 to 2017-10-01)'''
    product = fetch_can_quarterly('03790031', 'v65201809')
    '''3.1. Production Block: `v65201536`, Alternative Option Not Used'''
    '''`v65201536` - 379-0031 Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS); Canada; Seasonnaly\
    adjusted at annual rates; 2007 constant prices; Manufacturing (x 1,000,000) (monthly, 1997-01-01 to 2017-10-01)'''
    # # fetch_can_quarterly('03790031', 'v65201536')

    result_frame = pd.concat([labor, capital, product], axis=1, sort=True)
    result_frame = result_frame.dropna()
    result_frame.rename(columns={'v2523012':'labor', 0:'capital', 'v65201809':'product'}, inplace=True)
    return result_frame.reset_index(level=0, inplace=True)


def test_douglas(control, series_ids):
    '''control from Original Dataset;
    series_ids from Douglas Theory of Wages'''
    if control =='CDT2S4':
        control_frame = fetch_classic('dataset_usa_cobb-douglas.zip', 'CDT2S4') # # Total Fixed Capital in 1880 dollars (4)
    elif control =='J0014':
        control_frame = fetch_census('dataset_usa_census1949.zip', 'J0014')
    test_frame = fetch_classic('dataset_douglas.zip', series_ids)
    if control =='J0014':
        control_frame.iloc[:, 0] = 100*control_frame.iloc[:, 0].div(control_frame.iloc[36, 0]) # # 1899=100
        control_frame.iloc[:, 0] = control_frame.iloc[:, 0].round(0)
    else:
        pass
    control_frame = pd.concat([control_frame, test_frame], axis=1, sort=True)
    if control =='J0014':
        control_frame['dev'] = control_frame.iloc[:, 1]-control_frame.iloc[:, 0]
    elif control =='CDT2S4':
        control_frame['dev'] = control_frame.iloc[:, 0].div(control_frame.iloc[:, 1])
    else:
        pass
    control_frame = control_frame.dropna()
#    control_frame.plot(title = 'Cobb--Douglas Data Comparison', legend=True, grid=True)
    print(control_frame)


def options():
    '''The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926'''
    file_name = 'dataset_douglas.zip'
    fetch_classic(file_name, 'DT24AS01')
    '''Not Suitable: Total Capital (in millions of 1880 dollars)'''
    fetch_classic(file_name, 'DT63AS01')
    '''Not Suitable: Annual Increase (in millions of 1880 dollars)'''
    fetch_classic(file_name, 'DT63AS02')
    '''Not Suitable: Percentage Rate of Growth'''
    fetch_classic(file_name, 'DT63AS03')


def data_fetch_common_archived():
    """Data Fetch"""
    """Fixed Assets Series: k1n31gd1es000, 1925--2016"""
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_a = fetch_usa_bea_single(file_name, 'Section4ALL_xls.xls', '401 Ann', 'k1n31gd1es000')
    """Fixed Assets Series: k1ntotl1si000, 1925--2016"""
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_b = fetch_usa_bea_single(file_name, 'Section2ALL_xls.xls', '201 Ann', 'k1ntotl1si000')
    """Fixed Assets Series: k3n31gd1es000, 1925--2016"""
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_c = fetch_usa_bea_single(file_name, 'Section4ALL_xls.xls', '403 Ann', 'k3n31gd1es000')
    """Fixed Assets Series: k3ntotl1si000, 1925--2016"""
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_d = fetch_usa_bea_single(file_name, 'Section2ALL_xls.xls', '203 Ann', 'k3ntotl1si000')
    """Fixed Assets Series: K160491, 1951--1969"""
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea_single(file_name, 'Section5ALL_Hist.xls', '50900 Ann', 'K160491')
    """Fixed Assets Series: K160491, 1969--2011"""
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea_single(file_name, 'Section5all_xls.xls', '50900 Ann', 'K160491')
    semi_frame_e = sub_frame_a.append(sub_frame_b).drop_duplicates()

    semi_frame_f = fetch_usa_bea_labor()
# =============================================================================
# National Income: A032RC1, 1929--1969
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea_single(file_name, 'Section1ALL_Hist.xls', '11200 Ann', 'A032RC1')
# =============================================================================
# National Income: A032RC1, 1969--2013
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip'
    sub_frame_b = fetch_usa_bea_single(file_name, 'Section1all_xls.xls', '11200 Ann', 'A032RC1')
    semi_frame_g = sub_frame_a.append(sub_frame_b).drop_duplicates()

    semi_frame_g = semi_frame_g.set_index('Period')
# =============================================================================
# Nominal Gross Domestic Product Series: A191RC1, 1929--1969
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea_single(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
# =============================================================================
# Nominal Gross Domestic Product Series: A191RC1, 1969--2014
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip'
    sub_frame_b = fetch_usa_bea_single(file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
    semi_frame_h = sub_frame_a.append(sub_frame_b).drop_duplicates()

    semi_frame_h = semi_frame_h.set_index('Period')
# =============================================================================
# Real Gross Domestic Product Series: A191RX1, 1929--1969, 2009=100
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea_single(file_name, 'Section1ALL_Hist.xls', '10106 Ann', 'A191RX1')
# =============================================================================
# Real Gross Domestic Product Series: A191RX1, 1969--2014, 2009=100
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip'
    sub_frame_b = fetch_usa_bea_single(file_name, 'Section1all_xls.xls', '10106 Ann', 'A191RX1')
    semi_frame_i = sub_frame_a.append(sub_frame_b).drop_duplicates()

    semi_frame_i = semi_frame_i.set_index('Period')
    """Nominal Gross Domestic Product Series: A191RC1, 1929--1969"""
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea_single(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
    """Nominal Gross Domestic Product Series: A191RC1, 1969--2012"""
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea_single(file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
    semi_frame_j = sub_frame_a.append(sub_frame_b).drop_duplicates()

# =============================================================================
# Deflator Gross Domestic Product, A191RD3, 1929--1969, 2009=100
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea_single(file_name, 'Section1ALL_Hist.xls', '10109 Ann', 'A191RD3')
# =============================================================================
# Deflator Gross Domestic Product, A191RD3, 1969--2014, 2009=100'''
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip'
    sub_frame_b = fetch_usa_bea_single(file_name, 'Section1all_xls.xls', '10109 Ann', 'A191RD3')
    semi_frame_k = sub_frame_a.append(sub_frame_b).drop_duplicates()

    semi_frame_k = semi_frame_k.set_index('Period')
    semi_frame_k.iloc[:, 0] = 100/semi_frame_k.iloc[:, 0]
    """Real Gross Domestic Product Series: A191RX1, 1929--1969, 2005=100"""
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea_single(file_name, 'Section1ALL_Hist.xls', '10106 Ann', 'A191RX1')
    """Real Gross Domestic Product Series: A191RX1, 1969--2012, 2005=100"""
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea_single(file_name, 'Section1all_xls.xls', '10106 Ann', 'A191RX1')
    semi_frame_l = sub_frame_a.append(sub_frame_b).drop_duplicates()

    """Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012"""
    semi_frame_m = fetch_usa_frb_cu()
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e, \
                           semi_frame_f, semi_frame_g, semi_frame_h, semi_frame_i, semi_frame_j, \
                           semi_frame_k, semi_frame_l, semi_frame_m], axis=1, sort=True)
    return result_frame


def capital_combined_archived():
    '''Nominal Investment Series: A006RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea_single(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A006RC1') # # Through Year of 1968 Instead of 1969
    '''Nominal Investment Series: A006RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea_single(file_name, 'Section1all_xls.xls', '10105 Ann', 'A006RC1')
    semi_frame_a = sub_frame_a.append(sub_frame_b)

    '''Nominal Gross Domestic Product Series: A191RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea_single(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
    '''Nominal Gross Domestic Product Series: A191RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea_single(file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
    semi_frame_b = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Real Gross Domestic Product Series: A191RX1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea_single(file_name, 'Section1ALL_Hist.xls', '10106 Ann', 'A191RX1')
    '''Real Gross Domestic Product Series: A191RX1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea_single(file_name, 'Section1all_xls.xls', '10106 Ann', 'A191RX1')
    semi_frame_c = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012'''
    semi_frame_d = fetch_usa_frb_cu()
    '''U.S. Bureau of Economic Analysis, Produced assets, closing balance: Fixed assets (DISCONTINUED) [K160491A027NBEA], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/K160491A027NBEA, August 23, 2018.
    http://www.bea.gov/data/economic-accounts/national
    https://fred.stlouisfed.org/series/K160491A027NBEA
    https://search.bea.gov/search?affiliate = u.s.bureauofeconomicanalysis&query=k160491'''
    '''Fixed Assets Series: K160021, 1951--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea_single(file_name, 'Section5ALL_Hist.xls', '50900 Ann', 'K160021')
    '''Fixed Assets Series: K160021, 1969--2011'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea_single(file_name, 'Section5all_xls.xls', '50900 Ann', 'K160021')
    semi_frame_e = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Fixed Assets Series: K160491, 1951--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea_single(file_name, 'Section5ALL_Hist.xls', '50900 Ann', 'K160491')
    '''Fixed Assets Series: K160491, 1969--2011'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea_single(file_name, 'Section5all_xls.xls', '50900 Ann', 'K160491')
    semi_frame_f = sub_frame_a.append(sub_frame_b).drop_duplicates()

    semi_frame_g = fetch_usa_bea_labor()
    '''Labor Series: A4601C0, 1929--1948'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea_single(file_name, 'Section6ALL_Hist.xls', '60800A Ann', 'A4601C0')
    '''Labor Series: A4601C0, 1948--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_b = fetch_usa_bea_single(file_name, 'Section6ALL_Hist.xls', '60800B Ann', 'A4601C0')
    '''Labor Series: A4601C0, 1969--1987'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_c = fetch_usa_bea_single(file_name, 'Section6all_xls.xls', '60800B Ann', 'A4601C0')
    '''Labor Series: A4601C0, 1987--2000'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_d = fetch_usa_bea_single(file_name, 'Section6all_xls.xls', '60800C Ann', 'A4601C0')
    '''Labor Series: A4601C0, 1998--2011'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_e = fetch_usa_bea_single(file_name, 'Section6all_xls.xls', '60800D Ann', 'A4601C0')
    semi_frame_h = sub_frame_a.append(sub_frame_b).append(sub_frame_c).append(sub_frame_d).append(sub_frame_e).drop_duplicates()

    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e,
                           semi_frame_f, semi_frame_g, semi_frame_h], axis=1, sort=True).dropna(how='all')
    return result_frame


def fetch_usa_bea_single(archive_name, wb_name, sh_name, series_id):
# =============================================================================
# TODO: Eliminate This Function
# =============================================================================
# =============================================================================
# Data Frame Fetching from Bureau of Economic Analysis Zip Archives
# =============================================================================
    with pd.ExcelFile(ZipFile(archive_name, 'r').open(wb_name)) as xl_file:
# =============================================================================
#         Load
# =============================================================================
        data_frame = pd.read_excel(xl_file, sh_name, skiprows=7)
# =============================================================================
#         Re-Load
# =============================================================================
        data_frame = pd.read_excel(xl_file,
                                   sh_name,
                                   usecols=range(2, data_frame.shape[1]),
                                   skiprows=7)
    data_frame.dropna(inplace=True)
    data_frame.columns = ['period', *data_frame.columns[1:]]
    data_frame = data_frame.set_index(data_frame.columns[0]).transpose()
    return data_frame.loc[:, [series_id]]


os.chdir('/media/alexander/321B-6A94')
test_douglas('J0014', 'DT24AS01')
test_douglas('CDT2S4', 'DT63AS01')

