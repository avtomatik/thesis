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
    df = pd.read_excel(io.BytesIO(requests.get(URL).content), skiprows=2)
    df = df[df.iloc[:, 2] == 'Gross Domestic Product (GDP)']
    df.drop(
        [df.columns[0], df.columns[2]],
        axis=1,
        inplace=True
    )
    df = df.set_index(df.columns[0]).transpose()
    data = pd.DataFrame()
    data['us_to_world'] = df.loc[:, 'United States'].div(df.sum(1))
    data.plot(grid=True)


if __name__ == '__main__':
    main()
