# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:17:13 2020

@author: Alexander Mikhailov
"""


import os

from lib.collect import (collect_usa_manufacturing_latest,
                         collect_usa_manufacturing_three_fold,
                         collect_usa_manufacturing_two_fold,
                         stockpile_cobb_douglas)
from lib.plot import plot_cobb_douglas_complex


def main():
    DIR = '/media/green-machine/KINGSTON'

    os.chdir(DIR)
    # =========================================================================
    # On Original Dataset
    # =========================================================================
    _df = stockpile_cobb_douglas()
    df_a = _df.iloc[:, range(3)]
    df_b = _df.iloc[:, (0, 1, 3)]
    df_c = _df.iloc[:, (0, 1, 4)]
    # =========================================================================
    # On Expanded Dataset
    # =========================================================================
    df_d, df_e = collect_usa_manufacturing_two_fold()
    df_f, df_g, df_h = collect_usa_manufacturing_three_fold()
    plot_cobb_douglas_complex(df_a)
    plot_cobb_douglas_complex(df_b)
    plot_cobb_douglas_complex(df_c)
    # =========================================================================
    # No Capacity Utilization Adjustment
    # =========================================================================
    plot_cobb_douglas_complex(df_d)
    # =========================================================================
    # Capacity Utilization Adjustment
    # =========================================================================
    plot_cobb_douglas_complex(df_e)
    # =========================================================================
    # Option: 1929--2013, No Capacity Utilization Adjustment
    # =========================================================================
    plot_cobb_douglas_complex(df_f)
    # =========================================================================
    # Option: 1967--2013, No Capacity Utilization Adjustment
    # =========================================================================
    plot_cobb_douglas_complex(df_g)
    # =========================================================================
    # Option: 1967--2012, Capacity Utilization Adjustment
    # =========================================================================
    plot_cobb_douglas_complex(df_h)
    plot_cobb_douglas_complex(collect_usa_manufacturing_latest())


if __name__ == '__main__':
    main()