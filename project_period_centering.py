def fetch_usa_mcconnel(series_id, index=True):
    '''Data Frame Fetching from McConnell C.R. & Brue S.L.'''
    file_name = 'dataset_usa_mc-connell-brue.zip'
    data_frame = pd.read_csv(file_name, usecols=range(1, 4))
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:,[1, 2]]
    data_frame.sort_values(by=data_frame.columns[0], inplace=False)
    data_frame.set_index(data_frame.columns[0], inplace=True, verify_integrity=True)
    if index:
        return data_frame
    else:
        return data_frame.reset_index(level=0)


def period_centering(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Series
    '''
    '''Variables Initialised'''
    result_frame = source_frame # # DataFrame for Results
    period = result_frame.iloc[:, 0]
    series = result_frame.iloc[:, 1]
    '''Loop'''
    for i in range(1, 1 + result_frame.shape[0]//2):
        period = period.rolling(window=2).mean()
        series = series.rolling(window=2).mean()
        period_roll = period.shift(-(i//2))
        series_roll = series.shift(-(i//2))
        series_frac = series_roll.div(result_frame.iloc[:, 1])
        series_diff = (series_roll.shift(-2)-series_roll).div(2*series_roll.shift(-1))
        result_frame = pd.concat([result_frame, period_roll, series_roll, series_frac, series_diff], axis=1, sort=True)
    return result_frame


'''A032RC1'''
source_frame = fetch_usa_mcconnel('Национальный доход, млрд долл. США', False)
result_frame = period_centering(source_frame)
print(result_frame)

source_frame = fetch_bea_usa('dataset_usa_bea_nipadataa.txt', 'A032RC')
source_frame.reset_index(level=0, inplace=True)
result_frame = period_centering(source_frame)
print(result_frame)