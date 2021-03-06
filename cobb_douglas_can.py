#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 11:29:40 2022

@author: alexander
"""

from collect.lib import collect_can
from collect.lib import transform_cobb_douglas
from plot.lib import plot_cobb_douglas
from plot.lib import plot_cobb_douglas_3d


def main():
    # =========================================================================
    # Canada
    # =========================================================================
    MAP_FIG = {
        'fg_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
        'fg_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        'year_price': 2007,
    }
    _df = collect_can()
    plot_cobb_douglas(
        *transform_cobb_douglas(_df),
        MAP_FIG
    )
    plot_cobb_douglas_3d(_df)


if __name__ == '__main__':
    main()
