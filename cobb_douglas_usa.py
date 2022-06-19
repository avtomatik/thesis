# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 22:46:08 2021

@author: Mastermind
"""


from extract.lib import extract_usa_bea_from_url
from extract.lib import extract_usa_bea_from_loaded
from prepare.lib import get_data_usa_frb_ip
from prepare.lib import get_data_usa_frb_fa
from prepare.lib import get_data_usa_frb_fa_def
from prepare.lib import get_data_usa_capital
from prepare.lib import get_data_cobb_douglas_extension_capital
from prepare.lib import get_data_cobb_douglas_deflator
from prepare.lib import get_data_cobb_douglas_extension_labor
from prepare.lib import get_data_cobb_douglas_extension_product
from prepare.lib import get_data
from plot.lib import plot_cobb_douglas


def main():
    FIG_MAP = {
        'fg_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
        'fg_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        # =========================================================================
        # TODO: Update
        # =========================================================================
        'year_price': 1899,
    }

    result_frame = get_dataset()
    plot_cobb_douglas(result_frame)


if __name__ == '__main__':
    main()
