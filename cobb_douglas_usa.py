# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 22:46:08 2021

@author: Mastermind
"""


import os
from collect.lib import transform_cobb_douglas
from plot.lib import plot_cobb_douglas


def main():
    DIR = '/media/alexander/321B-6A94'
    MAP_FIG = {
        'fg_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
        'fg_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        # =========================================================================
        # TODO: Update
        # =========================================================================
        'year_price': 1899,
    }
    os.chdir(DIR)
    plot_cobb_douglas(
        *transform_cobb_douglas(collect()),
        MAP_FIG
    )


if __name__ == '__main__':
    main()
