#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 00:44:36 2022
@author: alexander
"""


import io
import sqlite3
from zipfile import ZipFile
from functools import cache
from pathlib import Path
import pandas as pd
import requests
from pandas import DataFrame


def numerify(df: DataFrame) -> DataFrame:
    '''


    Parameters
    ----------
    df : DataFrame
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    Returns
    -------
    DataFrame
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    assert df.shape[1] == 1
    df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    return df


@cache
def read_can(archive_id: int) -> DataFrame:
    '''


    Parameters
    ----------
    archive_id : int
    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    ...                ...
    df.iloc[:, -1]     Values
    ================== =================================
    '''
    MAP = {
        14100027: {'period': 0, 'series_id': 10, 'value': 12},
        36100096:
            {
                'period': 0,
                'geo': 1,
                'prices': 3,
                'industry': 4,
                'category': 5,
                'component': 6,
                'series_id': 11,
                'value': 13
        },
        36100434: {'period': 0, 'series_id': 10, 'value': 12},
    }
    url = f'https://www150.statcan.gc.ca/n1/tbl/csv/{archive_id}-eng.zip'
    kwargs = {
        'header': 0,
        'names': tuple(MAP.get(archive_id).keys()),
        'index_col': 0,
        'usecols': tuple(MAP.get(archive_id).values()),
        'parse_dates': archive_id == 36100434
    }
    if Path(f'{archive_id}-eng.zip').is_file():
        with ZipFile(f'{archive_id}-eng.zip', 'r').open(f'{archive_id}.csv') as f:
            return pd.read_csv(f, **kwargs)
    else:
        r = requests.get(url)
        with ZipFile(io.BytesIO(r.content)).open(f'{archive_id}.csv') as f:
            return pd.read_csv(f, **kwargs)


def read_can_former(archive_id: int) -> DataFrame:
    '''
    Retrieves DataFrame from CANSIM Zip Archives

    Parameters
    ----------
    archive_id : int
    Returns
    -------
    DataFrame
    '''
    MAP = {
        310004: {
            'period': 0,
            'prices': 2,
            'category': 4,
            'component': 5,
            'series_id': 6,
            'value': 8,
        },
        2820011:
        {
            'period': 0, 'geo': 1, 'classofworker': 2, 'industry': 3,
            'sex': 4, 'series_id': 5, 'value': 7
        },
        2820012: {'period': 0, 'series_id': 5, 'value': 7},
        3790031:
        {
            'period': 0, 'geo': 1, 'seas': 2, 'prices': 3, 'naics': 4,
            'series_id': 5, 'value': 7
        },
        3800084:
        {
            'period': 0, 'geo': 1, 'seas': 2, 'est': 3, 'series_id': 4,
            'value': 6
        },
        3800102: {'period': 0, 'series_id': 4, 'value': 6},
        3800106: {'period': 0, 'series_id': 3, 'value': 5},
        3800518: {'period': 0, 'series_id': 4, 'value': 6},
        3800566: {'period': 0, 'series_id': 3, 'value': 5},
        3800567: {'period': 0, 'series_id': 4, 'value': 6},
    }
    kwargs = {
        'filepath_or_buffer': f'dataset_can_{archive_id:08n}-eng.zip',
        'header': 0,
        'names': tuple(MAP.get(archive_id).keys()),
        'index_col': 0,
        'usecols': tuple(MAP.get(archive_id).values()),
        'parse_dates': archive_id in (2820011, 3790031, 3800084)
    }
    return pd.read_csv(**kwargs)


@cache
def read_from_url_usa_bea(url: str) -> DataFrame:
    '''
    Retrieves U.S. Bureau of Economic Analysis DataFrame from URL

    Parameters
    ----------
    url : str

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series IDs
    df.iloc[:, 1]      Values
    ================== =================================
    '''
    kwargs = {
        'header': 0,
        'names': ('series_ids', 'period', 'value'),
        'index_col': 1,
        'thousands': ','
    }
    if requests.head(url).status_code == 200:
        kwargs['filepath_or_buffer'] = io.BytesIO(requests.get(url).content)
    else:
        kwargs['filepath_or_buffer'] = url.split('/')[-1]
    return pd.read_csv(**kwargs)


@cache
def read_usa_bea(archive_name: str, wb_name: str, sh_name: str) -> DataFrame:
    '''
    Retrieves DataFrame from Bureau of Economic Analysis Zip Archives
    Parameters
    ----------
    archive_name : str
        DESCRIPTION.
    wb_name : str
        DESCRIPTION.
    sh_name : str
        DESCRIPTION.
    series_id : str
        DESCRIPTION.
    Returns
    -------
    TYPE
        DESCRIPTION.
    '''
    with pd.ExcelFile(ZipFile(archive_name, 'r').open(wb_name)) as xl_file:
        # =====================================================================
        # Load
        # =====================================================================
        df = pd.read_excel(xl_file, sh_name, skiprows=7)
        # =====================================================================
        # Re-Load
        # =====================================================================
        kwargs = {
            'io': xl_file,
            'sheet_name': sh_name,
            'index_col': 0,
            'usecols': range(2, df.shape[1]),
            'skiprows': 7
        }
        return pd.read_excel(**kwargs).dropna(axis=0).transpose()


def read_usa_nber(file_name: str, agg: str) -> DataFrame:
    _df = pd.read_csv(file_name)
    _df.drop(_df.columns[0], axis=1, inplace=True)
    if agg == 'mean':
        return _df.groupby(_df.columns[0]).mean()
    return _df.groupby(_df.columns[0]).sum()


def read_worldbank() -> DataFrame:
    URL = 'https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv'
    with ZipFile(io.BytesIO(requests.get(URL).content)) as archive:
        _map = {_.file_size: _.filename for _ in archive.filelist}
        # =====================================================================
        # Select Largest File
        # =====================================================================
        with archive.open(_map[max(_map)]) as f:
            kwargs = {
                'filepath_or_buffer': f,
                'index_col': 0,
                'skiprows': 4
            }
            df = pd.read_csv(**kwargs).dropna(axis=1, how='all').transpose()
            df.drop(df.index[:3], inplace=True)
            return df.rename_axis('period')


def read_pull_usa_bls(file_name: str, series_id: str) -> DataFrame:
    '''
    Bureau of Labor Statistics Data Fetch

    Parameters
    ----------
    file_name : str
        DESCRIPTION.
    series_id : str
        DESCRIPTION.

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    kwargs = {
        'filepath_or_buffer': file_name,
        'sep': '\t',
        'header': 0,
        'names': ('series_id', 'period', 'sub_period', series_id),
        'index_col': 1,
        'usecols': range(4),
        'low_memory': False
    }
    _df = pd.read_csv(**kwargs)
    _q = (_df.iloc[:, 0].str.contains(series_id)) & (_df.iloc[:, 1] == 'M13')
    _df.index = pd.to_numeric(
        _df.index.astype(str).to_series().str.slice(stop=4),
        downcast='integer'
    )
    _df.iloc[:, -1] = pd.to_numeric(_df.iloc[:, -1], errors='coerce')
    return _df[_q].iloc[:, [-1]]


def read_pull_usa_frb_cu() -> DataFrame:
    '''Indexed Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
    CAPUTL.B50001.A Fetching'''
    SERIES_ID = 'CAPUTL.B50001.A'
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_frb_g17_all_annual_2013_06_23.csv',
        'skiprows': 1,
        'index_col': 0,
        'usecols': range(5, 100)
    }
    df = pd.read_csv(**kwargs).transpose()
    df.index = pd.to_numeric(df.index, downcast='integer')
    df.rename_axis('period', inplace=True)
    return df.loc[:, [SERIES_ID]].dropna(axis=0)


def read_pull_usa_frb_ms() -> DataFrame:
    '''
    Money Stock Measures (H.6) Series
    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      M1
    ================== =================================
    '''
    # =========================================================================
    # hex(3**3 * 23 * 197 * 2039 * 445466883143470280668577791313)
    # =========================================================================
    URL = 'https://www.federalreserve.gov/datadownload/Output.aspx?rel=H6&series=5398d8d1734b19f731aba3105eb36d47&lastobs=&from=01/01/1959&to=12/31/2018&filetype=csv&label=include&layout=seriescolumn'
    kwargs = {
        'filepath_or_buffer': io.BytesIO(requests.get(URL).content),
        'header': 0,
        'names': ('period', 'm1_m'),
        'index_col': 0,
        'usecols': range(2),
        'skiprows': 5,
        'parse_dates': True
    }
    _df = pd.read_csv(**kwargs)
    return _df.groupby(_df.index.year).mean()


def read_pull_usa_fred(series_id: str) -> DataFrame:
    '''
    ('PPIACO', 'PRIME',)
    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    URL = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}'
    kwargs = {
        'filepath_or_buffer': io.BytesIO(requests.get(URL).content),
        'header': 0,
        'names': ('period', series_id.lower()),
        'index_col': 0,
        'parse_dates': True
    }
    _df = pd.read_csv(**kwargs)
    return _df.groupby(_df.index.year).mean()


def read_pull_usa_hist(archive_name: str, series_id: str) -> DataFrame:
    '''
    Extract Data from Enumerated Historical Datasets
    Parameters
    ----------
    archive_name : str
        DESCRIPTION.
    series_id : str
        DESCRIPTION.
    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    MAP = {
        'dataset_douglas.zip': {'series_id': 4, 'period': 5, series_id: 6},
        'dataset_usa_brown.zip': {'series_id': 3, 'period': 4, series_id: 5},
        'dataset_usa_census1949.zip': {'series_id': 8, 'period': 9, series_id: 10},
        'dataset_usa_census1975.zip': {'series_id': 8, 'period': 9, series_id: 10},
        'dataset_usa_cobb-douglas.zip': {'series_id': 5, 'period': 6, series_id: 7},
        'dataset_usa_kendrick.zip': {'series_id': 4, 'period': 5, series_id: 6}
    }
    kwargs = {
        'filepath_or_buffer': archive_name,
        'header': 0,
        'names': tuple(MAP.get(archive_name).keys()),
        'index_col': 1,
        'skiprows': (0, 4)[archive_name == 'dataset_usa_brown.zip'],
        'usecols': tuple(MAP.get(archive_name).values()),
        'dtype': str
    }
    df = pd.read_csv(**kwargs)
    df.index = pd.to_numeric(
        df.index.astype(str).to_series().str.slice(stop=4),
        downcast='integer'
    )
    df = numerify(pull_by_series_id(df, series_id))
    if 'census' in archive_name:
        return df.groupby(df.index).mean()
    return df.sort_index()


def read_pull_usa_mcconnel(series_id: str) -> DataFrame:
    '''
    Retrieves DataFrame from McConnell C.R. & Brue S.L.

    Parameters
    ----------
    series_id : str
        DESCRIPTION.

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    MAP = {
        'prime_rate': 'Ставка прайм-рейт, %',
        'A006RC1': 'Валовой объем внутренних частных инвестиций, млрд долл. США',
        'A032RC1': 'Национальный доход, млрд долл. США',
        'A191RC1': 'Валовой внутренний продукт, млрд долл. США',
    }
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_mc_connell_brue.zip',
        'header': 0,
        'names': ('series_id', 'period', series_id),
        'index_col': 1,
        'usecols': range(1, 4)
    }
    df = pd.read_csv(**kwargs)
    return df[df.iloc[:, 0] == MAP[series_id]].iloc[:, [1]].sort_index()


def read_pull_uscb_description(
        series_id: str,
        archive_name: str = 'dataset_usa_census1975.zip'
) -> str:
    '''
    Retrieves Series Description U.S. Bureau of the Census

    Parameters
    ----------
    series_id : str
        DESCRIPTION.
    archive_name : ('dataset_usa_census1949.zip' | 'dataset_usa_census1975.zip'), optional
        DESCRIPTION. The default is 'dataset_usa_census1975.zip': str.

    Returns
    -------
    str
        Series Description.

    '''
    MAP = {
        'source': 0,
        'table': 1,
        'note': 3,
        'group1': 4,
        'group2': 5,
        'group3': 6,
        'series_id': 8
    }
    lookup_columns = ('group1', 'group2', 'group3', 'note')
    FLAG = 'no_details'
    kwargs = {
        'filepath_or_buffer': archive_name,
        'header': 0,
        'names': tuple(MAP.keys()),
        'usecols': tuple(MAP.values()),
        'low_memory': False
    }
    _df = pd.read_csv(**kwargs)
    _df = _df[_df.loc[:, 'series_id'] == series_id].loc[:, lookup_columns]
    _df.drop_duplicates(inplace=True)
    return '\n'.join(v for k, v in dict(_df.iloc[0, :]).items() if v != FLAG)


def pull_by_series_id(df: DataFrame, series_id: str) -> DataFrame:
    '''


    Parameters
    ----------
    df : DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series IDs
    df.iloc[:, 1]      Values
    ================== =================================
    series_id : str
        DESCRIPTION.

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    assert df.shape[1] == 2
    return df[df.iloc[:, 0] == series_id].iloc[:, [1]].rename(
        columns={"value": series_id}
    )


def pull_can_capital(df: DataFrame, params: tuple[int, str]) -> DataFrame:
    '''
    WARNING: VERY EXPENSIVE OPERATION !
    Retrieves Series IDs from Statistics Canada -- Fixed Assets Tables

    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.
    params : tuple[int, str]
        param : BASE_YEAR : Basic Price Year.
        param : CATEGORY : Estimate Basis.
        param : COMPONENT : Search Key Word

    Returns
    -------
    DataFrame
        DESCRIPTION.

    '''
    DIR = "/home/alexander/science"
    DBNAME = "capital"
    stmt = f"""
    SELECT * FROM {DBNAME}
    WHERE
        geo = 'Canada'
        AND prices LIKE '%{params[0]} constant prices%'
        AND industry = '{params[1]}'
        AND category = '{params[2]}'
        AND component IN {params[-1]}
    ;
    """
    with sqlite3.connect(Path(DIR).joinpath(f"{DBNAME}.db")) as conn:
        cursor = conn.cursor()
        df.to_sql(DBNAME, conn, if_exists="replace", index=True)
        cursor = conn.execute(stmt)
        return pd.DataFrame(
            cursor.fetchall(),
            columns=("period", "geo", "prices", "industry", "category",
                     "component", "series_id", "value")
        )


def pull_can_capital_former(df: DataFrame, params: tuple[int, str]) -> DataFrame:
    '''
    Retrieves Series IDs from Statistics Canada -- Fixed Assets Tables

    Parameters
    ----------
    df : DataFrame
    params : tuple[int, str]
        param : BASE_YEAR : Basic Price Year.
        param : CATEGORY : Estimate Basis.
        param : COMPONENT : Search Key Word

    Returns
    -------
    DataFrame
        DESCRIPTION.
    '''
    DIR = "/home/alexander/science"
    DBNAME = "capital"
    stmt = f"""
    SELECT * FROM {DBNAME}
    WHERE
        prices LIKE '%{params[0]} constant prices%'
        AND category = '{params[1]}'
        AND lower(component) LIKE '%{params[-1]}%'
    ;
    """
    with sqlite3.connect(Path(DIR).joinpath(f"{DBNAME}.db")) as conn:
        cursor = conn.cursor()
        df.to_sql(DBNAME, conn, if_exists="replace", index=True)
        cursor = conn.execute(stmt)
        return pd.DataFrame(
            cursor.fetchall(),
            columns=("period", "prices", "category", "component",
                     "series_id", "value")
        )


def pull_can_quarter(df: DataFrame, series_id: str) -> DataFrame:
    '''
    DataFrame Fetching from Quarterly Data within CANSIM Zip Archives
    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.
    series_id : str
        DESCRIPTION.
    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    df = pull_by_series_id(df, series_id)
    return df.groupby(df.index.year).sum()


def pull_can_quarter_former(df: DataFrame, series_id: str) -> DataFrame:
    '''
    Retrieves DataFrame from Quarterly Data within CANSIM Zip Archives
    '''
    flag = 'seas' in df.columns
    df = numerify(pull_by_series_id(
        df.loc[:, ('series_id', 'value')], series_id))
    if flag:
        return df.groupby(df.index.year).sum()
    return df.groupby(df.index.year).mean()


def pull_series_ids(archive_name: str) -> dict[str]:
    '''Returns Dictionary for Series from Douglas's & Kendrick's Databases'''
    return pd.read_csv(archive_name, usecols=(3, 4), index_col=1).to_dict().get('series')
