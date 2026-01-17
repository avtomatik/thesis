from core.backend import stockpile
from core.classes import Dataset
from core.combine import enlist_series_ids
from core.plot import plot_uscb_complex


def uscb_complex():
    """
    Project VIII. Complex: United States Census Bureau

    Returns
    -------
    None.

    """
    SERIES_IDS = [
        "D0004",
        "D0130",
        "F0003",
        "F0004",
        "P0110",
        "U0001",
        "U0008",
        "X0414",
        "X0415",
    ]

    for series_id in SERIES_IDS:
        print(f"Processing {series_id}")
        stockpile(enlist_series_ids([series_id], Dataset.USCB)).pipe(
            plot_uscb_complex
        )
