def fetch_world_bank(file_name, series_id):
    source_frame = pd.read_csv(file_name)
    source_frame = source_frame[source_frame.columns[[1, 0, 2]]]
    source_frame = source_frame[source_frame.iloc[:, 0] == series_id]
    source_frame = source_frame[source_frame.columns[[1, 2]]]
    if file_name  == 'CHN_TUR_GDP.zip':
        source_frame.rename(columns={'Series Name: GDP (current US$)':'Value'},
                            inplace=True)
    else:
        source_frame.columns = source_frame.columns.str.title()
    source_frame = source_frame.set_index('Period')
    source_frame.reset_index(level=0, inplace=True)
    return source_frame


'''Project:
Correlogram, Pandas;
Bootstrap Plot, Pandas;
Lag Plot, Pandas'''
plot_built_in(autocorrelation_plot)
plot_built_in(bootstrap_plot)
plot_built_in(lag_plot)