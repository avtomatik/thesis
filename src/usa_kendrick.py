from thesis.src.lib.constants import MEASURES_KENDRICK, TITLES_KENDRICK
from thesis.src.lib.plot import plot_douglas


def usa_kendrick() -> None:
    # =========================================================================
    # Kendrick Macroeconomic Series
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
    GROUP_ITERS = (
        0,
        8,
        19,
        30,
        38,
        46,
        54,
        60,
        72,
        84,
        96,
        100,
        111,
        118,
    )

    plot_douglas(ARCHIVE_NAME, GROUP_ITERS, TITLES_KENDRICK, MEASURES_KENDRICK)
