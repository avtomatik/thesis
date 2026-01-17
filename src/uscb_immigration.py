from itertools import chain

from core.backend import stockpile
from core.classes import Dataset
from core.combine import enlist_series_ids
from core.plot import plot_uscb_immigration
from core.transform import transform_d

# =============================================================================
# Census Immigration
# =============================================================================


def uscb_immigration():
    SERIES_IDS = map(
        lambda _: f"C{_:04n}",
        chain(
            range(91, 102),
            range(103, 110),
            range(111, 116),
            range(117, 120),
        ),
    )

    SERIES_IDS = enlist_series_ids(SERIES_IDS, Dataset.USCB)

    stockpile(SERIES_IDS).pipe(transform_d, name="C0089").pipe(
        plot_uscb_immigration
    )
