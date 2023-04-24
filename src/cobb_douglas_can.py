#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 11:29:40 2022

@author: Alexander Mikhailov
"""

from thesis.src.common import get_fig_map
from thesis.src.lib.combine import combine_can
from thesis.src.lib.plot import plot_cobb_douglas, plot_cobb_douglas_3d
from thesis.src.lib.transform import transform_cobb_douglas


def main():
    # =========================================================================
    # Subproject V. Cobb--Douglas for Canada
    # =========================================================================
    # =========================================================================
    # First Figure: Exact Correspondence with 'note_incomplete_th05_2014_07_10.docx'
    # =========================================================================
    YEAR_BASE = 2007

    ARCHIVE_IDS = {
        # =====================================================================
        # Capital
        # =====================================================================
        310004: (YEAR_BASE, "Geometric (infinite) end-year net stock", "industrial"),
        # =====================================================================
        # Labor : "v2523012", Preferred Over "v3437501" Which Is Quarterly
        # =====================================================================
        'v2523012': 2820012,
        # =====================================================================
        # Manufacturing
        # =====================================================================
        'v65201809': 3790031,
    }
    ARCHIVE_IDS = {
        # =====================================================================
        # Capital
        # =====================================================================
        36100096: (
            2012,
            "Manufacturing",
            "Linear end-year net stock",
            (
                "Non-residential buildings",
                "Engineering construction",
                "Machinery and equipment"
            )
        ),
        # =====================================================================
        # Labor : "v2523012", Preferred Over "v3437501" Which Is Quarterly
        # =====================================================================
        'v2523012': 14100027,
        # =====================================================================
        # Manufacturing
        # =====================================================================
        'v65201809': 36100434,
    }
    df = combine_can(ARCHIVE_IDS)
    plot_cobb_douglas(
        *df.pipe(transform_cobb_douglas, year_base=YEAR_BASE), get_fig_map(YEAR_BASE)
    )
    df.pipe(plot_cobb_douglas_3d)


if __name__ == '__main__':
    main()
