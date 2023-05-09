from thesis.src.lib.combine import combine_uscb_metals
from thesis.src.lib.plot import plot_uscb_metals


def uscb_metals():
    plot_uscb_metals(*combine_uscb_metals())