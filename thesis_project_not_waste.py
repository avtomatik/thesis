# -*- coding: utf-8 -*-
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
# =============================================================================
# Fixed Assets Series: K160021, 1951--1969
# =============================================================================
# file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
# sub_frame_a = fetch_usa_bea(file_name, 'Section5ALL_Hist.xls', '50900 Ann', 'K160021')


def get_data_usa_xlsm():
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
    )
    SH_NAMES = (
        '10105 Ann',
        '10105 Ann',
        '10106 Ann',
        '10705 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        'A191RC1',
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        'A191RX1',
        # =====================================================================
        # Nominal National income Series: A032RC1, 1929--2011
        # =====================================================================
        'A032RC1',
    )
    _data = pd.concat(
        [
            pd.concat(
                [fetch_usa_bea(ARCHIVE_NAMES[0], WB_NAMES[0], _sh, _id)
                 for _sh, _id in zip(SH_NAMES, SERIES_IDS)],
                axis=1,
                sort=True
            ),
            pd.concat(
                [fetch_usa_bea(ARCHIVE_NAMES[1], WB_NAMES[1], _sh, _id)
                 for _sh, _id in zip(SH_NAMES, SERIES_IDS)],
                axis=1,
                sort=True
            ),
        ],
        sort=True).drop_duplicates()
    FILE_NAME = 'dataset_usa_0025_p_r.txt'
    return pd.concat(
        [
            _data,
            pd.read_csv(FILE_NAME, index_col=0)
        ],
        axis=1,
        sort=True
    )


# =============================================================================
# Gross fixed capital formation Data Block
# =============================================================================
'''Not Clear: v62143969 - 380-0068 Gross fixed capital formation; Canada; Chained (2007) dollars; Seasonally adjusted at annual rates; Industrial\
machinery and equipment (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)'''
'''Not Clear: v62143990 - 380-0068 Gross fixed capital formation; Canada; Chained (2007) dollars; Seasonally adjusted at annual rates; Industrial\
machinery and equipment (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)'''
# fetch_can_quarterly('03800068', 'v62143969')
# fetch_can_quarterly('03800068', 'v62143990')
# fetch_can_group_b('5245628780870031920', 3)
# fetch_can_group_a('7931814471809016759', 241)
# fetch_can_group_a('8448814858763853126', 81)
# =============================================================================
# Not Clear
# =============================================================================
# file_name = 'dataset_can_cansim-{}-eng-{}.csv'.format(0310003, 7591839622055840674)
# frame = pd.read_csv(file_name, skiprows=3)
# =============================================================================
# Unallocated
# =============================================================================
# =============================================================================
# Fixed Assets Series: k3n31gd1es000, 1947--2011
# =============================================================================
file_name = 'dataset_usa_bea-sfat-release-2012-08-15-SectionAll_xls.zip'
semi_frame_c = fetch_usa_bea(
    file_name, 'Section3ALL_xls.xls', '303ES Ann', 'k3n31gd1es000')
# =============================================================================
# Nominal Gross Domestic Product Series: A191RC1, 1929--1969
# =============================================================================
file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip'
sub_frame_a = fetch_usa_bea(
    file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
# =============================================================================
# Nominal Gross Domestic Product Series: A191RC1, 1969--2014
# =============================================================================
file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip'
sub_frame_b = fetch_usa_bea(
    file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
semi_frame_d = sub_frame_a.append(sub_frame_b).drop_duplicates()


def get_dataset_can():
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
    SERIES_IDS = ('v43975603', 'v43977683', 'v43978099', 'v43978515',
                  'v43978931', 'v43979347', 'v43979763', 'v43980179',
                  'v43980595', 'v43976019', 'v43976435', 'v43976851',
                  'v43977267', 'v43975594', 'v43977674', 'v43978090',
                  'v43978506', 'v43978922', 'v43979338', 'v43979754',
                  'v43980170', 'v43980586', 'v43976010', 'v43976426',
                  'v43976842', 'v43977258',)
    '''2.1. Fixed Assets Block, Alternative Option Not Used'''
    '''2.1.1. Chained (2007) dollars'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1,000,000): `v43980803`, `v43981843`, `v43982051`, `v43982259`, `v43982467`, `v43982675`, `v43982883`, `v43983091`, `v43983299`, \
    `v43981011`, `v43981219`, `v43981427`, `v43981635`'''
    '''Industrial machinery (x 1,000,000): `v43980794`, `v43981834`, `v43982042`, `v43982250`, `v43982458`, `v43982666`, `v43982874`, `v43983082`, `v43983290`, \
    `v43981002`, `v43981210`, `v43981418`, `v43981626`'''
    # SERIES_IDS = ('v43980803', 'v43981843', 'v43982051', 'v43982259',
    #               'v43982467', 'v43982675', 'v43982883', 'v43983091',
    #               'v43983299', 'v43981011', 'v43981219', 'v43981427',
    #               'v43981635', 'v43980794', 'v43981834', 'v43982042',
    #               'v43982250', 'v43982458', 'v43982666', 'v43982874',
    #               'v43983082', 'v43983290', 'v43981002', 'v43981210',
    #               'v43981418', 'v43981626',)
    '''2.1.2. Current prices'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1,000,000): `v43975395`, `v43977475`, `v43977891`, `v43978307`, `v43978723`, `v43979139`, `v43979555`, `v43979971`, `v43980387`, \
    `v43975811`, `v43976227`, `v43976643`, `v43977059`'''
    '''Industrial machinery (x 1,000,000): `v43975386`, `v43977466`, `v43977882`, `v43978298`, `v43978714`, `v43979130`, `v43979546`, `v43979962`, `v43980378`, \
    `v43975802`, `v43976218`, `v43976634`, `v43977050`'''
    # SERIES_IDS = ('v43975395', 'v43977475', 'v43977891', 'v43978307',
    #               'v43978723', 'v43979139', 'v43979555', 'v43979971',
    #               'v43980387', 'v43975811', 'v43976227', 'v43976643',
    #               'v43977059', 'v43975386', 'v43977466', 'v43977882',
    #               'v43978298', 'v43978714', 'v43979130', 'v43979546',
    #               'v43979962', 'v43980378', 'v43975802', 'v43976218',
    #               'v43976634', 'v43977050',)
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
    result_frame.rename(
        columns={'v2523012': 'labor', 0: 'capital', 'v65201809': 'product'}, inplace=True)
    return result_frame.reset_index(level=0, inplace=True)


def options():
    ARCHIVE_NAME = 'dataset_douglas.zip'
    SERIES_IDS = (
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01',
        # =====================================================================
        # Not Suitable: Total Capital (in millions of 1880 dollars)
        # =====================================================================
        'DT63AS01',
        # =====================================================================
        # Not Suitable: Annual Increase (in millions of 1880 dollars)
        # =====================================================================
        'DT63AS02',
        # =====================================================================
        # Not Suitable: Percentage Rate of Growth
        # =====================================================================
        'DT63AS03',
    )
    [
        print(extract_usa_classic(ARCHIVE_NAME, series_id))
        for series_id in SERIES_IDS
    ]


def get_dataset_common_archived():
    """Data Fetch"""
# =============================================================================
# Fixed Assets Series: k1n31gd1es000, 1925--2016
# =============================================================================
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_a = fetch_usa_bea(
        file_name, 'Section4ALL_xls.xls', '401 Ann', 'k1n31gd1es000')
# =============================================================================
# Fixed Assets Series: k1ntotl1si000, 1925--2016
# =============================================================================
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_b = fetch_usa_bea(
        file_name, 'Section2ALL_xls.xls', '201 Ann', 'k1ntotl1si000')
# =============================================================================
# Fixed Assets Series: k3n31gd1es000, 1925--2016
# =============================================================================
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_c = fetch_usa_bea(
        file_name, 'Section4ALL_xls.xls', '403 Ann', 'k3n31gd1es000')
# =============================================================================
# Fixed Assets Series: k3ntotl1si000, 1925--2016
# =============================================================================
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_d = fetch_usa_bea(
        file_name, 'Section2ALL_xls.xls', '203 Ann', 'k3ntotl1si000')
# =============================================================================
# Fixed Assets Series: K160491, 1951--1969
# =============================================================================
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(
        file_name, 'Section5ALL_Hist.xls', '50900 Ann', 'K160491')
# =============================================================================
# Fixed Assets Series: K160491, 1969--2011
# =============================================================================
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(
        file_name, 'Section5all_xls.xls', '50900 Ann', 'K160491')
    semi_frame_e = sub_frame_a.append(sub_frame_b).drop_duplicates()

    semi_frame_f = get_dataset_usa_bea_labor()
# =============================================================================
# National Income: A032RC1, 1929--1969
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(
        file_name, 'Section1ALL_Hist.xls', '11200 Ann', 'A032RC1')
# =============================================================================
# National Income: A032RC1, 1969--2013
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip'
    sub_frame_b = fetch_usa_bea(
        file_name, 'Section1all_xls.xls', '11200 Ann', 'A032RC1')
    semi_frame_g = sub_frame_a.append(sub_frame_b).drop_duplicates()

# =============================================================================
# Nominal Gross Domestic Product Series: A191RC1, 1929--1969
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(
        file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
# =============================================================================
# Nominal Gross Domestic Product Series: A191RC1, 1969--2014
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip'
    sub_frame_b = fetch_usa_bea(
        file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
    semi_frame_h = sub_frame_a.append(sub_frame_b).drop_duplicates()

# =============================================================================
# Real Gross Domestic Product Series: A191RX1, 1929--1969, 2009=100
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(
        file_name, 'Section1ALL_Hist.xls', '10106 Ann', 'A191RX1')
# =============================================================================
# Real Gross Domestic Product Series: A191RX1, 1969--2014, 2009=100
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip'
    sub_frame_b = fetch_usa_bea(
        file_name, 'Section1all_xls.xls', '10106 Ann', 'A191RX1')
    semi_frame_i = sub_frame_a.append(sub_frame_b).drop_duplicates()

# =============================================================================
# Nominal Gross Domestic Product Series: A191RC1, 1929--1969
# =============================================================================
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(
        file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
# =============================================================================
# Nominal Gross Domestic Product Series: A191RC1, 1969--2012
# =============================================================================
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(
        file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
    semi_frame_j = sub_frame_a.append(sub_frame_b).drop_duplicates()

# =============================================================================
# Deflator Gross Domestic Product, A191RD3, 1929--1969, 2009=100
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(
        file_name, 'Section1ALL_Hist.xls', '10109 Ann', 'A191RD3')
# =============================================================================
# Deflator Gross Domestic Product, A191RD3, 1969--2014, 2009=100'''
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip'
    sub_frame_b = fetch_usa_bea(
        file_name, 'Section1all_xls.xls', '10109 Ann', 'A191RD3')
    semi_frame_k = sub_frame_a.append(sub_frame_b).drop_duplicates()

    semi_frame_k.iloc[:, 0] = 100/semi_frame_k.iloc[:, 0]
# =============================================================================
# Real Gross Domestic Product Series: A191RX1, 1929--1969, 2005=100
# =============================================================================
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(
        file_name, 'Section1ALL_Hist.xls', '10106 Ann', 'A191RX1')
# =============================================================================
# Real Gross Domestic Product Series: A191RX1, 1969--2012, 2005=100
# =============================================================================
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(
        file_name, 'Section1all_xls.xls', '10106 Ann', 'A191RX1')
    semi_frame_l = sub_frame_a.append(sub_frame_b).drop_duplicates()

# =============================================================================
# Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
# =============================================================================
    semi_frame_m = get_dataset_usa_frb_cu()
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e,
                              semi_frame_f, semi_frame_g, semi_frame_h, semi_frame_i, semi_frame_j,
                              semi_frame_k, semi_frame_l, semi_frame_m], axis=1, sort=True)
    return result_frame


def get_data_capital_combined_archived():
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH_NAMES = (
        '10105 Ann',
        '10106 Ann',
        '50900 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        'A191RC1',
        # =====================================================================
        # Real Gross Domestic Product Series: A191RX1, 1929--2012
        # =====================================================================
        'A191RX1',
        # =====================================================================
        # U.S. Bureau of Economic Analysis, Produced assets, closing balance: Fixed assets (DISCONTINUED) [K160491A027NBEA], retrieved from FRED, Federal Reserve Bank of St. Louis;
        # https://fred.stlouisfed.org/series/K160491A027NBEA, August 23, 2018.
        # http://www.bea.gov/data/economic-accounts/national
        # https://fred.stlouisfed.org/series/K160491A027NBEA
        # https://search.bea.gov/search?affiliate=u.s.bureauofeconomicanalysis&query=k160491
        # =====================================================================
        # =====================================================================
        # Fixed Assets Series: K160021, 1951--2011
        # =====================================================================
        'K160021',
        # =====================================================================
        # Fixed Assets Series: K160491, 1951--2011
        # =====================================================================
        'K160491',
    )
    _data = pd.concat(
        [
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVE_NAMES[0], _wb, _sh, _id)
                    for _wb, _sh, _id in zip(
                        tuple(WB_NAMES[2*(_ // len(SH_NAMES))]
                              for _ in range(len(SERIES_IDS))),
                        tuple(SH_NAMES[2*(_ // len(SH_NAMES)) + ((_ - 1) % len(SH_NAMES)) *
                                       (2 - ((_ - 1) % len(SH_NAMES)))] for _ in range(len(SERIES_IDS))),
                        SERIES_IDS,
                    )
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVE_NAMES[1], _wb, _sh, _id)
                    for _wb, _sh, _id in zip(
                        tuple(WB_NAMES[1 + 2*(_ // len(SH_NAMES))]
                              for _ in range(len(SERIES_IDS))),
                        tuple(SH_NAMES[2*(_ // len(SH_NAMES)) + ((_ - 1) % len(SH_NAMES)) *
                                       (2 - ((_ - 1) % len(SH_NAMES)))] for _ in range(len(SERIES_IDS))),
                        SERIES_IDS,
                    )
                ],
                axis=1,
                sort=True
            ),
        ],
        sort=True).drop_duplicates()
    return pd.concat(
        [_data,
         # ====================================================================
         # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
         # ====================================================================
         get_data_usa_frb_cu(),
         # ====================================================================
         # Manufacturing Labor Series: _4313C0, 1929--2011
         # ====================================================================
         get_data_usa_bea_labor_mfg(),
         # ====================================================================
         # Labor Series: A4601C0, 1929--2011
         # ====================================================================
         get_data_usa_bea_labor()], axis=1, sort=True)


os.chdir('/media/alexander/321B-6A94')
test_douglas('J0014', 'DT24AS01')
test_douglas('CDT2S4', 'DT63AS01')
