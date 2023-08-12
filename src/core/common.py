import io
from pathlib import Path
from typing import Any

import requests

from .constants import TITLES_DEU
from .pull import pull_series_ids_description


def get_fig_map(year_base: int = 1899) -> dict[str, str]:
    return {
        'fg_a': f'Chart I Progress in Manufacturing {{}}$-${{}} ({year_base}=100)',
        'fg_b': f'Chart II Theoretical and Actual Curves of Production {{}}$-${{}} ({year_base}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        'year_base': year_base,
    }


def get_fig_map_us_ma(year_base: int = 1899) -> dict[str, str]:
    return {
        'fg_a': f'Chart 15 Relative Increase in Capital, Labor, and Physical Product in Manufacturing Industries of Massachussets, {{}}$-${{}} ({year_base}=100)',
        'fg_b': f'Chart 16 Theoretical and Actual Curves of Production, Massachusetts, {{}}$-${{}} ({year_base}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines, Massachusetts\nTrend Lines = 3 Year Moving Average',
        'fg_d': 'Chart 17 The Percentage Deviations of the Computed Product ($P\'$) from the Actual Product ($P$) in Massachusetts Manufacturing, {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        'year_base': year_base,
    }


def group_series_ids(series_ids: list[str], scenario: str, sep: str = 'S', upper_bound: int = 4) -> dict[str, list[str]]:
    # =============================================================================
    # TODO: Refactor
    # =============================================================================
    series_id_groups = {}

    if scenario == 'K':
        series_id_group_init = ''
        for series_id in series_ids:
            series_id_group_here, *_ = series_id.split(sep)
            if series_id_group_here != series_id_group_init:
                series_id_groups[series_id_group_here] = [series_id]
            else:
                series_id_groups[series_id_group_here].append(series_id)
            series_id_group_init = series_id_group_here

    if scenario == 'D':
        series_id_group = ''
        for series_id in series_ids:
            if series_id[:upper_bound] != series_id_group:
                series_id_groups[series_id[:upper_bound]] = [series_id]
            else:
                series_id_groups[series_id[:upper_bound]].append(series_id)
        series_id_group = series_id[:upper_bound]

    return series_id_groups


def get_labels(archive_name: str, key: str, scenario: str) -> list[list[str]]:
    # =============================================================================
    # TODO: Refactor
    # =============================================================================
    map_series_ids = pull_series_ids_description(archive_name, key)

    series_ids_struct = {}
    for series_id_group, series_ids in group_series_ids(sorted(map_series_ids), scenario).items():
        series_ids_struct[series_id_group] = dict(
            zip(series_ids, [archive_name] * len(series_ids))
        )

    labels = []

    for series_id_group, series_ids in series_ids_struct.items():
        if series_id_group == 'DT30':
            # =================================================================
            # Special Case for Statistisches Jahrbuch für das Deutsche Reich.
            # =================================================================
            labels.append(TITLES_DEU)
        else:
            labels.append(list(map(map_series_ids.get, series_ids.keys())))

    return labels


def get_pre_kwargs(file_name: str) -> dict[str, Any]:
    """
    Returns `kwargs` for `pd.read_csv()` for Usual Cases

    Parameters
    ----------
    file_name : str
        DESCRIPTION.

    Returns
    -------
    dict[str, Any]
        DESCRIPTION.

    """
    PATH_SRC = '/home/green-machine/data_science/data/interim'
    return {
        'filepath_or_buffer': Path(PATH_SRC).joinpath(file_name),
        'index_col': 0,
    }


def get_kwargs_usa_davis_ip() -> dict[str, Any]:
    return {
        'io': 'dataset_usa_davis-j-h-ip-total.xls',
        'header': None,
        'names': ['period', 'davis_index'],
        'index_col': 0,
        'skiprows': 5
    }


def get_kwargs_unstats() -> dict[str, Any]:
    URL = 'https://unstats.un.org/unsd/amaapi/api/file/2'
    return {
        'io': io.BytesIO(requests.get(URL).content),
        'index_col': 1,
        'skiprows': 2,
    }
