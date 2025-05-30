# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 18:28:15 2020

@author: Alexander Mikhailov
"""


import os

from core.combine import combine_cobb_douglas
from core.common import get_fig_map
from core.config import DATA_DIR
from core.plot import plot_cobb_douglas
from core.transform import transform_cobb_douglas


def main(
    year_base: int = 1899
) -> None:
    """
    Cobb--Douglas Algorithm as per
    C.W. Cobb, P.H. Douglas. A Theory of Production, 1928 &
    P.H. Douglas. The Theory of Wages, 1934;

    Parameters
    ----------
    path_src : str, optional
        DESCRIPTION. The default is '/media/green-machine/KINGSTON'.
    year_base : int, optional
        DESCRIPTION. The default is 1899.

    Returns
    -------
    None.

    """

    os.chdir(DATA_DIR)
    plot_cobb_douglas(
        *combine_cobb_douglas().pipe(
            transform_cobb_douglas, year_base=year_base
        ),
        get_fig_map(year_base)
    )


if __name__ == '__main__':
    main()
