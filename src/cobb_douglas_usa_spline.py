# =============================================================================
# Scipy Univariate Spline
# =============================================================================


import os

from core.combine import combine_cobb_douglas
from core.config import DATA_DIR
from core.tools import calculate_plot_uspline
from core.transform import transform_cobb_douglas


def main(
    year_base: int = 1899
) -> None:

    os.chdir(DATA_DIR)
    combine_cobb_douglas().pipe(
        transform_cobb_douglas, year_base=year_base
    )[0].iloc[:, [3, 4]].pipe(calculate_plot_uspline)


if __name__ == '__main__':
    main()
