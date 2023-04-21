# =============================================================================
# Scipy Univariate Spline
# =============================================================================


import os

from thesis.src.lib.combine import combine_cobb_douglas
from thesis.src.lib.tools import calculate_plot_uspline
from thesis.src.lib.transform import transform_cobb_douglas


def main():
    DIR = '/media/green-machine/KINGSTON'

    os.chdir(DIR)
    combine_cobb_douglas().pipe(
        transform_cobb_douglas, year_base=1899
    )[0].iloc[:, [3, 4]].pipe(calculate_plot_uspline)


if __name__ == '__main__':
    main()
