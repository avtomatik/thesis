import itertools

from core.plot import plot_uscb_commodities
from thesis.src.core.backend import stockpile_rebased


def main() -> None:
    # =============================================================================
    # Census Manufacturing Series
    # =============================================================================

    SERIES_IDS = map(
        lambda _: f'P{_:04n}',
        itertools.chain(
            range(231, 242),
            range(244, 245),
            range(247, 272),
            range(277, 278),
            range(279, 280),
            range(281, 285),
            range(286, 287),
            range(288, 289),
            range(290, 291),
            range(293, 301),
        )
    )

    SERIES_IDS = enlist_series_ids(SERIES_IDS, Dataset.USCB)

    SERIES_IDS = map(
        lambda _: f'P{_:04n}',
        itertools.chain(
            range(248, 252),
            [262],
            range(265, 270),
            range(293, 296),
        )
    )

    SERIES_IDS = enlist_series_ids(SERIES_IDS, Dataset.USCB)

    stockpile_rebased(SERIES_IDS).pipe(plot_uscb_commodities, SERIES_IDS)


if __name__ == '__main__':
    main()
