from lib.constants import TITLES_DEU
from lib.pull import pull_series_ids_description


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


def get_blueprint_former(year_base: int = 2007) -> dict:
    return {
        # =====================================================================
        # Capital
        # =====================================================================
        310004: (year_base, "Geometric (infinite) end-year net stock", "industrial"),
        # =====================================================================
        # Labor : {'v2523012': 2820012}, Preferred Over {'v3437501': 2820011} Which Is Quarterly
        # =====================================================================
        'v2523012': 2820012,
        # =====================================================================
        # Manufacturing
        # =====================================================================
        'v65201809': 3790031,
    }


def get_blueprint(year_base: int = 2012) -> dict:
    return {
        # =====================================================================
        # Capital
        # =====================================================================
        36100096: (
            year_base,
            "Manufacturing",
            "Linear end-year net stock",
            (
                "Non-residential buildings",
                "Engineering construction",
                "Machinery and equipment"
            )
        ),
        # =====================================================================
        # Labor : {'v2523012': 14100027}, Preferred Over {'v3437501': 2820011} Which Is Quarterly
        # =====================================================================
        'v2523012': 14100027,
        # =====================================================================
        # Manufacturing
        # =====================================================================
        'v65201809': 36100434,
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
