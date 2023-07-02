from core.combine import combine_uscb_metals
from core.plot import plot_uscb_metals


def uscb_metals():
    plot_uscb_metals(*combine_uscb_metals())