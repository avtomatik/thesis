# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 22:19:02 2020
@author: Mastermind
"""


import os
from prepare.lib import get_data_usa_bea_labor_mfg
from prepare.lib import get_data_usa_frb_cu
from prepare.lib import get_data_version_a
from prepare.lib import get_data_version_b
from prepare.lib import get_data_capital_purchases
from plot.lib import plot_capital_purchases
from plot.lib import plot_cobb_douglas_alt
from prepare.lib import transform_cobb_douglas
from prepare.lib import transform_cobb_douglas_alt
from toolkit.lib import calculate_curve_fit_params
from prepare.lib import get_data_cobb_douglas


print(__doc__)


def main():
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
    # =============================================================================
    # Project I. Classified
    # =============================================================================
    df = get_data_cobb_douglas(5)
    _df_b = df.iloc[:, [0, 1, 3]]
    plot_cobb_douglas_alt(
        *transform_cobb_douglas_alt(df),
        FIG_MAP
    )
    plot_cobb_douglas_alt(
        *transform_cobb_douglas_alt(_df_b),
        FIG_MAP
        )

    _df_a = df.iloc[:, [0, 1, 2]]
    _df_b = df.iloc[:, [0, 1, 3]]
    _df_c = df.iloc[:, [0, 1, 4]]
    _df_d, _df_e = get_data_version_a()
    _df_f, _df_g, _df_h = get_data_version_b()
    _df_i = dataset_version_c()
    calculate_curve_fit_params(_df_a)
    calculate_curve_fit_params(_df_b)
    calculate_curve_fit_params(_df_c)
    calculate_curve_fit_params(_df_d)
    calculate_curve_fit_params(_df_e)
    calculate_curve_fit_params(_df_f)
    calculate_curve_fit_params(_df_g)
    calculate_curve_fit_params(_df_h)
    calculate_curve_fit_params(_df_i)
    calculate_curve_fit_params(_df_a)
    calculate_curve_fit_params(_df_b)
    calculate_curve_fit_params(_df_c)
    # =============================================================================
    # No Capacity Utilization Adjustment
    # =============================================================================
    calculate_curve_fit_params(_df_d)
    # =============================================================================
    # Capacity Utilization Adjustment
    # =============================================================================
    calculate_curve_fit_params(_df_e)
    # =============================================================================
    # Option: 1929--2013, No Capacity Utilization Adjustment
    # =============================================================================
    calculate_curve_fit_params(_df_f)
    # =============================================================================
    # Option: 1967--2013, No Capacity Utilization Adjustment
    # =============================================================================
    calculate_curve_fit_params(_df_g)
    # =============================================================================
    # Option: 1967--2012, Capacity Utilization Adjustment
    # =============================================================================
    calculate_curve_fit_params(_df_h)
    calculate_curve_fit_params(_df_i)
    # =============================================================================
    # Project II. Scipy Signal Median Filter, Non-Linear Low-Pass Filter
    # =============================================================================
    procedure(_df_a)
    procedure(_df_b)
    procedure(_df_c)
    procedure(_df_d)
    procedure(_df_e)
    procedure(_df_f)
    procedure(_df_g)
    procedure(_df_h)
    procedure(_df_i)
    procedure(_df_a)
    procedure(_df_b)
    procedure(_df_c)
    # =============================================================================
    # Project III. Scipy Signal Wiener Filter
    # =============================================================================
    purchases_frame = get_dataset_capital_purchases()
    plot_capital_purchases(purchases_frame)


if __name__ == '__main__':
    main()
