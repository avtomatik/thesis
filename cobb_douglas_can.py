#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 11:29:40 2022

@author: Alexander Mikhailov
"""

from collect.lib import construct_can
from plot.lib import plot_cobb_douglas, plot_cobb_douglas_3d
from transform.lib import transform_cobb_douglas


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
        'year_base': 2007,
    }
    ARCHIVE_IDS = {
        # =====================================================================
        # Capital
        # =====================================================================
        310004: (2007, "Geometric (infinite) end-year net stock", "industrial"),
        # =====================================================================
        # Labor : "v2523012", Preferred Over "v3437501" Which Is Quarterly
        # =====================================================================
        2820012: 'v2523012',
        # =====================================================================
        # Production
        # =====================================================================
        3790031: 'v65201809',
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
        14100027: 'v2523012',
        # =====================================================================
        # Production
        # =====================================================================
        36100434: 'v65201809',
    }
    _df = construct_can(ARCHIVE_IDS)
    plot_cobb_douglas(
        *_df.pipe(transform_cobb_douglas, year_base=2007),
        MAP_FIG
    )
    plot_cobb_douglas_3d(_df)


if __name__ == '__main__':
    main()
