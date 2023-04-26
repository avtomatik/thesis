import os

from thesis.src.common import get_fig_map_us_ma
from thesis.src.lib.plot import plot_cobb_douglas
from thesis.src.lib.stockpile import stockpile_usa_hist
from thesis.src.lib.transform import transform_cobb_douglas


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
        'DT19AS03': 'dataset_douglas.zip',
        'DT19AS02': 'dataset_douglas.zip',
        'DT19AS01': 'dataset_douglas.zip'
    }

    os.chdir(path_src)
    plot_cobb_douglas(
        *stockpile_usa_hist(SERIES_IDS).pipe(
            transform_cobb_douglas, year_base=year_base
        ),
        get_fig_map_us_ma(year_base)
    )


if __name__ == '__main__':
    main()
