# -*- coding: utf-8 -*-
"""
Created on Sat May  2 22:26:24 2020

@author: Mastermind
"""


import io

import pandas as pd
import requests


def main(url: str = 'https://unstats.un.org/unsd/amaapi/api/file/2') -> None:
    """
    Visualizes the U.S. Contribution to World`s Gross Domestic Product (GDP)

    Parameters
    ----------
    url : str, optional
        DESCRIPTION. The default is 'https://unstats.un.org/unsd/amaapi/api/file/2'.

    Returns
    -------
    None.

    """
    kwargs = {
        'io': io.BytesIO(requests.get(url).content),
        'usecols': 1,
        'skiprows': 2,
    }
    _df = pd.read_excel(**kwargs)
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
