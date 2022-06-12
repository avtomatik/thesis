# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 18:28:15 2020

@author: Mastermind
"""


import os
from prepare.lib import get_data_cobb_douglas
from prepare.lib import transform_cobb_douglas
from plot.lib import plot_cobb_douglas


def main():
    '''
    Cobb--Douglas Algorithm as per
    C.W. Cobb, P.H. Douglas. A Theory of Production, 1928 &
    P.H. Douglas. The Theory of Wages, 1934;

    Returns
    -------
    None.

    '''
    FOLDER = '/media/alexander/321B-6A94'
    FIG_MAP = {
        'fg_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
        'fg_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        'year_price': 1899,
    }
    os.chdir(FOLDER)
    plot_cobb_douglas(
        *transform_cobb_douglas(get_data_cobb_douglas()),
        FIG_MAP
    )


if __name__ == '__main__':
    main()
