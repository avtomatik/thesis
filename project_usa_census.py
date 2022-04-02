# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 00:13:17 2020

@author: Mastermind
"""


def fetch_census_description(file_name, series_id):
    """Retrieve Series Description U.S. Bureau of the Census"""
    data_frame = pd.read_csv(
        file_name, usecols=[0, 1, 3, 4, 5, 6, 8], low_memory=False)
    data_frame = data_frame[data_frame.iloc[:, 6] == series_id]
    data_frame.drop_duplicates(inplace=True)
    if data_frame.iloc[0, 2] == 'no_details':
        if data_frame.iloc[0, 5] == 'no_details':
            if data_frame.iloc[0, 4] == 'no_details':
                description = '{}'.format(data_frame.iloc[0, 3])
            else:
                description = '{} -\n{}'.format(*data_frame.iloc[0, [3, 4]])
        else:
            description = '{} -\n{} -\n{}'.format(*
                                                  data_frame.iloc[0, [3, 4, 5]])
    else:
        if data_frame.iloc[0, 5] == 'no_details':
            if data_frame.iloc[0, 4] == 'no_details':
                description = '{}; {}'.format(*data_frame.iloc[0, [3, 2]])
            else:
                description = '{} -\n{}; {}'.format(*
                                                    data_frame.iloc[0, [3, 4, 2]])
        else:
            description = '{} -\n{} -\n{}; {}'.format(
                *data_frame.iloc[0, [3, 4, 5, 2]])
    return description


def get_dataset_census_a():
    '''Census Manufacturing Indexes, 1899=100'''
    FILE_NAMES = ('dataset_usa_census1949.zip', 'dataset_usa_census1975.zip',)
    SERIES_IDS = (
        # =====================================================================
        # HSUS 1949 Page 179, J13
        # =====================================================================
        'J0013',
        # =====================================================================
        # HSUS 1949 Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014',
        # =====================================================================
        # HSUS 1975 Page 667, P17: Edwin Frickey Series, Indexes of Manufacturing Production
        # =====================================================================
        'P0017',)
    _args = [tuple((FILE_NAMES[1], series_id,)) if series_id.startswith(
        'P') else tuple((FILE_NAMES[0], series_id,)) for series_id in SERIES_IDS]
    data_frame = pd.concat([fetch_census(*_)
                           for _ in _args], axis=1, sort=True)
    data_frame = data_frame.div(
        data_frame.iloc[data_frame.index.get_loc(1899), :]).mul(100)
    return data_frame, data_frame.index.get_loc(1899)


def get_dataset_census_c():
    '''Census Primary Metals & Railroad-Related Products Manufacturing Series'''
    file_name = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('P0262', 'P0265', 'P0266', 'P0267', 'P0268',
                  'P0269', 'P0293', 'P0294', 'P0295',)
# =============================================================================
# <base_year>=100
# =============================================================================
    BASE_YEARS = (1875, 1875, 1875, 1875, 1875, 1909, 1880, 1875, 1875,)
    SERIES_ID_YEAR_MAP = {_: base_year for _,
                          base_year in enumerate(BASE_YEARS)}
    data_frame = pd.concat(
        [fetch_census(FILE_NAME, series_id) for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    for i in range(data_frame.shape[1]):
        base_year = data_frame.index.get_loc(SERIES_ID_YEAR_MAP[i])
        data_frame.iloc[:, i] = data_frame.iloc[:, i].div(
            data_frame.iloc[base_year, i]).mul(100)
    return data_frame, SERIES_ID_YEAR_MAP


def get_dataset_census_e():
    '''Census Total Immigration Series'''
    file_name = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('C0091', 'C0092', 'C0093', 'C0094', 'C0095', 'C0096',
                  'C0097', 'C0098', 'C0099', 'C0100', 'C0101', 'C0103',
                  'C0104', 'C0105', 'C0106', 'C0107', 'C0108', 'C0109',
                  'C0111', 'C0112', 'C0113', 'C0114', 'C0115', 'C0117',
                  'C0118', 'C0119',)
    data_frame = pd.concat(
        [fetch_census(FILE_NAME, series_id) for series_id in SERIES_IDS],
        axis=1,
        sort=True)

    data_frame['C89'] = data_frame.sum(1)
    return data_frame.iloc[:, [-1]]


def get_dataset_census_f():
    '''Census Employment Series'''
    file_name = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('D0085', 'D0086', 'D0796', 'D0797', 'D0977', 'D0982',)
    data_frame = pd.concat(
        [fetch_census(FILE_NAME, series_id) for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    data_frame['workers'] = data_frame.iloc[:, 0].div(
        data_frame.iloc[:, 1]).mul(100)
    data_frame.iloc[:, 4].fillna(
        data_frame.iloc[:data_frame.index.get_loc(1906), 4].mean(), inplace=True)
    data_frame.iloc[:, 5].fillna(
        data_frame.iloc[:data_frame.index.get_loc(1906), 5].mean(), inplace=True)
    return data_frame


def get_dataset_census_g():
    '''Census Gross National Product Series'''
    file_name = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('F0003', 'F0004',)
    data_frame = pd.concat(
        [fetch_census(FILE_NAME, series_id) for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    data_frame = data_frame[data_frame.index.get_loc(1889):]
    return data_frame.div(data_frame.iloc[0, :]).mul(100)


def get_dataset_census_i():
    '''Census Foreign Trade Series'''
# =============================================================================
# TODO: Divide Into Three Functions
# =============================================================================
    file_name = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('U0001', 'U0008',)
    data_frame_a = pd.concat(
        [fetch_census(FILE_NAME, series_id) for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    SERIES_IDS = ('U0187', 'U0188', 'U0189',)
    data_frame_b = pd.concat(
        [fetch_census(FILE_NAME, series_id) for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    SERIES_IDS = (
        'U0319', 'U0320', 'U0321', 'U0322', 'U0323', 'U0325', 'U0326',
        'U0327', 'U0328', 'U0330', 'U0331', 'U0332', 'U0333', 'U0334',
        'U0337', 'U0338', 'U0339', 'U0340', 'U0341', 'U0343', 'U0344',
        'U0345', 'U0346', 'U0348', 'U0349', 'U0350', 'U0351', 'U0352',
    )
    data_frame_c = pd.concat(
        [fetch_census(FILE_NAME, series_id) for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    data_frame_c['exports'] = data_frame_c.loc[:,
                                               SERIES_IDS[:len(SERIES_IDS) // 2]].sum(1)
    data_frame_c['imports'] = data_frame_c.loc[:,
                                               SERIES_IDS[len(SERIES_IDS) // 2:]].sum(1)
    return data_frame_a, data_frame_b, data_frame_c


def get_dataset_census_j():
    '''Census Money Supply Aggregates'''
    file_name = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('X0410', 'X0414', 'X0415',)
    data_frame = pd.concat(
        [fetch_census(FILE_NAME, series_id) for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    data_frame = data_frame.div(
        data_frame.iloc[data_frame.index.get_loc(1915), :]).mul(100)
    return data_frame, data_frame.index.get_loc(1915)


def plot_census_a(source_frame, base):
    plt.figure()
    plt.plot(source_frame.iloc[:, 0], label='Fabricant S., Shiskin J., NBER')
    plt.plot(source_frame.iloc[:, 1], color='red',
             linewidth=4, label='W.M. Persons')
    plt.plot(source_frame.iloc[:, 2], label='E. Frickey')
    plt.axvline(x=source_frame.index[base], linestyle=':')
    plt.title('US Manufacturing Indexes Of Physical Production Of Manufacturing, {}=100'.format(
        source_frame.index[base]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
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


def plot_census_c(source_frame, base):
    plt.figure(1)
    plt.semilogy(
        source_frame.iloc[:, 1], label='P265 - Raw Steel Produced - Total, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(
        source_frame.iloc[:, 2], label='P266 - Raw Steel Produced - Bessemer, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(
        source_frame.iloc[:, 3], label='P267 - Raw Steel Produced - Open Hearth, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(
        source_frame.iloc[:, 4], label='P268 - Raw Steel Produced - Crucible, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(
        source_frame.iloc[:, 5], label='P269 - Raw Steel Produced - Electric and All Other, {}=100'.format(source_frame.index[base[2]]))
    plt.axvline(x=source_frame.index[base[0]], linestyle=':')
    plt.axvline(x=source_frame.index[base[2]], linestyle=':')
    plt.title('Steel Production')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.semilogy(
        source_frame.iloc[:, 0], label='P262 - Rails Produced, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(
        source_frame.iloc[:, 6], label='P293 - Locomotives Produced, {}=100'.format(source_frame.index[base[1]]))
    plt.semilogy(
        source_frame.iloc[:, 7], label='P294 - Railroad Passenger Cars Produced, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(
        source_frame.iloc[:, 8], label='P295 - Railroad Freight Cars Produced, {}=100'.format(source_frame.index[base[0]]))
    plt.axvline(x=source_frame.index[base[0]], linestyle=':')
    plt.axvline(x=source_frame.index[base[1]], linestyle=':')
    plt.title('Rails & Cars Production')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_d(series_ids):
    '''series_ids: List for Series'''
    file_name = 'dataset_usa_census1975.zip'
    result_frame = pd.DataFrame()
    for series_id in series_ids:
        title = fetch_census_description(file_name, series_id)
        print(f'<{series_id}> {title}')
        data_frame = fetch_census(file_name, series_id)
        data_frame = data_frame.div(data_frame.iloc[0, :]).mul(100)
        result_frame = pd.concat([result_frame, data_frame], axis=1, sort=True)

    plt.figure()
    plt.semilogy(result_frame)
    plt.title('Series P 231$-$300. Physical Output of Selected Manufactured Commodities: {}$-${}'.format(
        result_frame.index[0], result_frame.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend(series_ids)
    plt.show()


def plot_census_e(source_frame):
    plt.figure()
    plt.plot(source_frame.iloc[:, 0])
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
    axs_a.set_ylabel('Number', color=color)
    axs_a.plot(source_frame.iloc[:, 4], color=color, label='Stoppages')
    axs_a.set_title('Work Conflicts')
    axs_a.grid()
    axs_a.legend(loc=2)
    axs_a.tick_params(axis='y', labelcolor=color)
    axs_b = axs_a.twinx()
    color = 'tab:blue'
    axs_b.set_ylabel('1,000 People', color=color)
    axs_b.plot(source_frame.iloc[:, 5], color=color, label='Workers Involved')
    axs_b.legend(loc=1)
    axs_b.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()
    plt.show()


def plot_census_g(source_frame):
    plt.figure()
    plt.plot(source_frame.iloc[:, 0], label='Gross National Product')
    plt.plot(source_frame.iloc[:, 1],
             label='Gross National Product Per Capita')
    plt.title('Gross National Product, Prices {}=100, {}=100'.format(
        1958, source_frame.index[0]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


def plot_census_h():
    '''Census 1975, Land in Farms'''
    file_name = 'dataset_usa_census1975.zip'
    result_frame = fetch_census(file_name, 'K0005')
    plt.figure()
    plt.plot(result_frame.iloc[:, 0])
    plt.title('Land in Farms')
    plt.xlabel('Period')
    plt.ylabel('1,000 acres')
    plt.grid()
    plt.show()


def plot_census_i(source_frame_a, source_frame_b, source_frame_c):
    plt.figure(1)
    plt.plot(source_frame_a.iloc[:, 0], label='Exports, U1')
    plt.plot(source_frame_a.iloc[:, 1], label='Imports, U8')
    plt.plot(source_frame_a.iloc[:, 0].sub(
        source_frame_a.iloc[:, 1]), label='Net Exports')
    plt.title('Exports & Imports of Goods and Services, {}$-${}'.format(
        source_frame_a.index[0], source_frame_a.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.plot(source_frame_b.iloc[:, 0], label='Exports, U187')
    plt.plot(source_frame_b.iloc[:, 1], label='Imports, U188')
    plt.plot(source_frame_b.iloc[:, 2], label='Net Exports, U189')
    plt.title('Total Merchandise, Gold and Silver, {}$-${}'.format(
        source_frame_b.index[0], source_frame_b.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(3)
    plt.plot(source_frame_c.iloc[:, 0].sub(
        source_frame_c.iloc[:, 14]), label='America-Canada')
    plt.plot(source_frame_c.iloc[:, 1].sub(
        source_frame_c.iloc[:, 15]), label='America-Cuba')
    plt.plot(source_frame_c.iloc[:, 2].sub(
        source_frame_c.iloc[:, 16]), label='America-Mexico')
    plt.plot(source_frame_c.iloc[:, 3].sub(
        source_frame_c.iloc[:, 17]), label='America-Brazil')
    plt.plot(source_frame_c.iloc[:, 4].sub(
        source_frame_c.iloc[:, 18]), label='America-Other')
    plt.plot(source_frame_c.iloc[:, 5].sub(
        source_frame_c.iloc[:, 19]), label='Europe-United Kingdom')
    plt.plot(source_frame_c.iloc[:, 6].sub(
        source_frame_c.iloc[:, 20]), label='Europe-France')
    plt.plot(source_frame_c.iloc[:, 7].sub(
        source_frame_c.iloc[:, 21]), label='Europe-Germany')
    plt.plot(source_frame_c.iloc[:, 8].sub(
        source_frame_c.iloc[:, 22]), label='Europe-Other')
    plt.plot(source_frame_c.iloc[:, 9].sub(
        source_frame_c.iloc[:, 23]), label='Asia-Mainland China')
    plt.plot(source_frame_c.iloc[:, 10].sub(
        source_frame_c.iloc[:, 24]), label='Asia-Japan')
    plt.plot(source_frame_c.iloc[:, 11].sub(
        source_frame_c.iloc[:, 25]), label='Asia-Other')
    plt.plot(source_frame_c.iloc[:, 12].sub(
        source_frame_c.iloc[:, 26]), label='Australia and Oceania-All')
    plt.plot(source_frame_c.iloc[:, 13].sub(
        source_frame_c.iloc[:, 27]), label='Africa-All')
    plt.title('Net Exports')
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(4)
    plt.plot(source_frame_c.iloc[:, 0].sub(source_frame_c.iloc[:, 14]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Canada')
    plt.plot(source_frame_c.iloc[:, 1].sub(source_frame_c.iloc[:, 15]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Cuba')
    plt.plot(source_frame_c.iloc[:, 2].sub(source_frame_c.iloc[:, 16]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Mexico')
    plt.plot(source_frame_c.iloc[:, 3].sub(source_frame_c.iloc[:, 17]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Brazil')
    plt.plot(source_frame_c.iloc[:, 4].sub(source_frame_c.iloc[:, 18]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Other')
    plt.plot(source_frame_c.iloc[:, 5].sub(source_frame_c.iloc[:, 19]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Europe-United Kingdom')
    plt.plot(source_frame_c.iloc[:, 6].sub(source_frame_c.iloc[:, 20]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Europe-France')
    plt.plot(source_frame_c.iloc[:, 7].sub(source_frame_c.iloc[:, 21]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Europe-Germany')
    plt.plot(source_frame_c.iloc[:, 8].sub(source_frame_c.iloc[:, 22]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Europe-Other')
    plt.plot(source_frame_c.iloc[:, 9].sub(source_frame_c.iloc[:, 23]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Asia-Mainland China')
    plt.plot(source_frame_c.iloc[:, 10].sub(source_frame_c.iloc[:, 24]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Asia-Japan')
    plt.plot(source_frame_c.iloc[:, 11].sub(source_frame_c.iloc[:, 25]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Asia-Other')
    plt.plot(source_frame_c.iloc[:, 12].sub(source_frame_c.iloc[:, 26]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Australia and Oceania-All')
    plt.plot(source_frame_c.iloc[:, 13].sub(source_frame_c.iloc[:, 27]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Africa-All')
    plt.title('Net Exports')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.legend()
    plt.show()


def plot_census_j(data_frame, base):
    plt.figure()
    plt.semilogy(data_frame,
                 label=['Currency Held by the Public',
                        'M1 Money Supply (Currency Plus Demand Deposits)',
                        'M2 Money Supply (M1 Plus Time Deposits)'])
    plt.axvline(x=data_frame.index[base], linestyle=':')
    plt.title('Currency Dynamics, {}=100'.format(data_frame.index[base]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


def plot_census_k():
    """Census Financial Markets & Institutions Series"""
    file_name = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('X0410', 'X0411', 'X0412', 'X0413', 'X0414', 'X0415',
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
    for i, series_id in enumerate(SERIES_IDS):
        title = fetch_census_description(file_name, series_id)
        data_frame = fetch_census(file_name, series_id)
        data_frame = data_frame.div(data_frame.iloc[0, :]).mul(100)
        plt.figure(1+i)
        plt.plot(data_frame, label=f'{series_id}')
        plt.title('{}, {}$-${}'.format(title,
                  data_frame.index[0], data_frame.index[-1]))
        plt.xlabel('Period')
        plt.ylabel('Percentage')
        plt.grid(True)
        plt.legend()
        plt.show()


plot_census_a(*get_dataset_census_a())
plot_census_b(get_dataset_census_b_a(), get_dataset_census_b_b())
plot_census_c(*get_dataset_census_c())
# =============================================================================
# Census Production Series
# =============================================================================
SERIES_IDS = (
    'P0248', 'P0249', 'P0250', 'P0251', 'P0262',
    'P0265', 'P0266', 'P0267', 'P0268', 'P0269',
    'P0293', 'P0294', 'P0295',
)
alternative = (
    'P0231', 'P0232', 'P0233', 'P0234', 'P0235',
    'P0236', 'P0237', 'P0238', 'P0239', 'P0240',
    'P0241', 'P0244', 'P0247', 'P0248', 'P0249',
    'P0250', 'P0251', 'P0252', 'P0253', 'P0254',
    'P0255', 'P0256', 'P0257', 'P0258', 'P0259',
    'P0260', 'P0261', 'P0262', 'P0263', 'P0264',
    'P0265', 'P0266', 'P0267', 'P0268', 'P0269',
    'P0270', 'P0271', 'P0277', 'P0279', 'P0281',
    'P0282', 'P0283', 'P0284', 'P0286', 'P0288',
    'P0290', 'P0293', 'P0294', 'P0295', 'P0296',
    'P0297', 'P0298', 'P0299', 'P0300',
)
plot_census_d(SERIES_IDS)
plot_census_e(get_dataset_census_e())
result_frame = get_dataset_census_f()
plot_census_f_a(result_frame)
plot_census_f_b(result_frame)
plot_census_g(get_dataset_census_g())
plot_census_h()
plot_census_i(*get_dataset_census_i())
plot_census_j(*get_dataset_census_j())
plot_census_k()
