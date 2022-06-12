

from plot.lib import plot_cobb_douglas_3d
from extract.lib import extract_can_capital_query
from plot.lib import plot_cobb_douglas
# =============================================================================
# Canada
# =============================================================================
FIG_MAP = {
    'fg_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
    'fg_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
    'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
    'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
    'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
    'year_price': 2007,
}


print(__doc__)
# result_frame = get_dataset_can()
# # plot_cobb_douglas_canada(result_frame)
# # plot_cobb_douglas_3d(result_frame)
# df = fetch_from_url('https://www150.statcan.gc.ca/n1/en/tbl/csv/36100210-eng.zip')
df = fetch_from_url('https://www150.statcan.gc.ca/n1/tbl/csv/18100081-eng.zip')
