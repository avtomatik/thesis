# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 22:19:02 2020
@author: Alexander Mikhailov
"""


import os

from thesis.src.common import get_fig_map
from thesis.src.lib.combine import (combine_cobb_douglas,
                                    combine_usa_capital_purchases,
                                    combine_usa_manufacturing_latest,
                                    combine_usa_manufacturing_three_fold,
                                    combine_usa_manufacturing_two_fold)
from thesis.src.lib.plot import (plot_capital_purchases, plot_cobb_douglas,
                                 plot_cobb_douglas_alt)
from thesis.src.lib.tools import calculate_curve_fit_params
from thesis.src.lib.transform import (transform_cobb_douglas,
                                      transform_cobb_douglas_alt)


def main(
    path_src: str = '/media/green-machine/KINGSTON',
    year_base: int = 1899
) -> None:
    MAP_FIG = get_fig_map(year_base)

    os.chdir(path_src)
    # =========================================================================
    # Project I. Classified
    # =========================================================================
    df = combine_cobb_douglas(5)
    df_b = df.iloc[:, (0, 1, 3)]
    plot_cobb_douglas_alt(*df.pipe(transform_cobb_douglas_alt), MAP_FIG)
    plot_cobb_douglas_alt(*df_b.pipe(transform_cobb_douglas_alt), MAP_FIG)

    df_a = df.iloc[:, range(3)]
    df_c = df.iloc[:, (0, 1, 4)]
    df_d, df_e = combine_usa_manufacturing_two_fold()
    df_f, df_g, df_h = combine_usa_manufacturing_three_fold()

    # =========================================================================
    # combine_cobb_douglas().pipe(transform_cobb_douglas, year_base=YEAR_BASE)[0].iloc[:, [3, 4]].pipe(calculate_curve_fit_params)
    # =========================================================================

    df_a.pipe(calculate_curve_fit_params)
    df_b.pipe(calculate_curve_fit_params)
    df_c.pipe(calculate_curve_fit_params)
    # =========================================================================
    # No Capacity Utilization Adjustment
    # =========================================================================
    df_d.pipe(calculate_curve_fit_params)
    # =========================================================================
    # Capacity Utilization Adjustment
    # =========================================================================
    df_e.pipe(calculate_curve_fit_params)
    # =========================================================================
    # Option: 1929--2013, No Capacity Utilization Adjustment
    # =========================================================================
    df_f.pipe(calculate_curve_fit_params)
    # =========================================================================
    # Option: 1967--2013, No Capacity Utilization Adjustment
    # =========================================================================
    df_g.pipe(calculate_curve_fit_params)
    # =========================================================================
    # Option: 1967--2012, Capacity Utilization Adjustment
    # =========================================================================
    df_h.pipe(calculate_curve_fit_params)
    combine_usa_manufacturing_latest().pipe(calculate_curve_fit_params)

    # =========================================================================
    # Project II. Scipy Signal Median Filter, Non-Linear Low-Pass Filter
    # =========================================================================
    plot_cobb_douglas(
        *df_a.pipe(transform_cobb_douglas, year_base=year_base), MAP_FIG
    )
    plot_cobb_douglas(
        *df_b.pipe(transform_cobb_douglas, year_base=year_base), MAP_FIG
    )
    plot_cobb_douglas(
        *df_c.pipe(transform_cobb_douglas, year_base=year_base), MAP_FIG
    )
    plot_cobb_douglas(
        *df_d.pipe(transform_cobb_douglas, year_base=1929), MAP_FIG
    )
    plot_cobb_douglas(
        *df_e.pipe(transform_cobb_douglas, year_base=1929), MAP_FIG
    )
    plot_cobb_douglas(
        *df_f.pipe(transform_cobb_douglas, year_base=1929), MAP_FIG
    )
    plot_cobb_douglas(
        *df_g.pipe(transform_cobb_douglas, year_base=1967), MAP_FIG
    )
    plot_cobb_douglas(
        *df_h.pipe(transform_cobb_douglas, year_base=1967), MAP_FIG
    )
    plot_cobb_douglas(
        *combine_usa_manufacturing_latest().pipe(transform_cobb_douglas,
                                                 year_base=1967), MAP_FIG
    )
    # =========================================================================
    # Project III. Scipy Signal Wiener Filter
    # =========================================================================
    combine_usa_capital_purchases().pipe(plot_capital_purchases)


if __name__ == '__main__':
    main()
