from core.plot import plot_uscb_farm_lands
from core.stockpile import stockpile_usa_hist


def main() -> None:
    SERIES_IDS = {
        # =========================================================================
        # Census 1975, Land in Farms
        # =========================================================================
        'K0005': 'dataset_uscb.zip'
    }
    stockpile_usa_hist(SERIES_IDS).pipe(plot_uscb_farm_lands)


if __name__ == '__main__':
    main()
