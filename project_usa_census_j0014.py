# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 20:45:44 2019

@author: Mastermind
"""


def plot_growth_elasticity(df: pd.DataFrame) -> None:
    '''Growth Elasticity Plotting
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    # =========================================================================
    # TODO: Increase Cohesion of This Code: Send Plotting to Separate Function
    # =========================================================================
    df.reset_index(level=0, inplace=True)
    _df = pd.DataFrame()
    # =========================================================================
    # Period, Centered
    # =========================================================================
    _df[f'{df.columns[0]}'] = df.iloc[:, [0]].rolling(2).mean()
    df.index.to_series().rolling(2).mean()
    # =========================================================================
    # Series, Centered
    # =========================================================================
    _df[f'{df.columns[1]}_centered'] = df.iloc[:, [1]].rolling(2).mean()
    # =========================================================================
    # Series, Growth Rate
    # =========================================================================
    _df[f'{df.columns[1]}_growth_rate'] = df.iloc[:, [1]].sub(
        df.iloc[:, [1]].shift(2)).div(df.iloc[:, [1]].rolling(2).sum().shift(1))
    # =========================================================================
    # Series, Elasticity
    # =========================================================================
    _df[f'{df.columns[1]}_elasticity'] = df.iloc[:, [1]].rolling(2).sum(
    ).shift(-1).mul(2).div(df.iloc[:, [1]].rolling(4).sum().shift(-1)).sub(1)
    _df.set_index(_df.columns[0], inplace=True)
    _df.dropna(inplace=True)
    plt.figure()
    plt.plot(_df.iloc[:, [1]], label='Growth Rate')
    plt.plot(_df.iloc[:, [2]], label='Elasticity Rate')
    plt.title('Growth & Elasticity Rates')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.show()


file_name = 'dataset_usa_census1949.zip'
source_frame = fetch_census(file_name, 'J0014', False)
plot_growth_elasticity(source_frame)
plot_rmf(source_frame)
