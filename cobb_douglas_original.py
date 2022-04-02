# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 18:28:15 2020

@author: Mastermind
"""


def fetch_classic(file_id: str, series_id: str) -> pd.DataFrame:
    # =========================================================================
    # Data Fetch Procedure for Enumerated Classical Datasets
    # =========================================================================
    usecols = {
        'dataset_douglas.zip': (4, 7,),
        'dataset_usa_brown.zip': (3, 6,),
        'dataset_usa_cobb-douglas.zip': (5, 8,),
        'dataset_usa_kendrick.zip': (4, 7,),
    }
    data_frame = pd.read_csv(file_id,
                             skiprows=(None, 4)[file_id ==
                                                'dataset_usa_brown.zip'],
                             usecols=range(*usecols[file_id]))
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].astype(int)
    data_frame.iloc[:, 1] = pd.to_numeric(
        data_frame.iloc[:, 1], errors='coerce')
    data_frame.columns = ['period', series_id]
    return data_frame.set_index(data_frame.columns[0])


def fetch_census(file_name: str, series_id: str, index: bool = True) -> pd.DataFrame:
    # =============================================================================
    # Selected Series by U.S. Bureau of the Census
    # U.S. Bureau of the Census, Historical Statistics of the United States,
    # 1789--1945, Washington, D.C., 1949.
    # U.S. Bureau of the Census. Historical Statistics of the United States,
    # Colonial Times to 1970, Bicentennial Edition. Washington, D.C., 1975.
    # =============================================================================
    data_frame = pd.read_csv(file_name,
                             usecols=range(8, 11),
                             dtype=str)
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].str[:4].astype(int)
    data_frame.iloc[:, 1] = data_frame.iloc[:, 1].astype(float)
    data_frame.columns = [data_frame.columns[0], series_id]
    data_frame.sort_values(data_frame.columns[0], inplace=True)
    data_frame = data_frame.groupby(data_frame.columns[0]).mean()
    if index:
        return data_frame
    else:
        return data_frame.reset_index(level=0)


def plot_cobb_douglas(data_frame: pd.DataFrame) -> pd.DataFrame:
    # =============================================================================
    # TODO: Refactor to Increase Cohesion
    # =============================================================================
    # =============================================================================
    # Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    # data_frame.index: Period,
    # data_frame.iloc[:, 0]: Capital,
    # data_frame.iloc[:, 1]: Labor,
    # data_frame.iloc[:, 2]: Product
    # =============================================================================
    def pl(series, k=0.25, b=1.01):
        return b*series**(-k)

    def pc(series, k=0.25, b=1.01):
        return b*series**(1-k)

    FIGURES = {
        'fig_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
        'fig_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
        'fig_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fig_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
    }
    X = data_frame.iloc[:, 0].div(data_frame.iloc[:, 1])
    Y = data_frame.iloc[:, 2].div(data_frame.iloc[:, 1])
    X = log(X)
    Y = log(Y)
    # =============================================================================
    # Original: k=0.25
    # =============================================================================
    k, b = np.polyfit(X, Y, 1)
    b = np.exp(b)
    data_frame['prod_comp'] = b * \
        (data_frame.iloc[:, 0]**k)*(data_frame.iloc[:, 1]**(1-k))
    data_frame['prod_roll'] = data_frame.iloc[:,
                                              2].rolling(window=3, center=True).mean()
    data_frame['prod_roll_comp'] = data_frame.iloc[:,
                                                   3].rolling(window=3, center=True).mean()
    plt.figure(1)
    plt.semilogy(data_frame.iloc[:, 0], label='Fixed Capital')
    plt.semilogy(data_frame.iloc[:, 1], label='Labor Force')
    plt.semilogy(data_frame.iloc[:, 2], label='Physical Product')
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(FIGURES['fig_a'].format(data_frame.index[0],
                                      data_frame.index[-1],
                                      data_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.semilogy(data_frame.iloc[:, 2], label='Actual Product')
    plt.semilogy(
        data_frame.iloc[:, 3], label='Computed Product, $P\' = {:,.4f}L^{{{:,.4f}}}C^{{{:,.4f}}}$'.format(b, 1-k, k))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(FIGURES['fig_b'].format(data_frame.index[0],
                                      data_frame.index[-1],
                                      data_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(data_frame.iloc[:, 2].sub(data_frame.iloc[:, 4]),
             label='Deviations of $P$')
    plt.plot(data_frame.iloc[:, 3].sub(data_frame.iloc[:, 5]), '--',
             label='Deviations of $P\'$')
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(FIGURES['fig_c'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(data_frame.iloc[:, 3].div(data_frame.iloc[:, 2]).sub(1))
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(FIGURES['fig_d'].format(data_frame.index[0],
                                      data_frame.index[-1]))
    plt.grid(True)
    plt.figure(5, figsize=(5, 8))
    lc = np.arange(0.2, 1.0, 0.005)
    plt.scatter(data_frame.iloc[:, 1].div(data_frame.iloc[:, 0]),
                data_frame.iloc[:, 2].div(data_frame.iloc[:, 1]))
    plt.scatter(data_frame.iloc[:, 1].div(data_frame.iloc[:, 0]),
                data_frame.iloc[:, 2].div(data_frame.iloc[:, 0]))
    plt.plot(lc, pl(lc, k=k, b=b), label='$\\frac{3}{4}\\frac{P}{L}$')
    plt.plot(lc, pc(lc, k=k, b=b), label='$\\frac{1}{4}\\frac{P}{C}$')
    plt.xlabel('$\\frac{L}{C}$')
    plt.ylabel('Indexes')
    plt.title('Relative Final Productivities of Labor and Capital')
    plt.legend()
    plt.grid(True)
    return data_frame


def get_dataset_cobb_douglas() -> pd.DataFrame:
    '''Original Cobb--Douglas Data Preprocessing'''
    FILE_NAMES = ('dataset_usa_cobb-douglas.zip',
                  'dataset_usa_census1949.zip',)
    # =========================================================================
    # Total Fixed Capital in 1880 dollars (4)
    # Average Number Employed (in thousands)
    # HSUS 1949 Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
    # =========================================================================
    data_frame = pd.concat([fetch_classic(FILE_NAMES[0], 'CDT2S4'),
                            fetch_classic(FILE_NAMES[0], 'CDT3S1'),
                            fetch_census(FILE_NAMES[1], 'J0014')],
                           axis=1,
                           sort=True)
    data_frame.dropna(inplace=True)
    return data_frame.div(data_frame.iloc[0, :])


def get_dataset_cobb_douglas_extended() -> pd.DataFrame:
    '''Original Cobb--Douglas Data Preprocessing Extension'''
    FILE_NAMES = ('dataset_usa_cobb-douglas.zip',
                  'dataset_usa_census1949.zip',
                  'dataset_douglas.zip',)
    data_frame = pd.concat([fetch_classic(FILE_NAMES[0], 'CDT2S4'),
                            fetch_classic(FILE_NAMES[0], 'CDT3S1'),
                            fetch_census(FILE_NAMES[1], 'J0014'),
                            fetch_census(FILE_NAMES[1], 'J0013'),
                            # =================================================
                            # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
                            # =================================================
                            fetch_classic(FILE_NAMES[2], 'DT24AS01')], axis=1, sort=True)
    data_frame.dropna(inplace=True)
    return data_frame.div(data_frame.iloc[0, :])


result_frame = plot_cobb_douglas(get_dataset_cobb_douglas())
result_frame['lab_cap'] = result_frame.iloc[:, 1].div(result_frame.iloc[:, 0])
result_frame['lab_pro'] = result_frame.iloc[:, 2].div(result_frame.iloc[:, 1])
result_frame['cap_pro'] = result_frame.iloc[:, 2].div(result_frame.iloc[:, 0])
result_frame = result_frame.iloc[:, range(6, 9)]
result_frame = result_frame.mul(100)
result_frame.set_index('lab_cap', inplace=True)
# result_frame.dropna(inplace=True)
result_frame.to_csv('cobb_douglas_usa_pro.dat', sep=' ')
# result_frame = get_dataset_cobb_douglas()
# result_frame.columns = ['capital', 'labor', 'product']
# result_frame = result_frame.iloc[:, 2]
# result_frame = result_frame.mul(100)
# result_frame.to_csv('cobb_douglas_usa_pro.dat', sep=' ')
print(result_frame)
