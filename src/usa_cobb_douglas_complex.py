# =============================================================================
# Project VIII. Complex
# =============================================================================


from thesis.src.core.combine import combine_cobb_douglas
from thesis.src.core.plot import plot_uscb_complex
from thesis.src.core.transform import transform_cobb_douglas


def usa_cobb_douglas_complex():
    """
    Project VIII. Complex: Cobb--Douglas

    Returns
    -------
    None.

    """
    YEAR_BASE = 1899
    df = combine_cobb_douglas().pipe(
        transform_cobb_douglas, year_base=YEAR_BASE
    )[0].iloc[:, range(5)]

    for column in df.columns:
        df.loc[:, [column]].pipe(plot_uscb_complex)
