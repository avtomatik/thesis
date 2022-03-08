# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 00:13:17 2020
 
@author: Mastermind
"""

def bln_to_mln(source_frame,  column):
    """Convert Series in Billions of Dollars to Series in Millions of Dollars"""
    source_frame.iloc[:, column]  =  1000*source_frame.iloc[:, column]
    return source_frame


def fetch_census(source,  string,  index):
    """Selected Series by U.S. Bureau of the Census
    U.S. Bureau of the Census,  Historical Statistics of the United States, \
        1789--1945,  Washington,  D.C.,  1949.
    U.S. Bureau of the Census. Historical Statistics of the United States, \
        Colonial Times to 1970,  Bicentennial Edition. Washington,  D.C.,  1975."""
    import os
    import pandas as pd
    if source  ==  'census1975.zip':
        source_frame  =  pd.read_csv(source,  usecols=range(8, 11), 
                                   dtype = {'vector':str, 'period':str, 'value':str})
    else:
        source_frame  =  pd.read_csv(source,  usecols=range(8, 11))
    source_frame  =  source_frame[source_frame.iloc[:, 0] == string]
    source_frame  =  source_frame[source_frame.columns[[1, 2]]]
    if source  ==  'census1975.zip':
        source_frame.iloc[:, 0]  =  source_frame.iloc[:, 0].str[:4]
    else:
        pass
    source_frame.iloc[:, 1]  =  source_frame.iloc[:, 1].astype(float)
    source_frame.columns  =  source_frame.columns.str.title()
    source_frame.rename(columns = {'Value':string},  inplace=True)
    source_frame.iloc[:, 0]  =  source_frame.iloc[:, 0].astype(int)
    source_frame  =  source_frame.sort_values('Period')
    source_frame  =  source_frame.reset_index(drop = True)
    source_frame  =  source_frame.groupby('Period').mean()
    if index:
        return source_frame
    else:
        source_frame.reset_index(level = 0,  inplace=True)
        return source_frame


def fetch_census_description(source,  string):
    """Retrieve Series Description U.S. Bureau of the Census"""
    import pandas as pd
    source_frame  =  pd.read_csv(source,  usecols=[0, 1, 3, 4, 5, 6, 8],  low_memory = False)
    source_frame  =  source_frame[source_frame.iloc[:, 6] == string]
    source_frame.drop_duplicates(inplace=True)
    if source_frame.iloc[0, 2]  ==  'no_details':
        if source_frame.iloc[0, 5]  ==  'no_details':
            if source_frame.iloc[0, 4]  ==  'no_details':
                description  =  '{}'.format(source_frame.iloc[0, 3])
            else:
                description  =  '{} -\n{}'.format(source_frame.iloc[0, 3], 
                                                source_frame.iloc[0, 4])
        else:
            description  =  '{} -\n{} -\n{}'.format(source_frame.iloc[0, 3], 
                                                  source_frame.iloc[0, 4], 
                                                  source_frame.iloc[0, 5])
    else:
        if source_frame.iloc[0, 5]  ==  'no_details':
            if source_frame.iloc[0, 4]  ==  'no_details':
                description  =  '{}; {}'.format(source_frame.iloc[0, 3], 
                                              source_frame.iloc[0, 2])
            else:
                description  =  '{} -\n{}; {}'.format(source_frame.iloc[0, 3], 
                                                    source_frame.iloc[0, 4], 
                                                    source_frame.iloc[0, 2])
        else:
            description  =  '{} -\n{} -\n{}; {}'.format(source_frame.iloc[0, 3], 
                                                      source_frame.iloc[0, 4], 
                                                      source_frame.iloc[0, 5], 
                                                      source_frame.iloc[0, 2])
    return description


def prices_inverse_single(source_frame):
    '''Intent: Returns Prices Icrement Series from Cumulative Deflator Series;
    source: pandas Data_frame'''
    import pandas as pd
    D  =  source_frame.iloc[:, 0].div(source_frame.iloc[:, 0].shift(1))-1
    return D


def processing(source_frame,  col):
    interim_frame  =  source_frame[source_frame.columns[[col]]]
    interim_frame  =  interim_frame.dropna()
    result_frame  =  prices_inverse_single(interim_frame)
    result_frame  =  result_frame.dropna()
    return result_frame


def datafetch_census_a():
    """Census Manufacturing Indexes,  1899 = 100"""
    base  =  39 ##1899 = 100
    """HSUS 1949 Page 179,  J13"""
    semi_frame_a  =  fetch_census('census1949.zip',  'J0013',  True)
    """HSUS 1949 Page 179,  J14: Warren M. Persons,  Index of Physical Production of Manufacturing"""
    semi_frame_b  =  fetch_census('census1949.zip',  'J0014',  True)
    """HSUS 1975 Page 667,  P17: Edwin Frickey Series,  Indexes of Manufacturing Production"""
    semi_frame_c  =  fetch_census('census1975.zip',  'P0017',  True)
    result_frame  =  pd.concat([semi_frame_a,  semi_frame_b,  semi_frame_c],  axis = 1,  sort = True)
    result_frame.iloc[:, 1]  =  result_frame.iloc[:, 1].div(result_frame.iloc[base, 1]/100)
    return result_frame,  base


def datafetch_census_ba():
    """Returns Nominal Million-Dollar Capital,  Including Structures & Equipment,  Series"""
    from scipy import signal
    semi_frame_a  =  fetch_census('census1949.zip',  'J0149',  True) ##Nominal
    semi_frame_b  =  fetch_census('census1949.zip',  'J0150',  True) ##Nominal
    semi_frame_c  =  fetch_census('census1949.zip',  'J0151',  True) ##Nominal
    semi_frame_d  =  fetch_census('census1975.zip',  'P0107',  True) ##Nominal
    semi_frame_e  =  fetch_census('census1975.zip',  'P0108',  True) ##Nominal
    semi_frame_f  =  fetch_census('census1975.zip',  'P0109',  True) ##Nominal
    semi_frame_g  =  fetch_census('census1975.zip',  'P0110',  True) ##1958 = 100
    semi_frame_h  =  fetch_census('census1975.zip',  'P0111',  True) ##1958 = 100
    semi_frame_i  =  fetch_census('census1975.zip',  'P0112',  True) ##1958 = 100
    semi_frame_j  =  fetch_census('census1975.zip',  'P0113',  True) ##Nominal
    semi_frame_k  =  fetch_census('census1975.zip',  'P0114',  True) ##Nominal
    semi_frame_l  =  fetch_census('census1975.zip',  'P0115',  True) ##Nominal
    semi_frame_m  =  fetch_census('census1975.zip',  'P0116',  True) ##1958 = 100
    semi_frame_n  =  fetch_census('census1975.zip',  'P0117',  True) ##1958 = 100
    semi_frame_o  =  fetch_census('census1975.zip',  'P0118',  True) ##1958 = 100
    semi_frame_p  =  fetch_census('census1975.zip',  'P0119',  True) ##1958 = 100
    semi_frame_q  =  fetch_census('census1975.zip',  'P0120',  True) ##1958 = 100
    semi_frame_r  =  fetch_census('census1975.zip',  'P0121',  True) ##1958 = 100
    semi_frame_s  =  fetch_census('census1975.zip',  'P0122',  True) ##1958 = 100
    result_frame  =  pd.concat([semi_frame_a,  semi_frame_b,  semi_frame_c, \
                              semi_frame_d,  semi_frame_e,  semi_frame_f, \
                              semi_frame_g,  semi_frame_h,  semi_frame_i, \
                              semi_frame_j,  semi_frame_k,  semi_frame_l, \
                              semi_frame_m,  semi_frame_n,  semi_frame_o, \
                              semi_frame_p,  semi_frame_q,  semi_frame_r, \
                              semi_frame_s],  axis = 1,  sort = True)
    result_frame  =  result_frame[12:]
    for i in range(3, 19):
        result_frame  =  bln_to_mln(result_frame,  i)
    result_frame['total']        =  result_frame.iloc[:, [0, 3]].mean(1)
    result_frame['structures']   =  result_frame.iloc[:, [1, 4]].mean(1)
    result_frame['equipment']    =  result_frame.iloc[:, [2, 5]].mean(1)
#    result_frame.iloc[:, 19]  =  signal.wiener(result_frame.iloc[:, 19]).round()
#    result_frame.iloc[:, 20]  =  signal.wiener(result_frame.iloc[:, 20]).round()
#    result_frame.iloc[:, 21]  =  signal.wiener(result_frame.iloc[:, 21]).round()
    result_frame  =  result_frame[result_frame.columns[[19, 20, 21]]]
    return result_frame


def datafetch_census_bb():
    """Returns Census Fused Capital Deflator"""
    semi_frame_a  =  fetch_census('census1975.zip',  'P0107',  True) ##Nominal
    semi_frame_b  =  fetch_census('census1975.zip',  'P0108',  True) ##Nominal
    semi_frame_c  =  fetch_census('census1975.zip',  'P0109',  True) ##Nominal
    semi_frame_d  =  fetch_census('census1975.zip',  'P0110',  True) ##1958 = 100
    semi_frame_e  =  fetch_census('census1975.zip',  'P0111',  True) ##1958 = 100
    semi_frame_f  =  fetch_census('census1975.zip',  'P0112',  True) ##1958 = 100
    semi_frame_g  =  fetch_census('census1975.zip',  'P0113',  True) ##Nominal
    semi_frame_h  =  fetch_census('census1975.zip',  'P0114',  True) ##Nominal
    semi_frame_i  =  fetch_census('census1975.zip',  'P0115',  True) ##Nominal
    semi_frame_j  =  fetch_census('census1975.zip',  'P0116',  True) ##1958 = 100
    semi_frame_k  =  fetch_census('census1975.zip',  'P0117',  True) ##1958 = 100
    semi_frame_l  =  fetch_census('census1975.zip',  'P0118',  True) ##1958 = 100
    source_frame  =  pd.concat([semi_frame_a,  semi_frame_b,  semi_frame_c, \
                              semi_frame_d,  semi_frame_e,  semi_frame_f, \
                              semi_frame_g,  semi_frame_h,  semi_frame_i, \
                              semi_frame_j,  semi_frame_k,  semi_frame_l], 
                             axis = 1,  sort = True)
    del semi_frame_a,  semi_frame_b,  semi_frame_c,  semi_frame_d,  semi_frame_e, \
        semi_frame_f,  semi_frame_g,  semi_frame_h,  semi_frame_i,  semi_frame_j, \
            semi_frame_k,  semi_frame_l
    source_frame['pur_total']        =  source_frame.iloc[:, 0].div(source_frame.iloc[:, 3])
    source_frame['pur_structures']   =  source_frame.iloc[:, 1].div(source_frame.iloc[:, 4])
    source_frame['pur_equipment']    =  source_frame.iloc[:, 2].div(source_frame.iloc[:, 5])
    source_frame['dep_total']        =  source_frame.iloc[:, 6].div(source_frame.iloc[:, 9])
    source_frame['dep_structures']   =  source_frame.iloc[:, 7].div(source_frame.iloc[:, 10])
    source_frame['dep_equipment']    =  source_frame.iloc[:, 8].div(source_frame.iloc[:, 11])
    source_frame  =  source_frame[16:]
    semi_frame_a  =  processing(source_frame,  12)
    semi_frame_b  =  processing(source_frame,  13)
    semi_frame_c  =  processing(source_frame,  14)
    semi_frame_d  =  processing(source_frame,  15)
    semi_frame_e  =  processing(source_frame,  16)
    semi_frame_f  =  processing(source_frame,  17)
    interim_frame  =  pd.concat([semi_frame_a,  semi_frame_b,  semi_frame_c, \
                               semi_frame_d,  semi_frame_e,  semi_frame_f], 
                              axis = 1,  sort = True)
    del semi_frame_a,  semi_frame_b,  semi_frame_c,  semi_frame_d,  semi_frame_e, \
        semi_frame_f
    interim_frame['census_fused']  =  interim_frame.mean(1)
    result_frame  =  interim_frame[interim_frame.columns[[6]]]
    return result_frame


def datafetch_census_c():
    """Census Primary Metals & Railroad-Related Products Manufacturing Series"""
    base  =  (15, 20, 49) ## 1875 = 100,  1880 = 100,  1909 = 100
    semi_frame_a  =  fetch_census('census1975.zip',  'P0262',  True)
    semi_frame_b  =  fetch_census('census1975.zip',  'P0265',  True)
    semi_frame_c  =  fetch_census('census1975.zip',  'P0266',  True)
    semi_frame_d  =  fetch_census('census1975.zip',  'P0267',  True)
    semi_frame_e  =  fetch_census('census1975.zip',  'P0268',  True)
    semi_frame_f  =  fetch_census('census1975.zip',  'P0269',  True)
    semi_frame_g  =  fetch_census('census1975.zip',  'P0293',  True)
    semi_frame_h  =  fetch_census('census1975.zip',  'P0294',  True)
    semi_frame_i  =  fetch_census('census1975.zip',  'P0295',  True)
    result_frame  =  pd.concat([semi_frame_a,  semi_frame_b,  semi_frame_c, \
                              semi_frame_d,  semi_frame_e,  semi_frame_f, \
                              semi_frame_g,  semi_frame_h,  semi_frame_i],  axis = 1,  sort = True)
    result_frame.iloc[:, 0]  =  result_frame.iloc[:, 0].div(result_frame.iloc[base[0], 0]/100)
    result_frame.iloc[:, 1]  =  result_frame.iloc[:, 1].div(result_frame.iloc[base[0], 1]/100)
    result_frame.iloc[:, 2]  =  result_frame.iloc[:, 2].div(result_frame.iloc[base[0], 2]/100)
    result_frame.iloc[:, 3]  =  result_frame.iloc[:, 3].div(result_frame.iloc[base[0], 3]/100)
    result_frame.iloc[:, 4]  =  result_frame.iloc[:, 4].div(result_frame.iloc[base[0], 4]/100)
    result_frame.iloc[:, 5]  =  result_frame.iloc[:, 5].div(result_frame.iloc[base[2], 5]/100)
    result_frame.iloc[:, 6]  =  result_frame.iloc[:, 6].div(result_frame.iloc[base[1], 6]/100)
    result_frame.iloc[:, 7]  =  result_frame.iloc[:, 7].div(result_frame.iloc[base[0], 7]/100)
    result_frame.iloc[:, 8]  =  result_frame.iloc[:, 8].div(result_frame.iloc[base[0], 8]/100)
    return result_frame,  base


def data_fetch_plotting_census_d(series):
    """series: List for Series"""
    for i in range(len(series)):
        title  =  fetch_census_description('census1975.zip',  series[i])
        print('`{}` {}'.format(series[i],  title))
    result_frame  =  fetch_census('census1975.zip',  series[0],  True)
    result_frame  =  result_frame.div(result_frame.iloc[0, :]/100)
    for i in range(1,  len(series)):
        current_frame  =  fetch_census('census1975.zip',  series[i],  True)
        current_frame  =  current_frame.div(current_frame.iloc[0, :]/100)
        result_frame  =  pd.concat([result_frame,  current_frame],  axis = 1,  sort = True)
        del current_frame
    plt.figure()
    plt.semilogy(result_frame)
    plt.title('Series P 231$-$300. Physical Output of Selected Manufactured Commodities: {}$-${}'.format(result_frame.index[0],  result_frame.index[len(result_frame)-1]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend(series)
    plt.show()


def datafetch_census_e():
    """Census Total Immigration Series"""
    semi_frame_aa  =  fetch_census('census1975.zip',  'C0091',  True)
    semi_frame_ab  =  fetch_census('census1975.zip',  'C0092',  True)
    semi_frame_ac  =  fetch_census('census1975.zip',  'C0093',  True)
    semi_frame_ad  =  fetch_census('census1975.zip',  'C0094',  True)
    semi_frame_ae  =  fetch_census('census1975.zip',  'C0095',  True)
    semi_frame_af  =  fetch_census('census1975.zip',  'C0096',  True)
    semi_frame_ag  =  fetch_census('census1975.zip',  'C0097',  True)
    semi_frame_ah  =  fetch_census('census1975.zip',  'C0098',  True)
    semi_frame_ai  =  fetch_census('census1975.zip',  'C0099',  True)
    semi_frame_aj  =  fetch_census('census1975.zip',  'C0100',  True)
    semi_frame_ak  =  fetch_census('census1975.zip',  'C0101',  True)
    semi_frame_al  =  fetch_census('census1975.zip',  'C0103',  True)
    semi_frame_am  =  fetch_census('census1975.zip',  'C0104',  True)
    semi_frame_an  =  fetch_census('census1975.zip',  'C0105',  True)
    semi_frame_ao  =  fetch_census('census1975.zip',  'C0106',  True)
    semi_frame_ap  =  fetch_census('census1975.zip',  'C0107',  True)
    semi_frame_aq  =  fetch_census('census1975.zip',  'C0108',  True)
    semi_frame_ar  =  fetch_census('census1975.zip',  'C0109',  True)
    semi_frame_as  =  fetch_census('census1975.zip',  'C0111',  True)
    semi_frame_at  =  fetch_census('census1975.zip',  'C0112',  True)
    semi_frame_au  =  fetch_census('census1975.zip',  'C0113',  True)
    semi_frame_av  =  fetch_census('census1975.zip',  'C0114',  True)
    semi_frame_aw  =  fetch_census('census1975.zip',  'C0115',  True)
    semi_frame_ax  =  fetch_census('census1975.zip',  'C0117',  True)
    semi_frame_ay  =  fetch_census('census1975.zip',  'C0118',  True)
    semi_frame_az  =  fetch_census('census1975.zip',  'C0119',  True)
    result_frame  =  pd.concat([semi_frame_aa,  semi_frame_ab,  semi_frame_ac, \
                              semi_frame_ad,  semi_frame_ae,  semi_frame_af, \
                              semi_frame_ag,  semi_frame_ah,  semi_frame_ai, \
                              semi_frame_aj,  semi_frame_ak,  semi_frame_al, \
                              semi_frame_am,  semi_frame_an,  semi_frame_ao, \
                              semi_frame_ap,  semi_frame_aq,  semi_frame_ar, \
                              semi_frame_as,  semi_frame_at,  semi_frame_au, \
                              semi_frame_av,  semi_frame_aw,  semi_frame_ax, \
                              semi_frame_ay,  semi_frame_az],  axis = 1,  sort = True)
    del semi_frame_aa,  semi_frame_ab,  semi_frame_ac,  semi_frame_ad,  semi_frame_ae, \
        semi_frame_af,  semi_frame_ag,  semi_frame_ah,  semi_frame_ai,  semi_frame_aj, \
        semi_frame_ak,  semi_frame_al,  semi_frame_am,  semi_frame_an,  semi_frame_ao, \
        semi_frame_ap,  semi_frame_aq,  semi_frame_ar,  semi_frame_as,  semi_frame_at, \
        semi_frame_au,  semi_frame_av,  semi_frame_aw,  semi_frame_ax,  semi_frame_ay, \
        semi_frame_az
    result_frame['C89']  =  result_frame.sum(1)
    result_frame  =  result_frame[result_frame.columns[[result_frame.shape[1]-1]]]
    return result_frame


def datafetch_census_f():
    """Census Employment Series"""
    semi_frame_a  =  fetch_census('census1975.zip',  'D0085',  True)
    semi_frame_b  =  fetch_census('census1975.zip',  'D0086',  True)
    semi_frame_c  =  fetch_census('census1975.zip',  'D0796',  True)
    semi_frame_d  =  fetch_census('census1975.zip',  'D0797',  True)
    semi_frame_e  =  fetch_census('census1975.zip',  'D0977',  True)
    semi_frame_f  =  fetch_census('census1975.zip',  'D0982',  True)
    result_frame  =  pd.concat([semi_frame_a,  semi_frame_b,  semi_frame_c, \
                              semi_frame_d,  semi_frame_e,  semi_frame_f], 
                             axis = 1,  sort = True)
    del semi_frame_a,  semi_frame_b,  semi_frame_c,  semi_frame_d,  semi_frame_e, \
        semi_frame_f
    result_frame['workers']  =  result_frame.iloc[:, 0].div(result_frame.iloc[:, 1]/100)
    result_frame.iloc[:, 4].fillna(result_frame.iloc[:25, 4].mean(),  inplace=True)
    result_frame.iloc[:, 5].fillna(result_frame.iloc[:25, 5].mean(),  inplace=True)
    return result_frame


def datafetch_census_g():
    """Census Gross National Product Series"""
    semi_frame_aa  =  fetch_census('census1975.zip',  'F0003',  True)
    semi_frame_ab  =  fetch_census('census1975.zip',  'F0004',  True)
    result_frame  =  pd.concat([semi_frame_aa,  semi_frame_ab],  axis = 1,  sort = True)
    del semi_frame_aa,  semi_frame_ab
    result_frame  =  result_frame[2:]
    result_frame  =  result_frame.div(result_frame.iloc[0, :]/100)
    return result_frame


def data_fetch_plotting_census_h():
    """Census 1975,  Land in Farms"""
    result_frame  =  fetch_census('census1975.zip',  'K0005',  True)
    plt.figure()
    plt.plot(result_frame.index,  result_frame.iloc[:, 0])
    plt.title('Land in Farms')
    plt.xlabel('Period')
    plt.ylabel('1, 000 acres')
    plt.grid()
    plt.show()


def datafetch_census_i():
    """Census Foreign Trade Series"""
    semi_frame_aa  =  fetch_census('census1975.zip',  'U0001',  True)
    semi_frame_ab  =  fetch_census('census1975.zip',  'U0008',  True)
    result_frame_a  =  pd.concat([semi_frame_aa,  semi_frame_ab],  axis = 1,  sort = True)
    del semi_frame_aa,  semi_frame_ab
    semi_frame_aa  =  fetch_census('census1975.zip',  'U0187',  True)
    semi_frame_ab  =  fetch_census('census1975.zip',  'U0188',  True)
    semi_frame_ac  =  fetch_census('census1975.zip',  'U0189',  True)
    result_frame_b  =  pd.concat([semi_frame_aa,  semi_frame_ab,  semi_frame_ac], 
                               axis = 1,  sort = True)
    del semi_frame_aa,  semi_frame_ab,  semi_frame_ac
    semi_frame_aa  =  fetch_census('census1975.zip',  'U0319',  True)
    semi_frame_ab  =  fetch_census('census1975.zip',  'U0320',  True)
    semi_frame_ac  =  fetch_census('census1975.zip',  'U0321',  True)
    semi_frame_ad  =  fetch_census('census1975.zip',  'U0322',  True)
    semi_frame_ae  =  fetch_census('census1975.zip',  'U0323',  True)
    semi_frame_af  =  fetch_census('census1975.zip',  'U0325',  True)
    semi_frame_ag  =  fetch_census('census1975.zip',  'U0326',  True)
    semi_frame_ah  =  fetch_census('census1975.zip',  'U0327',  True)
    semi_frame_ai  =  fetch_census('census1975.zip',  'U0328',  True)
    semi_frame_aj  =  fetch_census('census1975.zip',  'U0330',  True)
    semi_frame_ak  =  fetch_census('census1975.zip',  'U0331',  True)
    semi_frame_al  =  fetch_census('census1975.zip',  'U0332',  True)
    semi_frame_am  =  fetch_census('census1975.zip',  'U0333',  True)
    semi_frame_an  =  fetch_census('census1975.zip',  'U0334',  True)
    semi_frame_ao  =  fetch_census('census1975.zip',  'U0337',  True)
    semi_frame_ap  =  fetch_census('census1975.zip',  'U0338',  True)
    semi_frame_aq  =  fetch_census('census1975.zip',  'U0339',  True)
    semi_frame_ar  =  fetch_census('census1975.zip',  'U0340',  True)
    semi_frame_as  =  fetch_census('census1975.zip',  'U0341',  True)
    semi_frame_at  =  fetch_census('census1975.zip',  'U0343',  True)
    semi_frame_au  =  fetch_census('census1975.zip',  'U0344',  True)
    semi_frame_av  =  fetch_census('census1975.zip',  'U0345',  True)
    semi_frame_aw  =  fetch_census('census1975.zip',  'U0346',  True)
    semi_frame_ax  =  fetch_census('census1975.zip',  'U0348',  True)
    semi_frame_ay  =  fetch_census('census1975.zip',  'U0349',  True)
    semi_frame_az  =  fetch_census('census1975.zip',  'U0350',  True)
    semi_frame_ba  =  fetch_census('census1975.zip',  'U0351',  True)
    semi_frame_bb  =  fetch_census('census1975.zip',  'U0352',  True)
    result_frame_c  =  pd.concat([semi_frame_aa,  semi_frame_ab,  semi_frame_ac, \
                                semi_frame_ad,  semi_frame_ae,  semi_frame_af, \
                                semi_frame_ag,  semi_frame_ah,  semi_frame_ai, \
                                semi_frame_aj,  semi_frame_ak,  semi_frame_al, \
                                semi_frame_am,  semi_frame_an,  semi_frame_ao, \
                                semi_frame_ap,  semi_frame_aq,  semi_frame_ar, \
                                semi_frame_as,  semi_frame_at,  semi_frame_au, \
                                semi_frame_av,  semi_frame_aw,  semi_frame_ax, \
                                semi_frame_ay,  semi_frame_az,  semi_frame_ba, \
                                semi_frame_bb],  axis = 1,  sort = True)
    del semi_frame_aa,  semi_frame_ab,  semi_frame_ac,  semi_frame_ad,  semi_frame_ae, \
        semi_frame_af,  semi_frame_ag,  semi_frame_ah,  semi_frame_ai,  semi_frame_aj, \
        semi_frame_ak,  semi_frame_al,  semi_frame_am,  semi_frame_an,  semi_frame_ao, \
        semi_frame_ap,  semi_frame_aq,  semi_frame_ar,  semi_frame_as,  semi_frame_at, \
        semi_frame_au,  semi_frame_av,  semi_frame_aw,  semi_frame_ax,  semi_frame_ay, \
        semi_frame_az,  semi_frame_ba,  semi_frame_bb
    result_frame_c['Exports']  =  result_frame_c.iloc[:, 0:14].sum(1)
    result_frame_c['Imports']  =  result_frame_c.iloc[:, 14:28].sum(1)
    return result_frame_a,  result_frame_b,  result_frame_c


def datafetch_census_j():
    """Census Money Supply Aggregates"""
    base  =  48 ## 1915 = 100
    semi_frame_aa  =  fetch_census('census1975.zip',  'X0410',  True)
    semi_frame_ab  =  fetch_census('census1975.zip',  'X0414',  True)
    semi_frame_ac  =  fetch_census('census1975.zip',  'X0415',  True)
    result_frame  =  pd.concat([semi_frame_aa,  semi_frame_ab,  semi_frame_ac], 
                             axis = 1,  sort = True)
    del semi_frame_aa,  semi_frame_ab,  semi_frame_ac
    result_frame  =  result_frame.div(result_frame.iloc[base, :]/100)
    return result_frame,  base


def data_fetch_plotting_census_k():
    """Census Financial Markets & Institutions Series"""
    series  =  ('X0410', 'X0411', 'X0412', 'X0413', 'X0414', 'X0415', 'X0416', 'X0417', 'X0418', \
                'X0419', 'X0420', 'X0421', 'X0422', 'X0423', 'X0580', 'X0581', 'X0582', 'X0583', \
                'X0584', 'X0585', 'X0586', 'X0587', 'X0610', 'X0611', 'X0612', 'X0613', 'X0614', \
                'X0615', 'X0616', 'X0617', 'X0618', 'X0619', 'X0620', 'X0621', 'X0622', 'X0623', \
                'X0624', 'X0625', 'X0626', 'X0627', 'X0628', 'X0629', 'X0630', 'X0631', 'X0632', \
                'X0633', 'X0741', 'X0742', 'X0743', 'X0744', 'X0745', 'X0746', 'X0747', 'X0748', \
                'X0749', 'X0750', 'X0751', 'X0752', 'X0753', 'X0754', 'X0755', 'X0879', 'X0880', \
                'X0881', 'X0882', 'X0883', 'X0884', 'X0885', 'X0886', 'X0887', 'X0888', 'X0889', \
                'X0890', 'X0891', 'X0892', 'X0893', 'X0894', 'X0895', 'X0896', 'X0897', 'X0898', \
                'X0899', 'X0900', 'X0901', 'X0902', 'X0903', 'X0904', 'X0905', 'X0906', 'X0907', \
                'X0908', 'X0909', 'X0910', 'X0911', 'X0912', 'X0913', 'X0914', 'X0915', 'X0916', \
                'X0917', 'X0918', 'X0919', 'X0920', 'X0921', 'X0922', 'X0923', 'X0924', 'X0925', \
                'X0926', 'X0927', 'X0928', 'X0929', 'X0930', 'X0931', 'X0932', 'X0947', 'X0948', \
                'X0949', 'X0950', 'X0951', 'X0952', 'X0953', 'X0954', 'X0955', 'X0956')
    for i in range(len(series)):
        current_frame  =  fetch_census('census1975.zip',  series[i],  True)
        current_frame  =  current_frame.div(current_frame.iloc[0, :]/100)
        title  =  fetch_census_description('census1975.zip',  series[i])
        plt.figure(1+i)
        plt.plot(current_frame.index,  current_frame.iloc[:, 0],  label = '{}'.format(series[i]))
        plt.title('{},  {}$-${}'.format(title,  current_frame.index[0],  current_frame.index[len(current_frame)-1]))
        plt.xlabel('Period')
        plt.ylabel('Percentage')
        plt.grid(True)
        plt.legend()
        plt.show()
        del current_frame


def plotting_census_a(source_frame,  base):
    plt.figure()
    plt.plot(source_frame.iloc[:, 0],  label = 'Fabricant S.,  Shiskin J.,  NBER')
    plt.plot(source_frame.iloc[:, 1],  color = 'red',  linewidth = 4,  label = 'W.M. Persons')
    plt.plot(source_frame.iloc[:, 2],  label = 'E. Frickey')    
    plt.axvline(x = source_frame.index[base],  linestyle = ':')
    plt.title('US Manufacturing Indexes Of Physical Production Of Manufacturing,  %d = 100' %(source_frame.index[base]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


def plotting_census_b(capital_frame,  deflator_frame):
    """Census Manufacturing Fixed Assets Series"""
    plt.figure(1)
    plt.semilogy(capital_frame.iloc[:, 0],  label = 'Total')
    plt.semilogy(capital_frame.iloc[:, 1],  label = 'Structures')
    plt.semilogy(capital_frame.iloc[:, 2],  label = 'Equipment')
    plt.title('Manufacturing Fixed Assets,  {}$-${}'.format(capital_frame.index[0], 
                                                           capital_frame.index[len(capital_frame)-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.plot(deflator_frame)
    plt.title('Census Fused Capital Deflator,  {}$-${}'.format(deflator_frame.index[0], 
                                                              deflator_frame.index[len(deflator_frame)-1]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.show()


def plotting_census_c(source_frame,  base):
    plt.figure(1)
    plt.semilogy(source_frame.index,  source_frame.iloc[:, 1], 
                 label = 'P265 - Raw Steel Produced - Total,  %d = 100' %(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index,  source_frame.iloc[:, 2], 
                 label = 'P266 - Raw Steel Produced - Bessemer,  %d = 100' %(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index,  source_frame.iloc[:, 3], 
                 label = 'P267 - Raw Steel Produced - Open Hearth,  %d = 100' %(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index,  source_frame.iloc[:, 4], 
                 label = 'P268 - Raw Steel Produced - Crucible,  %d = 100' %(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index,  source_frame.iloc[:, 5], 
                 label = 'P269 - Raw Steel Produced - Electric and All Other,  %d = 100' %(source_frame.index[base[2]]))
    plt.axvline(x = source_frame.index[base[0]],  linestyle = ':')
    plt.axvline(x = source_frame.index[base[2]],  linestyle = ':')
    plt.title('Steel Production')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.semilogy(source_frame.index,  source_frame.iloc[:, 0], 
                 label = 'P262 - Rails Produced,  %d = 100' %(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index,  source_frame.iloc[:, 6], 
                 label = 'P293 - Locomotives Produced,  %d = 100' %(source_frame.index[base[1]]))
    plt.semilogy(source_frame.index,  source_frame.iloc[:, 7], 
                 label = 'P294 - Railroad Passenger Cars Produced,  %d = 100' %(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index,  source_frame.iloc[:, 8], 
                 label = 'P295 - Railroad Freight Cars Produced,  %d = 100' %(source_frame.index[base[0]]))
    plt.axvline(x = source_frame.index[base[0]],  linestyle = ':')
    plt.axvline(x = source_frame.index[base[1]],  linestyle = ':')
    plt.title('Rails & Cars Production')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plotting_census_e(source_frame):
    plt.figure()
    plt.plot(source_frame.index,  source_frame.iloc[:, 0])
    plt.title('Total Immigration,  {}$-${}'.format(source_frame.index[0], 
                                                  source_frame.index[len(source_frame)-1]))
    plt.xlabel('Period')
    plt.ylabel('People')
    plt.grid()
    plt.show()


def plotting_census_fa(source_frame):
    plt.figure(1)
    source_frame.iloc[:, 1].plot()
    plt.title('Unemployment,  Percent of Civilian Labor Force')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.figure(2)
    plt.plot(source_frame.iloc[:, 2],  label = 'Bureau of Labour')
    plt.plot(source_frame.iloc[:, 3],  label = 'Wolman')
    plt.title('All Manufacturing,  Average Full-Time Weekly Hours,  1890-1899 = 100')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.figure(3)
    source_frame.iloc[:, 6].plot()
    plt.title('Implicit Number of Workers')
    plt.xlabel('Period')
    plt.ylabel('Persons')
    plt.grid()
    plt.show()


def plotting_census_fb(source_frame):
    fig,  axs_a  =  plt.subplots()
    color  =  'tab:red'
    axs_a.set_xlabel('Period')
    axs_a.set_ylabel('Number',  color = color)
    axs_a.plot(source_frame.index,  source_frame.iloc[:, 4],  color = color,  label = 'Stoppages')
    axs_a.set_title('Work Conflicts')
    axs_a.grid()
    axs_a.legend(loc = 2)
    axs_a.tick_params(axis = 'y',  labelcolor = color)
    axs_b  =  axs_a.twinx()
    color  =  'tab:blue'
    axs_b.set_ylabel('1, 000 People',  color = color)
    axs_b.plot(source_frame.index,  source_frame.iloc[:, 5],  color = color,  label = 'Workers Involved')
    axs_b.legend(loc = 1)
    axs_b.tick_params(axis = 'y',  labelcolor = color)
    fig.tight_layout()
    plt.show()


def plotting_census_g(source_frame):
    plt.figure()
    plt.plot(source_frame.index,  source_frame.iloc[:, 0],  label = 'Gross National Product')
    plt.plot(source_frame.index,  source_frame.iloc[:, 1],  label = 'Gross National Product Per Capita')
    plt.title('Gross National Product,  Prices {} = 100,  {} = 100'.format(1958,  source_frame.index[0]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


def plotting_census_i(source_frame_a,  source_frame_b,  source_frame_c):
    plt.figure(1)
    plt.plot(source_frame_a.iloc[:, 0],  label = 'Exports,  U1')
    plt.plot(source_frame_a.iloc[:, 1],  label = 'Imports,  U8')
    plt.plot(source_frame_a.iloc[:, 0].sub(source_frame_a.iloc[:, 1]),  label = 'Net Exports')
    plt.title('Exports & Imports of Goods and Services,  {}$-${}'.format(source_frame_a.index[0],  source_frame_a.index[len(source_frame_a)-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.plot(source_frame_b.iloc[:, 0],  label = 'Exports,  U187')
    plt.plot(source_frame_b.iloc[:, 1],  label = 'Imports,  U188')
    plt.plot(source_frame_b.iloc[:, 2],  label = 'Net Exports,  U189')
    plt.title('Total Merchandise,  Gold and Silver,  {}$-${}'.format(source_frame_b.index[0],  source_frame_b.index[len(source_frame_b)-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(3)
    plt.plot(source_frame_c.iloc[:, 0].sub(source_frame_c.iloc[:, 14]),  label = 'America-Canada')
    plt.plot(source_frame_c.iloc[:, 1].sub(source_frame_c.iloc[:, 15]),  label = 'America-Cuba')
    plt.plot(source_frame_c.iloc[:, 2].sub(source_frame_c.iloc[:, 16]),  label = 'America-Mexico')
    plt.plot(source_frame_c.iloc[:, 3].sub(source_frame_c.iloc[:, 17]),  label = 'America-Brazil')
    plt.plot(source_frame_c.iloc[:, 4].sub(source_frame_c.iloc[:, 18]),  label = 'America-Other')
    plt.plot(source_frame_c.iloc[:, 5].sub(source_frame_c.iloc[:, 19]),  label = 'Europe-United Kingdom')
    plt.plot(source_frame_c.iloc[:, 6].sub(source_frame_c.iloc[:, 20]),  label = 'Europe-France')
    plt.plot(source_frame_c.iloc[:, 7].sub(source_frame_c.iloc[:, 21]),  label = 'Europe-Germany')
    plt.plot(source_frame_c.iloc[:, 8].sub(source_frame_c.iloc[:, 22]),  label = 'Europe-Other')
    plt.plot(source_frame_c.iloc[:, 9].sub(source_frame_c.iloc[:, 23]),  label = 'Asia-Mainland China')
    plt.plot(source_frame_c.iloc[:, 10].sub(source_frame_c.iloc[:, 24]),  label = 'Asia-Japan')
    plt.plot(source_frame_c.iloc[:, 11].sub(source_frame_c.iloc[:, 25]),  label = 'Asia-Other')
    plt.plot(source_frame_c.iloc[:, 12].sub(source_frame_c.iloc[:, 26]),  label = 'Australia and Oceania-All')
    plt.plot(source_frame_c.iloc[:, 13].sub(source_frame_c.iloc[:, 27]),  label = 'Africa-All')
    plt.title('Net Exports')
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(4)
    plt.plot(source_frame_c.iloc[:, 0].sub(source_frame_c.iloc[:, 14]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])),  label = 'America-Canada')
    plt.plot(source_frame_c.iloc[:, 1].sub(source_frame_c.iloc[:, 15]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])),  label = 'America-Cuba')
    plt.plot(source_frame_c.iloc[:, 2].sub(source_frame_c.iloc[:, 16]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])),  label = 'America-Mexico')
    plt.plot(source_frame_c.iloc[:, 3].sub(source_frame_c.iloc[:, 17]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])),  label = 'America-Brazil')
    plt.plot(source_frame_c.iloc[:, 4].sub(source_frame_c.iloc[:, 18]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])),  label = 'America-Other')
    plt.plot(source_frame_c.iloc[:, 5].sub(source_frame_c.iloc[:, 19]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])),  label = 'Europe-United Kingdom')
    plt.plot(source_frame_c.iloc[:, 6].sub(source_frame_c.iloc[:, 20]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])),  label = 'Europe-France')
    plt.plot(source_frame_c.iloc[:, 7].sub(source_frame_c.iloc[:, 21]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])),  label = 'Europe-Germany')
    plt.plot(source_frame_c.iloc[:, 8].sub(source_frame_c.iloc[:, 22]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])),  label = 'Europe-Other')
    plt.plot(source_frame_c.iloc[:, 9].sub(source_frame_c.iloc[:, 23]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])),  label = 'Asia-Mainland China')
    plt.plot(source_frame_c.iloc[:, 10].sub(source_frame_c.iloc[:, 24]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])),  label = 'Asia-Japan')
    plt.plot(source_frame_c.iloc[:, 11].sub(source_frame_c.iloc[:, 25]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])),  label = 'Asia-Other')
    plt.plot(source_frame_c.iloc[:, 12].sub(source_frame_c.iloc[:, 26]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])),  label = 'Australia and Oceania-All')
    plt.plot(source_frame_c.iloc[:, 13].sub(source_frame_c.iloc[:, 27]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])),  label = 'Africa-All')
    plt.title('Net Exports')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.legend()
    plt.show()


def plotting_census_j(source_frame,  base):
    plt.figure()
    plt.semilogy(source_frame.index,  source_frame.iloc[:, 0], 
                 label = 'Currency Held by the Public')
    plt.semilogy(source_frame.index,  source_frame.iloc[:, 1], 
                 label = 'M1 Money Supply (Currency Plus Demand Deposits)')
    plt.semilogy(source_frame.index,  source_frame.iloc[:, 2], 
                 label = 'M2 Money Supply (M1 Plus Time Deposits)')
    plt.axvline(x = source_frame.index[base],  linestyle = ':')
    plt.title('Currency Dynamics,  {} = 100'.format(source_frame.index[base]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


import pandas as pd
import matplotlib.pyplot as plt
result_frame,  base  =  datafetch_census_a()
plotting_census_a(result_frame,  base)
capital      =  datafetch_census_ba()
deflator     =  datafetch_census_bb()
plotting_census_b(capital,  deflator)
result_frame,  base  =  datafetch_census_c()
plotting_census_c(result_frame,  base)
"""Census Production Series"""
series       =  ('P0248', 'P0249', 'P0250', 'P0251', 'P0262', 'P0265', 'P0266', 'P0267', \
               'P0268', 'P0269', 'P0293', 'P0294', 'P0295')
alternative  =  ('P0231', 'P0232', 'P0233', 'P0234', 'P0235', 'P0236', 'P0237', 'P0238', \
                'P0239', 'P0240', 'P0241', 'P0244', 'P0247', 'P0248', 'P0249', 'P0250', \
                'P0251', 'P0252', 'P0253', 'P0254', 'P0255', 'P0256', 'P0257', 'P0258', \
                'P0259', 'P0260', 'P0261', 'P0262', 'P0263', 'P0264', 'P0265', 'P0266', \
                'P0267', 'P0268', 'P0269', 'P0270', 'P0271', 'P0277', 'P0279', 'P0281', \
                'P0282', 'P0283', 'P0284', 'P0286', 'P0288', 'P0290', 'P0293', 'P0294', \
                'P0295', 'P0296', 'P0297', 'P0298', 'P0299', 'P0300')
data_fetch_plotting_census_d(series)
result_frame  =  datafetch_census_e()
plotting_census_e(result_frame)
result_frame  =  datafetch_census_f()
plotting_census_fa(result_frame)
plotting_census_fb(result_frame)
result_frame  =  datafetch_census_g()
plotting_census_g(result_frame)
data_fetch_plotting_census_h()
result_framea,  result_frameb,  result_framec  =  datafetch_census_i()
plotting_census_i(result_framea,  result_frameb,  result_framec)
result_frame,  base  =  datafetch_census_j()
plotting_census_j(result_frame,  base)
data_fetch_plotting_census_k()
