# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 22:19:02 2020
@author: Alexander Mikhailov
"""


import os

from .lib.collect import (collect_usa_capital_purchases,
                          collect_usa_manufacturing_latest,
                          collect_usa_manufacturing_three_fold,
                          collect_usa_manufacturing_two_fold,
                          stockpile_cobb_douglas)
from .lib.plot import (plot_capital_purchases, plot_cobb_douglas,
                       plot_cobb_douglas_alt)
from .lib.tools import calculate_curve_fit_params
from .lib.transform import transform_cobb_douglas, transform_cobb_douglas_alt


def main():
    DIR = '/media/green-machine/KINGSTON'
    MAP_FIG = {
        'fg_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
        'fg_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        'year_base': 1899,
    }

    os.chdir(DIR)
    # =========================================================================
    # Project I. Classified
    # =========================================================================
    df = stockpile_cobb_douglas(5)
    _df_b = df.iloc[:, (0, 1, 3)]
    plot_cobb_douglas_alt(*df.pipe(transform_cobb_douglas_alt), MAP_FIG)
    plot_cobb_douglas_alt(*_df_b.pipe(transform_cobb_douglas_alt), MAP_FIG)

    _df_a = df.iloc[:, range(3)]
    _df_b = df.iloc[:, (0, 1, 3)]
    _df_c = df.iloc[:, (0, 1, 4)]
    _df_d, _df_e = collect_usa_manufacturing_two_fold()
    _df_f, _df_g, _df_h = collect_usa_manufacturing_three_fold()
    _df_i = collect_usa_manufacturing_latest()

# =============================================================================
#     df = collect_cobb_douglas().pipe(transform_cobb_douglas, year_base=1899)[0].iloc[:, (3, 4)]
#     calculate_curve_fit_params(df)
# =============================================================================

    calculate_curve_fit_params(_df_a)
    calculate_curve_fit_params(_df_b)
    calculate_curve_fit_params(_df_c)
    calculate_curve_fit_params(_df_d)
    calculate_curve_fit_params(_df_e)
    calculate_curve_fit_params(_df_f)
    calculate_curve_fit_params(_df_g)
    calculate_curve_fit_params(_df_h)
    calculate_curve_fit_params(_df_i)

    # =========================================================================
    # No Capacity Utilization Adjustment
    # =========================================================================
    calculate_curve_fit_params(_df_d)
    # =========================================================================
    # Capacity Utilization Adjustment
    # =========================================================================
    calculate_curve_fit_params(_df_e)
    # =========================================================================
    # Option: 1929--2013, No Capacity Utilization Adjustment
    # =========================================================================
    calculate_curve_fit_params(_df_f)
    # =========================================================================
    # Option: 1967--2013, No Capacity Utilization Adjustment
    # =========================================================================
    calculate_curve_fit_params(_df_g)
    # =========================================================================
    # Option: 1967--2012, Capacity Utilization Adjustment
    # =========================================================================
    calculate_curve_fit_params(_df_h)
    calculate_curve_fit_params(_df_i)
    # =========================================================================
    # Project II. Scipy Signal Median Filter, Non-Linear Low-Pass Filter
    # =========================================================================
    plot_cobb_douglas(
        *_df_a.pipe(transform_cobb_douglas, year_base=1899), MAP_FIG
    )
    plot_cobb_douglas(
        *_df_b.pipe(transform_cobb_douglas, year_base=1899), MAP_FIG
    )
    plot_cobb_douglas(
        *_df_c.pipe(transform_cobb_douglas, year_base=1899), MAP_FIG
    )
    plot_cobb_douglas(
        *_df_d.pipe(transform_cobb_douglas, year_base=1929), MAP_FIG
    )
    plot_cobb_douglas(
        *_df_e.pipe(transform_cobb_douglas, year_base=1929), MAP_FIG
    )
    plot_cobb_douglas(
        *_df_f.pipe(transform_cobb_douglas, year_base=1929), MAP_FIG
    )
    plot_cobb_douglas(
        *_df_g.pipe(transform_cobb_douglas, year_base=1967), MAP_FIG
    )
    plot_cobb_douglas(
        *_df_h.pipe(transform_cobb_douglas, year_base=1967), MAP_FIG
    )
    plot_cobb_douglas(
        *_df_i.pipe(transform_cobb_douglas, year_base=1967), MAP_FIG
    )
    # =========================================================================
    # Project III. Scipy Signal Wiener Filter
    # =========================================================================
    plot_capital_purchases(collect_usa_capital_purchases())


if __name__ == '__main__':
    main()
