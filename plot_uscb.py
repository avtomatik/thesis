# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 00:13:17 2020

@author: Alexander Mikhailov
"""


import itertools
import os

from collect.lib import (collect_uscb_cap, collect_uscb_cap_deflator,
                         collect_uscb_employment_conflicts, collect_uscb_gnp,
                         collect_uscb_manufacturing, collect_uscb_metals,
                         collect_uscb_trade_by_countries,
                         collect_uscb_unemployment_hours_worked,
                         stockpile_usa_hist)
from plot.lib import (plot_uscb_cap, plot_uscb_cap_deflator,
                      plot_uscb_commodities, plot_uscb_employment_conflicts,
                      plot_uscb_farm_lands, plot_uscb_finance, plot_uscb_gnp,
                      plot_uscb_immigration, plot_uscb_manufacturing,
                      plot_uscb_metals, plot_uscb_money_stock, plot_uscb_trade,
                      plot_uscb_trade_by_countries,
                      plot_uscb_trade_gold_silver,
                      plot_uscb_unemployment_hours_worked)
from transform.lib import transform_mean, transform_sum


def main():
    DIR = '/media/green-machine/KINGSTON'
    ARCHIVE_NAME = 'dataset_uscb.zip'

    os.chdir(DIR)
    plot_uscb_manufacturing(*collect_uscb_manufacturing())

    plot_uscb_cap(collect_uscb_cap())

    plot_uscb_cap_deflator(
        collect_uscb_cap_deflator().pipe(transform_mean, name="census_fused")
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
    plot_uscb_immigration(stockpile_usa_hist(
        SERIES_IDS).pipe(transform_sum, name="C0089"))

    plot_uscb_unemployment_hours_worked(
        collect_uscb_unemployment_hours_worked()
    )

    plot_uscb_employment_conflicts(collect_uscb_employment_conflicts())

    plot_uscb_unemployment_hours_worked(df)

    plot_uscb_employment_conflicts(df)

    SERIES_IDS = {
        # =========================================================================
        # Census Gross National Product Series
        # =========================================================================
        'F0003': 'dataset_uscb.zip', 'F0004': 'dataset_uscb.zip'
    }
    df = stockpile_usa_hist(SERIES_IDS).truncate(before=1889)
    df.div(df.iloc[0, :]).mul(100).pipe(plot_uscb_gnp)

    SERIES_ID = {
        # =========================================================================
        # Census 1975, Land in Farms
        # =========================================================================
        'K0005': 'dataset_uscb.zip'
    }
    stockpile_usa_hist(SERIES_ID).pipe(plot_uscb_farm_lands)

    SERIES_IDS = {
        # =========================================================================
        # Census Foreign Trade Series
        # =========================================================================
        'U0001': 'dataset_uscb.zip', 'U0008': 'dataset_uscb.zip', 'U0015': 'dataset_uscb.zip'
    }
    stockpile_usa_hist(SERIES_IDS).pipe(plot_uscb_trade)

    SERIES_IDS = {
        # =========================================================================
        # Census Foreign Trade Series
        # =========================================================================
        'U0187': 'dataset_uscb.zip', 'U0188': 'dataset_uscb.zip', 'U0189': 'dataset_uscb.zip'
    }
    stockpile_usa_hist(SERIES_IDS).pipe(plot_uscb_trade_gold_silver)

    plot_uscb_trade_by_countries(collect_uscb_trade_by_countries())

    SERIES_IDS = {
        # =========================================================================
        # Census Money Supply Aggregates
        # =========================================================================
        'X0410': 'dataset_uscb.zip', 'X0414': 'dataset_uscb.zip', 'X0415': 'dataset_uscb.zip'
    }
    YEAR_BASE = 1915
    df = stockpile_usa_hist(SERIES_IDS)
    df.div(df.loc[YEAR_BASE, :]).mul(100).pipe(plot_uscb_money_stock)

    plot_uscb_finance()


if __name__ == '__main__':
    main()
