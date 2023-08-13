#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 03:31:27 2023

@author: green-machine

Project XI. USA Census J14
"""


import os

from core.plot import plot_filter_rolling_mean, plot_growth_elasticity

from thesis.src.core.backend import stockpile


def main(
    path_src: str = '/media/green-machine/KINGSTON',
    series_id: dict[str, str] = [SeriesID('J0014', Dataset.USCB)]
):

    os.chdir(path_src)
    df = stockpile(series_id)
    df.pipe(plot_growth_elasticity)
    df.pipe(plot_filter_rolling_mean)


if __name__ == '__main__':
    main()
