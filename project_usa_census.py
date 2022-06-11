# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 00:13:17 2020

@author: Mastermind
"""


def extract_usa_census_description(archive_name: str, series_id: str) -> str:
    '''Retrieve Series Description U.S. Bureau of the Census'''
    FLAG = 'no_details'
    _df = pd.read_csv(
        archive_name,
        usecols=[0, 1, 3, 4, 5, 6, 8],
        low_memory=False
    )
    _df = _df[_df.iloc[:, 6] == series_id]
    _df.drop_duplicates(inplace=True)
    if _df.iloc[0, 2] == FLAG:
        if _df.iloc[0, 5] == FLAG:
            if _df.iloc[0, 4] == FLAG:
                description = '{}'.format(_df.iloc[0, 3])
            else:
                description = '{} -\n{}'.format(*_df.iloc[0, [3, 4]])
        else:
            description = '{} -\n{} -\n{}'.format(*_df.iloc[0, [3, 4, 5]])
    else:
        if _df.iloc[0, 5] == FLAG:
            if _df.iloc[0, 4] == FLAG:
                description = '{}; {}'.format(*_df.iloc[0, [3, 2]])
            else:
                description = '{} -\n{}; {}'.format(*_df.iloc[0, [3, 4, 2]])
        else:
            description = '{} -\n{} -\n{}; {}'.format(
                *_df.iloc[0, [3, 4, 5, 2]])
    return description


def get_data_census_a():
    '''Census Manufacturing Indexes, 1899=100'''
    ARCHIVE_NAMES = ('dataset_usa_census1949.zip',
                     'dataset_usa_census1975.zip',)
    SERIES_IDS = (
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014',
        # =====================================================================
        # HSUS 1975 Page 667, P17: Edwin Frickey Series, Indexes of Manufacturing Production
        # =====================================================================
        'P0017',)
    _args = [tuple((ARCHIVE_NAMES[1], series_id,)) if series_id.startswith(
        'P') else tuple((ARCHIVE_NAMES[0], series_id,)) for series_id in SERIES_IDS]
    data_frame = pd.concat([extract_usa_census(*_)
                           for _ in _args], axis=1, sort=True)
    data_frame = data_frame.div(
        data_frame.iloc[data_frame.index.get_loc(1899), :]).mul(100)
    return data_frame, data_frame.index.get_loc(1899)


def get_data_census_c() -> tuple[pd.DataFrame, tuple[int]]:
    '''Census Primary Metals & Railroad-Related Products Manufacturing Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = (
        'P0262', 'P0265', 'P0266', 'P0267', 'P0268', 'P0269', 'P0293', 'P0294', 'P0295',
    )
    # =========================================================================
    # <base_year>=100
    # =========================================================================
    # =========================================================================
    # TODO: Extract Base Years
    # =========================================================================
    BASE_YEARS = (1875, 1875, 1875, 1875, 1875, 1909, 1880, 1875, 1875,)
    data_frame = pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)
    for _ in range(data_frame.shape[1]):
        base_year = data_frame.index.get_loc(BASE_YEARS[_])
        data_frame.iloc[:, _] = data_frame.iloc[:, _].div(
            data_frame.iloc[base_year, _]).mul(100)
    return data_frame, BASE_YEARS


def get_data_census_e() -> pd.DataFrame:
    '''Census Total Immigration Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = (
        'C0091', 'C0092', 'C0093', 'C0094', 'C0095', 'C0096', 'C0097', 'C0098',
        'C0099', 'C0100', 'C0101', 'C0103', 'C0104', 'C0105', 'C0106', 'C0107',
        'C0108', 'C0109', 'C0111', 'C0112', 'C0113', 'C0114', 'C0115', 'C0117',
        'C0118', 'C0119',
    )
    data_frame = pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)

    data_frame['C89'] = data_frame.sum(1)
    return data_frame.iloc[:, [-1]]


def get_data_census_f() -> pd.DataFrame:
    '''Census Employment Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('D0085', 'D0086', 'D0796', 'D0797', 'D0977', 'D0982',)
    df = pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)
    df['workers'] = df.iloc[:, 0].div(df.iloc[:, 1]).mul(100)
    df.iloc[:, 4].fillna(
        df.iloc[:df.index.get_loc(1906), 4].mean(), inplace=True)
    df.iloc[:, 5].fillna(
        df.iloc[:df.index.get_loc(1906), 5].mean(), inplace=True)
    return df


def get_data_census_g() -> pd.DataFrame:
    '''Census Gross National Product Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('F0003', 'F0004',)
    data_frame = pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)
    data_frame = data_frame[data_frame.index.get_loc(1889):]
    return data_frame.div(data_frame.iloc[0, :]).mul(100)


def get_data_census_i_a() -> pd.DataFrame:
    '''Census Foreign Trade Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('U0001', 'U0008', 'U0015',)
    return pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)


def get_data_census_i_b() -> pd.DataFrame:
    '''Census Foreign Trade Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('U0187', 'U0188', 'U0189',)
    return pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)


def get_data_census_i_c() -> pd.DataFrame:
    '''Census Foreign Trade Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = (
        'U0319', 'U0320', 'U0321', 'U0322', 'U0323', 'U0325', 'U0326', 'U0327',
        'U0328', 'U0330', 'U0331', 'U0332', 'U0333', 'U0334', 'U0337', 'U0338',
        'U0339', 'U0340', 'U0341', 'U0343', 'U0344', 'U0345', 'U0346', 'U0348',
        'U0349', 'U0350', 'U0351', 'U0352',
    )
    df = pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)

    for _ in range(len(SERIES_IDS) // 2):
        _title = f'{df.columns[_]}_net_{df.columns[_ + len(SERIES_IDS) // 2]}'
        df[_title] = df.iloc[:, _].sub(df.iloc[:, _ + len(SERIES_IDS) // 2])

    df['exports'] = df.loc[:, SERIES_IDS[:len(SERIES_IDS) // 2]].sum(1)
    df['imports'] = df.loc[:, SERIES_IDS[len(SERIES_IDS) // 2:]].sum(1)

    for _ in range(len(SERIES_IDS) // 2):
        _title = f'{df.columns[_ + len(SERIES_IDS)]}_over_all'
        df[_title] = df.iloc[:, _ +
                             len(SERIES_IDS)].div(df.loc[:, 'exports'].sub(df.loc[:, 'imports']))

    return df


def get_data_census_j() -> pd.DataFrame:
    '''Census Money Supply Aggregates'''
    YEAR_BASE = 1915
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('X0410', 'X0414', 'X0415',)
    df = pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)
    return df.div(df.iloc[df.index.get_loc(YEAR_BASE), :]).mul(100)


def plot_census_a(df: pd.DataFrame, base: int) -> None:
    plt.figure()
    plt.plot(df.iloc[:, [0, 2]], label=[
        'Fabricant S., Shiskin J., NBER',
        'E. Frickey',
    ])
    plt.plot(df.iloc[:, 1], color='red', linewidth=4, label='W.M. Persons')
    plt.axvline(x=df.index[base], linestyle=':')
    plt.title(
        'US Manufacturing Indexes Of Physical Production Of Manufacturing, {}=100, {}$-${}'.format(
            df.index[base], *df.index[[0, -1]])
    )
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_b_capital(df: pd.DataFrame) -> None:
    '''Census Manufacturing Fixed Assets Series'''
    plt.figure()
    plt.semilogy(df, label=['Total', 'Structures', 'Equipment'])
    plt.title('Census Manufacturing Fixed Assets, {}$-${}'.format(
        *df.index[[0, -1]]
    ))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_b_deflator(df: pd.DataFrame) -> None:
    '''Census Manufacturing Fixed Assets Deflator Series'''
    plt.figure()
    plt.plot(df)
    plt.title('Census Fused Fixed Assets Deflator, {}$-${}'.format(
        *df.index[[0, -1]])
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.show()


def plot_census_c(df: pd.DataFrame, base: tuple[int]) -> None:
    _DESCS_RAW = (
        'P262 - Rails Produced, {}=100',
        'P265 - Raw Steel Produced - Total, {}=100',
        'P266 - Raw Steel Produced - Bessemer, {}=100',
        'P267 - Raw Steel Produced - Open Hearth, {}=100',
        'P268 - Raw Steel Produced - Crucible, {}=100',
        'P269 - Raw Steel Produced - Electric and All Other, {}=100',
        'P293 - Locomotives Produced, {}=100',
        'P294 - Railroad Passenger Cars Produced, {}=100',
        'P295 - Railroad Freight Cars Produced, {}=100',
    )
    _DESCS = [_desc.format(_b) for _desc, _b in zip(_DESCS_RAW, base)]
    _MAPPING = dict(zip(df.columns, _DESCS))
    _COLUMN_LOCS = [_ for _ in range(df.shape[1]) if _ not in range(1, 6)]
    plt.figure(1)
    plt.semilogy(
        df.iloc[:, range(1, 6)],
        label=[_MAPPING[_] for _ in df.columns[range(1, 6)]]
    )
    for _ in range(1, 6):
        plt.axvline(x=base[_], linestyle=':')
    plt.title('Steel Production')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.semilogy(
        df.iloc[:, _COLUMN_LOCS],
        label=[_MAPPING[_] for _ in df.columns[_COLUMN_LOCS]]
    )
    for _ in _COLUMN_LOCS:
        plt.axvline(x=base[_], linestyle=':')
    plt.title('Rails & Cars Production')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_d(series_ids: tuple[str]) -> None:
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    df = pd.DataFrame()
    for series_id in series_ids:
        title = extract_usa_census_description(ARCHIVE_NAME, series_id)
        print(f'<{series_id}> {title}')
        chunk = extract_usa_census(ARCHIVE_NAME, series_id)
        df = pd.concat(
            [
                df,
                chunk.div(chunk.iloc[0, :]).mul(100)
            ],
            axis=1, sort=True)
    _title = 'Series P 231$-$300. Physical Output of Selected Manufactured Commodities: {}$-${}'.format(
        *df.index[[0, -1]]
    )
    plt.figure()
    plt.semilogy(df)
    plt.title(_title)
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend(series_ids)
    plt.show()


def plot_census_e(df: pd.DataFrame) -> None:
    plt.figure()
    plt.plot(df)
    plt.title('Total Immigration, {}$-${}'.format(*df.index[[0, -1]]))
    plt.xlabel('Period')
    plt.ylabel('People')
    plt.grid(True)
    plt.show()


def plot_census_f_a(df: pd.DataFrame) -> None:
    plt.figure(1)
    plt.plot(df.iloc[:, 1])
    plt.title('Unemployment, Percent of Civilian Labor Force')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.figure(2)
    plt.plot(df.iloc[:, [2, 3]], label=['Bureau of Labour', 'Wolman'])
    plt.title('All Manufacturing, Average Full-Time Weekly Hours, 1890-1899=100')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.plot(df.iloc[:, 6])
    plt.title('Implicit Number of Workers')
    plt.xlabel('Period')
    plt.ylabel('Persons')
    plt.grid(True)
    plt.show()


def plot_census_f_b(df: pd.DataFrame) -> None:
    fig, _axs_stoppages = plt.subplots()
    color = 'tab:red'
    _axs_stoppages.set_xlabel('Period')
    _axs_stoppages.set_ylabel('Number', color=color)
    _axs_stoppages.plot(df.iloc[:, 4], color=color, label='Stoppages')
    _axs_stoppages.set_title('Work Conflicts')
    _axs_stoppages.grid(True)
    _axs_stoppages.legend(loc=2)
    _axs_stoppages.tick_params(axis='y', labelcolor=color)
    _axs_workers = _axs_stoppages.twinx()
    color = 'tab:blue'
    _axs_workers.set_ylabel('1,000 People', color=color)
    _axs_workers.plot(df.iloc[:, 5], color=color, label='Workers Involved')
    _axs_workers.legend(loc=1)
    _axs_workers.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()
    plt.show()


def plot_census_g(df: pd.DataFrame) -> None:
    plt.figure()
    plt.plot(df, label=[
        'Gross National Product',
        'Gross National Product Per Capita',
    ])
    plt.title(
        'Gross National Product, Prices {}=100, {}=100'.format(
            1958, df.index[0]
        ))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_h() -> None:
    '''Census 1975, Land in Farms'''
    _kwargs = {
        'archive_name': 'dataset_usa_census1975.zip',
        'series_id': 'K0005',
    }
    plt.figure()
    plt.plot(extract_usa_census(**_kwargs))
    plt.title('Land in Farms')
    plt.xlabel('Period')
    plt.ylabel('1,000 acres')
    plt.grid(True)
    plt.show()


def plot_census_i_a(df: pd.DataFrame) -> None:
    plt.figure()
    plt.plot(df, label=[
        'Exports, U1',
        'Imports, U8',
        'Net Exports, U15',
    ])
    plt.title(
        'Exports & Imports of Goods and Services, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_i_b(df: pd.DataFrame) -> None:
    plt.figure()
    plt.plot(df, label=[
        'Exports, U187',
        'Imports, U188',
        'Net Exports, U189',
    ])
    plt.title(
        'Total Merchandise, Gold and Silver, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_i_c(df: pd.DataFrame) -> None:
    assert df.shape[1] == 58, 'Works on DataFrame Produced with `get_data_census_i_c()`'
    _LABELS = (
        'America-Canada',
        'America-Cuba',
        'America-Mexico',
        'America-Brazil',
        'America-Other',
        'Europe-United Kingdom',
        'Europe-France',
        'Europe-Germany',
        'Europe-Other',
        'Asia-Mainland China',
        'Asia-Japan',
        'Asia-Other',
        'Australia and Oceania-All',
        'Africa-All',
    )
    plt.figure(1)
    plt.plot(df.iloc[:, range(28, 42)], label=_LABELS)
    plt.title('Net Exports by Regions')
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.semilogy(df.iloc[:, -len(_LABELS):], label=_LABELS)
    plt.title('Net Exports by Regions to Overall Net Exports')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_j(df: pd.DataFrame) -> None:
    YEAR_BASE = 1915
    plt.figure()
    plt.semilogy(
        df,
        label=[
            'Currency Held by the Public',
            'M1 Money Supply (Currency Plus Demand Deposits)',
            'M2 Money Supply (M1 Plus Time Deposits)',
        ]
    )
    plt.axvline(x=YEAR_BASE, linestyle=':')
    plt.title('Currency Dynamics, {}=100'.format(YEAR_BASE))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_k() -> None:
    '''Census Financial Markets & Institutions Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = (
        'X0410', 'X0411', 'X0412', 'X0413', 'X0414', 'X0415', 'X0416',
        'X0417', 'X0418', 'X0419', 'X0420', 'X0421', 'X0422', 'X0423',
        'X0580', 'X0581', 'X0582', 'X0583', 'X0584', 'X0585', 'X0586',
        'X0587', 'X0610', 'X0611', 'X0612', 'X0613', 'X0614', 'X0615',
        'X0616', 'X0617', 'X0618', 'X0619', 'X0620', 'X0621', 'X0622',
        'X0623', 'X0624', 'X0625', 'X0626', 'X0627', 'X0628', 'X0629',
        'X0630', 'X0631', 'X0632', 'X0633', 'X0741', 'X0742', 'X0743',
        'X0744', 'X0745', 'X0746', 'X0747', 'X0748', 'X0749', 'X0750',
        'X0751', 'X0752', 'X0753', 'X0754', 'X0755', 'X0879', 'X0880',
        'X0881', 'X0882', 'X0883', 'X0884', 'X0885', 'X0886', 'X0887',
        'X0888', 'X0889', 'X0890', 'X0891', 'X0892', 'X0893', 'X0894',
        'X0895', 'X0896', 'X0897', 'X0898', 'X0899', 'X0900', 'X0901',
        'X0902', 'X0903', 'X0904', 'X0905', 'X0906', 'X0907', 'X0908',
        'X0909', 'X0910', 'X0911', 'X0912', 'X0913', 'X0914', 'X0915',
        'X0916', 'X0917', 'X0918', 'X0919', 'X0920', 'X0921', 'X0922',
        'X0923', 'X0924', 'X0925', 'X0926', 'X0927', 'X0928', 'X0929',
        'X0930', 'X0931', 'X0932', 'X0947', 'X0948', 'X0949', 'X0950',
        'X0951', 'X0952', 'X0953', 'X0954', 'X0955', 'X0956',
    )
    for _, series_id in enumerate(SERIES_IDS, start=1):
        df = extract_usa_census(ARCHIVE_NAME, series_id)
        df = df.div(df.iloc[0, :]).mul(100)
        _title = extract_usa_census_description(ARCHIVE_NAME, series_id)
        plt.figure(_)
        plt.plot(df, label=series_id)
        plt.title('{}, {}$-${}'.format(_title, *df.index[[0, -1]]))
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
