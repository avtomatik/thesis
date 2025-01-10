# =============================================================================
# Census Immigration
# =============================================================================


import itertools

from thesis.src.core.backend import stockpile
from thesis.src.core.plot import plot_uscb_immigration


def uscb_immigration():
    SERIES_IDS = map(
        lambda _: f'C{_:04n}',
        itertools.chain(
            range(91, 102),
            range(103, 110),
            range(111, 116),
            range(117, 120),
        )
    )

    SERIES_IDS = enlist_series_ids(SERIES_IDS, Dataset.USCB)

    stockpile(SERIES_IDS).pipe(
        transform_sum, name="C0089"
    ).pipe(plot_uscb_immigration)
