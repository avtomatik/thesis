# =============================================================================
# D:\archiveProjectUSACobbDouglasOptions.py
# =============================================================================


import os

import matplotlib.pyplot as plt
import pandas as pd

from .lib.collect import (collect_usa_macroeconomics,
                          collect_usa_manufacturing_latest)
from .lib.plot import plot_increment


def transform_add_dx_dy(df: pd.DataFrame) -> pd.DataFrame:
    """


    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Capital
        df.iloc[:, 1]      Labor
        df.iloc[:, 2]      Product
        ================== =================================
    Returns
    -------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Labor Capital Intensity
        df.iloc[:, 1]      Labor Productivity
        df.iloc[:, 2]      Labor Capital Intensity Increment
        df.iloc[:, 3]      Labor Productivity Increment
        ================== =================================
    """
    _df = df.copy()
    _df.dropna(inplace=True)
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    _df['lab_cap_int'] = _df.iloc[:, 0].div(_df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    _df['lab_product'] = _df.iloc[:, 2].div(_df.iloc[:, 1])
    # =========================================================================
    # Labor Capital Intensity Increment
    # =========================================================================
    _df['lab_cap_int_inc'] = _df.iloc[:, -2].pct_change().add(1)
    # =========================================================================
    # Labor Productivity Increment
    # =========================================================================
    _df['lab_product_inc'] = _df.iloc[:, -2].pct_change().add(1)
    return _df.iloc[:, -4:].dropna(axis=0)


def plot_local(df: pd.DataFrame) -> None:
    """


    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Labor Capital Intensity
        df.iloc[:, 1]      Labor Productivity
        df.iloc[:, 2]      Labor Capital Intensity Increment
        df.iloc[:, 3]      Labor Productivity Increment
        ================== =================================
    Returns
    -------
    None
        DESCRIPTION.

    """
    # =========================================================================
    # Scenario I
    # =========================================================================
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(df.iloc[:, range(2)])
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    for _ in range(4, df.shape[0], 5):
        ax.annotate(df.index[_], (df.iloc[_, 0], df.iloc[_, 1]))
    plt.grid()
    plt.show()
    # =========================================================================
    # Scenario II
    # =========================================================================
    plt.figure()
    plt.plot(df.iloc[:, range(2)], 'o', df.iloc[:, range(2)], '-')
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.show()


def main():
    # =========================================================================
    # TODO: Revise Dataset
    # =========================================================================
    DIR = '/media/green-machine/KINGSTON'

    os.chdir(DIR)
    _df = collect_usa_macroeconomics()
    # =========================================================================
    # Deflator, 2009=100
    # =========================================================================
    _defl = _df.loc[:, ['A191RX1']].div(_df.loc[:, ['A191RC1']])
    # =========================================================================
    # Fixed Assets, K160491
    # =========================================================================
    cap_a_a = _df.loc[:, ['K160491']].mul(_defl)
    # =========================================================================
    # Fixed Assets, k3n31gd1es000
    # =========================================================================
    cap_a_b = _df.loc[:, ['k3n31gd1es000']].mul(_defl)
    cap_b_a = _df.loc[:, ['k1ntotl1si000']].mul(_df.loc[:, ['A191RD3']])
    cap_b_b = _df.loc[:, ['k1ntotl1si000']].mul(_defl)
    cap_b_c = _df.loc[:, ['k3n31gd1es000']].mul(_df.loc[:, ['A191RD3']])
    cap_b_d = _df.loc[:, ['k3n31gd1es000']].mul(_defl)
    L = _df.loc[:, ['bea_labor_mfg']]
    # =========================================================================
    # Production
    # =========================================================================
    prd_a_a = _df.loc[:, ['A032RC1']].mul(_defl)
    # =========================================================================
    # Production Maximum
    # =========================================================================
    prd_a_b = _df.loc[:, ['A032RC1']].div(
        _df.loc[:, ['CAPUTLB50001A']]).mul(_defl).mul(100)
    prd_b_a = _df.loc[:, ['A191RC1']].mul(_df.loc[:, ['A191RD3']])
    prd_b_b = _df.loc[:, ['A191RX1']]
    # =========================================================================
    # Option 1: 1967--2012
    # =========================================================================
    df = pd.concat(
        [_df.loc[:, ('K160491',)].mul(_defl), L, prd_a_a], axis=1
    ).pipe(transform_add_dx_dy)
    # =========================================================================
    # Option 2: 1967--2012
    # =========================================================================
    df = pd.concat(
        [_df.loc[:, ('K160491',)].mul(_defl), L, prd_a_b], axis=1
    ).pipe(transform_add_dx_dy)
    # =========================================================================
    # Option 3: 1967--2012
    # =========================================================================
    df = pd.concat([cap_a_b, L, prd_a_a], axis=1).pipe(transform_add_dx_dy)
    # =========================================================================
    # Option 4: 1967--2012
    # =========================================================================
    df = pd.concat([cap_a_b, L, prd_a_b], axis=1).pipe(transform_add_dx_dy)
    # =========================================================================
    # TODO: test `k1ntotl1si000`
    # =========================================================================
    # =========================================================================
    # Option 1: 1929--2013
    # =========================================================================
    df = pd.concat([cap_b_a, L, prd_b_a], axis=1).pipe(transform_add_dx_dy)
    # =========================================================================
    # Option 2: 1929--2013
    # =========================================================================
    df = pd.concat([cap_b_b, L, prd_b_b], axis=1).pipe(transform_add_dx_dy)
    # =========================================================================
    # Option 5: 1929--2013
    # =========================================================================
    df = pd.concat([cap_b_c, L, prd_b_a], axis=1).pipe(transform_add_dx_dy)
    # =========================================================================
    # Option 6: 1929--2013
    # =========================================================================
    df = pd.concat([cap_b_d, L, prd_b_b], axis=1).pipe(transform_add_dx_dy)
    plot_increment(df)
    plot_local(df)

    # =========================================================================
    # Update from `project.py`
    # =========================================================================

    _df = collect_usa_manufacturing_latest().pipe(transform_add_dx_dy)
    plot_increment(_df)
    plot_local(_df)


if __name__ == '__main__':
    main()
