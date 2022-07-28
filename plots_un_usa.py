# -*- coding: utf-8 -*-
"""
Created on Sat May  2 22:26:24 2020

@author: Mastermind
"""


import io
import pandas as pd
import requests


def main():
    '''
    Visualize the U.S. Contribution to World`s Gross Domestic Product (GDP)

    Returns
    -------
    None.

    '''
    URL = 'https://unstats.un.org/unsd/amaapi/api/file/2'
    _df = pd.read_excel(
        io.BytesIO(requests.get(URL).content),
        index_col=1,
        skiprows=2
    )
    _df = _df[_df.iloc[:, 1] == 'Gross Domestic Product (GDP)']
    _df = _df.drop(
        _df.columns[:2],
        axis=1,
    ).transpose()
    df = pd.DataFrame()
    df['us_to_world'] = _df.loc[:, 'United States'].div(_df.sum(1))
    df.plot(grid=True)


if __name__ == '__main__':
    main()
