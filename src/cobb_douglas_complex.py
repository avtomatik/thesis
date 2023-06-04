# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:17:13 2020

@author: Alexander Mikhailov
"""


import os

from thesis.src.lib.combine import (combine_cobb_douglas,
                                    combine_usa_manufacturing_latest,
                                    combine_usa_manufacturing_three_fold,
                                    combine_usa_manufacturing_two_fold)
from thesis.src.lib.plot import plot_cobb_douglas_complex


def main(path_src: str = '/media/green-machine/KINGSTON') -> None:

    os.chdir(path_src)
    # =========================================================================
    # On Original Dataset
    # =========================================================================
    df = combine_cobb_douglas(5)

    df.iloc[:, range(3)].pipe(plot_cobb_douglas_complex)
    df.iloc[:, [0, 1, 3]].pipe(plot_cobb_douglas_complex)
    df.iloc[:, [0, 1, 4]].pipe(plot_cobb_douglas_complex)

    # =========================================================================
    # On Expanded Dataset
    # =========================================================================
    df_d, df_e = combine_usa_manufacturing_two_fold()
    df_f, df_g, df_h = combine_usa_manufacturing_three_fold()

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
    combine_usa_manufacturing_latest().pipe(plot_cobb_douglas_complex)


if __name__ == '__main__':
    main()
