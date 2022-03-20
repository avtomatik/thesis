#-*- coding: utf-8 -*-
"""
Created on Sat Jan 18 00:13:17 2020

@author: Mastermind
"""


def fetch_census_description(file_name, series_id):
    """Retrieve Series Description U.S. Bureau of the Census"""
    data_frame = pd.read_csv(file_name, usecols=[0, 1, 3, 4, 5, 6, 8], low_memory=False)
    data_frame = data_frame[data_frame.iloc[:, 6] == series_id]
    data_frame.drop_duplicates(inplace=True)
    if data_frame.iloc[0, 2] == 'no_details':
        if data_frame.iloc[0, 5] == 'no_details':
            if data_frame.iloc[0, 4] == 'no_details':
                description = '{}'.format(data_frame.iloc[0, 3])
            else:
                description = '{} -\n{}'.format(*data_frame.iloc[0, [3, 4]])
        else:
            description = '{} -\n{} -\n{}'.format(*data_frame.iloc[0, [3, 4, 5]])
    else:
        if data_frame.iloc[0, 5] == 'no_details':
            if data_frame.iloc[0, 4] == 'no_details':
                description = '{}; {}'.format(*data_frame.iloc[0, [3, 2]])
            else:
                description = '{} -\n{}; {}'.format(*data_frame.iloc[0, [3, 4, 2]])
        else:
            description = '{} -\n{} -\n{}; {}'.format(*data_frame.iloc[0, [3, 4, 5, 2]])
    return description


def data_fetch_census_a():
    """Census Manufacturing Indexes, 1899=100"""
    base = 39 # # 1899=100
    """HSUS 1949 Page 179, J13"""
    file_name = 'dataset_usa_census1949.zip'
    semi_frame_a = fetch_census(file_name, 'J0013')
    """HSUS 1949 Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing"""
    file_name = 'dataset_usa_census1949.zip'
    semi_frame_b = fetch_census(file_name, 'J0014')
    """HSUS 1975 Page 667, P17: Edwin Frickey Series, Indexes of Manufacturing Production"""
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_c = fetch_census(file_name, 'P0017')
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c], axis=1, sort=True)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].div(result_frame.iloc[base, 1]/100)
    return result_frame, base


def data_fetch_census_b_a():
    """Returns Nominal Million-Dollar Capital, Including Structures & Equipment, Series"""

    file_name = 'dataset_usa_census1949.zip'
    semi_frame_a = fetch_census(file_name, 'J0149') # Nominal
    file_name = 'dataset_usa_census1949.zip'
    semi_frame_b = fetch_census(file_name, 'J0150') # Nominal
    file_name = 'dataset_usa_census1949.zip'
    semi_frame_c = fetch_census(file_name, 'J0151') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_d = fetch_census(file_name, 'P0107') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_e = fetch_census(file_name, 'P0108') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_f = fetch_census(file_name, 'P0109') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_g = fetch_census(file_name, 'P0110') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_h = fetch_census(file_name, 'P0111') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_i = fetch_census(file_name, 'P0112') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_j = fetch_census(file_name, 'P0113') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_k = fetch_census(file_name, 'P0114') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_l = fetch_census(file_name, 'P0115') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_m = fetch_census(file_name, 'P0116') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_n = fetch_census(file_name, 'P0117') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_o = fetch_census(file_name, 'P0118') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_p = fetch_census(file_name, 'P0119') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_q = fetch_census(file_name, 'P0120') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_r = fetch_census(file_name, 'P0121') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_s = fetch_census(file_name, 'P0122') # 1958=100
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, \
                              semi_frame_d, semi_frame_e, semi_frame_f, \
                              semi_frame_g, semi_frame_h, semi_frame_i, \
                              semi_frame_j, semi_frame_k, semi_frame_l, \
                              semi_frame_m, semi_frame_n, semi_frame_o, \
                              semi_frame_p, semi_frame_q, semi_frame_r, \
                              semi_frame_s], axis=1, sort=True)
    result_frame = result_frame[12:]
    for i in range(3, 19):
        result_frame = bln_to_mln(result_frame, i)
    result_frame['total'] = result_frame.iloc[:, [0, 3]].mean(1)
    result_frame['structures'] = result_frame.iloc[:, [1, 4]].mean(1)
    result_frame['equipment'] = result_frame.iloc[:, [2, 5]].mean(1)
#    result_frame.iloc[:, 19] = signal.wiener(result_frame.iloc[:, 19]).round()
#    result_frame.iloc[:, 20] = signal.wiener(result_frame.iloc[:, 20]).round()
#    result_frame.iloc[:, 21] = signal.wiener(result_frame.iloc[:, 21]).round()
    result_frame = result_frame[result_frame.columns[[19, 20, 21]]]
    return result_frame


def data_fetch_census_c():
    """Census Primary Metals & Railroad-Related Products Manufacturing Series"""
    base = (15, 20, 49) # # 1875=100, 1880=100, 1909=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_a = fetch_census(file_name, 'P0262')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_b = fetch_census(file_name, 'P0265')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_c = fetch_census(file_name, 'P0266')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_d = fetch_census(file_name, 'P0267')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_e = fetch_census(file_name, 'P0268')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_f = fetch_census(file_name, 'P0269')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_g = fetch_census(file_name, 'P0293')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_h = fetch_census(file_name, 'P0294')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_i = fetch_census(file_name, 'P0295')
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, \
                              semi_frame_d, semi_frame_e, semi_frame_f, \
                              semi_frame_g, semi_frame_h, semi_frame_i], axis=1, sort=True)
    result_frame.iloc[:, 0] = result_frame.iloc[:, 0].div(result_frame.iloc[base[0], 0]/100)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].div(result_frame.iloc[base[0], 1]/100)
    result_frame.iloc[:, 2] = result_frame.iloc[:, 2].div(result_frame.iloc[base[0], 2]/100)
    result_frame.iloc[:, 3] = result_frame.iloc[:, 3].div(result_frame.iloc[base[0], 3]/100)
    result_frame.iloc[:, 4] = result_frame.iloc[:, 4].div(result_frame.iloc[base[0], 4]/100)
    result_frame.iloc[:, 5] = result_frame.iloc[:, 5].div(result_frame.iloc[base[2], 5]/100)
    result_frame.iloc[:, 6] = result_frame.iloc[:, 6].div(result_frame.iloc[base[1], 6]/100)
    result_frame.iloc[:, 7] = result_frame.iloc[:, 7].div(result_frame.iloc[base[0], 7]/100)
    result_frame.iloc[:, 8] = result_frame.iloc[:, 8].div(result_frame.iloc[base[0], 8]/100)
    return result_frame, base


def data_fetch_census_e():
    """Census Total Immigration Series"""
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_aa = fetch_census(file_name, 'C0091')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ab = fetch_census(file_name, 'C0092')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ac = fetch_census(file_name, 'C0093')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ad = fetch_census(file_name, 'C0094')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ae = fetch_census(file_name, 'C0095')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_af = fetch_census(file_name, 'C0096')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ag = fetch_census(file_name, 'C0097')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ah = fetch_census(file_name, 'C0098')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ai = fetch_census(file_name, 'C0099')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_aj = fetch_census(file_name, 'C0100')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ak = fetch_census(file_name, 'C0101')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_al = fetch_census(file_name, 'C0103')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_am = fetch_census(file_name, 'C0104')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_an = fetch_census(file_name, 'C0105')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ao = fetch_census(file_name, 'C0106')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ap = fetch_census(file_name, 'C0107')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_aq = fetch_census(file_name, 'C0108')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ar = fetch_census(file_name, 'C0109')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_as = fetch_census(file_name, 'C0111')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_at = fetch_census(file_name, 'C0112')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_au = fetch_census(file_name, 'C0113')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_av = fetch_census(file_name, 'C0114')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_aw = fetch_census(file_name, 'C0115')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ax = fetch_census(file_name, 'C0117')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ay = fetch_census(file_name, 'C0118')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_az = fetch_census(file_name, 'C0119')
    result_frame = pd.concat([semi_frame_aa, semi_frame_ab, semi_frame_ac, \
                              semi_frame_ad, semi_frame_ae, semi_frame_af, \
                              semi_frame_ag, semi_frame_ah, semi_frame_ai, \
                              semi_frame_aj, semi_frame_ak, semi_frame_al, \
                              semi_frame_am, semi_frame_an, semi_frame_ao, \
                              semi_frame_ap, semi_frame_aq, semi_frame_ar, \
                              semi_frame_as, semi_frame_at, semi_frame_au, \
                              semi_frame_av, semi_frame_aw, semi_frame_ax, \
                              semi_frame_ay, semi_frame_az], axis=1, sort=True)

    result_frame['C89'] = result_frame.sum(1)
    result_frame = result_frame[result_frame.columns[[result_frame.shape[1]-1]]]
    return result_frame


def data_fetch_census_f():
    """Census Employment Series"""
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_a = fetch_census(file_name, 'D0085')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_b = fetch_census(file_name, 'D0086')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_c = fetch_census(file_name, 'D0796')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_d = fetch_census(file_name, 'D0797')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_e = fetch_census(file_name, 'D0977')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_f = fetch_census(file_name, 'D0982')
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, \
                              semi_frame_d, semi_frame_e, semi_frame_f],
                             axis=1, sort=True)
    result_frame['workers'] = result_frame.iloc[:, 0].div(result_frame.iloc[:, 1]/100)
    result_frame.iloc[:, 4].fillna(result_frame.iloc[:25, 4].mean(), inplace=True)
    result_frame.iloc[:, 5].fillna(result_frame.iloc[:25, 5].mean(), inplace=True)
    return result_frame


def data_fetch_census_g():
    """Census Gross National Product Series"""
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_aa = fetch_census(file_name, 'F0003')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ab = fetch_census(file_name, 'F0004')
    result_frame = pd.concat([semi_frame_aa, semi_frame_ab], axis=1, sort=True)
    result_frame = result_frame[2:]
    result_frame = result_frame.div(result_frame.iloc[0, :]/100)
    return result_frame


def data_fetch_census_i():
    """Census Foreign Trade Series"""
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_aa = fetch_census(file_name, 'U0001')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ab = fetch_census(file_name, 'U0008')
    result_frame_a = pd.concat([semi_frame_aa, semi_frame_ab], axis=1, sort=True)

    file_name = 'dataset_usa_census1975.zip'
    semi_frame_aa = fetch_census(file_name, 'U0187')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ab = fetch_census(file_name, 'U0188')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ac = fetch_census(file_name, 'U0189')
    result_frame_b = pd.concat([semi_frame_aa, semi_frame_ab, semi_frame_ac],
                               axis=1, sort=True)

    file_name = 'dataset_usa_census1975.zip'
    semi_frame_aa = fetch_census(file_name, 'U0319')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ab = fetch_census(file_name, 'U0320')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ac = fetch_census(file_name, 'U0321')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ad = fetch_census(file_name, 'U0322')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ae = fetch_census(file_name, 'U0323')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_af = fetch_census(file_name, 'U0325')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ag = fetch_census(file_name, 'U0326')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ah = fetch_census(file_name, 'U0327')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ai = fetch_census(file_name, 'U0328')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_aj = fetch_census(file_name, 'U0330')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ak = fetch_census(file_name, 'U0331')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_al = fetch_census(file_name, 'U0332')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_am = fetch_census(file_name, 'U0333')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_an = fetch_census(file_name, 'U0334')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ao = fetch_census(file_name, 'U0337')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ap = fetch_census(file_name, 'U0338')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_aq = fetch_census(file_name, 'U0339')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ar = fetch_census(file_name, 'U0340')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_as = fetch_census(file_name, 'U0341')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_at = fetch_census(file_name, 'U0343')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_au = fetch_census(file_name, 'U0344')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_av = fetch_census(file_name, 'U0345')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_aw = fetch_census(file_name, 'U0346')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ax = fetch_census(file_name, 'U0348')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ay = fetch_census(file_name, 'U0349')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_az = fetch_census(file_name, 'U0350')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ba = fetch_census(file_name, 'U0351')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_bb = fetch_census(file_name, 'U0352')
    result_frame_c = pd.concat([semi_frame_aa, semi_frame_ab, semi_frame_ac, \
                                semi_frame_ad, semi_frame_ae, semi_frame_af, \
                                semi_frame_ag, semi_frame_ah, semi_frame_ai, \
                                semi_frame_aj, semi_frame_ak, semi_frame_al, \
                                semi_frame_am, semi_frame_an, semi_frame_ao, \
                                semi_frame_ap, semi_frame_aq, semi_frame_ar, \
                                semi_frame_as, semi_frame_at, semi_frame_au, \
                                semi_frame_av, semi_frame_aw, semi_frame_ax, \
                                semi_frame_ay, semi_frame_az, semi_frame_ba, \
                                semi_frame_bb], axis=1, sort=True)

    result_frame_c['Exports'] = result_frame_c.iloc[:, 0:14].sum(1)
    result_frame_c['Imports'] = result_frame_c.iloc[:, 14:28].sum(1)
    return result_frame_a, result_frame_b, result_frame_c


def data_fetch_census_j():
    """Census Money Supply Aggregates"""
    base = 48 # # 1915=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_aa = fetch_census(file_name, 'X0410')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ab = fetch_census(file_name, 'X0414')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_ac = fetch_census(file_name, 'X0415')
    result_frame = pd.concat([semi_frame_aa, semi_frame_ab, semi_frame_ac],
                             axis=1, sort=True)
    result_frame = result_frame.div(result_frame.iloc[base, :]/100)
    return result_frame, base


def data_fetch_plot_census_k():
    """Census Financial Markets & Institutions Series"""
    file_name = 'dataset_usa_census1975.zip'
    series_ids = ('X0410', 'X0411', 'X0412', 'X0413', 'X0414', 'X0415',
                  'X0416', 'X0417', 'X0418', 'X0419', 'X0420', 'X0421',
                  'X0422', 'X0423', 'X0580', 'X0581', 'X0582', 'X0583',
                  'X0584', 'X0585', 'X0586', 'X0587', 'X0610', 'X0611',
                  'X0612', 'X0613', 'X0614', 'X0615', 'X0616', 'X0617',
                  'X0618', 'X0619', 'X0620', 'X0621', 'X0622', 'X0623',
                  'X0624', 'X0625', 'X0626', 'X0627', 'X0628', 'X0629',
                  'X0630', 'X0631', 'X0632', 'X0633', 'X0741', 'X0742',
                  'X0743', 'X0744', 'X0745', 'X0746', 'X0747', 'X0748',
                  'X0749', 'X0750', 'X0751', 'X0752', 'X0753', 'X0754',
                  'X0755', 'X0879', 'X0880', 'X0881', 'X0882', 'X0883',
                  'X0884', 'X0885', 'X0886', 'X0887', 'X0888', 'X0889',
                  'X0890', 'X0891', 'X0892', 'X0893', 'X0894', 'X0895',
                  'X0896', 'X0897', 'X0898', 'X0899', 'X0900', 'X0901',
                  'X0902', 'X0903', 'X0904', 'X0905', 'X0906', 'X0907',
                  'X0908', 'X0909', 'X0910', 'X0911', 'X0912', 'X0913',
                  'X0914', 'X0915', 'X0916', 'X0917', 'X0918', 'X0919',
                  'X0920', 'X0921', 'X0922', 'X0923', 'X0924', 'X0925',
                  'X0926', 'X0927', 'X0928', 'X0929', 'X0930', 'X0931',
                  'X0932', 'X0947', 'X0948', 'X0949', 'X0950', 'X0951',
                  'X0952', 'X0953', 'X0954', 'X0955', 'X0956')
    for i, series_id in enumerate(series_ids):
        title = fetch_census_description(file_name, series_id)
        data_frame = fetch_census(file_name, series_id)
        data_frame = data_frame.div(data_frame.iloc[0, :]/100)
        plt.figure(1+i)
        plt.plot(data_frame, label=f'{series_id}')
        plt.title('{}, {}$-${}'.format(title, data_frame.index[0], data_frame.index[-1]))
        plt.xlabel('Period')
        plt.ylabel('Percentage')
        plt.grid(True)
        plt.legend()
        plt.show()


def plot_census_b(capital_frame, deflator_frame):
    """Census Manufacturing Fixed Assets Series"""
    plt.figure(1)
    plt.semilogy(capital_frame.iloc[:, 0], label='Total')
    plt.semilogy(capital_frame.iloc[:, 1], label='Structures')
    plt.semilogy(capital_frame.iloc[:, 2], label='Equipment')
    plt.title('Manufacturing Fixed Assets, {}$-${}'.format(capital_frame.index[0],
                                                           capital_frame.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.plot(deflator_frame)
    plt.title('Census Fused Capital Deflator, {}$-${}'.format(deflator_frame.index[0],
                                                              deflator_frame.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.show()


def plot_census_e(source_frame):
    plt.figure()
    plt.plot(source_frame.index, source_frame.iloc[:, 0])
    plt.title('Total Immigration, {}$-${}'.format(source_frame.index[0],
                                                  source_frame.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('People')
    plt.grid()
    plt.show()


def plot_census_f_a(source_frame):
    plt.figure(1)
    source_frame.iloc[:, 1].plot()
    plt.title('Unemployment, Percent of Civilian Labor Force')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.figure(2)
    plt.plot(source_frame.iloc[:, 2], label='Bureau of Labour')
    plt.plot(source_frame.iloc[:, 3], label='Wolman')
    plt.title('All Manufacturing, Average Full-Time Weekly Hours, 1890-1899=100')
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


def plot_census_f_b(source_frame):
    fig, axs_a = plt.subplots()
    color = 'tab:red'
    axs_a.set_xlabel('Period')
    axs_a.set_ylabel('Number', color = color)
    axs_a.plot(source_frame.index, source_frame.iloc[:, 4], color = color, label='Stoppages')
    axs_a.set_title('Work Conflicts')
    axs_a.grid()
    axs_a.legend(loc = 2)
    axs_a.tick_params(axis = 'y', labelcolor = color)
    axs_b = axs_a.twinx()
    color = 'tab:blue'
    axs_b.set_ylabel('1,000 People', color = color)
    axs_b.plot(source_frame.index, source_frame.iloc[:, 5], color = color, label='Workers Involved')
    axs_b.legend(loc = 1)
    axs_b.tick_params(axis = 'y', labelcolor = color)
    fig.tight_layout()
    plt.show()


def plot_census_g(source_frame):
    plt.figure()
    plt.plot(source_frame.index, source_frame.iloc[:, 0], label='Gross National Product')
    plt.plot(source_frame.index, source_frame.iloc[:, 1], label='Gross National Product Per Capita')
    plt.title('Gross National Product, Prices {}=100, {}=100'.format(1958, source_frame.index[0]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


def plot_census_i(source_frame_a, source_frame_b, source_frame_c):
    plt.figure(1)
    plt.plot(source_frame_a.iloc[:, 0], label='Exports, U1')
    plt.plot(source_frame_a.iloc[:, 1], label='Imports, U8')
    plt.plot(source_frame_a.iloc[:, 0].sub(source_frame_a.iloc[:, 1]), label='Net Exports')
    plt.title('Exports & Imports of Goods and Services, {}$-${}'.format(source_frame_a.index[0], source_frame_a.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.plot(source_frame_b.iloc[:, 0], label='Exports, U187')
    plt.plot(source_frame_b.iloc[:, 1], label='Imports, U188')
    plt.plot(source_frame_b.iloc[:, 2], label='Net Exports, U189')
    plt.title('Total Merchandise, Gold and Silver, {}$-${}'.format(source_frame_b.index[0], source_frame_b.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(3)
    plt.plot(source_frame_c.iloc[:, 0].sub(source_frame_c.iloc[:, 14]), label='America-Canada')
    plt.plot(source_frame_c.iloc[:, 1].sub(source_frame_c.iloc[:, 15]), label='America-Cuba')
    plt.plot(source_frame_c.iloc[:, 2].sub(source_frame_c.iloc[:, 16]), label='America-Mexico')
    plt.plot(source_frame_c.iloc[:, 3].sub(source_frame_c.iloc[:, 17]), label='America-Brazil')
    plt.plot(source_frame_c.iloc[:, 4].sub(source_frame_c.iloc[:, 18]), label='America-Other')
    plt.plot(source_frame_c.iloc[:, 5].sub(source_frame_c.iloc[:, 19]), label='Europe-United Kingdom')
    plt.plot(source_frame_c.iloc[:, 6].sub(source_frame_c.iloc[:, 20]), label='Europe-France')
    plt.plot(source_frame_c.iloc[:, 7].sub(source_frame_c.iloc[:, 21]), label='Europe-Germany')
    plt.plot(source_frame_c.iloc[:, 8].sub(source_frame_c.iloc[:, 22]), label='Europe-Other')
    plt.plot(source_frame_c.iloc[:, 9].sub(source_frame_c.iloc[:, 23]), label='Asia-Mainland China')
    plt.plot(source_frame_c.iloc[:, 10].sub(source_frame_c.iloc[:, 24]), label='Asia-Japan')
    plt.plot(source_frame_c.iloc[:, 11].sub(source_frame_c.iloc[:, 25]), label='Asia-Other')
    plt.plot(source_frame_c.iloc[:, 12].sub(source_frame_c.iloc[:, 26]), label='Australia and Oceania-All')
    plt.plot(source_frame_c.iloc[:, 13].sub(source_frame_c.iloc[:, 27]), label='Africa-All')
    plt.title('Net Exports')
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(4)
    plt.plot(source_frame_c.iloc[:, 0].sub(source_frame_c.iloc[:, 14]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Canada')
    plt.plot(source_frame_c.iloc[:, 1].sub(source_frame_c.iloc[:, 15]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Cuba')
    plt.plot(source_frame_c.iloc[:, 2].sub(source_frame_c.iloc[:, 16]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Mexico')
    plt.plot(source_frame_c.iloc[:, 3].sub(source_frame_c.iloc[:, 17]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Brazil')
    plt.plot(source_frame_c.iloc[:, 4].sub(source_frame_c.iloc[:, 18]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Other')
    plt.plot(source_frame_c.iloc[:, 5].sub(source_frame_c.iloc[:, 19]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Europe-United Kingdom')
    plt.plot(source_frame_c.iloc[:, 6].sub(source_frame_c.iloc[:, 20]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Europe-France')
    plt.plot(source_frame_c.iloc[:, 7].sub(source_frame_c.iloc[:, 21]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Europe-Germany')
    plt.plot(source_frame_c.iloc[:, 8].sub(source_frame_c.iloc[:, 22]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Europe-Other')
    plt.plot(source_frame_c.iloc[:, 9].sub(source_frame_c.iloc[:, 23]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Asia-Mainland China')
    plt.plot(source_frame_c.iloc[:, 10].sub(source_frame_c.iloc[:, 24]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Asia-Japan')
    plt.plot(source_frame_c.iloc[:, 11].sub(source_frame_c.iloc[:, 25]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Asia-Other')
    plt.plot(source_frame_c.iloc[:, 12].sub(source_frame_c.iloc[:, 26]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Australia and Oceania-All')
    plt.plot(source_frame_c.iloc[:, 13].sub(source_frame_c.iloc[:, 27]).div(source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Africa-All')
    plt.title('Net Exports')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.legend()
    plt.show()


def plot_census_j(source_frame, base):
    plt.figure()
    plt.semilogy(source_frame.index, source_frame.iloc[:, 0],
                 label='Currency Held by the Public')
    plt.semilogy(source_frame.index, source_frame.iloc[:, 1],
                 label='M1 Money Supply (Currency Plus Demand Deposits)')
    plt.semilogy(source_frame.index, source_frame.iloc[:, 2],
                 label='M2 Money Supply (M1 Plus Time Deposits)')
    plt.axvline(x = source_frame.index[base], linestyle = ':')
    plt.title('Currency Dynamics, {}=100'.format(source_frame.index[base]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


result_frame, base = data_fetch_census_a()
plot_census_a(result_frame, base)
capital = data_fetch_census_b_a()
deflator = data_fetch_census_b_b()
plot_census_b(capital, deflator)
result_frame, base = data_fetch_census_c()
plot_census_c(result_frame, base)
"""Census Production Series"""
series_ids = ('P0248', 'P0249', 'P0250', 'P0251', 'P0262', 'P0265', 'P0266', 'P0267', \
               'P0268', 'P0269', 'P0293', 'P0294', 'P0295')
alternative = ('P0231', 'P0232', 'P0233', 'P0234', 'P0235', 'P0236', 'P0237', 'P0238', \
                'P0239', 'P0240', 'P0241', 'P0244', 'P0247', 'P0248', 'P0249', 'P0250', \
                'P0251', 'P0252', 'P0253', 'P0254', 'P0255', 'P0256', 'P0257', 'P0258', \
                'P0259', 'P0260', 'P0261', 'P0262', 'P0263', 'P0264', 'P0265', 'P0266', \
                'P0267', 'P0268', 'P0269', 'P0270', 'P0271', 'P0277', 'P0279', 'P0281', \
                'P0282', 'P0283', 'P0284', 'P0286', 'P0288', 'P0290', 'P0293', 'P0294', \
                'P0295', 'P0296', 'P0297', 'P0298', 'P0299', 'P0300')
data_fetch_plot_census_d(series_ids)
result_frame = data_fetch_census_e()
plot_census_e(result_frame)
result_frame = data_fetch_census_f()
plot_census_f_a(result_frame)
plot_census_f_b(result_frame)
result_frame = data_fetch_census_g()
plot_census_g(result_frame)
data_fetch_plot_census_h()
result_framea, result_frameb, result_framec = data_fetch_census_i()
plot_census_i(result_framea, result_frameb, result_framec)
result_frame, base = data_fetch_census_j()
plot_census_j(result_frame, base)
data_fetch_plot_census_k()
