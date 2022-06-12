# =============================================================================
# Scipy Univariate Spline
# =============================================================================


import os
from prepare.lib import get_data_cobb_douglas
from toolkit.lib import calculate_plot_uspline


def main():
    FOLDER = '/media/alexander/321B-6A94'
    os.chdir(FOLDER)
    calculate_plot_uspline(get_data_cobb_douglas())


if __name__ == '__main__':
    main()
