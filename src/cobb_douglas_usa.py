# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 22:46:08 2021

@author: Alexander Mikhailov
"""


import os

from core.combine import combine_usa_manufacturing_latest
from core.common import get_fig_map
from core.plot import plot_cobb_douglas
from core.transform import transform_cobb_douglas


def main(
    path_src: str = '/media/green-machine/KINGSTON',
    year_base: int = 2012
) -> None:

    os.chdir(path_src)
    plot_cobb_douglas(
        *combine_usa_manufacturing_latest().pipe(
            transform_cobb_douglas, year_base=year_base
        ),
        get_fig_map(year_base)
    )


if __name__ == '__main__':
    main()
