from core.plot import plot_uscb_manufacturing
from core.stockpile import stockpile


def main():
    # =============================================================================
    # Census Manufacturing Indexes
    # =============================================================================
    SERIES_IDS = {
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013': Dataset.USCB,
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014': Dataset.USCB,
        # =====================================================================
        # HSUS 1975 Page 667, P17: Edwin Frickey Series, Indexes of Manufacturing Production
        # =====================================================================
        'P0017': Dataset.USCB,
    }
    YEAR_BASE = 1899
    df = stockpile(SERIES_IDS)
    df.div(df.loc[YEAR_BASE, :]).mul(100).pipe(
        plot_uscb_manufacturing, YEAR_BASE
    )


if __name__ == '__main__':
    main()
