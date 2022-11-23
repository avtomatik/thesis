# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 18:28:15 2020

@author: Alexander Mikhailov
"""


import os

from collect.lib import collect_cobb_douglas
from plot.lib import plot_cobb_douglas
from transform.lib import transform_cobb_douglas


def main():
    """
    Cobb--Douglas Algorithm as per
    C.W. Cobb, P.H. Douglas. A Theory of Production, 1928 &
    P.H. Douglas. The Theory of Wages, 1934;

    Returns
    -------
    None.

    """
    DIR = '/media/green-machine/KINGSTON'
    MAP_FIG = {
        'fg_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
        'fg_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        'year_price': 1899,
    }

    os.chdir(DIR)
    plot_cobb_douglas(
        *collect_cobb_douglas().pipe(transform_cobb_douglas, year_base=1899),
        MAP_FIG
    )


if __name__ == '__main__':
    main()
