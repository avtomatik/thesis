# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 00:13:17 2020

@author: Alexander Mikhailov
"""


import itertools
import os

from collect.lib import (collect_usa_hist, collect_uscb_cap,
                         collect_uscb_cap_deflator,
                         collect_uscb_employment_conflicts, collect_uscb_gnp,
                         collect_uscb_immigration, collect_uscb_manufacturing,
                         collect_uscb_metals, collect_uscb_money_stock,
                         collect_uscb_trade, collect_uscb_trade_by_countries,
                         collect_uscb_trade_gold_silver,
                         collect_uscb_unemployment_hours_worked)
from plot.lib import (plot_uscb_cap, plot_uscb_cap_deflator,
                      plot_uscb_commodities, plot_uscb_employment_conflicts,
                      plot_uscb_farm_lands, plot_uscb_finance, plot_uscb_gnp,
                      plot_uscb_immigration, plot_uscb_manufacturing,
                      plot_uscb_metals, plot_uscb_money_stock, plot_uscb_trade,
                      plot_uscb_trade_by_countries,
                      plot_uscb_trade_gold_silver,
                      plot_uscb_unemployment_hours_worked)
from transform.lib import transform_mean_wide, transform_sum_wide


def main():
    DIR = '/media/green-machine/KINGSTON'
    ARCHIVE_NAME = 'dataset_uscb.zip'

    os.chdir(DIR)
    plot_uscb_manufacturing(*collect_uscb_manufacturing())
    plot_uscb_cap(collect_uscb_cap())
    plot_uscb_cap_deflator(
        collect_uscb_cap_deflator().pipe(transform_mean_wide, name="census_fused")
    )
    plot_uscb_metals(*collect_uscb_metals())
    # =========================================================================
    # Census Production Series
    # =========================================================================
    SERIES_IDS = {
        f'P{_:04n}': ARCHIVE_NAME
        for _ in itertools.chain(
            range(248, 252),
            (262,),
            range(265, 270),
            range(293, 296),
        )
    }
    SERIES_IDS_ALT = {
        f'P{_:04n}': ARCHIVE_NAME
        for _ in itertools.chain(
            range(231, 242),
            range(244, 245),
            range(247, 272),
            range(277, 278),
            range(279, 280),
            range(281, 285),
            range(286, 287),
            range(288, 289),
            range(290, 291),
            range(293, 301),
        )
    }

    plot_uscb_commodities(SERIES_IDS)
    ARCHIVE_NAME = 'dataset_uscb.zip'
    SERIES_IDS = {
        f'C{_:04n}': ARCHIVE_NAME
        for _ in itertools.chain(
            range(91, 102),
            range(103, 110),
            range(111, 116),
            range(117, 120),
        )
    }
    plot_uscb_immigration(collect_usa_hist(
        SERIES_IDS).pipe(transform_sum_wide, name="C89"))
    plot_uscb_unemployment_hours_worked(
        collect_uscb_unemployment_hours_worked()
    )
    plot_uscb_employment_conflicts(collect_uscb_employment_conflicts())
    plot_uscb_unemployment_hours_worked(df)
    plot_uscb_employment_conflicts(df)
    plot_uscb_gnp(collect_uscb_gnp())
    plot_uscb_farm_lands()
    plot_uscb_trade(collect_uscb_trade())
    plot_uscb_trade_gold_silver(collect_uscb_trade_gold_silver())
    plot_uscb_trade_by_countries(collect_uscb_trade_by_countries())
    plot_uscb_money_stock(collect_uscb_money_stock())
    plot_uscb_finance()


if __name__ == '__main__':
    main()
