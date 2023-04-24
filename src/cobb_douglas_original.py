# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 18:28:15 2020

@author: Alexander Mikhailov
"""


import os

from thesis.src.common import get_fig_map
from thesis.src.lib.combine import combine_cobb_douglas
from thesis.src.lib.plot import plot_cobb_douglas
from thesis.src.lib.transform import transform_cobb_douglas


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
    YEAR_BASE = 1899

    os.chdir(DIR)
    plot_cobb_douglas(
        *combine_cobb_douglas().pipe(transform_cobb_douglas, year_base=YEAR_BASE),
        get_fig_map(YEAR_BASE)
    )


if __name__ == '__main__':
    main()
