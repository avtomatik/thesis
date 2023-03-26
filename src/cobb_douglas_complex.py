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
    df = stockpile_cobb_douglas(5)

    # =========================================================================
    # On Expanded Dataset
    # =========================================================================
    df_d, df_e = collect_usa_manufacturing_two_fold()
    df_f, df_g, df_h = collect_usa_manufacturing_three_fold()
    df.iloc[:, range(3)].pipe(plot_cobb_douglas_complex)
    df.iloc[:, (0, 1, 3)].pipe(plot_cobb_douglas_complex)
    df.iloc[:, (0, 1, 4)].pipe(plot_cobb_douglas_complex)
    # =========================================================================
    # No Capacity Utilization Adjustment
    # =========================================================================
    df_d.pipe(plot_cobb_douglas_complex)
    # =========================================================================
    # Capacity Utilization Adjustment
    # =========================================================================
    df_e.pipe(plot_cobb_douglas_complex)
    # =========================================================================
    # Option: 1929--2013, No Capacity Utilization Adjustment
    # =========================================================================
    df_f.pipe(plot_cobb_douglas_complex)
    # =========================================================================
    # Option: 1967--2013, No Capacity Utilization Adjustment
    # =========================================================================
    df_g.pipe(plot_cobb_douglas_complex)
    # =========================================================================
    # Option: 1967--2012, Capacity Utilization Adjustment
    # =========================================================================
    df_h.pipe(plot_cobb_douglas_complex)
    collect_usa_manufacturing_latest().pipe(plot_cobb_douglas_complex)


if __name__ == '__main__':
    main()
