# =============================================================================
# Scipy Univariate Spline
# =============================================================================


import os

from collect.lib import collect_cobb_douglas
from toolkit.lib import calculate_plot_uspline
from transform.lib import transform_cobb_douglas


def main():
    DIR = '/media/green-machine/KINGSTON'

    os.chdir(DIR)
    calculate_plot_uspline(
        collect_cobb_douglas().pipe(transform_cobb_douglas)[0].iloc[:, [3, 4]]
    )


if __name__ == '__main__':
    main()
