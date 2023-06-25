#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 11:29:40 2022

@author: Alexander Mikhailov
"""

from thesis.src.common import get_blueprint, get_fig_map
from thesis.src.lib.combine import combine_can
from thesis.src.lib.plot import plot_cobb_douglas, plot_cobb_douglas_3d
from thesis.src.lib.transform import transform_cobb_douglas


def main(year_base: int = 2012) -> None:
    # =========================================================================
    # Project V. Cobb--Douglas for Canada
    # =========================================================================
    # =========================================================================
    # First Figure: Exact Correspondence with 'note_incomplete_th05_2014_07_10.docx'
    # =========================================================================
    ARCHIVE_IDS = get_blueprint(year_base)

    df = combine_can(ARCHIVE_IDS)
    plot_cobb_douglas(
        *df.pipe(
            transform_cobb_douglas, year_base=year_base
        ),
        get_fig_map(year_base)
    )
    df.pipe(plot_cobb_douglas_3d)


if __name__ == '__main__':
    main()
