# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 22:46:08 2021

@author: Alexander Mikhailov
"""


import os

from thesis.src.lib.combine import combine_usa_manufacturing_latest
from thesis.src.lib.plot import plot_cobb_douglas
from thesis.src.lib.transform import transform_cobb_douglas


def main():
    DIR = '/media/green-machine/KINGSTON'
    YEAR_BASE = 1899
    MAP_FIG = {
        'fg_a': f'Chart I Progress in Manufacturing {{}}$-${{}} ({YEAR_BASE}=100)',
        'fg_b': f'Chart II Theoretical and Actual Curves of Production {{}}$-${{}} ({YEAR_BASE}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        # =========================================================================
        # TODO: Update
        # =========================================================================
        'year_base': YEAR_BASE,
    }

    os.chdir(DIR)
    plot_cobb_douglas(
        *combine_usa_manufacturing_latest().pipe(transform_cobb_douglas, year_base=2012),
        MAP_FIG
    )


if __name__ == '__main__':
    main()
