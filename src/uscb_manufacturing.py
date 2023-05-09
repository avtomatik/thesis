from thesis.src.lib.plot import plot_uscb_manufacturing
from thesis.src.lib.stockpile import stockpile_usa_hist


def main():
    # =============================================================================
    # Census Manufacturing Indexes
    # =============================================================================
    SERIES_IDS = {
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014': 'dataset_uscb.zip',
        # =====================================================================
        # HSUS 1975 Page 667, P17: Edwin Frickey Series, Indexes of Manufacturing Production
        # =====================================================================
        'P0017': 'dataset_uscb.zip',
    }
    YEAR_BASE = 1899
    df = stockpile_usa_hist(SERIES_IDS)
    df.div(df.loc[YEAR_BASE, :]).mul(100).pipe(
        plot_uscb_manufacturing, YEAR_BASE
    )


if __name__ == '__main__':
    main()
