# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 21:17:48 2020

@author: Alexander Mikhailov
"""


import os

from lib.collect import collect_usa_general
from lib.plot import (plot_c, plot_d, plot_e, plot_investment,
                      plot_investment_manufacturing, plot_kurenkov)
from lib.transform import (combine_kurenkov, transform_b, transform_d,
                           transform_e, transform_investment_manufacturing,
                           transform_manufacturing_money)


def main():
    DIR = '/media/green-machine/KINGSTON'

    os.chdir(DIR)
    df_a = collect_usa_general()
    # =========================================================================
    # Project: Initial Version Dated: 05 October 2012
    # =========================================================================
    df_a_a = df_a.pipe(transform_investment_manufacturing)
    plot_investment_manufacturing(df_a_a)
    # =========================================================================
    # Project: Initial Version Dated: 23 November 2012
    # =========================================================================
    df_b_a = df_a.pipe(transform_b)
    plot_investment(df_b_a)
    # =========================================================================
    # Project: Initial Version Dated: 16 June 2013
    # =========================================================================
    df_c_a = df_a.pipe(transform_manufacturing_money)
    plot_c(df_c_a)
    # =========================================================================
    # Project: Initial Version Dated: 15 June 2015
    # =========================================================================
    plot_d(df_a.pipe(transform_d))
    # =========================================================================
    # Project: Initial Version Dated: 17 February 2013
    # =========================================================================
    df_e_a, df_e_b = df_a.pipe(transform_e)
    plot_e(df_e_a)
    plot_e(df_e_b)
    # =========================================================================
    # Project: BEA Data Compared with Kurenkov Yu.V. Data
    # =========================================================================
    plot_kurenkov(df_a.pipe(combine_kurenkov))


if __name__ == '__main__':
    main()
