from core.plot import plot_uscb_farm_lands

from thesis.src.core.backend import stockpile


def main() -> None:
    # =============================================================================
    # Census 1975, Land in Farms
    # =============================================================================
    SERIES_IDS = [SeriesID('K0005', Dataset.USCB)]
    stockpile(SERIES_IDS).pipe(plot_uscb_farm_lands)


if __name__ == '__main__':
    main()
