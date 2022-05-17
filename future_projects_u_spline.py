# =============================================================================
# Scipy Univariate Spline
# =============================================================================


import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from functools import partial
from scipy.interpolate import UnivariateSpline


def fetch_usa_census(archive_name: str, series_id: str) -> pd.DataFrame:
    # =========================================================================
    # Selected Series by U.S. Bureau of the Census
    # U.S. Bureau of the Census, Historical Statistics of the United States,
    # 1789--1945, Washington, D.C., 1949.
    # U.S. Bureau of the Census. Historical Statistics of the United States,
    # Colonial Times to 1970, Bicentennial Edition. Washington, D.C., 1975.
    # =========================================================================
    data_frame = pd.read_csv(archive_name,
                             usecols=range(8, 11),
                             dtype=str)
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].str[:4].astype(int)
    data_frame.iloc[:, 1] = data_frame.iloc[:, 1].astype(float)
    data_frame.columns = [data_frame.columns[0], series_id]
    data_frame.sort_values(data_frame.columns[0], inplace=True)
    return data_frame.groupby(data_frame.columns[0]).mean()


def fetch_usa_classic(archive_name: str, series_id: str) -> pd.DataFrame:
    # =========================================================================
    # Data Fetch Procedure for Enumerated Classical Datasets
    # =========================================================================
    USECOLS = {
        'dataset_douglas.zip': (4, 7,),
        'dataset_usa_brown.zip': (3, 6,),
        'dataset_usa_cobb-douglas.zip': (5, 8,),
        'dataset_usa_kendrick.zip': (4, 7,),
    }
    data_frame = pd.read_csv(
        archive_name,
        skiprows=(None, 4)[archive_name == 'dataset_usa_brown.zip'],
        usecols=range(*USECOLS[archive_name])
    )
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].astype(int)
    data_frame.iloc[:, 1] = pd.to_numeric(
        data_frame.iloc[:, 1], errors='coerce')
    data_frame.columns = [data_frame.columns[0], series_id]
    return data_frame.set_index(data_frame.columns[0])


def get_data_cobb_douglas(series_number: int = 3) -> pd.DataFrame:
    '''Original Cobb--Douglas Data Preprocessing Extension'''
    ARCHIVE_NAMES = (
        'dataset_usa_cobb-douglas.zip',
        'dataset_usa_cobb-douglas.zip',
        'dataset_usa_census1949.zip',
        'dataset_usa_census1949.zip',
        'dataset_douglas.zip',
    )
    SERIES_IDS = {
        # =====================================================================
        # Cobb C.W., Douglas P.H. Capital Series: Total Fixed Capital in 1880 dollars (4)
        # =====================================================================
        'CDT2S4': 'capital',
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        'CDT3S1': 'labor',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014': 'product',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013': 'product_nber',
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01': 'product_rev',
    }
    FUNCTIONS = (
        fetch_usa_classic,
        fetch_usa_classic,
        fetch_usa_census,
        fetch_usa_census,
        fetch_usa_classic,
    )
    data_frame = pd.concat(
        [
            partial(func, **{'archive_name': archive_name,
                             'series_id': series_id})()
            for archive_name, series_id, func in zip(ARCHIVE_NAMES, SERIES_IDS.keys(), FUNCTIONS)
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    data_frame.columns = SERIES_IDS.values()
    return data_frame.div(data_frame.iloc[0, :]).iloc[:, range(series_number)]


def calculate_plot_uspline(df: pd.DataFrame):
    '''
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Labor,
    df.iloc[:, 2]: Product
    '''
    # =========================================================================
    # TODO: Increase Cohesion
    # =========================================================================
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    chunk = df.iloc[:, -2:]
    chunk.sort_values(chunk.columns[0], inplace=True)
    spl = UnivariateSpline(chunk.iloc[:, [0]], chunk.iloc[:, [1]])
    # =========================================================================
    # _new_axis = np.linspace(chunk.iloc[:, [0]].min(), chunk.iloc[:, [0]].max(), chunk.shape[0] - 1)
    # =========================================================================
    plt.figure()
    plt.scatter(chunk.iloc[:, [0]], chunk.iloc[:, [1]], label='Original')
    plt.plot(
        chunk.iloc[:, 0],
        spl(chunk.iloc[:, 0]),
        'g',
        lw=3,
        label='Spline'
    )
    plt.title(
        'Labor Capital Intensity & Labor Productivity, {}$-${}'.format(
            df.index[0],
            df.index[-1]
        )
    )
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    # =========================================================================
    # TODO: Figure Out How It Works
    # =========================================================================
    print(spl.antiderivative())
    # =========================================================================
    # TODO: Figure Out How It Works
    # =========================================================================
    print(spl.derivative())
    print(spl.derivatives(1))
    print(spl.ext)
    print(spl.get_coeffs())
    print(spl.get_knots())
    print(spl.get_residual())
    print(spl.integral(1., 1.75))
    print(spl.roots())
    print(spl.set_smoothing_factor(0.25))
    plt.show()


def main():
    os.chdir('/media/alexander/321B-6A94')
    calculate_plot_uspline(get_data_cobb_douglas())


if __name__ == '__main__':
    main()
