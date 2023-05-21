# =============================================================================
# annotations.py
# =============================================================================


import os

import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

from thesis.src.lib.combine import (combine_usa_macroeconomics,
                                    combine_usa_manufacturing_latest)
from thesis.src.lib.plot import plot_increment


def transform_add_dx_dy(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Capital
        df.iloc[:, 1]      Labor
        df.iloc[:, 2]      Product
        ================== =================================
    Returns
    -------
    df : DataFrame
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


def plot_increment(df: DataFrame) -> None:
    """


    Parameters
    ----------
    df : DataFrame
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


def main(
    path_src: str = '/media/green-machine/KINGSTON'
):
    # =========================================================================
    # TODO: Revise Dataset
    # =========================================================================

    os.chdir(path_src)
    df = combine_usa_macroeconomics().pipe(transform_macroeconomics)

    # =========================================================================
    # Option 1: 1967--2012
    # =========================================================================
    pd.concat([df['cap_0x0'], L, df['prd_0x0']], axis=1
              ).pipe(transform_add_dx_dy)
    # =========================================================================
    # Option 2: 1967--2012
    # =========================================================================
    pd.concat([df['cap_0x0'], L, df['prd_0x1']], axis=1
              ).pipe(transform_add_dx_dy)
    # =========================================================================
    # Option 3: 1967--2012
    # =========================================================================
    pd.concat([df['cap_0x3'], L, df['prd_0x0']],
              axis=1).pipe(transform_add_dx_dy)
    # =========================================================================
    # Option 4: 1967--2012
    # =========================================================================
    pd.concat([df['cap_0x3'], L, df['prd_0x1']],
              axis=1).pipe(transform_add_dx_dy)
    # =========================================================================
    # TODO: test 'k1ntotl1si00'
    # =========================================================================
    # =========================================================================
    # Option 1: 1929--2013
    # =========================================================================
    pd.concat([df['cap_0x2'], L, df['prd_0x3']],
              axis=1).pipe(transform_add_dx_dy)
    # =========================================================================
    # Option 2: 1929--2013
    # =========================================================================
    pd.concat([df['cap_0x1'], L, df['prd_0x4']],
              axis=1).pipe(transform_add_dx_dy)
    # =========================================================================
    # Option 5: 1929--2013
    # =========================================================================
    pd.concat([df['cap_0x4'], L, df['prd_0x3']],
              axis=1).pipe(transform_add_dx_dy)

    # =========================================================================
    # Option 6: 1929--2013
    # =========================================================================
    pd.concat([df['cap_0x3'], L, df['prd_0x4']], axis=1).pipe(
        transform_add_dx_dy
    ).pipe(plot_increment)

    combine_usa_manufacturing_latest().pipe(
        transform_add_dx_dy
    ).pipe(plot_increment)


if __name__ == '__main__':
    main()
