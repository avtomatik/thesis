def get_fig_map(year_base: int = 1899) -> dict[str, str]:
    return {
        'fg_a': f'Chart I Progress in Manufacturing {{}}$-${{}} ({year_base}=100)',
        'fg_b': f'Chart II Theoretical and Actual Curves of Production {{}}$-${{}} ({year_base}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        'year_base': year_base,
    }


def get_fig_map_us_ma(year_base: int = 1899) -> dict[str, str]:
    return {
        'fg_a': f'Chart 15 Relative Increase in Capital, Labor, and Physical Product in Manufacturing Industries of Massachussets, {{}}$-${{}} ({year_base}=100)',
        'fg_b': f'Chart 16 Theoretical and Actual Curves of Production, Massachusetts, {{}}$-${{}} ({year_base}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines, Massachusetts\nTrend Lines = 3 Year Moving Average',
        'fg_d': 'Chart 17 The Percentage Deviations of the Computed Product ($P\'$) from the Actual Product ($P$) in Massachusetts Manufacturing, {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        'year_base': year_base,
    }
