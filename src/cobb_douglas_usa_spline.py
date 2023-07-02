# =============================================================================
# Scipy Univariate Spline
# =============================================================================


import os

from core.combine import combine_cobb_douglas
from core.tools import calculate_plot_uspline
from core.transform import transform_cobb_douglas


def main(
    path_src: str = '/media/green-machine/KINGSTON',
    year_base: int = 1899
) -> None:

    os.chdir(path_src)
    combine_cobb_douglas().pipe(
        transform_cobb_douglas, year_base=year_base
    )[0].iloc[:, [3, 4]].pipe(calculate_plot_uspline)


if __name__ == '__main__':
    main()
