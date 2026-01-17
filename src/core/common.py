import io
from typing import Any

import requests

from core.backend import read_get_desc
from core.classes import SeriesGroupingModel
from core.config import DATA_DIR
from core.constants import TITLES_DEU


def get_figure_labels(year_base: int = 1899) -> dict[str, str]:
    return {
        "fg_a": f"Chart I Progress in Manufacturing {{}}$-${{}} ({year_base}=100)",
        "fg_b": f"Chart II Theoretical and Actual Curves of Production {{}}$-${{}} ({year_base}=100)",
        "fg_c": "Chart III Percentage Deviations of $P$ and $P'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average",
        "fg_d": "Chart IV Percentage Deviations of Computed from Actual Product {}$-${}",
        "fg_e": "Chart V Relative Final Productivities of Labor and Capital",
        "year_base": year_base,
    }


def group_series_by_model(
    series_id_list: list[str],
    grouping_model: SeriesGroupingModel,
    kendrick_separator: str = "S",
    douglas_prefix_len: int = 4,
) -> dict[str, list[str]]:
    """
    Group series IDs according to the selected grouping model.

    Args:
        series_id_list: List of series ID strings to group.
        grouping_model: Either SeriesGroupingModel.DOUGLAS_MODEL or KENDRICK_MODEL.
        kendrick_separator: Separator for KENDRICK_MODEL grouping (default: "S").
        douglas_prefix_len: Prefix length for DOUGLAS_MODEL grouping (default: 4).

    Returns:
        Dictionary mapping group keys to lists of series IDs.
    """
    grouped_ids: dict[str, list[str]] = {}

    for series_id in series_id_list:
        group_key = grouping_model.compute_group_key(
            series_id,
            kendrick_separator=kendrick_separator,
            douglas_prefix_len=douglas_prefix_len,
        )
        grouped_ids.setdefault(group_key, []).append(series_id)

    return grouped_ids


def get_labels(archive_name: str, key: str, scenario: str) -> list[list[str]]:
    # =============================================================================
    # TODO: Refactor
    # =============================================================================
    map_series_ids = read_get_desc(archive_name, key)

    series_ids_struct = {}
    for series_id_group, series_ids in group_series_by_model(
        sorted(map_series_ids), scenario
    ).items():
        series_ids_struct[series_id_group] = dict(
            zip(series_ids, [archive_name] * len(series_ids))
        )

    labels = []

    for series_id_group, series_ids in series_ids_struct.items():
        if series_id_group == "DT30":
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
    return {
        "filepath_or_buffer": DATA_DIR / file_name,
        "index_col": 0,
    }


def get_kwargs_usa_davis_ip() -> dict[str, Any]:
    FILE_NAME = "dataset_usa_davis-j-h-ip-total.xls"
    return {
        "io": DATA_DIR / FILE_NAME,
        "header": None,
        "names": ["period", "davis_index"],
        "index_col": 0,
        "skiprows": 5,
    }


def get_kwargs_unstats() -> dict[str, Any]:
    URL = "https://unstats.un.org/unsd/amaapi/api/file/2"
    return {
        "io": io.BytesIO(requests.get(URL).content),
        "index_col": 1,
        "skiprows": 2,
    }
