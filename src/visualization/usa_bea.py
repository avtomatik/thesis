# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 21:17:48 2020

@author: Alexander Mikhailov
"""


import os

from lib.collect import collect_usa_general
from lib.plot import (plot_d, plot_e, plot_investment,
                      plot_investment_manufacturing, plot_kurenkov,
                      plot_manufacturing_money)
from lib.transform import (combine_kurenkov, transform_d, transform_e,
                           transform_investment,
                           transform_investment_manufacturing,
                           transform_manufacturing_money)


def main():
    DIR = '/media/green-machine/KINGSTON'

    os.chdir(DIR)
    df = collect_usa_general()
    # =========================================================================
    # Project: Initial Version Dated: 05 October 2012
    # =========================================================================
    df.pipe(transform_investment_manufacturing).pipe(plot_investment_manufacturing)
    # =========================================================================
    # Project: Initial Version Dated: 23 November 2012
    # =========================================================================
    df.pipe(transform_investment).pipe(plot_investment)
    # =========================================================================
    # Project: Initial Version Dated: 16 June 2013
    # =========================================================================
    df.pipe(transform_manufacturing_money).pipe(plot_manufacturing_money)
    # =========================================================================
    # Project: Initial Version Dated: 15 June 2015
    # =========================================================================
    df.pipe(transform_d).pipe(plot_d)
    # =========================================================================
    # Project: Initial Version Dated: 17 February 2013
    # =========================================================================
    df_e_a, df_e_b = df.pipe(transform_e)
    df_e_a.pipe(plot_e)
    df_e_b.pipe(plot_e)
    # =========================================================================
    # Project: BEA Data Compared with Kurenkov Yu.V. Data
    # =========================================================================
    plot_kurenkov(df.pipe(combine_kurenkov))


if __name__ == '__main__':
    main()
