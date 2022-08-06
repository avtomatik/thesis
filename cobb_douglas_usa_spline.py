# =============================================================================
# Scipy Univariate Spline
# =============================================================================


import os
from collect.lib import collect_cobb_douglas
from collect.lib import transform_cobb_douglas
from toolkit.lib import calculate_plot_uspline


def main():
    DIR = '/media/alexander/321B-6A94'

    os.chdir(DIR)
    calculate_plot_uspline(
        transform_cobb_douglas(collect_cobb_douglas())[0].iloc[:, [3, 4]]
    )


if __name__ == '__main__':
    main()
