import os

from core.common import get_fig_map_us_ma
from core.plot import plot_cobb_douglas
from core.stockpile import stockpile
from core.transform import transform_cobb_douglas


def main(
    path_src: str = '/media/green-machine/KINGSTON',
    year_base: int = 1899
) -> None:
    """
    Cobb--Douglas Algorithm as per
    C.W. Cobb, P.H. Douglas. A Theory of Production, 1928 &
    P.H. Douglas. The Theory of Wages, 1934;

    Parameters
    ----------
    path_src : str, optional
        DESCRIPTION. The default is '/media/green-machine/KINGSTON'.
    year_base : int, optional
        DESCRIPTION. The default is 1899.

    Returns
    -------
    None.

    """
    # =========================================================================
    # Douglas Production Function
    # =========================================================================
    SERIES_IDS = {
        'DT19AS03': Dataset.DOUGLAS,
        'DT19AS02': Dataset.DOUGLAS,
        'DT19AS01': Dataset.DOUGLAS
    }

    os.chdir(path_src)
    plot_cobb_douglas(
        *stockpile(SERIES_IDS).pipe(
            transform_cobb_douglas, year_base=year_base
        ),
        get_fig_map_us_ma(year_base)
    )


if __name__ == '__main__':
    main()
