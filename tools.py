#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 20:54:06 2022

@author: alexander
"""


def append_series_ids(source_frame, data_frame, series_ids):
    for series_id in series_ids:
        chunk = source_frame.loc[:, [series_id]]
        chunk.dropna(axis=0, inplace=True)
        data_frame = pd.concat([data_frame, chunk], axis=1, sort=False)
    return data_frame


def append_series_ids_sum(source_frame, data_frame, series_ids):
    chunk = pd.DataFrame()
    for series_id in series_ids:
        _ = source_frame.loc[:, [series_id]]
        _.dropna(axis=0, inplace=True)
        chunk = pd.concat([chunk, _], axis=1, sort=False)
    series_ids.extend(['sum'])
    chunk['_'.join(series_ids)] = chunk.sum(1)
    data_frame = pd.concat(
        [data_frame, chunk.iloc[:, [-1]]], axis=1, sort=False)
    return data_frame


def calculate_power_function_fit_params_a(df: pd.DataFrame, params: tuple[float]):
    '''
    df.index: Regressor: = Period,
    df.iloc[:, 0]: Regressand,
    params: Parameters
    '''
    df.reset_index(level=0, inplace=True)
    _t_0 = df.iloc[:, 0].min() - 1
    # =========================================================================
    # {RESULT}(Yhat) = params[0] + params[1]*(T-T_0)**params[2]
    # =========================================================================
    df[f'estimate_{df.columns[-1]}'] = df.iloc[:, 0].sub(_t_0).pow(
        params[2]).mul(params[1]).add(params[0])
    print(f'Model Parameter: T_0 = {_t_0};')
    print(f'Model Parameter: Y_0 = {params[0]};')
    print(f'Model Parameter: A = {params[1]:.4f};')
    print(f'Model Parameter: Alpha = {params[2]:.4f};')
    print(f'Estimator Result: Mean Value: {df.iloc[:, 2].mean():,.4f};')
    print('Estimator Result: Mean Squared Deviation, MSD: {:,.4f};'.format(
        mean_squared_error(df.iloc[:, 1], df.iloc[:, 2])))
    print('Estimator Result: Root-Mean-Square Deviation, RMSD: {:,.4f}.'.format(
        np.sqrt(mean_squared_error(df.iloc[:, 1], df.iloc[:, 2]))))


def calculate_power_function_fit_params_b(df: pd.DataFrame, params: tuple[float]):
    '''
    df.index: Period,
    df.iloc[:, 0]: Regressor,
    df.iloc[:, 1]: Regressand,
    params: Model Parameters
    '''
    _param = (params[3]-params[2])/(params[1]-params[0])**params[4]
    # =========================================================================
    # '{RESULT}(Yhat) = U_1 + ((U_2-U_1)/(TAU_2-TAU_1)**Alpha)*({X}-TAU_1)**Alpha'
    # =========================================================================
    df[f'estimate_{df.columns[-1]}'] = df.iloc[:, 0].sub(params[0]).pow(
        params[4]).mul(_param).add(params[2])
    print(f'Model Parameter: TAU_1 = {params[0]};')
    print(f'Model Parameter: TAU_2 = {params[1]};')
    print(f'Model Parameter: U_1 = {params[2]};')
    print(f'Model Parameter: U_2 = {params[3]};')
    print(f'Model Parameter: Alpha = {params[4]:.4f};')
    print(f'Model Parameter: A: = (U_2-U_1)/(TAU_2-TAU_1)**Alpha = {_param:,.4f};')
    print(f'Estimator Result: Mean Value: {df.iloc[:, 1].mean():,.4f};')
    print('Estimator Result: Mean Squared Deviation, MSD: {:,.4f};'.format(
        mean_squared_error(df.iloc[:, 1], df.iloc[:, 2])))
    print('Estimator Result: Root-Mean-Square Deviation, RMSD: {:,.4f}.'.format(
        np.sqrt(mean_squared_error(df.iloc[:, 1], df.iloc[:, 2]))))


def calculate_power_function_fit_params_c(df: pd.DataFrame, params: tuple[float]):
    '''
    df.index: Period,
    df.iloc[:, 0]: Regressor,
    df.iloc[:, 1]: Regressand,
    params: Model Parameters
    '''
    _alpha = (np.log(params[3])-np.log(params[2])) / \
        (np.log(params[0])-np.log(params[1]))
    # =========================================================================
    # '{RESULT}{Hat}{Y} = Y_1*(X_1/{X})**Alpha'
    # =========================================================================
    df[f'estimate_{df.columns[-1]}'] = df.iloc[:, 0].rdiv(params[0]).pow(_alpha).mul(params[2])
    print(f'Model Parameter: X_1 = {params[0]:.4f};')
    print(f'Model Parameter: X_2 = {params[1]};')
    print(f'Model Parameter: Y_1 = {params[2]:.4f};')
    print(f'Model Parameter: Y_2 = {params[3]};')
    print(f'Model Parameter: Alpha: = LN(Y_2/Y_1)/LN(X_1/X_2) = {_alpha:.4f};')
    print(f'Estimator Result: Mean Value: {df.iloc[:, 1].mean():,.4f};')
    print('Estimator Result: Mean Squared Deviation, MSD: {:,.4f};'.format(
        mean_squared_error(df.iloc[:, 1], df.iloc[:, 2])))
    print('Estimator Result: Root-Mean-Square Deviation, RMSD: {:,.4f}.'.format(
        np.sqrt(mean_squared_error(df.iloc[:, 1], df.iloc[:, 2]))))


def calculate_capital(df: pd.DataFrame, p_i: tuple[float], p_t: tuple[float], ratio: float):
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Investment
    df.iloc[:, 1]      Production
    df.iloc[:, 2]      Capital
    df.iloc[:, 3]      Capital Retirement
    ================== =================================
    p_i[0]: S - Gross Fixed Investment to Gross Domestic Product Ratio - Slope over Period,
    p_i[1]: S - Gross Fixed Investment to Gross Domestic Product Ratio - Absolute Term over Period,
    p_t[0]: Λ - Fixed Assets Turnover Ratio - Slope over Period,
    p_t[1]: Λ - Fixed Assets Turnover Ratio - Absolute Term over Period,
    ratio: Investment to Capital Conversion Ratio
    '''
    return df.index.to_series().shift(1).mul(p_i[0]).add(p_i[1]).mul(df.index.to_series().shift(1).mul(p_t[0]).add(p_t[1])).mul(ratio).add(1).sub(df.iloc[:, 3].shift(1)).mul(df.iloc[:, 2].shift(1))


def calculate_capital_acquisition(df: pd.DataFrame) -> None:
    '''
    Interactive Shell for Processing Capital Acquisitions

    Parameters
    ----------
    df : pd.DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Nominal Investment
    df.iloc[:, 1]      Nominal Production
    df.iloc[:, 2]      Real Production
    df.iloc[:, 3]      Maximum Real Production
    df.iloc[:, 4]      Nominal Capital
    df.iloc[:, 5]      Labor
    ================== =================================

    Returns
    -------
    None
        Draws matplotlib.pyplot Plots.

    '''
    _df = df.copy()
    _df.reset_index(level=0, inplace=True)
    _df.columns = ['period', *_df.columns[1:]]
    # =========================================================================
    # TODO: Separate Basic Year Function
    # =========================================================================
    _df['__deflator'] = _df.iloc[:, 2].div(_df.iloc[:, 3]).sub(1).abs()
    _b = _df.iloc[:, -1].astype(float).argmin()
    _df.drop(_df.columns[-1], axis=1, inplace=True)
    _title = (_df.index[_b], _df.index[0], _df.index[-1])
    # =========================================================================
    # Calculate Static Values
    # =========================================================================
    # =========================================================================
    # Fixed Assets Turnover Ratio
    # =========================================================================
    _df['c_turnover'] = _df.iloc[:, 3].div(_df.iloc[:, 5])
    # =========================================================================
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I_0/Y_0)
    # =========================================================================
    _df['inv_to_gdp'] = _df.iloc[:, 1].div(_df.iloc[:, 3])
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    _df['lab_cap_int'] = _df.iloc[:, 5].div(_df.iloc[:, 6])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    _df['lab_product'] = _df.iloc[:, 3].div(_df.iloc[:, 6])
    _df.iloc[:, -3:] = _df.iloc[:, -3:].div(_df.iloc[0, -3:])
    # =========================================================================
    # Log Labor Capital Intensity, LN((K/L)/(K_0/L_0))
    # =========================================================================
    _df[f'{_df.columns[-2]}_log_bas'] = np.log(_df.iloc[:, -2].astype(float))
    # =========================================================================
    # Log Labor Productivity, LN((Y/L)/(Y_0/L_0))
    # =========================================================================
    _df[f'{_df.columns[-2]}_log_bas'] = np.log(_df.iloc[:, -2].astype(float))
    # =========================================================================
    # Max: Fixed Assets Turnover Ratio
    # =========================================================================
    _df[f'{_df.columns[-6]}_max'] = _df.iloc[:, 4].div(_df.iloc[:, 5])
    # =========================================================================
    # Max: Investment to Gross Domestic Product Ratio
    # =========================================================================
    _df[f'{_df.columns[-6]}_max'] = _df.iloc[:, 1].div(_df.iloc[:, 4])
    # =========================================================================
    # Max: Labor Productivity
    # =========================================================================
    _df[f'{_df.columns[-5]}_max'] = _df.iloc[:, 4].div(_df.iloc[:, 6])
    _df.iloc[:, -2:] = _df.iloc[:, -2:].div(_df.iloc[0, -2:])
    # =========================================================================
    # Max: Log Labor Productivity
    # =========================================================================
    _df[f'{_df.columns[-1]}_log_bas'] = np.log(_df.iloc[:, -1].astype(float))
    # =========================================================================
    # Calculate Dynamic Values
    # =========================================================================
    # =========================================================================
    # Number of Periods
    # =========================================================================
    N = int(input('Define Number of Line Spans for Pi (N, N >= 1): '))
    print(f'Number of Spans Provided: {N}')
    assert N >= 1, f'N >= 1 is Required, N = {N} Was Provided'
    # =========================================================================
    # Pi & Pi Switch Points
    # =========================================================================
    pi, _knots = [], [0, ]
    _ = 0
    if N == 1:
        _knots.append(_df.index[-1])
        pi.append(float(input('Define Pi for Period from {} to {}: '.format(
            _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _] - 1, 0]))))
    elif N >= 2:
        while _ < N:
            if 1 + _ == N:
                _knots.append(_df.index[-1])
                pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                    _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _] - 1, 0]))))
            else:
                _knot = int(input('Select Row for Year, Should Be More Than {}: = {}: '.format(
                    0, _df.iloc[0, 0])))
                if _knot > _knots[_]:
                    _knots.append(_knot)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                        _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _], 0]))))
            _ += 1
    else:
        print('Error')
    # =========================================================================
    # Calculate Dynamic Values
    # =========================================================================
    _calculated = [np.nan, ]
    if N == 1:
        j = 0
        for i in range(_knots[j], _knots[1 + j]):
            # =================================================================
            # Estimate: GCF[-] or CA[+]
            # =================================================================
            _calculated.append(
                _df.iloc[1 + i, 5] - _df.iloc[i, 5] + pi[j]*_df.iloc[1 + i, 1]
            )
    else:
        for j in range(N):
            if 1 + j == N:
                for i in range(_knots[j], _knots[1 + j]):
                    # =========================================================
                    # Estimate: GCF[-] or CA[+]
                    # =========================================================
                    _calculated.append(
                        _df.iloc[1 + i, 5] - _df.iloc[i, 5] +
                        pi[j]*_df.iloc[1 + i, 1]
                    )
            else:
                for i in range(_knots[j], _knots[1 + j]):
                    # =========================================================
                    # Estimate: GCF[-] or CA[+]
                    # =========================================================
                    _calculated.append(
                        _df.iloc[1 + i, 5] - _df.iloc[i, 5] +
                        pi[j]*_df.iloc[1 + i, 1]
                    )
    _df = pd.concat(
        [
            _df,
            pd.DataFrame(_calculated, columns=['_calculated'])
        ],
        axis=1)
    _df.set_index(_df.columns[0], inplace=True)
    # =========================================================================
    # `-` Gross Capital Formation
    # `+` Capital Acquisitions
    # =========================================================================
    for _ in range(N):
        if 1 + _ == N:
            print(
                f'Model Parameter: Pi for Period from {_df.index[_knots[_]]} to {_df.index[_knots[1 + _] - 1]}: {pi[_]:.6f}'
            )
            continue
        print(
            f'Model Parameter: Pi for Period from {_df.index[_knots[_]]} to {_df.index[_knots[1 + _]]}: {pi[_]:.6f}'
        )
    plt.figure(1)
    plt.plot(_df.iloc[:, 8], _df.iloc[:, 9])
    plt.plot(_df.iloc[:, 8], _df.iloc[:, 14])
    plt.title(
        'Labor Productivity, Observed & Max, {}=100, {}$-${}'.format(
            *_title
        )
    )
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel(f'Labor Productivity, {_df.index[_b]}=100')
    plt.grid(True)
    plt.figure(2)
    plt.plot(_df.iloc[:, 10], _df.iloc[:, 11])
    plt.plot(_df.iloc[:, 10], _df.iloc[:, 15])
    plt.title(
        'Log Labor Productivity, Observed & Max, {}=100, {}$-${}'.format(
            *_title
        )
    )
    plt.xlabel('Log Labor Capital Intensity')
    plt.ylabel(f'Log Labor Productivity, {_df.index[_b]}=100')
    plt.grid(True)
    plt.figure(3)
    plt.plot(_df.iloc[:, 6])
    plt.plot(_df.iloc[:, 12])
    plt.title(
        'Fixed Assets Turnover ($\\lambda$), Observed & Max, {}=100, {}$-${}'.format(
            *_title
        )
    )
    plt.xlabel('Period')
    plt.ylabel(f'Fixed Assets Turnover ($\\lambda$), {_df.index[_b]}=100')
    plt.grid(True)
    plt.figure(4)
    plt.plot(_df.iloc[:, 7])
    plt.plot(_df.iloc[:, 13])
    plt.title(
        'Investment to Gross Domestic Product Ratio, \nObserved & Max, {}=100, {}$-${}'.format(
            *_title
        )
    )
    plt.xlabel('Period')
    plt.ylabel(
        f'Investment to Gross Domestic Product Ratio, {_df.index[_b]}=100')
    plt.grid(True)
    plt.figure(5)
    plt.plot(_df.iloc[:, 16])
    plt.title(
        'Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), {}=100, {}$-${}'.format(
            *_title
        )
    )
    plt.xlabel('Period')
    plt.ylabel(f'GCF or CA, {_df.index[_b]}=100')
    plt.grid(True)
    plt.show()


def calculate_capital_retirement(df: pd.DataFrame) -> None:
    '''
    Interactive Shell for Processing Capital Retirement

    Parameters
    ----------
    df : pd.DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Nominal Investment
    df.iloc[:, 1]      Nominal Production
    df.iloc[:, 2]      Real Production
    df.iloc[:, 3]      Nominal Capital
    df.iloc[:, 4]      Labor
    ================== =================================

    Returns
    -------
    None
        Draws matplotlib.pyplot Plots.

    '''
    _df = df.copy()
    _df.reset_index(level=0, inplace=True)
    _df.columns = ['period', *_df.columns[1:]]
    # =========================================================================
    # Define Basic Year for Deflator
    # =========================================================================
    # =========================================================================
    # TODO: Separate Basic Year Function
    # =========================================================================
    _df['__deflator'] = _df.iloc[:, 2].div(_df.iloc[:, 3]).sub(1).abs()
    _b = _df.iloc[:, -1].astype(float).argmin()
    _df.drop(_df.columns[-1], axis=1, inplace=True)
    _title = (_df.index[_b], _df.index[0], _df.index[-1])
    # =========================================================================
    # Calculate Static Values
    # =========================================================================
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    _df['lab_cap_int_log_bas'] = _df.iloc[:, 4].div(_df.iloc[:, 5])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    _df['lab_product_log_bas'] = _df.iloc[:, 3].div(_df.iloc[:, 5])
    # =========================================================================
    # Investment to Gross Domestic Product Ratio
    # =========================================================================
    _df['inv_to_gdp'] = _df.iloc[:, 1].div(_df.iloc[:, 3])
    # =========================================================================
    # Basing
    # =========================================================================
    _df.iloc[:, -3:] = _df.iloc[:, -3:].div(_df.iloc[0, -3:])
    # =========================================================================
    # Log Labor Capital Intensity, LN((K/L)/(K_0/L_0))
    # =========================================================================
    _df.iloc[:, -3] = np.log(_df.iloc[:, -3].astype(float))
    # =========================================================================
    # Log Labor Productivity, LN((Y/L)/(Y_0/L_0))
    # =========================================================================
    _df.iloc[:, -2] = np.log(_df.iloc[:, -2].astype(float))
    # =========================================================================
    # Fixed Assets Turnover Ratio
    # =========================================================================
    _df['c_turnover'] = _df.iloc[:, 3].div(_df.iloc[:, 4])
    # =========================================================================
    # Number of Periods
    # =========================================================================
    N = int(input('Define Number of Line Segments for Pi: '))
    print(f'Number of Periods Provided: {N}')
    assert N >= 1, f'N >= 1 is Required, N = {N} Was Provided'
    # =========================================================================
    # Pi & Pi Switch Points
    # =========================================================================
    pi, _knots = [], [0, ]
    _ = 0
    if N == 1:
        _knots.append(_df.index[-1])
        pi.append(float(input('Define Pi for Period from {} to {}: '.format(
            _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _], 0]))))
    elif N >= 2:
        while _ < N:
            if 1 + _ == N:
                _knots.append(_df.index[-1])
                pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                    _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _], 0]))))
            else:
                _knot = int(input('Select Row for Year: '))
                if _knot > _knots[_]:
                    _knots.append(_knot)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                        _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _], 0]))))
            _ += 1
    else:
        print('Error')
    # =========================================================================
    # Calculate Dynamic Values
    # =========================================================================
    # =========================================================================
    # Fixed Assets Retirement Value
    # =========================================================================
    _value = [np.nan, ]
    # =========================================================================
    # Fixed Assets Retirement Ratio
    # =========================================================================
    _ratio = [np.nan, ]
    if N == 1:
        j = 0
        for i in range(_knots[j], _knots[1 + j]):
            # =================================================================
            # Fixed Assets Retirement Value
            # =================================================================
            _value.append(
                _df.iloc[i, 4] - _df.iloc[1 + i, 4] + pi[j]*_df.iloc[i, 1]
            )
            # =================================================================
            # Fixed Assets Retirement Ratio
            # =================================================================
            _ratio.append(
                (_df.iloc[i, 4] - _df.iloc[1 + i, 4] + pi[j]
                 * _df.iloc[i, 1]) / _df.iloc[1 + i, 4]
            )
    else:
        for j in range(N):
            if 1 + j == N:
                for i in range(_knots[j], _knots[1 + j]):
                    # =========================================================
                    # Fixed Assets Retirement Value
                    # =========================================================
                    _value.append(
                        _df.iloc[i, 4] - _df.iloc[1 + i, 4] +
                        pi[j]*_df.iloc[i, 1]
                    )
                    # =========================================================
                    # Fixed Assets Retirement Ratio
                    # =========================================================
                    _ratio.append(
                        (_df.iloc[i, 4] - _df.iloc[1 + i, 4] +
                         pi[j]*_df.iloc[i, 1]) / _df.iloc[1 + i, 4]
                    )
            else:
                for i in range(_knots[j], _knots[1 + j]):
                    # =========================================================
                    # Fixed Assets Retirement Value
                    # =========================================================
                    _value.append(
                        _df.iloc[i, 4] - _df.iloc[1 + i, 4] +
                        pi[j]*_df.iloc[i, 1]
                    )
                    # =========================================================
                    # Fixed Assets Retirement Ratio
                    # =========================================================
                    _ratio.append(
                        (_df.iloc[i, 4] - _df.iloc[1 + i, 4] +
                         pi[j]*_df.iloc[i, 1]) / _df.iloc[1 + i, 4]
                    )
    _df = pd.concat(
        [
            _df,
            pd.DataFrame(_value, columns=['_value']),
            pd.DataFrame(_ratio, columns=['_ratio'])
        ],
        axis=1)
    _df.set_index(_df.columns[0], inplace=True)
    _df['_ratio_deviation_abs'] = _df.iloc[:, 10].sub(
        _df.iloc[:, 10].mean()).abs()
    _df['_ratio_increment_abs'] = _df.iloc[:, 10].sub(
        _df.iloc[:, 10].shift(1)).abs()
    for _ in range(N):
        if 1 + _ == N:
            print(
                f'Model Parameter: Pi for Period from {_df.index[_knots[_]]} to {_df.index[_knots[1 + _] - 1]}: {pi[_]:.6f}'
            )
            continue
        print(
            f'Model Parameter: Pi for Period from {_df.index[_knots[_]]} to {_df.index[_knots[1 + _]]}: {pi[_]:.6f}'
        )
    plt.figure(1)
    plt.title('Product, {}=100, {}$-${}'.format(*_title))
    plt.xlabel('Period')
    plt.ylabel(f'Product, {_df.index[_b]}=100')
    plt.plot(_df.iloc[:, 2])
    plt.grid(True)
    plt.figure(2)
    plt.title('Capital, {}=100, {}$-${}'.format(*_title))
    plt.xlabel('Period')
    plt.ylabel(f'Capital, {_df.index[_b]}=100')
    plt.plot(_df.iloc[:, 3])
    plt.grid(True)
    plt.figure(3)
    plt.title(
        'Fixed Assets Turnover ($\\lambda$), {}=100, {}$-${}'.format(*_title)
    )
    plt.xlabel('Period')
    plt.ylabel(f'Fixed Assets Turnover ($\\lambda$), {_df.index[_b]}=100')
    plt.plot(_df.iloc[:, 2].div(_df.iloc[:, 3]))
    plt.grid(True)
    plt.figure(4)
    plt.title(
        'Investment to Gross Domestic Product Ratio, {}=100, {}$-${}'.format(
            *_title)
    )
    plt.xlabel('Period')
    plt.ylabel(
        f'Investment to Gross Domestic Product Ratio, {_df.index[_b]}=100'
    )
    plt.plot(_df.iloc[:, 7])
    plt.grid(True)
    plt.figure(5)
    plt.title(
        '$\\alpha(t)$, Fixed Assets Retirement Ratio, {}=100, {}$-${}'.format(*_title)
    )
    plt.xlabel('Period')
    plt.ylabel(f'$\\alpha(t)$, {_df.index[_b]}=100')
    plt.plot(_df.iloc[:, 9])
    plt.grid(True)
    plt.figure(6)
    plt.title(
        'Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, {}=100, {}$-${}'.format(
            *_title)
    )
    plt.xlabel(f'$\\alpha(t)$, {_df.index[_b]}=100')
    plt.ylabel(f'Fixed Assets Retirement Value, {_df.index[_b]}=100')
    plt.plot(_df.iloc[:, 9], _df.iloc[:, 8])
    plt.grid(True)
    plt.figure(7)
    plt.title('Labor Capital Intensity, {}=100, {}$-${}'.format(*_title))
    plt.xlabel(f'Labor Capital Intensity, {_df.index[_b]}=100')
    plt.ylabel(f'Labor Productivity, {_df.index[_b]}=100')
    plt.plot(np.exp(_df.iloc[:, 5]), np.exp(_df.iloc[:, 6]))
    plt.grid(True)
    plt.show()


def convert_url(string):
    return '/'.join(('https://www150.statcan.gc.ca/n1/tbl/csv', '{}-eng.zip'.format(string.split('=')[1][:-2])))


def string_to_url(string):
    return f'https://www150.statcan.gc.ca/n1/tbl/csv/{string}'


def data_select(data, query):
    for column, value in query['filter'].items():
        data = data[data.iloc[:, column] == value]
    return data


def _m_spline_error_metrics(df: pd.DataFrame) -> None:
    '''Error Metrics Function'''
    print('Criterion, C: {:.6f}'.format(
        df.iloc[:, 2].div(df.iloc[:, 1]).sub(1).abs().mean()))


def fetch_can_annually(file_id, series_id):
    # =========================================================================
    # Data Frame Fetching from CANSIM Zip Archives
    # =========================================================================
    USECOLS = {
        2820012: (5, 7,),
        3800102: (4, 6,),
        3800106: (3, 5,),
        3800518: (4, 6,),
        3800566: (3, 5,),
        3800567: (4, 6,),
    }
    data_frame = pd.read_csv(
        f'dataset_can_{file_id:08n}-eng.zip', usecols=[0, *USECOLS[file_id]]
    )
    data_frame = data_frame[data_frame.iloc[:, 1] == series_id].iloc[:, [0, 2]]
    data_frame.columns = [data_frame.columns[0].upper(), series_id]
    data_frame.set_index(data_frame.columns[0], inplace=True)
    data_frame.iloc[:, 0] = pd.to_numeric(data_frame.iloc[:, 0])
    return data_frame


def fetch_can_capital_query() -> list[str]:
    # =========================================================================
    # Fetch <SERIES_IDS> from Statistics Canada. Table: 36-10-0238-01 (formerly
    # CANSIM 031-0004): Flows and stocks of fixed non-residential capital, total
    # all industries, by asset, provinces and territories, annual
    # (dollars x 1,000,000)
    # =========================================================================
    URL = 'https://www150.statcan.gc.ca/n1/en/tbl/csv/36100096-eng.zip'
    df = fetch_can_from_url(URL, usecols=[3, 4, 5, 11])
    query = (df.iloc[:, 0].str.contains('2012 constant prices')) & \
            (df.iloc[:, 1].str.contains('manufacturing', flags=re.IGNORECASE)) & \
            (df.iloc[:, 2] == 'Linear end-year net stock')
    df = df[query]
    return sorted(set(df.iloc[:, -1]))


def fetch_can_capital_query_archived() -> list[str]:
    # =========================================================================
    # TODO: Consider Using sqlite3
    # =========================================================================
    # =========================================================================
    # https://blog.panoply.io/how-to-read-a-sql-query-into-a-pandas-dataframe
    # =========================================================================
    # =========================================================================
    # Fetch <series_ids> from CANSIM Table 031-0004: Flows and stocks of fixed
    # non-residential capital, total all industries, by asset, provinces and
    # territories, annual (dollars x 1,000,000)
    # =========================================================================
    ARCHIVE_NAME = 'dataset_can_00310004-eng.zip'
    df = pd.read_csv(ARCHIVE_NAME, usecols=[2, 4, 5, 6])
    query = (df.iloc[:, 0].str.contains('2007 constant prices')) & \
            (df.iloc[:, 1] == 'Geometric (infinite) end-year net stock') & \
            (df.iloc[:, 2].str.contains('industrial', flags=re.IGNORECASE))
    df = df[query]
    return sorted(set(df.iloc[:, -1]))


def fetch_can_capital_query(df) -> list[str]:
    # =========================================================================
    # '''Fetch `Series series_ids` from Statistics Canada. Table: 36-10-0238-01\
    # (formerly CANSIM 031-0004): Flows and stocks of fixed non-residential\
    # capital, total all industries, by asset, provinces and territories, annual\
    # (dollars x 1,000,000)'''
    # =========================================================================
    # =========================================================================
    # ?: 36100096-eng.zip'
    # =========================================================================
    # =========================================================================
    # usecols = [3, 5, 6, 11]
    # =========================================================================
    query = (df.iloc[:, 0].str.contains('2007 constant prices')) &\
            (df.iloc[:, 1] == 'Straight-line end-year net stock') &\
            (df.iloc[:, 2].str.contains('Industrial'))
    df = df[query]
    return sorted(set(df.iloc[:, -1]))


def fetch_can_capital(series_ids):
    # =========================================================================
    # Fetch <pd.DataFrame> from Statistics Canada. Table: 36-10-0238-01 (formerly
    # CANSIM 031-0004): Flows and stocks of fixed non-residential capital, total
    # all industries, by asset, provinces and territories, annual
    # (dollars x 1,000,000)
    # =========================================================================
    URL = 'https://www150.statcan.gc.ca/n1/en/tbl/csv/36100096-eng.zip'
    data_frame = fetch_can_from_url(URL, usecols=[0, 11, 13])
    data_frame = data_frame[data_frame.iloc[:, 1].isin(series_ids)]
    result_frame = pd.DataFrame()
    for series_id in series_ids:
        chunk = data_frame[data_frame.iloc[:, 1] == series_id].iloc[:, [0, 2]]
        chunk.columns = [chunk.columns[0], series_id]
        chunk.set_index(chunk.columns[0],
                        inplace=True,
                        verify_integrity=True)
        result_frame = pd.concat([result_frame, chunk], axis=1, sort=True)
    result_frame['sum'] = result_frame.sum(axis=1)
    return result_frame.iloc[:, [-1]]


def fetch_can(data_frame, series_id):
    # =========================================================================
    # Data Frame Fetching from CANSIM Zip Archives
    # =========================================================================
    data_frame = data_frame[data_frame.iloc[:, 10]
                            == series_id].iloc[:, [0, 12]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].astype(int)
    data_frame.iloc[:, 1] = data_frame.iloc[:, 1].astype(float)
    data_frame.columns = [data_frame.columns[0], series_id]
    return data_frame.set_index(data_frame.columns[0])


def fetch_can_fixed_assets(series_ids):
    # =========================================================================
    # Fetch <series_ids> from CANSIM Table 031-0004: Flows and stocks of fixed
    # non-residential capital, total all industries, by asset, provinces and
    # territories, annual (dollars x 1,000,000)
    # =========================================================================
    ARCHIVE_NAME = 'dataset_can_00310004-eng.zip'
    data_frame = pd.read_csv(ARCHIVE_NAME, usecols=[0, 6, 8])
    data_frame = data_frame[data_frame.iloc[:, 1].isin(series_ids)]
    data_frame.iloc[:, 2] = pd.to_numeric(
        data_frame.iloc[:, 2], errors='coerce')
    result_frame = pd.DataFrame()
    for series_id in series_ids:
        chunk = data_frame[data_frame.iloc[:, 1] == series_id].iloc[:, [0, 2]]
        chunk.columns = [chunk.columns[0].upper(), series_id]
        chunk.set_index(chunk.columns[0],
                        inplace=True,
                        verify_integrity=True)
        result_frame = pd.concat([result_frame, chunk], axis=1, sort=True)
    result_frame['sum'] = result_frame.sum(axis=1)
    return result_frame.iloc[:, [-1]]


def fetch_can_from_url(url: str, usecols: list = None) -> pd.DataFrame:
    '''Downloading zip file from url'''
    name = url.split('/')[-1]
    if os.path.exists(name):
        with ZipFile(name, 'r').open(name.replace('-eng.zip', '.csv')) as f:
            return pd.read_csv(f, usecols=usecols)
    else:
        r = requests.get(url)
        with ZipFile(io.BytesIO(r.content)).open(name.replace('-eng.zip', '.csv')) as f:
            return pd.read_csv(f, usecols=usecols)


def fetch_can_group_a(file_id, skiprows):
    # =========================================================================
    # Not Used Anywhere
    # =========================================================================
    data_frame = pd.read_csv(f'dataset_can_cansim{file_id}.csv',
                             skiprows=skiprows)
    if file_id == '7931814471809016759':
        data_frame.columns = [column[:7] for column in data_frame.columns]
        data_frame.iloc[:, -
                        1] = pd.to_numeric(data_frame.iloc[:, -1].str.replace(';', ''))
    data_frame = data_frame.set_index(data_frame.columns[0]).transpose()
    data_frame.reset_index(inplace=True)
    data_frame[['quarter',
                'period', ]] = data_frame.iloc[:, 0].str.split(expand=True)
    data_frame.set_index(data_frame.columns[0], inplace=True)
    return data_frame.groupby(data_frame.columns[-1]).mean()


def fetch_can_group_b(file_id, skiprows):
    # =========================================================================
    # Not Used Anywhere
    # =========================================================================
    data_frame = pd.read_csv(f'dataset_can_cansim{file_id}.csv',
                             skiprows=skiprows)
    data_frame[['month',
                'period', ]] = data_frame.iloc[:, 0].str.split('-', expand=True)
    return data_frame.groupby(data_frame.columns[-1]).mean()


def fetch_can_quarterly(file_id, series_id):
    # =========================================================================
    # Data Frame Fetching from Quarterly Data within CANSIM Zip Archives
    # Should Be [x 7 columns]
    # =========================================================================
    RESERVED_FILE_IDS = (2820011, 2820012, 3790031, 3800068,)
    RESERVED_COMBINATIONS = ((3790031, 'v65201809',),
                             (3800084, 'v62306938',),)
    USECOLS = ((4, 6,), (5, 7,),)
    usecols = (USECOLS[0], USECOLS[1])[file_id in RESERVED_FILE_IDS]
    data_frame = pd.read_csv(f'dataset_can_{file_id:08n}-eng.zip',
                             usecols=[0, *usecols])
    data_frame = data_frame[data_frame.iloc[:, 1] == series_id].iloc[:, [0, 2]]
    data_frame.columns = [data_frame.columns[0], series_id]
    data_frame[['period',
                'sub_period', ]] = data_frame.iloc[:, 0].str.split('/', expand=True)
    data_frame.iloc[:, 1] = data_frame.iloc[:, 1].astype(float)
    data_frame.iloc[:, -2] = data_frame.iloc[:, -2].astype(int)
    if (file_id, series_id,) in RESERVED_COMBINATIONS:
        return data_frame.groupby(data_frame.columns[-2]).sum()
    else:
        return data_frame.groupby(data_frame.columns[-2]).mean()


def fetch_can_quarterly(data_frame, series_id):
    # =========================================================================
    # Data Frame Fetching from Quarterly Data within CANSIM Zip Archives
    # =========================================================================
    data_frame = data_frame[data_frame.iloc[:, 10]
                            == series_id].iloc[:, [0, 12]]
    data_frame.columns = [data_frame.columns[0], series_id]
    data_frame[['period',
                'sub_period', ]] = data_frame.iloc[:, 0].str.split('-', expand=True)
    data_frame.iloc[:, 1] = data_frame.iloc[:, 1].astype(float)
    data_frame.iloc[:, -2] = data_frame.iloc[:, -2].astype(int)
    return data_frame.groupby(data_frame.columns[-2]).sum()


def fetch_usa_bea(archive_name: str, wb_name: str, sh_name: str, series_id: str) -> pd.DataFrame:
    # =========================================================================
    # Data Frame Fetching from Bureau of Economic Analysis Zip Archives
    # =========================================================================
    with pd.ExcelFile(ZipFile(archive_name, 'r').open(wb_name)) as xl_file:
        # =====================================================================
        # Load
        # =====================================================================
        data_frame = pd.read_excel(xl_file, sh_name, skiprows=7)
        # =====================================================================
        # Re-Load
        # =====================================================================
        data_frame = pd.read_excel(xl_file,
                                   sh_name,
                                   usecols=range(2, data_frame.shape[1]),
                                   skiprows=7)
    data_frame.dropna(axis=0, inplace=True)
    data_frame.columns = ['period', *data_frame.columns[1:]]
    data_frame = data_frame.set_index(data_frame.columns[0]).transpose()
    return data_frame.loc[:, [series_id]]


def fetch_usa_bea_filter(series_id):
    # =========================================================================
    # Retrieve Yearly Data for BEA Series' Code
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-nipa-2015-05-01.zip'
    data_frame = pd.read_csv(ARCHIVE_NAME, usecols=[0, *range(14, 18)])
    query = (data_frame.iloc[:, 1] == series_id) & \
            (data_frame.iloc[:, 3] == 0)
    data_frame = data_frame[query]
    combined = pd.DataFrame()
    for source_id in sorted(set(data_frame.iloc[:, 0])):
        chunk = data_frame[data_frame.iloc[:, 0] == source_id].iloc[:, [2, 4]]
        chunk.columns = [chunk.columns[0],
                         '{}{}'.format(source_id.split()[1].replace('.', '_'), series_id)]
        chunk.drop_duplicates(inplace=True)
        chunk.set_index(chunk.columns[0], inplace=True, verify_integrity=True)
        combined = pd.concat([combined, chunk], axis=1, sort=True)
    return combined


def fetch_usa_bea_from_loaded(data_frame: pd.DataFrame, series_id: str) -> pd.DataFrame:
    '''`NipaDataA.txt`: U.S. Bureau of Economic Analysis'''
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    data_frame.columns = [data_frame.columns[0].lower(), series_id]
    return data_frame.set_index(data_frame.columns[0], verify_integrity=True)


def fetch_usa_bea_from_url(url: str) -> pd.DataFrame:
    '''Retrieves U.S. Bureau of Economic Analysis DataFrame from URL'''
    return pd.read_csv(io.BytesIO(requests.get(url).content), thousands=',')


def fetch_usa_bea_sfat_series():
    ARCHIVE_NAME = 'dataset_usa_bea-nipa-selected.zip'
    SERIES_ID = 'k3n31gd1es000'
    data_frame = pd.read_csv(ARCHIVE_NAME, usecols=[0, *range(8, 11)])
    data_frame = data_frame[data_frame.iloc[:, 1] == SERIES_ID]
    control_frame = pd.DataFrame()
    for source_id in sorted(set(data_frame.iloc[:, 0])):
        chunk = data_frame[data_frame.iloc[:, 0] == source_id].iloc[:, [2, 3]]
        chunk.columns = [chunk.columns[0],
                         '{}{}'.format(source_id.split()[1].replace('.', '_'), SERIES_ID)]
        chunk.set_index(chunk.columns[0], inplace=True, verify_integrity=True)
        control_frame = pd.concat([control_frame, chunk], axis=1, sort=True)

    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WB_NAME = 'Section4ALL_xls.xls'
    SH_NAME = '403 Ann'
    # =========================================================================
    # Fixed Assets Series, 1925--2016
    # =========================================================================
    SERIES_IDS = ('k3n31gd1es000', 'k3n31gd1eq000',
                  'k3n31gd1ip000', 'k3n31gd1st000',)
    test_frame = pd.concat(
        [
            fetch_usa_bea(ARCHIVE_NAME, WB_NAME, SH_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    return pd.concat([test_frame, control_frame], axis=1, sort=True)


def fetch_usa_bls(file_name, series_id):
    # =========================================================================
    # Bureau of Labor Statistics Data Fetch
    # =========================================================================
    data_frame = pd.read_csv(file_name,
                             sep='\t',
                             usecols=range(4),
                             low_memory=False)
    query = (data_frame.iloc[:, 0].str.contains(series_id)) & \
            (data_frame.iloc[:, 2] == 'M13')
    data_frame = data_frame[query].iloc[:, [1, 3]]
    data_frame.columns = [data_frame.columns[0], series_id]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].astype(int)
    data_frame.iloc[:, 1] = data_frame.iloc[:, 1].astype(float)
    return data_frame.set_index(data_frame.columns[0])


def fetch_usa_census_description(file_name, series_id):
    """Retrieve Series Description U.S. Bureau of the Census"""
    data_frame = pd.read_csv(
        file_name, usecols=[0, 1, 3, 4, 5, 6, 8], low_memory=False)
    data_frame = data_frame[data_frame.iloc[:, 6] == series_id]
    data_frame.drop_duplicates(inplace=True)
    if data_frame.iloc[0, 2] == 'no_details':
        if data_frame.iloc[0, 5] == 'no_details':
            if data_frame.iloc[0, 4] == 'no_details':
                description = '{}'.format(data_frame.iloc[0, 3])
            else:
                description = '{} -\n{}'.format(*data_frame.iloc[0, [3, 4]])
        else:
            description = '{} -\n{} -\n{}'.format(*
                                                  data_frame.iloc[0, [3, 4, 5]])
    else:
        if data_frame.iloc[0, 5] == 'no_details':
            if data_frame.iloc[0, 4] == 'no_details':
                description = '{}; {}'.format(*data_frame.iloc[0, [3, 2]])
            else:
                description = '{} -\n{}; {}'.format(*
                                                    data_frame.iloc[0, [3, 4, 2]])
        else:
            description = '{} -\n{} -\n{}; {}'.format(
                *data_frame.iloc[0, [3, 4, 5, 2]])
    return description


def fetch_usa_census(archive_name: str, series_id: str) -> pd.DataFrame:
    # =========================================================================
    # Selected Series by U.S. Bureau of the Census
    # U.S. Bureau of the Census, Historical Statistics of the United States,
    # 1789--1945, Washington, D.C., 1949.
    # U.S. Bureau of the Census. Historical Statistics of the United States,
    # Colonial Times to 1970, Bicentennial Edition. Washington, D.C., 1975.
    # =========================================================================
    data_frame = pd.read_csv(archive_name,
                             usecols=range(8, 11),
                             dtype=str)
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].str[:4].astype(int)
    data_frame.iloc[:, 1] = data_frame.iloc[:, 1].astype(float)
    data_frame.columns = [data_frame.columns[0], series_id]
    data_frame.sort_values(data_frame.columns[0], inplace=True)
    return data_frame.groupby(data_frame.columns[0]).mean()


def fetch_usa_classic(archive_name: str, series_id: str) -> pd.DataFrame:
    # =========================================================================
    # Data Fetch Procedure for Enumerated Classical Datasets
    # =========================================================================
    USECOLS = {
        'dataset_douglas.zip': (4, 7,),
        'dataset_usa_brown.zip': (3, 6,),
        'dataset_usa_cobb-douglas.zip': (5, 8,),
        'dataset_usa_kendrick.zip': (4, 7,),
    }
    data_frame = pd.read_csv(
        archive_name,
        skiprows=(None, 4)[archive_name == 'dataset_usa_brown.zip'],
        usecols=range(*USECOLS[archive_name])
    )
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].astype(int)
    data_frame.iloc[:, 1] = pd.to_numeric(
        data_frame.iloc[:, 1], errors='coerce')
    data_frame.columns = [data_frame.columns[0], series_id]
    return data_frame.set_index(data_frame.columns[0])


def fetch_usa_mcconnel(series_id: str) -> pd.DataFrame:
    '''Data Frame Fetching from McConnell C.R. & Brue S.L.'''
    ARCHIVE_NAME = 'dataset_usa_mc_connell_brue.zip'
    data_frame = pd.read_csv(ARCHIVE_NAME, index_col=1, usecols=range(1, 4))
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1]]
    return data_frame.sort_index()


def fetch_world_bank(data_frame: pd.DataFrame, series_id: str) -> pd.DataFrame:
    df = data_frame[data_frame.iloc[:, 1] == series_id].iloc[:, [0, 2]]
    df.columns = [df.columns[0], series_id]
    return df.set_index(df.columns[0])


def get_data_archived() -> pd.DataFrame:
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH_NAMES = (
        '10105 Ann',
        '10106 Ann',
        '50900 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        'A191RX1',
        # =====================================================================
        # Fixed Assets Series: K160491, 1951--2011
        # `K160491` Replaced with `K10070` in `get_data_combined()`
        # =====================================================================
        'K160491',
    )
    _data_bea = pd.concat(
        [
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVE_NAMES[0], _wb, _sh, _id)
                    for _wb, _sh, _id in zip(tuple(WB_NAMES[2*(_ // 2)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVE_NAMES[1], _wb, _sh, _id)
                    for _wb, _sh, _id in zip(tuple(WB_NAMES[1 + 2*(_ // 2)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
        ],
        sort=True
    ).drop_duplicates()
    _df = pd.concat(
        [
            # =====================================================================
            # Do Not Use As It Is CPI-U Not PPI
            # =====================================================================
            get_data_usa_bls_cpiu(),
            _data_bea,
        ],
        axis=1, sort=True).dropna(axis=0)
    # =========================================================================
    # Deflator, 2005=100
    # =========================================================================
    _df['def'] = _df.iloc[:, 0].add(1).cumprod()
    _df.iloc[:, -1] = _df.iloc[:, -
                               1].rdiv(_df.iloc[_df.index.get_loc(2005), -1])
    # =========================================================================
    # Investment, 2005=100
    # =========================================================================
    _df['inv'] = _df.iloc[:, 1].mul(_df.iloc[:, -1])
    # =========================================================================
    # Capital, 2005=100
    # =========================================================================
    _df['cap'] = _df.iloc[:, 3].mul(_df.iloc[:, -1])
    # =========================================================================
    # Capital Retirement Ratio
    # =========================================================================
    _df['ratio_mu'] = _df.iloc[:, -2].mul(1).sub(_df.iloc[:, -1].shift(-1)).div(
        _df.iloc[:, -1]).add(1)
    return (
        _df.loc[:, ['inv', 'A191RX1', 'cap', 'ratio_mu']].dropna(axis=0),
        _df.loc[:, ['ratio_mu']].dropna(axis=0),
        _df.index.get_loc(2005)
    )


def get_data_bea_def() -> pd.DataFrame:
    '''Intent: Returns Cumulative Price Index for Some Base Year from Certain Type BEA Deflator File'''
    FILE_NAME = 'dataset_usa_bea-GDPDEF.xls'
    data_frame = pd.read_excel(
        FILE_NAME,
        names=['period', 'value'],
        index_col=0,
        skiprows=15,
        parse_dates=True
    )
    return data_frame.groupby(data_frame.index.year).prod().pow(1/4)


def get_data_bea_gdp():
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
    )
    SH_NAMES = (
        '10105 Ann',
        '10106 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        'A191RC1',
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        'A191RX1',
    )
    return pd.concat(
        [
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVE_NAMES[0], WB_NAMES[0], sh, _id)
                    for sh, _id in zip(SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVE_NAMES[1], WB_NAMES[1], sh, _id)
                    for sh, _id in zip(SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
        ],
        sort=True
    ).drop_duplicates()


def get_data_brown():
    # =========================================================================
    # Fetch Data from `Reference RU Brown M. 0597_088.pdf`, Page 193
    # Dependent on `fetch_usa_classic`
    # Out of Kendrick J.W. Data & Table 2. of `Reference RU Brown M. 0597_088.pdf`
    # =========================================================================
    # =========================================================================
    # FN:Murray Brown
    # ORG:University at Buffalo;Economics
    # TITLE:Professor Emeritus, Retired
    # EMAIL;PREF;INTERNET:mbrown@buffalo.edu
    # =========================================================================
    ARCHIVE_NAMES = ('dataset_usa_brown.zip', 'dataset_usa_kendrick.zip',)
    data_frame = pd.read_csv(ARCHIVE_NAMES[0], skiprows=4, usecols=range(3, 6))
    data_frame.columns = ['series_id', 'period', 'value']
    _b_frame = pd.concat(
        [
            fetch_usa_classic(ARCHIVE_NAMES[0], series_id)
            for series_id in sorted(set(data_frame.iloc[:, 0]))
        ],
        axis=1,
        sort=True)
    _b_frame.columns = [
        f'series_{hex(_)}' for _, column in enumerate(_b_frame.columns)
    ]
    # =========================================================================
    # Валовой продукт (в млн. долл., 1929 г.)
    # Чистый основной капитал (в млн. долл., 1929 г.)
    # Используемый основной капитал (в млн. долл., 1929 г.)
    # Отработанные человеко-часы
    # Первая аппроксимация рядов загрузки мощностей, полученная с помощью метода Уортонской школы
    # Вторая аппроксимация рядов загрузки мощностей, полученная с помощью итеративного процесса
    # =========================================================================
    # =========================================================================
    # Gross Domestic Product, USD 1,000,000, 1929=100
    # Net Fixed Assets, USD 1,000,000, 1929=100
    # Utilized Fixed Assets, USD 1,000,000, 1929=100
    # Actual Man-Hours Worked
    # _
    # _
    # =========================================================================
    SERIES_IDS = ('KTA03S07', 'KTA03S08', 'KTA10S08', 'KTA15S07', 'KTA15S08',)
    _k_frame = pd.concat(
        [fetch_usa_classic(ARCHIVE_NAMES[1], series_id)
         for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    result_frame = pd.concat(
        [
            _k_frame[_k_frame.index.get_loc(
                1889):2+_k_frame.index.get_loc(1952)],
            # =================================================================
            # Первая аппроксимация рядов загрузки мощностей, полученная с помощью метода Уортонской школы
            # =================================================================
            _b_frame.iloc[:1+_b_frame.index.get_loc(1953), [4]]
        ],
        axis=1,
        sort=True)
    result_frame = result_frame.assign(
        series_0x0=result_frame.iloc[:, 0].sub(result_frame.iloc[:, 1]),
        series_0x1=result_frame.iloc[:, 3].add(result_frame.iloc[:, 4]),
        series_0x2=result_frame.iloc[:, [3, 4]].sum(axis=1).rolling(
            window=2).mean().mul(result_frame.iloc[:, 5]).div(100),
        series_0x3=result_frame.iloc[:, 2],
    )
    result_frame = result_frame.iloc[:, [6, 7, 8, 9]].dropna(axis=0)
    return pd.concat(
        [
            result_frame,
            # =================================================================
            # Brown M. Numbers Not Found in Kendrick J.W. For Years Starting From 1954 Inclusive
            # =================================================================
            _b_frame.iloc[1+_b_frame.index.get_loc(1953):, [0, 1, 2, 3]]
        ]
    ).round()


def get_data_can():
    # =========================================================================
    # '''A. Fixed Assets Block: `Industrial buildings`, `Industrial machinery`\
    # for `Newfoundland and Labrador`, `Prince Edward Island`, `Nova Scotia`, \
    # `New Brunswick`, `Quebec`, `Ontario`, `Manitoba`, `Saskatchewan`, `Alberta`, \
    # `British Columbia`, `Yukon`, `Northwest Territories`, `Nunavut`'''
    # '''2007 constant prices'''
    # '''Geometric (infinite) end-year net stock'''
    # '''Industrial buildings (x 1,000,000): `v43975603`, `v43977683`, `v43978099`, \
    # `v43978515`, `v43978931`, `v43979347`, `v43979763`, `v43980179`, `v43980595`, \
    # `v43976019`, `v43976435`, `v43976851`, `v43977267`'''
    # '''Industrial machinery (x 1,000,000): `v43975594`, `v43977674`, `v43978090`, \
    # `v43978506`, `v43978922`, `v43979338`, `v43979754`, `v43980170`, `v43980586`, \
    # `v43976010`, `v43976426`, `v43976842`, `v43977258`'''
    # '''Table: 36-10-0238-01 (formerly CANSIM 031-0004): Flows and stocks of\
    # fixed non-residential capital, total all industries, by asset, provinces\
    # and territories, annual (dollars x 1,000,000)'''
    # =========================================================================
    URL = 'https://www150.statcan.gc.ca/n1/en/tbl/csv/36100096-eng.zip'
    capital = fetch_can_from_url(URL)
    capital = fetch_can_capital(fetch_can_capital_query())
    # =========================================================================
    # '''B. Labor Block: `v2523012`, Preferred Over `v3437501` Which Is Quarterly'''
    # '''`v2523012` - Table: 14-10-0027-01 (formerly CANSIM 282-0012): Employment\
    # by class of worker, annual (x 1,000)'''
    # =========================================================================
    URL = 'https://www150.statcan.gc.ca/n1/tbl/csv/14100027-eng.zip'
    labor = fetch_can_from_url(URL)
    labor = fetch_can(labor, 'v2523012')
    # =========================================================================
    # '''C. Production Block: `v65201809`'''
    # '''`v65201809` - Table: 36-10-0434-01 (formerly CANSIM 379-0031): Gross\
    # domestic product (GDP) at basic prices, by industry, monthly (x 1,000,000)'''
    # =========================================================================
    URL = 'https://www150.statcan.gc.ca/n1/tbl/csv/36100434-eng.zip'
    product = fetch_can_from_url(URL)
    product = fetch_can_quarterly(product, 'v65201809')
    result_frame = pd.concat([capital, labor, product], axis=1, sort=True)
    # result_frame = result_frame.dropna(axis=0)
    result_frame.columns = ['capital', 'labor', 'product']
    # result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame


def get_data_can():
    data_frame = pd.concat(
        [
            # =============================================================================
            # A. Fixed Assets Block: `Industrial buildings`, `Industrial machinery` for `Newfoundland and Labrador`, `Prince Edward Island`, `Nova Scotia`, `New Brunswick`, \
            #     `Quebec`, `Ontario`, `Manitoba`, `Saskatchewan`, `Alberta`, `British Columbia`, `Yukon`, `Northwest Territories`, `Nunavut`
            # 2007 constant prices
            # Geometric (infinite) end-year net stock
            # Industrial buildings (x 1,000,000): `v43975603`, `v43977683`, `v43978099`, `v43978515`, `v43978931`, `v43979347`, `v43979763`, `v43980179`, `v43980595`, \
            #     `v43976019`, `v43976435`, `v43976851`, `v43977267`
            # Industrial machinery (x 1,000,000): `v43975594`, `v43977674`, `v43978090`, `v43978506`, `v43978922`, `v43979338`, `v43979754`, `v43980170`, `v43980586`, \
            #     `v43976010`,  `v43976426`, `v43976842`, `v43977258`
            # =============================================================================
            fetch_can_fixed_assets(fetch_can_capital_query_archived()),
            # =============================================================================
            # B. Labor Block: `v2523012`, Preferred Over `v3437501` Which Is Quarterly
            # `v2523012` - 282-0012 Labour Force Survey Estimates (LFS), employment by class of worker, North American Industry Classification System (NAICS)\
            # and sex; Canada; Total employed, all class of workers; Manufacturing; Both sexes (x 1,000) (annual, 1987 to 2017)
            # =============================================================================
            fetch_can_annually(2820012, 'v2523012'),
            # =============================================================================
            # C. Production Block: `v65201809`
            # `v65201809` - 379-0031 Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS); Canada; Trading-day\
            # adjusted; 2007 constant prices; Manufacturing (x 1,000,000) (monthly, 1997-01-01 to 2017-10-01)
            # =============================================================================
            fetch_can_quarterly(3790031, 'v65201809'),
        ], axis=1, sort=True
    ).dropna(axis=0)
    data_frame.columns = ['capital', 'labor', 'product']
    return data_frame


def get_data_can():
    '''Number 1. CANSIM Table 282-0012 Labour Force Survey Estimates (LFS), employment by class of worker, North American Industry Classification\
    System (NAICS) and sex'''
    '''Number 2. CANSIM Table 03790031'''
    '''Title: Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS)'''
    '''Measure: monthly (dollars x 1,000,000)'''
    '''Number 3. CANSIM Table 03800068'''
    '''Title: Gross fixed capital formation'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 4. CANSIM Table 031-0004: Flows and stocks of fixed non-residential capital, total all industries, by asset, provinces and territories, \
    annual (dollars x 1,000,000)'''
    '''Number 5. CANSIM Table 03790028'''
    '''Title: Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS), provinces and territories'''
    '''Measure: annual (percentage share)'''
    '''Number 6. CANSIM Table 03800001'''
    '''Title: Gross domestic product (GDP), income-based, *Terminated*'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 7. CANSIM Table 03800002'''
    '''Title: Gross domestic product (GDP), expenditure-based, *Terminated*'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 8. CANSIM Table 03800063'''
    '''Title: Gross domestic product, income-based'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 9. CANSIM Table 03800064'''
    '''Title: Gross domestic product, expenditure-based'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 10. CANSIM Table 03800069'''
    '''Title: Investment in inventories'''
    '''Measure: quarterly (dollars unless otherwise noted)'''
    '''---'''
    '''1.0. Labor Block: `v2523012`, Preferred Over `v3437501` Which Is Quarterly'''
    '''`v2523012` - 282-0012 Labour Force Survey Estimates (LFS), employment by class of worker, North American Industry Classification System (NAICS)\
    and sex; Canada; Total employed, all class of workers; Manufacturing; Both sexes (x 1,000) (annual, 1987 to 2017)'''
    labor = fetch_can_annually(2820012, 'v2523012')
    '''1.1. Labor Block, Alternative Option Not Used'''
    '''`v3437501` - 282-0011 Labour Force Survey estimates (LFS), employment by class of worker, North American Industry Classification System (NAICS)\
    and sex, unadjusted for seasonality; Canada; Total employed, all classes of workers; Manufacturing; Both sexes (x 1,000) (monthly, 1987-01-01 to\
    2017-12-01)'''
    # =============================================================================
    # fetch_can_quarterly(2820011, 'v3437501')
    # =============================================================================
    '''2.i. Fixed Assets Block: `Industrial buildings`, `Industrial machinery` for `Newfoundland and Labrador`, `Prince Edward Island`, `Nova Scotia`, `New Brunswick`, \
    `Quebec`, `Ontario`, `Manitoba`, `Saskatchewan`, `Alberta`, `British Columbia`, `Yukon`, `Northwest Territories`, `Nunavut`'''
    '''2.0. 2007 constant prices'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1,000,000): `v43975603`, `v43977683`, `v43978099`, `v43978515`, `v43978931`, `v43979347`, `v43979763`, `v43980179`, `v43980595`, \
    `v43976019`, `v43976435`, `v43976851`, `v43977267`'''
    '''Industrial machinery (x 1,000,000): `v43975594`, `v43977674`, `v43978090`, `v43978506`, `v43978922`, `v43979338`, `v43979754`, `v43980170`, `v43980586`, \
    `v43976010`, `v43976426`, `v43976842`, `v43977258`'''
    SERIES_IDS = ('v43975603', 'v43977683', 'v43978099', 'v43978515',
                  'v43978931', 'v43979347', 'v43979763', 'v43980179',
                  'v43980595', 'v43976019', 'v43976435', 'v43976851',
                  'v43977267', 'v43975594', 'v43977674', 'v43978090',
                  'v43978506', 'v43978922', 'v43979338', 'v43979754',
                  'v43980170', 'v43980586', 'v43976010', 'v43976426',
                  'v43976842', 'v43977258',)
    '''2.1. Fixed Assets Block, Alternative Option Not Used'''
    '''2.1.1. Chained (2007) dollars'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1,000,000): `v43980803`, `v43981843`, `v43982051`, `v43982259`, `v43982467`, `v43982675`, `v43982883`, `v43983091`, `v43983299`, \
    `v43981011`, `v43981219`, `v43981427`, `v43981635`'''
    '''Industrial machinery (x 1,000,000): `v43980794`, `v43981834`, `v43982042`, `v43982250`, `v43982458`, `v43982666`, `v43982874`, `v43983082`, `v43983290`, \
    `v43981002`, `v43981210`, `v43981418`, `v43981626`'''
    # SERIES_IDS = ('v43980803', 'v43981843', 'v43982051', 'v43982259',
    #               'v43982467', 'v43982675', 'v43982883', 'v43983091',
    #               'v43983299', 'v43981011', 'v43981219', 'v43981427',
    #               'v43981635', 'v43980794', 'v43981834', 'v43982042',
    #               'v43982250', 'v43982458', 'v43982666', 'v43982874',
    #               'v43983082', 'v43983290', 'v43981002', 'v43981210',
    #               'v43981418', 'v43981626',)
    '''2.1.2. Current prices'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1,000,000): `v43975395`, `v43977475`, `v43977891`, `v43978307`, `v43978723`, `v43979139`, `v43979555`, `v43979971`, `v43980387`, \
    `v43975811`, `v43976227`, `v43976643`, `v43977059`'''
    '''Industrial machinery (x 1,000,000): `v43975386`, `v43977466`, `v43977882`, `v43978298`, `v43978714`, `v43979130`, `v43979546`, `v43979962`, `v43980378`, \
    `v43975802`, `v43976218`, `v43976634`, `v43977050`'''
    # SERIES_IDS = ('v43975395', 'v43977475', 'v43977891', 'v43978307',
    #               'v43978723', 'v43979139', 'v43979555', 'v43979971',
    #               'v43980387', 'v43975811', 'v43976227', 'v43976643',
    #               'v43977059', 'v43975386', 'v43977466', 'v43977882',
    #               'v43978298', 'v43978714', 'v43979130', 'v43979546',
    #               'v43979962', 'v43980378', 'v43975802', 'v43976218',
    #               'v43976634', 'v43977050',)
    capital = fetch_can_fixed_assets(fetch_can_capital_query_archived())
    '''3.i. Production Block: `v65201809`, Preferred Over `v65201536` Which Is Quarterly'''
    '''3.0. Production Block: `v65201809`'''
    '''`v65201809` - 379-0031 Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS); Canada; Trading-day\
    adjusted; 2007 constant prices; Manufacturing (x 1,000,000) (monthly, 1997-01-01 to 2017-10-01)'''
    product = fetch_can_quarterly(3790031, 'v65201809')
    '''3.1. Production Block: `v65201536`, Alternative Option Not Used'''
    '''`v65201536` - 379-0031 Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS); Canada; Seasonnaly\
    adjusted at annual rates; 2007 constant prices; Manufacturing (x 1,000,000) (monthly, 1997-01-01 to 2017-10-01)'''
    # =============================================================================
    # fetch_can_quarterly(3790031, 'v65201536')
    # =============================================================================
    data_frame = pd.concat(
        [
            capital,
            labor,
            product
        ], axis=1, sort=True).dropna(axis=0)
    data_frame.columns = ['capital', 'labor', 'product']
    return data_frame


def get_data_capital_combined_archived():
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH_NAMES = (
        '10105 Ann',
        '10106 Ann',
        '50900 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        'A191RC1',
        # =====================================================================
        # Real Gross Domestic Product Series: A191RX1, 1929--2012
        # =====================================================================
        'A191RX1',
        # =====================================================================
        # U.S. Bureau of Economic Analysis, Produced assets, closing balance: Fixed assets (DISCONTINUED) [K160491A027NBEA], retrieved from FRED, Federal Reserve Bank of St. Louis;
        # https://fred.stlouisfed.org/series/K160491A027NBEA, August 23, 2018.
        # http://www.bea.gov/data/economic-accounts/national
        # https://fred.stlouisfed.org/series/K160491A027NBEA
        # https://search.bea.gov/search?affiliate=u.s.bureauofeconomicanalysis&query=k160491
        # =====================================================================
        # =====================================================================
        # Fixed Assets Series: K160021, 1951--2011
        # =====================================================================
        'K160021',
        # =====================================================================
        # Fixed Assets Series: K160491, 1951--2011
        # =====================================================================
        'K160491',
    )
    _data = pd.concat(
        [
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVE_NAMES[0], _wb, _sh, _id)
                    for _wb, _sh, _id in zip(
                        tuple(WB_NAMES[2*(_ // len(SH_NAMES))] for _ in range(len(SERIES_IDS))),
                        tuple(SH_NAMES[2*(_ // len(SH_NAMES)) + ((_ - 1) % len(SH_NAMES)) *
                                  (2 - ((_ - 1) % len(SH_NAMES)))] for _ in range(len(SERIES_IDS))),
                        SERIES_IDS,
                    )
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVE_NAMES[1], _wb, _sh, _id)
                    for _wb, _sh, _id in zip(
                        tuple(WB_NAMES[1 + 2*(_ // len(SH_NAMES))]
                              for _ in range(len(SERIES_IDS))),
                        tuple(SH_NAMES[2*(_ // len(SH_NAMES)) + ((_ - 1) % len(SH_NAMES)) *
                                  (2 - ((_ - 1) % len(SH_NAMES)))] for _ in range(len(SERIES_IDS))),
                        SERIES_IDS,
                    )
                ],
                axis=1,
                sort=True
            ),
        ],
        sort=True).drop_duplicates()
    return pd.concat(
        [_data,
         # ====================================================================
         # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
         # ====================================================================
         get_data_usa_frb_cu(),
         # ====================================================================
         # Manufacturing Labor Series: _4313C0, 1929--2011
         # ====================================================================
         get_data_usa_bea_labor_mfg(),
         # ====================================================================
         # Labor Series: A4601C0, 1929--2011
         # ====================================================================
         get_data_usa_bea_labor()], axis=1, sort=True)


def get_data_capital_purchases():
    ARCHIVE_NAMES = (
        # =====================================================================
        # CDT2S1: Nominal; CDT2S3: 1880=100;
        # =====================================================================
        'dataset_usa_cobb-douglas.zip',
        # =====================================================================
        # DT63AS01: 1880=100; DT63AS02: Do Not Use; DT63AS03: Do Not Use;
        # =====================================================================
        'dataset_douglas.zip',)
    SERIES_IDS = ('CDT2S1', 'CDT2S3', 'DT63AS01', 'DT63AS02', 'DT63AS03',)
    _args = [tuple(((ARCHIVE_NAMES[0], ARCHIVE_NAMES[1])[series_id.startswith(
        'DT')], series_id,)) for series_id in SERIES_IDS]
    _data_frame = pd.concat(
        [fetch_usa_classic(*arg) for arg in _args],
        axis=1,
        sort=True)

    ARCHIVE_NAMES = (
        # =====================================================================
        # Nominal Series, USD Millions
        # =====================================================================
        'dataset_usa_census1949.zip',
        # =====================================================================
        # P0107, P0108, P0109, P0113, P0114, P0115 -- Nominal Series, USD Billions
        # P0110, P0111, P0112, P0116, P0117, P0118, P0119, P0120, P0121, P0122 -- Real Series, 1958=100, USD Billions
        # =====================================================================
        'dataset_usa_census1975.zip',)
    SERIES_IDS = (
        'J0149', 'J0150', 'J0151', 'P0107', 'P0108', 'P0109', 'P0110',
        'P0111', 'P0112', 'P0113', 'P0114', 'P0115', 'P0116', 'P0117',
        'P0118', 'P0119', 'P0120', 'P0121', 'P0122',
    )
    _args = [(tuple((ARCHIVE_NAMES[0], series_id, 1,)), tuple((ARCHIVE_NAMES[1], series_id, 1000,)))[
        series_id.startswith('P')] for series_id in SERIES_IDS]
    data_frame_ = pd.concat(
        [fetch_usa_census(*_[:2]).mul(_[-1]) for _ in _args],
        axis=1,
        sort=True)
    data_frame = pd.concat([_data_frame, data_frame_], axis=1, sort=True)
    data_frame = data_frame[data_frame.index.get_loc(1875):]
    data_frame['total'] = data_frame.loc[:, [
        'CDT2S1', 'J0149', 'P0107']].mean(axis=1)
    data_frame['struc'] = data_frame.loc[:, ['J0150', 'P0108']].mean(axis=1)
    data_frame['equip'] = data_frame.loc[:, ['J0151', 'P0109']].mean(axis=1)
    data_frame.iloc[:, -3] = signal.wiener(data_frame.iloc[:, -3]).round()
    data_frame.iloc[:, -2] = signal.wiener(data_frame.iloc[:, -2]).round()
    data_frame.iloc[:, -1] = signal.wiener(data_frame.iloc[:, -1]).round()
    return data_frame


def get_data_census_a():
    '''Census Manufacturing Indexes, 1899=100'''
    ARCHIVE_NAMES = ('dataset_usa_census1949.zip',
                     'dataset_usa_census1975.zip',)
    SERIES_IDS = (
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014',
        # =====================================================================
        # HSUS 1975 Page 667, P17: Edwin Frickey Series, Indexes of Manufacturing Production
        # =====================================================================
        'P0017',)
    _args = [tuple((ARCHIVE_NAMES[1], series_id,)) if series_id.startswith(
        'P') else tuple((ARCHIVE_NAMES[0], series_id,)) for series_id in SERIES_IDS]
    data_frame = pd.concat([fetch_usa_census(*_)
                           for _ in _args], axis=1, sort=True)
    data_frame = data_frame.div(
        data_frame.iloc[data_frame.index.get_loc(1899), :]).mul(100)
    return data_frame, data_frame.index.get_loc(1899)


def get_data_census_b_a():
    '''Returns Nominal Million-Dollar Capital, Including Structures & Equipment, Series'''
    ARCHIVE_NAMES = (
        # =====================================================================
        # Nominal Series, USD Millions
        # =====================================================================
        'dataset_usa_census1949.zip',
        # =====================================================================
        # P0107, P0108, P0109, P0113, P0114, P0115 -- Nominal Series, USD Billions
        # P0110, P0111, P0112, P0116, P0117, P0118, P0119, P0120, P0121, P0122 -- Real Series, 1958=100, USD Billions
        # =====================================================================
        'dataset_usa_census1975.zip',)
    SERIES_IDS = (
        'J0149', 'J0150', 'J0151', 'P0107', 'P0108', 'P0109', 'P0110',
        'P0111', 'P0112', 'P0113', 'P0114', 'P0115', 'P0116', 'P0117',
        'P0118', 'P0119', 'P0120', 'P0121', 'P0122',
    )
    _args = [(tuple((ARCHIVE_NAMES[0], series_id, 1,)), tuple((ARCHIVE_NAMES[1], series_id, 1000,)))[
        series_id.startswith('P')] for series_id in SERIES_IDS]
    data_frame = pd.concat(
        [fetch_usa_census(*_[:2]).mul(_[-1]) for _ in _args],
        axis=1,
        sort=True)
    data_frame = data_frame[data_frame.index.get_loc(1875):]
    data_frame['total'] = data_frame.loc[:, ['J0149', 'P0107']].mean(axis=1)
    data_frame['struc'] = data_frame.loc[:, ['J0150', 'P0108']].mean(axis=1)
    data_frame['equip'] = data_frame.loc[:, ['J0151', 'P0109']].mean(axis=1)
    # data_frame.iloc[:, -3] = signal.wiener(data_frame.iloc[:, -3]).round()
    # data_frame.iloc[:, -2] = signal.wiener(data_frame.iloc[:, -2]).round()
    # data_frame.iloc[:, -1] = signal.wiener(data_frame.iloc[:, -1]).round()
    return data_frame.iloc[:, -3:]


def get_data_census_b_b():
    '''Returns Census Fused Capital Deflator'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = (
        'P0107',  # Nominal
        'P0108',  # Nominal
        'P0109',  # Nominal
        'P0110',  # 1958=100
        'P0111',  # 1958=100
        'P0112',  # 1958=100
        'P0113',  # Nominal
        'P0114',  # Nominal
        'P0115',  # Nominal
        'P0116',  # 1958=100
        'P0117',  # 1958=100
        'P0118',  # 1958=100
    )
    _data_frame = pd.concat(
        [fetch_usa_census(ARCHIVE_NAME, series_id)
         for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    _data_frame = _data_frame[_data_frame.index.get_loc(1879):]
    _data_frame['purchases_total'] = _data_frame.iloc[:, 0].div(
        _data_frame.iloc[:, 3])
    _data_frame['purchases_struc'] = _data_frame.iloc[:, 1].div(
        _data_frame.iloc[:, 4])
    _data_frame['purchases_equip'] = _data_frame.iloc[:, 2].div(
        _data_frame.iloc[:, 5])
    _data_frame['depreciat_total'] = _data_frame.iloc[:, 6].div(
        _data_frame.iloc[:, 9])
    _data_frame['depreciat_struc'] = _data_frame.iloc[:, 7].div(
        _data_frame.iloc[:, 10])
    _data_frame['depreciat_equip'] = _data_frame.iloc[:, 8].div(
        _data_frame.iloc[:, 11])
    data_frame = pd.concat(
        [price_inverse_single(
            _data_frame.iloc[:, [-(1+i)]].dropna()).dropna() for i in range(6)],
        axis=1,
        sort=True)
    data_frame['census_fused'] = data_frame.mean(axis=1)
    return data_frame.iloc[:, [-1]]


def get_data_census_c():
    '''Census Primary Metals & Railroad-Related Products Manufacturing Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('P0262', 'P0265', 'P0266', 'P0267', 'P0268',
                  'P0269', 'P0293', 'P0294', 'P0295',)
    # =========================================================================
    # <base_year>=100
    # =========================================================================
    BASE_YEARS = (1875, 1875, 1875, 1875, 1875, 1909, 1880, 1875, 1875,)
    data_frame = pd.concat(
        [fetch_usa_census(ARCHIVE_NAME, series_id)
         for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    for i in range(data_frame.shape[1]):
        base_year = data_frame.index.get_loc(BASE_YEARS[i])
        data_frame.iloc[:, i] = data_frame.iloc[:, i].div(
            data_frame.iloc[base_year, i]).mul(100)
    return data_frame, BASE_YEARS


def get_data_census_e():
    '''Census Total Immigration Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('C0091', 'C0092', 'C0093', 'C0094', 'C0095', 'C0096',
                  'C0097', 'C0098', 'C0099', 'C0100', 'C0101', 'C0103',
                  'C0104', 'C0105', 'C0106', 'C0107', 'C0108', 'C0109',
                  'C0111', 'C0112', 'C0113', 'C0114', 'C0115', 'C0117',
                  'C0118', 'C0119',)
    data_frame = pd.concat(
        [fetch_usa_census(ARCHIVE_NAME, series_id)
         for series_id in SERIES_IDS],
        axis=1,
        sort=True)

    data_frame['C89'] = data_frame.sum(1)
    return data_frame.iloc[:, [-1]]


def get_data_census_f():
    '''Census Employment Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('D0085', 'D0086', 'D0796', 'D0797', 'D0977', 'D0982',)
    data_frame = pd.concat(
        [fetch_usa_census(ARCHIVE_NAME, series_id)
         for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    data_frame['workers'] = data_frame.iloc[:, 0].div(
        data_frame.iloc[:, 1]).mul(100)
    data_frame.iloc[:, 4].fillna(
        data_frame.iloc[:data_frame.index.get_loc(1906), 4].mean(), inplace=True)
    data_frame.iloc[:, 5].fillna(
        data_frame.iloc[:data_frame.index.get_loc(1906), 5].mean(), inplace=True)
    return data_frame


def get_data_census_g():
    '''Census Gross National Product Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('F0003', 'F0004',)
    data_frame = pd.concat(
        [fetch_usa_census(ARCHIVE_NAME, series_id)
         for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    data_frame = data_frame[data_frame.index.get_loc(1889):]
    return data_frame.div(data_frame.iloc[0, :]).mul(100)


def get_data_census_i():
    '''Census Foreign Trade Series'''
    # =========================================================================
    # TODO: Divide Into Three Functions
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('U0001', 'U0008',)
    data_frame_a = pd.concat(
        [fetch_usa_census(ARCHIVE_NAME, series_id)
         for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    SERIES_IDS = ('U0187', 'U0188', 'U0189',)
    data_frame_b = pd.concat(
        [fetch_usa_census(ARCHIVE_NAME, series_id)
         for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    SERIES_IDS = (
        'U0319', 'U0320', 'U0321', 'U0322', 'U0323', 'U0325', 'U0326',
        'U0327', 'U0328', 'U0330', 'U0331', 'U0332', 'U0333', 'U0334',
        'U0337', 'U0338', 'U0339', 'U0340', 'U0341', 'U0343', 'U0344',
        'U0345', 'U0346', 'U0348', 'U0349', 'U0350', 'U0351', 'U0352',
    )
    data_frame_c = pd.concat(
        [fetch_usa_census(ARCHIVE_NAME, series_id)
         for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    data_frame_c['exports'] = data_frame_c.loc[:,
                                               SERIES_IDS[:len(SERIES_IDS) // 2]].sum(1)
    data_frame_c['imports'] = data_frame_c.loc[:,
                                               SERIES_IDS[len(SERIES_IDS) // 2:]].sum(1)
    return data_frame_a, data_frame_b, data_frame_c


def get_data_census_j():
    '''Census Money Supply Aggregates'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('X0410', 'X0414', 'X0415',)
    data_frame = pd.concat(
        [fetch_usa_census(ARCHIVE_NAME, series_id)
         for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    data_frame = data_frame.div(
        data_frame.iloc[data_frame.index.get_loc(1915), :]).mul(100)
    return data_frame, data_frame.index.get_loc(1915)


def get_data_cobb_douglas_deflator():
    '''Fixed Assets Deflator, 2009=100'''
    # =========================================================================
    # TODO: Change Name; Be Careful with Usage Due to Change in Behavior
    # =========================================================================
    # =========================================================================
    # Combine L2, L15, E7, E23, E40, E68 & P107/P110
    # =========================================================================
    # =========================================================================
    # Bureau of Labor Statistics: Data Not Used As It Covers Only Years of 1998--2017
    # =========================================================================
    # =========================================================================
    # Results:
    # HSUS 1949 - 'L0036' Offset with HSUS 1975 - 'E0183'
    # HSUS 1949 - 'L0038' Offset with HSUS 1975 - 'E0184'
    # HSUS 1949 - 'L0039' Offset with HSUS 1975 - 'E0185'
    # HSUS 1975 - 'E0052' Offset With HSUS 1949 - 'L0002
    # =========================================================================
    # =========================================================================
    # Cost-Of-Living Indexes
    # =========================================================================
    # =========================================================================
    # E0183: Federal Reserve Bank, 1913=100
    # E0184: Burgess, 1913=100
    # E0185: Douglas, 1890-99=100
    # =========================================================================
    # =========================================================================
    # Bureau of the Census
    # =========================================================================
    # =========================================================================
    # Correlation Test:
    # `data_frame.corr(method='kendall')`
    # `data_frame.corr(method='pearson')`
    # `data_frame.corr(method='spearman')`
    # Correlation Test Result: kendall & pearson & spearman: L2, L15, E7, E23, E40, E68
    # =========================================================================
    ARCHIVE_NAMES = (
        'dataset_usa_census1949.zip',
        'dataset_usa_census1949.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
    )
    CS_SERIES_IDS = (
        'L0002',
        'L0015',
        'E0007',
        'E0023',
        'E0040',
        'E0068',
        'P0107',
        'P0110',
    )
    # =========================================================================
    # Bureau of Economic Analysis
    # =========================================================================
    URL = 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    BE_SERIES_IDS = (
        # =====================================================================
        # Fixed Assets: k1n31gd1es00, 1925--2019, Table 4.1. Current-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'k1n31gd1es00',
        # =====================================================================
        # Fixed Assets: kcn31gd1es00, 1925--2019, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'kcn31gd1es00',
        # =====================================================================
        # Not Used: Fixed Assets: k3n31gd1es00, 1925--2019, Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # Not Used: Fixed Assets: k3ntotl1si00, 1925--2019, Table 2.3. Historical-Cost Net Stock of Private Fixed Assets, Equipment, Structures, and Intellectual Property Products by Type
        # Not Used: mcn31gd1es00, 1925--2019, Table 4.5. Chain-Type Quantity Indexes for Depreciation of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # Not Used: mcntotl1si00, 1925--2019, Table 2.5. Chain-Type Quantity Indexes for Depreciation of Private Fixed Assets, Equipment, Structures, and Intellectual Property Products by Type
        # =====================================================================
        'k3n31gd1es00',
        'k3ntotl1si00',
        'mcn31gd1es00',
        'mcntotl1si00',
    )
    data_frame = pd.concat(
        [
            pd.concat(
                [
                    fetch_usa_census(**{
                        'archive_name': archive_name,
                        'series_id': series_id,
                    })
                    for archive_name, series_id in zip(ARCHIVE_NAMES[:-2], CS_SERIES_IDS[:-2])
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    fetch_usa_census(**{
                        'archive_name': archive_name,
                        'series_id': series_id,
                    })
                    for archive_name, series_id in zip(ARCHIVE_NAMES[-2:], CS_SERIES_IDS[-2:])
                ],
                axis=1,
                sort=True
            ).truncate(before=1885),
        ],
        axis=1,
        sort=True
    )
    # =========================================================================
    # Bureau of Economic Analysis
    # =========================================================================
    web_data = fetch_usa_bea_from_url(URL)
    data_frame = pd.concat(
        [
            # =================================================================
            # Bureau of the Census
            # =================================================================
            data_frame,
            # =================================================================
            # Bureau of Economic Analysis
            # =================================================================
            pd.concat(
                [
                    fetch_usa_bea_from_loaded(**{
                        'data_frame': web_data,
                        'series_id': series_id,
                    }
                    )
                    for series_id in BE_SERIES_IDS[:2]
                ],
                axis=1,
                sort=True
            ),
            # =================================================================
            # Federal Reserve Board Data
            # =================================================================
            get_data_usa_frb_fa_def(),
        ],
        axis=1,
        sort=True
    ).truncate(before=1794)
    data_frame['fa_def_cs'] = data_frame.loc[:, CS_SERIES_IDS[-2]].div(
        data_frame.loc[:, CS_SERIES_IDS[-1]])
    data_frame['ppi_bea'] = data_frame.loc[:, BE_SERIES_IDS[0]].div(
        data_frame.loc[:, BE_SERIES_IDS[1]]).div(data_frame.loc[2012, BE_SERIES_IDS[0]]).mul(100)
    data_frame.drop(
        [*CS_SERIES_IDS[-2:], *BE_SERIES_IDS[:2]],
        axis=1,
        inplace=True
    )
    # =========================================================================
    # Strip Deflators
    # =========================================================================
    for _ in range(data_frame.shape[1]):
        data_frame.iloc[:, _] = strip_cumulated_deflator(
            data_frame.iloc[:, [_]]
        )
    data_frame['def_mean'] = data_frame.mean(axis=1)
    return data_frame.iloc[:, [-1]].dropna()


def get_data_cobb_douglas(series_number: int = 3) -> pd.DataFrame:
    '''Original Cobb--Douglas Data Preprocessing Extension'''
    ARCHIVE_NAMES = (
        'dataset_usa_cobb-douglas.zip',
        'dataset_usa_cobb-douglas.zip',
        'dataset_usa_census1949.zip',
        'dataset_usa_census1949.zip',
        'dataset_douglas.zip',
    )
    SERIES_IDS = {
        # =====================================================================
        # Cobb C.W., Douglas P.H. Capital Series: Total Fixed Capital in 1880 dollars (4)
        # =====================================================================
        'CDT2S4': 'capital',
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        'CDT3S1': 'labor',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014': 'product',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013': 'product_nber',
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01': 'product_rev',
    }
    FUNCTIONS = (
        fetch_usa_classic,
        fetch_usa_classic,
        fetch_usa_census,
        fetch_usa_census,
        fetch_usa_classic,
    )
    data_frame = pd.concat(
        [
            partial(func, **{'archive_name': archive_name,
                             'series_id': series_id})()
            for archive_name, series_id, func in zip(ARCHIVE_NAMES, SERIES_IDS.keys(), FUNCTIONS)
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    data_frame.columns = SERIES_IDS.values()
    return data_frame.div(data_frame.iloc[0, :]).iloc[:, range(series_number)]


def get_data_cobb_douglas_extension_capital() -> pd.DataFrame:
    # =========================================================================
    # Existing Capital Dataset
    # =========================================================================
    df = get_data_usa_capital()
    # =========================================================================
    # Convert Capital Series into Current (Historical) Prices
    # =========================================================================
    df['nominal_cbb_dg'] = df.iloc[:, 0].mul(
        df.iloc[:, 2]).div(df.iloc[:, 1]).div(1000)
    df['nominal_census'] = df.iloc[:, 5].mul(df.iloc[:, 7]).div(df.iloc[:, 6])
    df['nominal_dougls'] = df.iloc[:, 0].mul(
        df.iloc[:, 9]).div(df.iloc[:, 1]).div(1000)
    df['nominal_kndrck'] = df.iloc[:, 5].mul(
        df.iloc[:, 8]).div(df.iloc[:, 6]).div(1000)
    df.iloc[:, -1] = df.iloc[:, -1].mul(
        df.loc[1929, df.columns[6]]).div(df.loc[1929, df.columns[5]])
    # =========================================================================
    # Douglas P.H. -- Kendrick J.W. (Blended) Series
    # =========================================================================
    df['nominal_doug_kndrck'] = df.iloc[:, -2:].mean(axis=1)
    # =========================================================================
    # Cobb C.W., Douglas P.H. -- FRB (Blended) Series
    # =========================================================================
    df['nominal_cbb_dg_frb'] = df.iloc[:, [10, 12]].mean(axis=1)
    # =========================================================================
    # Capital Structure Series: `Cobb C.W., Douglas P.H. -- FRB (Blended) Series` to `Douglas P.H. -- Kendrick J.W. (Blended) Series`
    # =========================================================================
    df['struct_ratio'] = df.iloc[:, -1].div(df.iloc[:, -2])
    # =========================================================================
    # Filling the Gaps within Capital Structure Series
    # =========================================================================
    df.loc[1899:, df.columns[-1]].fillna(0.275, inplace=True)
    df.loc[:, df.columns[-1]].fillna(df.loc[1899, df.columns[-1]], inplace=True)
    # =========================================================================
    # Patch Series `Douglas P.H. -- Kendrick J.W. (Blended) Series` Multiplied by `Capital Structure Series`
    # =========================================================================
    df['nominal_patch'] = df.iloc[:, -3].mul(df.iloc[:, -1])
    # =========================================================================
    # `Cobb C.W., Douglas P.H. -- FRB (Blended) Series` Patched with `Patch Series`
    # =========================================================================
    df['nominal_extended'] = df.iloc[:, -3::2].mean(axis=1)
    return df.iloc[:, [-1]].dropna(axis=0)


def get_data_cobb_douglas_extension_labor():
    '''Manufacturing Laborers` Series Comparison'''
    # =========================================================================
    # TODO: Bureau of Labor Statistics
    # TODO: Federal Reserve Board
    # =========================================================================
    URL = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    FILE_NAME = 'dataset_usa_reference_ru_kurenkov_yu_v.csv'
    ARCHIVE_NAMES = (
        'dataset_usa_cobb-douglas.zip',
        'dataset_usa_census1949.zip',
        'dataset_usa_census1949.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_kendrick.zip',
    )
    SERIES_IDS = (
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        'CDT3S1',
        # =====================================================================
        # Census Bureau 1949, D69
        # =====================================================================
        'D0069',
        # =====================================================================
        # Census Bureau 1949, J4
        # =====================================================================
        'J0004',
        # =====================================================================
        # Census Bureau 1975, D130
        # =====================================================================
        'D0130',
        # =====================================================================
        # Census Bureau 1975, P5
        # =====================================================================
        'P0005',
        # =====================================================================
        # Census Bureau 1975, P62
        # =====================================================================
        'P0062',
        # =====================================================================
        # J.W. Kendrick, Productivity Trends in the United States, Table D-II, `Persons Engaged` Column, pp. 465--466
        # =====================================================================
        'KTD02S02',
    )
    FUNCTIONS = (
        fetch_usa_classic,
        fetch_usa_census,
        fetch_usa_census,
        fetch_usa_census,
        fetch_usa_census,
        fetch_usa_census,
        fetch_usa_classic,
    )
    data_frame = pd.concat(
        [
            partial(func, **{'archive_name': archive_name,
                             'series_id': series_id})()
            for archive_name, series_id, func in zip(ARCHIVE_NAMES, SERIES_IDS, FUNCTIONS)
        ],
        axis=1,
        sort=True
    )
    # =========================================================================
    # Bureau of Economic Analysis, H4313C & J4313C & A4313C & N4313C
    # =========================================================================
    _data_frame = fetch_usa_bea_from_url(URL)
    SERIES_IDS = (
        'H4313C',
        'J4313C',
        'A4313C',
        'N4313C',
    )
    data_nipa = pd.concat(
        [
            fetch_usa_bea_from_loaded(_data_frame, series_id) for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    data_nipa['bea_mfg_labor'] = data_nipa.mean(axis=1)
    data_nipa = data_nipa.iloc[:, [-1]]
    data_frame = pd.concat(
        [
            data_frame,
            data_nipa,
            # =================================================================
            # Yu.V. Kurenkov
            # =================================================================
            pd.read_csv(FILE_NAME, index_col=0, usecols=[0, 2]),
        ],
        axis=1, sort=True
    )
    data_frame.drop(data_frame[data_frame.index < 1889].index, inplace=True)
    data_frame.iloc[:, 6] = data_frame.iloc[:, 6].mul(data_frame.iloc[data_frame.index.get_loc(
        1899), 0]).div(data_frame.iloc[data_frame.index.get_loc(1899), 6])
    data_frame['labor'] = data_frame.iloc[:, [0, 1, 3, 6, 7, 8]].mean(axis=1)
    return data_frame.iloc[:, [-1]]


def get_data_cobb_douglas_extension_product():
    ARCHIVE_NAMES = (
        'dataset_usa_census1949.zip',
        'dataset_usa_census1949.zip',
        'dataset_usa_census1975.zip',
        'dataset_douglas.zip',
    )
    SERIES_IDS = (
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014',
        # =====================================================================
        # Bureau of the Census, 1975, Page 667, P17: Edwin Frickey Index of Manufacturing Production
        # =====================================================================
        'P0017',
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01',
    )
    FUNCTIONS = (
        fetch_usa_census,
        fetch_usa_census,
        fetch_usa_census,
        fetch_usa_classic,
    )
    data_frame = pd.concat(
        [
            partial(func, **{'archive_name': archive_name,
                             'series_id': series_id})()
            for archive_name, series_id, func in zip(ARCHIVE_NAMES, SERIES_IDS, FUNCTIONS)
        ],
        axis=1,
        sort=True
    )
    FILE_NAME = 'dataset_usa_davis-j-h-ip-total.xls'
    data_frame = pd.concat(
        [
            data_frame,
            # =================================================================
            # Joseph H. Davis Production Index
            # =================================================================
            pd.read_excel(FILE_NAME, header=None, names=[
                'period', 'davis_index'], index_col=0, skiprows=5),
            # =================================================================
            # Federal Reserve, AIPMASAIX
            # =================================================================
            get_data_usa_frb_ip(),
        ],
        axis=1,
        sort=True
    )
    data_frame.iloc[:, 1] = data_frame.iloc[:, 1].div(
        data_frame.iloc[data_frame.index.get_loc(1899), 1]).mul(100)
    data_frame.iloc[:, 4] = data_frame.iloc[:, 4].div(
        data_frame.iloc[data_frame.index.get_loc(1899), 4]).mul(100)
    data_frame.iloc[:, 5] = data_frame.iloc[:, 5].div(
        data_frame.iloc[data_frame.index.get_loc(1939), 5]).mul(100)
    data_frame['fused_classic'] = data_frame.iloc[:, range(5)].mean(axis=1)
    data_frame.iloc[:, -1] = data_frame.iloc[:, -1].div(
        data_frame.iloc[data_frame.index.get_loc(1939), -1]).mul(100)
    data_frame['fused'] = data_frame.iloc[:, -2:].mean(axis=1)
    return data_frame.iloc[:, [-1]]


def get_data_combined():
    '''Most Up-To-Date Version'''
    # =========================================================================
    # TODO: Refactor It
    # =========================================================================
    URL = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    _data = fetch_usa_bea_from_url(URL)
    SERIES_IDS = (
        'A006RC',
        'A006RD',
        'A008RC',
        'A008RD',
        'A032RC',
        'A191RA',
        'A191RC',
        'A191RX',
        'W170RC',
        'W170RX',
    )
    _data_nipa = pd.concat(
        [
            fetch_usa_bea_from_loaded(_data, _id) for _id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    SERIES_IDS = (
        'H4313C',
        'J4313C',
        'A4313C',
        'N4313C',
    )
    _labor_frame = pd.concat(
        [
            fetch_usa_bea_from_loaded(_data, _id) for _id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    _labor_frame['mfg_labor'] = _labor_frame.mean(axis=1)
    _labor_frame = _labor_frame.iloc[:, [-1]]
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
    )
    WB_NAMES = (
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH_NAME, SERIES_ID = ('51000 Ann', 'K100701',)
    # =========================================================================
    # Fixed Assets Series: K100701, 1951--2013
    # =========================================================================
    _data_sfat = pd.concat(
        [
            fetch_usa_bea(_archive, _wb, SH_NAME, SERIES_ID) for _archive, _wb in zip(ARCHIVE_NAMES, WB_NAMES)
        ],
        sort=True
    ).drop_duplicates()
    # =========================================================================
    # US BEA Fixed Assets Series Tests
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WB_NAMES = (
        'Section1ALL_xls.xls',
        'Section2ALL_xls.xls',
    )
    SH_NAMES = (
        '105 Ann',
        '106 Ann',
        '101 Ann',
        '203 Ann',
        '202 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Investment in Fixed Assets, Private, i3ptotl1es000, 1901--2016
        # =====================================================================
        'i3ptotl1es000',
        # =====================================================================
        # Chain-Type Quantity Index for Investment in Fixed Assets, Private, icptotl1es000, 1901--2016
        # =====================================================================
        'icptotl1es000',
        # =====================================================================
        # Current-Cost Net Stock of Fixed Assets, Private, k1ptotl1es000, 1925--2016
        # =====================================================================
        'k1ptotl1es000',
        # =====================================================================
        # Historical-Cost Net Stock of Private Fixed Assets, Private Fixed Assets, k3ptotl1es000, 1925--2016
        # =====================================================================
        'k3ptotl1es000',
        # =====================================================================
        # Chain-Type Quantity Indexes for Net Stock of Fixed Assets, Private, kcptotl1es000, 1925--2016
        # =====================================================================
        'kcptotl1es000',
    )
    _data_sfat_ = pd.concat(
        [
            fetch_usa_bea(ARCHIVE_NAME, _wb, _sh, _id) for _wb, _sh, _id in zip(
                tuple(WB_NAMES[_ // 3] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
        ],
        axis=1,
        sort=True
    )
    FILE_NAME = 'dataset_usa_0025_p_r.txt'
    return pd.concat(
        [
            _data_nipa,
            _labor_frame,
            _data_sfat,
            _data_sfat_,
            get_data_usa_frb_ms(),
            get_data_usa_frb_ms(),
            get_data_usa_frb_ms(),
            pd.read_csv(FILE_NAME, index_col=0),
        ],
        axis=1,
        sort=True
    )


def get_data_combined_archived():
    '''Version: 02 December 2013'''
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH_NAMES = (
        '10103 Ann',
        '10105 Ann',
        '10105 Ann',
        '10105 Ann',
        '10106 Ann',
        '10109 Ann',
        '10109 Ann',
        '10705 Ann',
        '50100 Ann',
        '50206 Ann',
        '50900 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Gross Domestic Product, 2005=100: B191RA3, 1929--2012
        # =====================================================================
        'B191RA3',
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Gross private domestic investment -- Nonresidential: A008RC1, 1929--2012
        # =====================================================================
        'A008RC1',
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        'A191RC1',
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        'A191RX1',
        # =====================================================================
        # Implicit Price Deflator Series: A006RD3, 1929--2012
        # =====================================================================
        'A006RD3',
        # =====================================================================
        # Implicit Price Deflator -- Gross private domestic investment -- Nonresidential: A008RD3, 1929--2012
        # =====================================================================
        'A008RD3',
        # =====================================================================
        # Nominal National income Series: A032RC1, 1929--2011
        # =====================================================================
        'A032RC1',
        # =====================================================================
        # Gross Domestic Investment, W170RC1, 1929--2012
        # =====================================================================
        'W170RC1',
        # =====================================================================
        # Gross Domestic Investment, W170RX1, 1967--2011
        # =====================================================================
        'W170RX1',
        # =====================================================================
        # `K160491` Replaced with `K10070` in `get_data_combined()`
        # Fixed Assets Series: K160491, 1951--2011
        # =====================================================================
        'K160491',
    )
    _data_nipa = pd.concat(
        [
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVE_NAMES[0], _wb, _sh, _id) for _wb, _sh, _id in zip(
                        tuple(WB_NAMES[2*(_ // 8)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVE_NAMES[1], _wb, _sh, _id) for _wb, _sh, _id in zip(
                        tuple(WB_NAMES[1 + 2*(_ // 8)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
        ],
        sort=True
    ).drop_duplicates()
    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2012-08-15-SectionAll_xls.zip'
    WB_NAMES = (
        'Section1ALL_xls.xls',
        'Section2ALL_xls.xls',
    )
    SH_NAMES = (
        '105 Ann',
        '106 Ann',
        '101 Ann',
        '203 Ann',
        '202 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Investment in Fixed Assets and Consumer Durable Goods, Private, i3ptotl1es000, 1901--2011
        # =====================================================================
        'i3ptotl1es000',
        # =====================================================================
        # Chain-Type Quantity Indexes for Investment in Fixed Assets and Consumer Durable Goods, Private, icptotl1es000, 1901--2011
        # =====================================================================
        'icptotl1es000',
        # =====================================================================
        # Current-Cost Net Stock of Fixed Assets and Consumer Durable Goods, Private, k1ptotl1es000, 1925--2011
        # =====================================================================
        'k1ptotl1es000',
        # =====================================================================
        # Historical-Cost Net Stock of Private Fixed Assets, Equipment and Software, and Structures by Type, Private fixed assets, k3ptotl1es000, 1925--2011
        # =====================================================================
        'k3ptotl1es000',
        # =====================================================================
        # Chain-Type Quantity Indexes for Net Stock of Private Fixed Assets, Equipment and Software, and Structures by Type, Private fixed assets, kcptotl1es000, 1925--2011
        # =====================================================================
        'kcptotl1es000',
    )
    _data_sfat = pd.concat(
        [
            fetch_usa_bea(ARCHIVE_NAME, _wb, _sh, _id) for _wb, _sh, _id in zip(
                tuple(WB_NAMES[_ // 3] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
        ],
        axis=1,
        sort=True
    )
    FILE_NAMES = (
        'dataset_usa_0022_m1.txt',
        'dataset_usa_0025_p_r.txt',
    )
    _data = pd.concat(
        [
            pd.read_csv(file_name, index_col=0) for file_name in FILE_NAMES
        ],
        axis=1,
        sort=True
    )
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_ID = 'X0414'
    data_frame = pd.concat(
        [_data_nipa,
         _data_sfat,
         _data,
         # ====================================================================
         # Labor Series
         # ====================================================================
         get_data_usa_bea_labor_mfg(),
         fetch_usa_census(ARCHIVE_NAME, SERIES_ID),
         get_data_usa_frb_ms()],
        axis=1,
        sort=True
    )
    return data_frame.iloc[:, [0, 1, 2, 3, 4, 7, 5, 6, 18, 9, 10, 8, 11, 12, 13, 14, 15, 16, 19, 20, 17, ]]


def get_data_common_archived():
    """Data Fetch"""
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH_NAMES = (
        '10105 Ann',
        '10106 Ann',
        '10109 Ann',
        '11200 Ann',
        '51000 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1, 1929--2014
        # =====================================================================
        'A191RC1',
        # =====================================================================
        # Real Gross Domestic Product Series: A191RX1, 1929--2014, 2009=100
        # =====================================================================
        'A191RX1',
        # =====================================================================
        # Deflator Gross Domestic Product, A191RD3, 1929--2014, 2009=100
        # =====================================================================
        'A191RD3',
        # =====================================================================
        # National Income: A032RC1, 1929--2014
        # =====================================================================
        'A032RC1',
        # =====================================================================
        # Fixed Assets Series: K100021, 1951--2014
        # =====================================================================
        'K100021',
    )
    _data_nipa = pd.concat(
        [
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVE_NAMES[0], _wb, _sh, _id) for _wb, _sh, _id in zip(
                        tuple(WB_NAMES[2*(_ // 4)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVE_NAMES[1], _wb, _sh, _id) for _wb, _sh, _id in zip(
                        tuple(WB_NAMES[1 + 2*(_ // 4)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
        ],
        sort=True
    ).drop_duplicates()
    _data_nipa.loc[:, [SERIES_IDS[2]]] = _data_nipa.loc[:, [SERIES_IDS[2]]].rdiv(100)

    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WB_NAMES = (
        'Section2ALL_xls.xls',
        'Section4ALL_xls.xls',
    )
    SH_NAMES = (
        '201 Ann',
        '203 Ann',
        '401 Ann',
        '403 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Fixed Assets Series: k1ntotl1si000, 1925--2016
        # =====================================================================
        'k1ntotl1si000',
        # =====================================================================
        # Fixed Assets Series: k3ntotl1si000, 1925--2016
        # =====================================================================
        'k3ntotl1si000',
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es000, 1925--2016
        # =====================================================================
        'k1n31gd1es000',
        # =====================================================================
        # Fixed Assets Series: k3n31gd1es000, 1925--2016
        # =====================================================================
        'k3n31gd1es000',
    )
    _data_sfat = pd.concat(
        [
            fetch_usa_bea(ARCHIVE_NAME, _wb, _sh, _id) for _wb, _sh, _id in zip(
                tuple(WB_NAMES[_ // 2] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
        ],
        axis=1,
        sort=True
    )

    return pd.concat(
        [_data_nipa,
         _data_sfat,
         get_data_usa_bea_labor_mfg(),
         # =====================================================================
         # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
         # =====================================================================
         get_data_usa_frb_cu(), ],
        axis=1,
        sort=True)


def get_data_douglas():
    '''Douglas Data Preprocessing'''
    ARCHIVE_NAME = 'dataset_douglas.zip'
    SERIES_IDS = ('DT19AS03', 'DT19AS02', 'DT19AS01',)
    data_frame = pd.concat(
        [fetch_usa_classic(ARCHIVE_NAME, series_id)
         for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    return data_frame.div(data_frame.iloc[data_frame.index.get_loc(1899), :])


def get_data_usa_sahr_infcf():
    '''Retrieve Yearly Price Rates from `dataset_usa_infcf16652007.zip`'''
    ARCHIVE_NAME = 'dataset_usa_infcf16652007.zip'
    data_frame = pd.read_csv(ARCHIVE_NAME, usecols=range(4, 7))
    result_frame = pd.DataFrame()
    # =========================================================================
    # Retrieve First 14 Series
    # =========================================================================
    for series_id in data_frame.iloc[:, 0].unique()[:14]:
        chunk = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
        chunk.columns = [chunk.columns[0],
                         series_id.replace(' ', '_').lower()]
        chunk.set_index(chunk.columns[0], inplace=True)
        chunk = chunk.rdiv(1)
        chunk = -price_inverse_single(chunk)
        result_frame = pd.concat([result_frame, chunk], axis=1, sort=True)
    result_frame['cpiu_fused'] = result_frame.mean(axis=1)
    return result_frame.iloc[:, [-1]].dropna(axis=0)


def get_data_local():
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH_NAMES = (
        '10105 Ann',
        '10105 Ann',
        '10106 Ann',
        '50900 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        'A191RC1',
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        'A191RX1',
        # =====================================================================
        # `K160491` Replaced with `K10070` in `get_data_combined()`
        # Fixed Assets Series: K160491, 1951--2011
        # =====================================================================
        'K160491',
    )
    _data_nipa = pd.concat(
        [
            pd.concat(
                [fetch_usa_bea(ARCHIVE_NAMES[0], _wb, _sh, _id)
                 for _wb, _sh, _id in zip(tuple(WB_NAMES[2*(_ // 3)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)],
                axis=1,
                sort=True,
            ),
            pd.concat(
                [fetch_usa_bea(ARCHIVE_NAMES[1], _wb, _sh, _id)
                 for _wb, _sh, _id in zip(tuple(WB_NAMES[1 + 2*(_ // 3)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)],
                axis=1,
                sort=True,
            ),
        ],
        sort=True).drop_duplicates()
    return pd.concat(
        [
            _data_nipa,
            get_data_usa_bea_labor_mfg(),
            get_data_usa_frb_cu(),
        ],
        axis=1,
        sort=True
    )


def get_dataset() -> pd.DataFrame:
    '''Data Fetch'''
    # =========================================================================
    # TODO: Update Accodring to Change in get_data_cobb_douglas_deflator()
    # =========================================================================
    capital = pd.concat(
        [
            # =================================================================
            # Data Fetch for Capital
            # =================================================================
            get_data_cobb_douglas_extension_capital(),
            # =================================================================
            # Data Fetch for Capital Deflator
            # =================================================================
            get_data_cobb_douglas_deflator(),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    capital['capital_real'] = capital.iloc[:, 0].div(capital.iloc[:, 1])
    data_frame = pd.concat(
        [
            capital.iloc[:, [-1]],
            # =================================================================
            # Data Fetch for Labor
            # =================================================================
            get_data_cobb_douglas_extension_labor(),
            # =================================================================
            # Data Fetch for Product
            # =================================================================
            get_data_cobb_douglas_extension_product(),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    return data_frame.div(data_frame.iloc[0, :])


def get_data_updated():
    URL = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    _data = fetch_usa_bea_from_url(URL)
    SERIES_IDS = (
        'A006RC',
        'A006RD',
        'A191RC',
        'A191RX',
    )
    _data_nipa = pd.concat(
        [
            fetch_usa_bea_from_loaded(_data, _id) for _id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WB_NAME = 'Section4ALL_xls.xls'
    SH_NAMES = (
        '403 Ann',
        '402 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Not Used: Fixed Assets: k3n31gd1es000, 1925--2016, Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'k3n31gd1es000',
        # =====================================================================
        # Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'kcn31gd1es000',
    )
    _data_sfat = pd.concat(
        [
            fetch_usa_bea(ARCHIVE_NAME, WB_NAME, _sh, _id) for _sh, _id in zip(SH_NAMES, SERIES_IDS)
        ],
        axis=1,
        sort=True
    )
    _data = pd.concat(
        [
            _data_nipa,
            _data_sfat,
        ],
        axis=1,
        sort=True
    )
    # =========================================================================
    # Investment, 2012=100
    # =========================================================================
    _data['_inv'] = _data.loc[:, 'A006RD'].mul(
        _data.loc[2012, 'A006RC']).div(100)
    # =========================================================================
    # Capital, 2012=100
    # =========================================================================
    _data['_cap'] = _data.loc[:, 'kcn31gd1es000'].mul(
        _data.loc[2009, 'k3n31gd1es000']).mul(1000).div(100)
    # =========================================================================
    # Capital Retirement Ratio
    # =========================================================================
    _data['_ratio_mu'] = _data.iloc[:, -
                               2].mul(1).sub(_data.iloc[:, -1].shift(-1)).div(_data.iloc[:, -1]).add(1)
    return (
        _data.loc[:, ['_inv', 'A191RX', '_cap', '_ratio_mu']].dropna(axis=0),
        _data.loc[:, ['_ratio_mu']].dropna(axis=0),
        _data.index.get_loc(2012)
    )


def get_data_usa_bea_labor():
    # =========================================================================
    # Labor Series: A4601C0, 1929--2011
    # =========================================================================
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section6ALL_Hist.xls',
        'Section6ALL_Hist.xls',
        'Section6all_xls.xls',
        'Section6all_xls.xls',
        'Section6all_xls.xls',
    )
    SH_NAMES = (
        '60800A Ann',
        '60800B Ann',
        '60800B Ann',
        '60800C Ann',
        '60800D Ann',
    )
    SERIES_ID = 'A4601C0'
    data_frame = pd.concat(
        [fetch_usa_bea(archive_name, wb, sh, SERIES_ID)
         for archive_name, wb, sh in zip(ARCHIVE_NAMES, WB_NAMES, SH_NAMES)],
        axis=1,
        sort=True)
    data_frame[SERIES_ID] = data_frame.mean(axis=1)
    return data_frame.iloc[:, [-1]].dropna(axis=0)


def get_data_usa_bea_labor_mfg():
    # =========================================================================
    # Manufacturing Labor Series: H4313C0, 1929--1948
    # Manufacturing Labor Series: J4313C0, 1948--1969
    # Manufacturing Labor Series: J4313C0, 1969--1987
    # Manufacturing Labor Series: A4313C0, 1987--2000
    # Manufacturing Labor Series: N4313C0, 1998--2011
    # =========================================================================
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section6ALL_Hist.xls',
        'Section6ALL_Hist.xls',
        'Section6all_xls.xls',
        'Section6all_xls.xls',
        'Section6all_xls.xls',
    )
    SH_NAMES = (
        '60500A Ann',
        '60500B Ann',
        '60500B Ann',
        '60500C Ann',
        '60500D Ann',
    )
    SERIES_IDS = (
        'H4313C0',
        'J4313C0',
        'J4313C0',
        'A4313C0',
        'N4313C0',
    )
    data_frame = pd.concat(
        [fetch_usa_bea(archive_name, wb, sh, _id)
         for archive_name, wb, sh, _id in zip(ARCHIVE_NAMES, WB_NAMES, SH_NAMES, SERIES_IDS)],
        axis=1,
        sort=True)
    data_frame['mfg_labor'] = data_frame.mean(axis=1)
    return data_frame.iloc[:, [-1]].dropna(axis=0)


def get_data_usa_bls_cpiu():
    '''BLS CPI-U Price Index Fetch'''
    FILE_NAME = 'dataset_usa_bls_cpiai.txt'
    data_frame = pd.read_csv(FILE_NAME,
                             sep='\s+',
                             index_col=0,
                             usecols=range(13),
                             skiprows=16)
    data_frame.rename_axis('period', inplace=True)
    data_frame['mean'] = data_frame.mean(axis=1)
    data_frame['sqrt'] = data_frame.iloc[:, :-1].prod(1).pow(1/12)
    # =========================================================================
    # Tests
    # =========================================================================
    data_frame['mean_less_sqrt'] = data_frame.iloc[:, -
                                                   2].sub(data_frame.iloc[:, -1])
    data_frame['dec_on_dec'] = data_frame.iloc[:, -
                                               3].div(data_frame.iloc[:, -3].shift(1)).sub(1)
    data_frame['mean_on_mean'] = data_frame.iloc[:, -
                                                 4].div(data_frame.iloc[:, -4].shift(1)).sub(1)
    return data_frame.iloc[:, [-1]].dropna(axis=0)


def get_data_usa_capital():
    # =========================================================================
    # Series Not Used - `k3ntotl1si00`
    # =========================================================================
    URL = 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    ARCHIVE_NAME = 'dataset_usa_cobb-douglas.zip'
    SERIES_IDS = (
        # =====================================================================
        # Annual Increase in Terms of Cost Price (1)
        # =====================================================================
        'CDT2S1',
        # =====================================================================
        # Annual Increase in Terms of 1880 dollars (3)
        # =====================================================================
        'CDT2S3',
        # =====================================================================
        # Total Fixed Capital in 1880 dollars (4)
        # =====================================================================
        'CDT2S4',
    )
    data_frame = pd.concat(
        [
            fetch_usa_classic(ARCHIVE_NAME, series_id) for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    _data_frame = fetch_usa_bea_from_url(URL)
    SERIES_IDS = (
        # =====================================================================
        # Fixed Assets: k1n31gd1es00, 1925--2019, Table 4.1. Current-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'k1n31gd1es00',
        # =====================================================================
        # Not Used: Fixed Assets: k3n31gd1es00, 1925--2019, Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'k3n31gd1es00',
    )
    data_frame = pd.concat(
        [
            data_frame,
            pd.concat(
                [
                    fetch_usa_bea_from_loaded(_data_frame, series_id) for series_id in SERIES_IDS
                ],
                axis=1,
                sort=True
            )
        ],
        axis=1,
        sort=True
    )
    ARCHIVE_NAMES = (
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_kendrick.zip',
        'dataset_douglas.zip',
    )
    SERIES_IDS = (
        'P0107',
        'P0110',
        'P0119',
        # =====================================================================
        # Kendrick J.W., Productivity Trends in the United States, Page 320
        # =====================================================================
        'KTA15S08',
        # =====================================================================
        # Douglas P.H., Theory of Wages, Page 332
        # =====================================================================
        'DT63AS01',
    )
    FUNCTIONS = (
        fetch_usa_census,
        fetch_usa_census,
        fetch_usa_census,
        fetch_usa_classic,
        fetch_usa_classic,
    )
    return pd.concat(
        [
            data_frame,
            pd.concat(
                [
                    partial(func, **{'archive_name': archive_name,
                                     'series_id': series_id})()
                    for archive_name, series_id, func in zip(ARCHIVE_NAMES, SERIES_IDS, FUNCTIONS)
                ],
                axis=1,
                sort=True
            ).truncate(before=1869),
            # =================================================================
            # FRB Data
            # =================================================================
            get_data_usa_frb_fa(),
        ],
        axis=1,
        sort=True
    )


def get_data_usa_frb_cu():
    '''Indexed Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
    CAPUTL.B50001.A Fetching'''
    FILE_NAME = 'dataset_usa_frb_g17_all_annual_2013_06_23.csv'
    SERIES_ID = 'CAPUTLB50001A'
    data_frame = pd.read_csv(FILE_NAME, skiprows=1, usecols=range(5, 100))
    data_frame.columns = ['period', *data_frame.columns[1:]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].str.replace(r"[,@\'?\.$%_]",
                                                              '',
                                                              regex=True)
    data_frame = data_frame.set_index(data_frame.columns[0]).transpose()
    data_frame.index = pd.to_numeric(data_frame.index, downcast='integer')
    return data_frame.loc[:, [SERIES_ID]].dropna(axis=0)


def get_data_usa_frb_fa():
    '''Returns Frame of Manufacturing Fixed Assets Series, Billion USD:
    data_frame.iloc[:,0]: Nominal;
    data_frame.iloc[:,1]: Real
    '''
    FILE_NAME = 'dataset_usa_frb_invest_capital.csv'
    data_frame = pd.read_csv(FILE_NAME,
                             skiprows=4, skipfooter=688, engine='python')
    data_frame.columns = ['period', *data_frame.columns[1:]]
    data_frame = data_frame.set_index(data_frame.columns[0]).transpose()
    data_frame.index = data_frame.index.astype(int)
    data_frame['frb_nominal'] = ((data_frame.iloc[:, 1].mul(data_frame.iloc[:, 2]).div(data_frame.iloc[:, 0])).add(
        data_frame.iloc[:, 4].mul(data_frame.iloc[:, 5]).div(data_frame.iloc[:, 3]))).div(1000)
    data_frame['frb_real'] = data_frame.iloc[:, [2, 5]].sum(axis=1).div(1000)
    return data_frame.iloc[:, -2:]


def get_data_usa_frb_fa_def():
    '''Returns Frame of Deflator for Manufacturing Fixed Assets Series, Index:
    result_frame.iloc[:,0]: Deflator
    '''
    FILE_NAME = 'dataset_usa_frb_invest_capital.csv'
    data_frame = pd.read_csv(FILE_NAME,
                             skiprows=4, skipfooter=688, engine='python')
    data_frame.columns = ['period', *data_frame.columns[1:]]
    data_frame = data_frame.set_index(data_frame.columns[0]).transpose()
    data_frame.index = data_frame.index.astype(int)
    data_frame['fa_def_frb'] = (data_frame.iloc[:, [1, 4]].sum(axis=1)).div(
        data_frame.iloc[:, [0, 3]].sum(axis=1))
    return data_frame.iloc[:, [-1]]


def get_data_usa_frb_ip():
    '''Indexed Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018'''
    # =========================================================================
    # TODO: https://www.federalreserve.gov/datadownload/Output.aspx?rel=g17&filetype=zip
    # =========================================================================
    # =========================================================================
    # with ZipFile('FRB_g17.zip', 'r').open('G17_data.xml') as f:
    # =========================================================================
    FILE_NAME = 'dataset_usa_frb_us3_ip_2018_09_02.csv'
    SERIES_ID = 'AIPMA_SA_IX'
    data_frame = pd.read_csv(FILE_NAME, skiprows=7, parse_dates=[0])
    data_frame.columns = [column.strip() for column in data_frame.columns]
    data_frame = data_frame.loc[:, [data_frame.columns[0], SERIES_ID]]
    data_frame['period'] = data_frame.iloc[:, 0].dt.year
    return data_frame.groupby(data_frame.columns[-1]).mean()


def get_data_usa_frb_ms() -> pd.DataFrame:
    ''''Indexed Money Stock Measures (H.6) Series'''
    URL = 'https://www.federalreserve.gov/datadownload/Output.aspx?rel=H6&series=5398d8d1734b19f731aba3105eb36d47&lastobs=&from=01/01/1959&to=12/31/2018&filetype=csv&label=include&layout=seriescolumn'
    data_frame = pd.read_csv(
        io.BytesIO(requests.get(URL).content),
        names=['period', 'm1_m'],
        index_col=0,
        usecols=range(2),
        skiprows=6,
        parse_dates=True,
        thousands=','
    )
    return data_frame.groupby(data_frame.index.year).mean()


def get_data_usa_mcconnel_a():
    SERIES_ID = 'Валовой внутренний продукт, млрд долл. США'
    data_frame = fetch_usa_mcconnel(SERIES_ID)
    return data_frame[data_frame.index.get_loc(1980):]


def get_data_usa_mcconnel_b():
    SERIES_IDS = {
        'Ставка прайм-рейт, %': 'prime_rate',
        'Национальный доход, млрд долл. США': 'A032RC1',
    }
    data_frame = pd.concat([fetch_usa_mcconnel(series_id)
                           for series_id in SERIES_IDS.keys()],
                           axis=1,
                           sort=True)
    data_frame.columns = SERIES_IDS.values()
    return data_frame[data_frame.index.get_loc(1980):]


def get_data_usa_mcconnel_c():
    SERIES_IDS = {
        'Ставка прайм-рейт, %': 'prime_rate',
        'Валовой объем внутренних частных инвестиций, млрд долл. США': 'A006RC1',
    }
    data_frame = pd.concat([fetch_usa_mcconnel(series_id)
                           for series_id in SERIES_IDS.keys()],
                           axis=1,
                           sort=True)
    data_frame.columns = SERIES_IDS.values()
    return data_frame[data_frame.index.get_loc(1980):]


def get_data_usa_xlsm():
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
    )
    SH_NAMES = (
        '10105 Ann',
        '10105 Ann',
        '10106 Ann',
        '10705 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        'A191RC1',
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        'A191RX1',
        # =====================================================================
        # Nominal National income Series: A032RC1, 1929--2011
        # =====================================================================
        'A032RC1',
    )
    _data = pd.concat(
        [
            pd.concat(
                [fetch_usa_bea(ARCHIVE_NAMES[0], WB_NAMES[0], _sh, _id)
                 for _sh, _id in zip(SH_NAMES, SERIES_IDS)],
                axis=1,
                sort=True
            ),
            pd.concat(
                [fetch_usa_bea(ARCHIVE_NAMES[1], WB_NAMES[1], _sh, _id)
                 for _sh, _id in zip(SH_NAMES, SERIES_IDS)],
                axis=1,
                sort=True
            ),
        ],
        sort=True).drop_duplicates()
    FILE_NAME = 'dataset_usa_0025_p_r.txt'
    return pd.concat(
        [
            _data,
            pd.read_csv(FILE_NAME, index_col=0)
        ],
        axis=1,
        sort=True
    )


def get_data_version_a():
    '''Data Fetch Archived
    Returns:
        _data_a: Capital, Labor, Product;
        _data_b: Capital, Labor, Product Adjusted to Capacity Utilisation'''
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
    )
    SH_NAME, SERIES_ID = ('10106 Ann', 'A191RX1')
    KWARGS = {
        'archive_name': 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
        'wb_name': 'Section4ALL_xls.xls',
        'sh_name': '402 Ann',
        'series_id': 'kcn31gd1es000',
    }
    _data_a = pd.concat(
        [
            # =================================================================
            # Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
            # =================================================================
            fetch_usa_bea(**KWARGS),
            # =================================================================
            # Labor
            # =================================================================
            get_data_usa_bea_labor_mfg(),
            # =================================================================
            # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
            # =================================================================
            pd.concat(
                [
                    fetch_usa_bea(_archive_name, _wb, SH_NAME, SERIES_ID) for _archive_name, _wb in zip(ARCHIVE_NAMES, WB_NAMES)
                ],
                sort=True).drop_duplicates(),
        ],
        axis=1, sort=True).dropna(axis=0)
    _data_b = pd.concat(
        [
            # =================================================================
            # Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
            # =================================================================
            fetch_usa_bea(**KWARGS),
            # =================================================================
            # Labor
            # =================================================================
            get_data_usa_bea_labor_mfg(),
            # =================================================================
            # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
            # =================================================================
            pd.concat(
                [
                    fetch_usa_bea(_archive_name, _wb, SH_NAME, SERIES_ID) for _archive_name, _wb in zip(ARCHIVE_NAMES, WB_NAMES)
                ],
                sort=True).drop_duplicates(),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            get_data_usa_frb_cu(),
        ],
        axis=1, sort=True).dropna(axis=0)
    _data_b.iloc[:, 2] = _data_b.iloc[:, 2].div(_data_b.iloc[:, 3]).mul(100)
    return _data_a.div(_data_a.iloc[0, :]), _data_b.div(_data_b.iloc[0, :]).iloc[:, range(3)]


def get_data_version_b():
    """
    Returns
        data_frame_a: Capital, Labor, Product;
        data_frame_b: Capital, Labor, Product;
        data_frame_c: Capital, Labor, Product Adjusted to Capacity Utilisation
    """
    '''Data Fetch Revised'''
    KWARGS = {
        'archive_name': 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
        'wb_name': 'Section4ALL_xls.xls',
        'sh_name': '402 Ann',
        'series_id': 'kcn31gd1es000',
    }
    data_frame_a = pd.concat(
        [
            # =================================================================
            # Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
            # =================================================================
            fetch_usa_bea(**KWARGS),
            # =================================================================
            # Labor
            # =================================================================
            get_data_usa_bea_labor_mfg(),
            # =================================================================
            # Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018
            # =================================================================
            get_data_usa_frb_ip(),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    data_frame_b = data_frame_a[data_frame_a.index.get_loc(1967):]
    data_frame_c = pd.concat(
        [
            # =================================================================
            # Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
            # =================================================================
            fetch_usa_bea(**KWARGS),
            # =================================================================
            # Labor
            # =================================================================
            get_data_usa_bea_labor_mfg(),
            # =================================================================
            # Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018
            # =================================================================
            get_data_usa_frb_ip(),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            get_data_usa_frb_cu(),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    data_frame_c.iloc[:, 2] = data_frame_c.iloc[:, 2].div(
        data_frame_c.iloc[:, 3]).mul(100)
    return (
        data_frame_a.div(data_frame_a.iloc[0, :]),
        data_frame_b.div(data_frame_b.iloc[0, :]),
        data_frame_c.div(data_frame_c.iloc[0, :]).iloc[:, range(3)]
    )


def get_data_version_c():
    """Data Fetch"""
    # =========================================================================
    # Data Fetch for Capital
    # Data Fetch for Capital Deflator
    # =========================================================================
    capital_frame = pd.concat(
        [get_data_cobb_douglas_extension_capital(), get_data_cobb_douglas_deflator()],
        axis=1, sort=True).dropna(axis=0)
    capital_frame['capital_real'] = capital_frame.iloc[:, 0].div(
        capital_frame.iloc[:, 1])
    # =========================================================================
    # Data Fetch for Labor
    # =========================================================================
    labor_frame = get_data_cobb_douglas_extension_labor()
    # =========================================================================
    # Data Fetch for Product
    # =========================================================================
    product_frame = get_data_cobb_douglas_extension_product()
    result_frame = pd.concat(
        [capital_frame.iloc[:, 2], labor_frame, product_frame], axis=1, sort=True).dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame


def get_mean_for_min_std():
    # =========================================================================
    # Determine Year & Mean Value for Base Vectors for Year with Minimum StandardError
    # =========================================================================
    # =========================================================================
    # Base Vector v123355112
    # Base Vector v1235071986
    # Base Vector v2057609
    # Base Vector v2057818
    # Base Vector v2523013
    # =========================================================================
    result = pd.DataFrame()
    FILE_NAME = '/home/alexander/projects/stat_can_lab.xlsx'
    _ = pd.read_excel(FILE_NAME)
    _.set_index(_.columns[0], inplace=True)
    SERIES_IDS = (
        'v123355112',
        'v1235071986',
        'v2057609',
        'v2057818',
        'v2523013',
    )
    for series_id in SERIES_IDS:
        chunk = _.loc[:, [series_id]]
        chunk.dropna(axis=0, inplace=True)
        result = pd.concat([result, chunk], axis=1, sort=False)
    result.dropna(axis=0, inplace=True)
    result['std'] = result.std(axis=1)
    return (result.iloc[:, [-1]].idxmin()[0],
            result.loc[result.iloc[:, [-1]].idxmin()[0], :][:-1].mean())


def get_series_ids(archive_name):
    '''Returns Dictionary for Series from Douglas's & Kendrick's Databases'''
    data_frame = pd.read_csv(archive_name, usecols=[3, 4, ])
    return dict(zip(data_frame.iloc[:, 1], data_frame.iloc[:, 0]))


def kol_zur_filter(data_frame: pd.DataFrame, k: int = None) -> tuple[pd.DataFrame]:
    '''Kolmogorov--Zurbenko Filter
        data_frame.index: Period,
        data_frame.iloc[:, 0]: Series
    '''
    if k is None:
        k = data_frame.shape[0] // 2
    data_frame.reset_index(level=0, inplace=True)
    # =========================================================================
    # DataFrame for Kolmogorov--Zurbenko Filter Results: Odd
    # =========================================================================
    data_frame_o = pd.concat(
        [
            # =================================================================
            # No Period Shift
            # =================================================================
            data_frame,
        ],
        axis=1,
    )
    # =========================================================================
    # DataFrame for Kolmogorov--Zurbenko Filter Results: Even
    # =========================================================================
    data_frame_e = pd.concat(
        [
            # =================================================================
            # Period Shift
            # =================================================================
            data_frame.iloc[:, [0]].rolling(2).mean(),
        ],
        axis=1,
    )
    # =========================================================================
    # DataFrame for Kolmogorov--Zurbenko Filter Residuals: Odd
    # =========================================================================
    residuals_o = pd.concat(
        [
            # =================================================================
            # Period Shift
            # =================================================================
            data_frame.iloc[:, [0]].rolling(2).mean(),
        ],
        axis=1,
    )
    # =========================================================================
    # DataFrame for Kolmogorov--Zurbenko Filter Residuals: Even
    # =========================================================================
    residuals_e = pd.concat(
        [
            # =================================================================
            # No Period Shift
            # =================================================================
            data_frame.iloc[:, [0]],
        ],
        axis=1,
    )
    chunk = data_frame.iloc[:, [1]]
    for _ in range(k):
        chunk = chunk.rolling(2).mean()
        if _ % 2 == 1:
            # =================================================================
            # DataFrame for Kolmogorov--Zurbenko Filter Results: Odd
            # =================================================================
            data_frame_o = pd.concat(
                [
                    data_frame_o,
                    chunk.shift(-((1 + _) // 2)),
                ],
                axis=1,
            )
            data_frame_o.columns = [*data_frame_o.columns[:-1],
                                    f'{data_frame.columns[1]}_{hex(2 + _)}', ]
            # =================================================================
            # DataFrame for Kolmogorov--Zurbenko Filter Residuals: Odd
            # =================================================================
            residuals_o = pd.concat(
                [
                    residuals_o,
                    data_frame_o.iloc[:, [-2]
                                      ].div(data_frame_o.iloc[:, [-2]].shift(1)).sub(1),
                ],
                axis=1,
            )
        else:
            # =================================================================
            # DataFrame for Kolmogorov--Zurbenko Filter Results: Even
            # =================================================================
            data_frame_e = pd.concat(
                [
                    data_frame_e,
                    chunk.shift(-((1 + _) // 2)),
                ],
                axis=1,
            )
            data_frame_e.columns = [*data_frame_e.columns[:-1],
                                    f'{data_frame.columns[1]}_{hex(2 + _)}', ]
            # =================================================================
            # DataFrame for Kolmogorov--Zurbenko Filter Residuals: Even
            # =================================================================
            residuals_e = pd.concat(
                [
                    residuals_e,
                    data_frame_e.iloc[:, [-1]
                                      ].shift(-1).div(data_frame_e.iloc[:, [-1]]).sub(1),
                ],
                axis=1,
            )
    data_frame_o.set_index(data_frame_o.columns[0], inplace=True)
    data_frame_e.set_index(data_frame_e.columns[0], inplace=True)
    residuals_o.set_index(residuals_o.columns[0], inplace=True)
    residuals_e.set_index(residuals_e.columns[0], inplace=True)
    data_frame_o.dropna(how='all', inplace=True)
    data_frame_e.dropna(how='all', inplace=True)
    residuals_o.dropna(how='all', inplace=True)
    residuals_e.dropna(how='all', inplace=True)
    return data_frame_o, data_frame_e, residuals_o, residuals_e


def rolling_mean_filter(data_frame: pd.DataFrame, k: int = None) -> tuple[pd.DataFrame]:
    '''Rolling Mean Filter
        data_frame.index: Period,
        data_frame.iloc[:, 0]: Series
    '''
    if k is None:
        k = data_frame.shape[0] // 2
    data_frame.reset_index(level=0, inplace=True)
    # =========================================================================
    # DataFrame for Rolling Mean Filter Results: Odd
    # =========================================================================
    data_frame_o = pd.concat(
        [
            # =================================================================
            # No Period Shift
            # =================================================================
            data_frame,
        ],
        axis=1,
    )
    # =========================================================================
    # DataFrame for Rolling Mean Filter Results: Even
    # =========================================================================
    data_frame_e = pd.concat(
        [
            # =================================================================
            # Period Shift
            # =================================================================
            data_frame.iloc[:, [0]].rolling(2, center=True).mean(),
        ],
        axis=1,
    )
    # =========================================================================
    # DataFrame for Rolling Mean Filter Residuals: Odd
    # =========================================================================
    residuals_o = pd.concat(
        [
            # =================================================================
            # Period Shift
            # =================================================================
            data_frame.iloc[:, [0]].rolling(2).mean(),
        ],
        axis=1,
    )
    # =========================================================================
    # DataFrame for Rolling Mean Filter Residuals: Even
    # =========================================================================
    residuals_e = pd.concat(
        [
            # =================================================================
            # No Period Shift
            # =================================================================
            data_frame.iloc[:, [0]],
        ],
        axis=1,
    )
    for _ in range(k):
        if _ % 2 == 1:
            # =================================================================
            # DataFrame for Rolling Mean Filter Results: Odd
            # =================================================================
            data_frame_o = pd.concat(
                [
                    data_frame_o,
                    data_frame.iloc[:, [1]].rolling(2 + _, center=True).mean(),
                ],
                axis=1,
            )
            data_frame_o.columns = [*data_frame_o.columns[:-1],
                                    f'{data_frame.columns[1]}_{hex(2 + _)}', ]
            # =================================================================
            # DataFrame for Rolling Mean Filter Residuals: Odd
            # =================================================================
            residuals_o = pd.concat(
                [
                    residuals_o,
                    data_frame_o.iloc[:, [-2]
                                      ].div(data_frame_o.iloc[:, [-2]].shift(1)).sub(1),
                ],
                axis=1,
            )
        else:
            # =================================================================
            # DataFrame for Rolling Mean Filter Results: Even
            # =================================================================
            data_frame_e = pd.concat(
                [
                    data_frame_e,
                    data_frame.iloc[:, [1]].rolling(2 + _, center=True).mean(),
                ],
                axis=1,
            )
            data_frame_e.columns = [*data_frame_e.columns[:-1],
                                    f'{data_frame.columns[1]}_{hex(2 + _)}', ]
            # =================================================================
            # DataFrame for Rolling Mean Filter Residuals: Even
            # =================================================================
            residuals_e = pd.concat(
                [
                    residuals_e,
                    data_frame_e.iloc[:, [-1]
                                      ].shift(-1).div(data_frame_e.iloc[:, [-1]]).sub(1),
                ],
                axis=1,
            )
    data_frame_o.set_index(data_frame_o.columns[0], inplace=True)
    data_frame_e.set_index(data_frame_e.columns[0], inplace=True)
    residuals_o.set_index(residuals_o.columns[0], inplace=True)
    residuals_e.set_index(residuals_e.columns[0], inplace=True)
    data_frame_o.dropna(how='all', inplace=True)
    data_frame_e.dropna(how='all', inplace=True)
    residuals_o.dropna(how='all', inplace=True)
    residuals_e.dropna(how='all', inplace=True)
    return data_frame_o, data_frame_e, residuals_o, residuals_e


def lookup(data_frame):
    for _, series_id in enumerate(data_frame.columns):
        series = sorted(set(data_frame.iloc[:, _]))
        print(f'{series_id:*^50}')
        print(series)


def mean_by_year(data):
    # =========================================================================
    # Process Non-Indexed Flat DataFrame
    # =========================================================================
    # =========================================================================
    # Index Width Check
    # =========================================================================
    width = 0
    for item in data.index:
        width = max(len(f'{item}'), width)
    if width > 4:
        data[['YEAR', 'Q']] = data.index.to_series().str.split('-', expand=True)
        data = data.iloc[:, [1, 0]]
        data = data.apply(pd.to_numeric)
        data = data.groupby('YEAR').mean()
        data.index.rename('REF_DATE', inplace=True)
    return data


def m_spline_ea(df: pd.DataFrame, n_spans: int, knots: tuple[int]) -> tuple[pd.DataFrame, tuple[float]]:
    '''Exponential Spline, Type A
    ================== =================================
    df.iloc[:, 0]      Period
    df.iloc[:, 1]      Target Series
    ================== =================================
    n_spans            Number of Spans
    knots              Interpolation Knots
    ================== =================================
    '''
    _params_a, _params_k, _splined = [], [], []
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using `continue` Statement
    # =========================================================================
    # =========================================================================
    # Coefficient Section
    # =========================================================================
    for j in range(n_spans):
        _params_a.append(
            ((df.iloc[knots[1 + j], 0] - df.iloc[knots[0], 0])*np.log(df.iloc[knots[j], 1]) - (df.iloc[knots[j], 0] -
                                                                                               df.iloc[knots[0], 0])*np.log(df.iloc[knots[1 + j], 1])) / (df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])
        )
        if j == 0:
            _params_k.append(
                (np.log(df.iloc[knots[1 + j], 1]) - np.log(df.iloc[knots[j], 1])) /
                (df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])
            )
        else:
            _params_k.append(
                _params_k[j - 1] + np.log(df.iloc[knots[1 + j], 1]) / (df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0]) -
                (df.iloc[knots[1 + j], 0] - df.iloc[knots[j - 1], 0])*np.log(df.iloc[knots[j], 1]) / ((df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])*(df.iloc[knots[j], 0] - df.iloc[knots[j - 1], 0])) +
                np.log(df.iloc[knots[j - 1], 1]) /
                (df.iloc[knots[j], 0] - df.iloc[knots[j - 1], 0])
            )
        # =====================================================================
        # Splined Section
        # =====================================================================
        if 1 + j == n_spans:
            for i in range(knots[j], 1 + knots[1 + j]):
                _splined.append(
                    np.exp(_params_a[j] + _params_k[j] *
                           (df.iloc[i, 0] - df.iloc[0, 0]))
                )
        else:
            for i in range(knots[j], knots[1 + j]):
                _splined.append(
                    np.exp(_params_a[j] + _params_k[j] *
                           (df.iloc[i, 0] - df.iloc[0, 0]))
                )
    return (
        pd.concat(
            [
                df,
                pd.DataFrame(_splined, columns=['Splined']),
            ],
            axis=1, sort=True),
        tuple(_params_k)
    )


def m_spline_eb(df: pd.DataFrame, n_spans: int, knots: tuple[int]) -> tuple[pd.DataFrame, tuple[float]]:
    '''Exponential Spline, Type B
    ================== =================================
    df.iloc[:, 0]      Period
    df.iloc[:, 1]      Target Series
    ================== =================================
    n_spans            Number of Spans
    knots              Interpolation Knots
    ================== =================================
    '''
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using `continue` Statement
    # =========================================================================
    _params_k, _splined = [], []
    # =========================================================================
    # Coefficient Section
    # =========================================================================
    for j in range(n_spans):
        _params_k.append(
            (np.log(df.iloc[knots[1 + j], 1]) - np.log(df.iloc[knots[j], 1]))/(
                df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])
        )
        # =====================================================================
        # Spline Section
        # =====================================================================
        if 1 + j == n_spans:
            for i in range(knots[j], 1 + knots[1 + j]):
                _splined.append(
                    df.iloc[knots[j], 1]*np.exp(_params_k[j] *
                                                (df.iloc[i, 0] - df.iloc[knots[j], 0]))
                )
        else:
            for i in range(knots[j], knots[1 + j]):
                _splined.append(
                    df.iloc[knots[j], 1]*np.exp(_params_k[j] *
                                                (df.iloc[i, 0] - df.iloc[knots[j], 0]))
                )
    return (
        pd.concat(
            [
                df,
                pd.DataFrame(_splined, columns=['Spline'])
            ],
            axis=1, sort=True),
        tuple(_params_k)
    )


def m_spline_la(df: pd.DataFrame, n_spans: int, knots: tuple[int]) -> tuple[pd.DataFrame, tuple[float]]:
    '''Linear Spline, Type A
    ================== =================================
    df.iloc[:, 0]      Period
    df.iloc[:, 1]      Target Series
    ================== =================================
    n_spans            Number of Spans
    knots              Interpolation Knots
    ================== =================================
    '''
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using `continue` Statement
    # =========================================================================
    _params_a, _params_k, _splined = [], [], []
    for j in range(n_spans):
        _params_a.append(
            ((df.iloc[knots[1 + j], 0] - df.iloc[knots[0], 0])*df.iloc[knots[j], 1] - (df.iloc[knots[j], 0] -
                                                                                   df.iloc[knots[0], 0])*df.iloc[knots[1 + j], 1])/(df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])
        )
        if j == 0:
            _params_k.append(
                (df.iloc[knots[1 + j], 1] - df.iloc[knots[j], 1]) /
                (df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])
            )
        else:
            _params_k.append(
                _params_k[j - 1] + df.iloc[knots[1 + j], 1]/(df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0]) -
                (df.iloc[knots[1 + j], 0] - df.iloc[knots[j - 1], 0])*df.iloc[knots[j], 1]/((df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])*(df.iloc[knots[j], 0] - df.iloc[knots[j - 1], 0])) +
                df.iloc[knots[j - 1], 1] /
                (df.iloc[knots[j], 0] - df.iloc[knots[j - 1], 0])
            )
        if 1 + j == n_spans:
            for i in range(knots[j], 1 + knots[1 + j]):
                _splined.append(
                    _params_a[j] + _params_k[j]*(df.iloc[i, 0] - df.iloc[0, 0])
                )
        else:
            for i in range(knots[j], knots[1 + j]):
                _splined.append(
                    _params_a[j] + _params_k[j]*(df.iloc[i, 0] - df.iloc[0, 0])
                )
    return (
        pd.concat(
            [
                df,
                pd.DataFrame(_splined, columns=['Spline'])
            ],
            axis=1, sort=True),
        tuple(_params_k)
    )


def m_spline_lb(df: pd.DataFrame, n_spans: int, knots: tuple[int]) -> tuple[pd.DataFrame, tuple[float]]:
    '''Linear Spline, Type B
    ================== =================================
    df.iloc[:, 0]      Period
    df.iloc[:, 1]      Target Series
    ================== =================================
    n_spans            Number of Spans
    knots              Interpolation Knots
    ================== =================================
    '''
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using `continue` Statement
    # =========================================================================
    _params_k, _splined = [], []
    for j in range(n_spans):
        _params_k.append(
            (df.iloc[knots[1 + j], 1] - df.iloc[knots[j], 1]) /
            (df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])
        )
        if 1 + j == n_spans:
            for i in range(knots[j], 1 + knots[1 + j]):
                _splined.append(
                    df.iloc[knots[j], 1] + _params_k[j] *
                    (df.iloc[i, 0] - df.iloc[knots[j], 0])
                )
        else:
            for i in range(knots[j], knots[1 + j]):
                _splined.append(
                    df.iloc[knots[j], 1] + _params_k[j] *
                    (df.iloc[i, 0] - df.iloc[knots[j], 0])
                )
    return (
        pd.concat(
            [
                df,
                pd.DataFrame(_splined, columns=['Spline'])
            ],
            axis=1, sort=True),
        tuple(_params_k)
    )


def m_spline_lls(df: pd.DataFrame, n_spans: int, knots: tuple[int]) -> tuple[pd.DataFrame, tuple[float]]:
    '''Linear Spline, Linear Regression Kernel
    ================== =================================
    df.iloc[:, 0]      Period
    df.iloc[:, 1]      Target Series
    ================== =================================
    n_spans            Number of Spans
    knots              Interpolation Knots
    ================== =================================
    '''
    _params_a, _params_k, _splined = [], [], []
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using `continue` Statement
    # =========================================================================
    for _ in range(n_spans):
        if 1 + _ == n_spans:
            _s__x = df.iloc[knots[_]:, 0].sum()
            _s__y = df.iloc[knots[_]:, 1].sum()
            _s_x2 = df.iloc[knots[_]:, 0].pow(2).sum()
            _s_xy = df.iloc[knots[_]:, 0].mul(df.iloc[knots[_]:, 1]).sum()
            _params_a.append(
                ((1 + knots[1 + _] - knots[_])*_s_xy - _s__x*_s__y) /
                ((1 + knots[1 + _] - knots[_])*_s_x2 - _s__x**2)
            )
        else:
            _s__x = df.iloc[knots[_]:knots[1 + _], 0].sum()
            _s__y = df.iloc[knots[_]:knots[1 + _], 1].sum()
            _s_x2 = df.iloc[knots[_]:knots[1 + _], 0].pow(2).sum()
            _s_xy = df.iloc[knots[_]:knots[1 + _],
                            0].mul(df.iloc[knots[_]:knots[1 + _], 1]).sum()
            if _ == 0:
                _params_a.append(
                    (_s__y*_s_x2 - _s__x*_s_xy) /
                    ((knots[1 + _] - knots[_])*_s_x2 - _s__x**2)
                )
            _params_a.append(
                ((knots[1 + _] - knots[_])*_s_xy - _s__x*_s__y) /
                ((knots[1 + _] - knots[_])*_s_x2 - _s__x**2)
            )

    for _ in range(n_spans):
        if _ == 0:
            _params_k.append(_params_a[_])
        else:
            _params_k.append(
                _params_k[_ - 1] + (_params_a[_] - _params_a[1 + _])*df.iloc[knots[_], 0])

        if 1 + _ == n_spans:
            for _i in range(knots[_], 1 + knots[1 + _]):
                _splined.append(_params_k[_] + _params_a[1 + _]*df.iloc[_i, 0])
        else:
            for _i in range(knots[_], knots[1 + _]):
                _splined.append(_params_k[_] + _params_a[1 + _]*df.iloc[_i, 0])
    return (
        pd.concat(
            [
                df,
                pd.DataFrame(_splined, columns=['Splined']),
            ],
            axis=1, sort=True),
        tuple(_params_a)
    )


def get_data_centered_by_period(data_frame: pd.DataFrame) -> pd.DataFrame:
    '''
    data_frame.index: Period,
    data_frame.iloc[:, 0]: Series
    '''
    # =========================================================================
    # TODO: Any Use?
    # =========================================================================
    # =========================================================================
    # DataFrame for Results
    # =========================================================================
    _data = data_frame.reset_index(level=0).copy()
    period = _data.iloc[:, 0]
    series = _data.iloc[:, 1]
    # =========================================================================
    # Loop
    # =========================================================================
    for _ in range(_data.shape[0] // 2):
        period = period.rolling(2).mean()
        series = series.rolling(2).mean()
        period_roll = period.shift(-((1 + _) // 2))
        series_roll = series.shift(-((1 + _) // 2))
        _data = pd.concat(
            [
                _data,
                period_roll,
                series_roll,
                series_roll.div(_data.iloc[:, 1]),
                series_roll.shift(-2).sub(series_roll).div(series_roll.shift(-1)).div(2),
            ],
            axis=1,
            sort=True
        )
    return _data


def preprocessing_a(df: pd.DataFrame) -> pd.DataFrame:
    df = df.iloc[:, [0, 4, 6, 7]].dropna()
    return df.div(df.iloc[0, :])


def preprocessing_b(df: pd.DataFrame) -> pd.DataFrame:
    return df.iloc[:, [0, 6, 7, 20]].dropna()


def preprocessing_c(df: pd.DataFrame) -> pd.DataFrame:
    df_production = df.iloc[:, [0, 6, 7]].dropna()
    df_production = df_production.div(df_production.iloc[0, :])
    df_money = df.iloc[:, range(18, 20)].dropna(how='all')
    df_money['m1_fused'] = df_money.mean(axis=1)
    df_money = df_money.iloc[:, -1].div(df_money.iloc[0, -1])
    _df = pd.concat(
        [
            df_production,
            df_money
        ],
        axis=1).dropna()
    return _df.div(_df.iloc[0, :])


def preprocessing_d(df: pd.DataFrame) -> pd.DataFrame:
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    return df.iloc[:, [0, 1, 2, 3, 7]].dropna()


def preprocessing_e(df: pd.DataFrame) -> tuple[pd.DataFrame]:
    assert df.shape[1] == 21, 'Works on DataFrame Produced with `get_data_combined_archived()`'
    # =========================================================================
    # `Real` Investment
    # =========================================================================
    df['inv'] = df.iloc[:, 0].mul(df.iloc[:, 7]).div(df.iloc[:, 6])
    # =========================================================================
    # `Real` Capital
    # =========================================================================
    df['cap'] = df.iloc[:, 11].mul(df.iloc[:, 7]).div(df.iloc[:, 6])
    return (
        # =====================================================================
        # DataFrame Nominal
        # =====================================================================
        df.iloc[:, [0, 6, 11]].dropna(),
        # =====================================================================
        # DataFrame `Real`
        # =====================================================================
        df.iloc[:, [-2, 7, -1]].dropna(),
    )


def preprocessing_kurenkov(data_testing: pd.DataFrame) -> tuple[pd.DataFrame]:
    '''Returns Four DataFrames with Comparison of data_testing: pd.DataFrame and Yu.V. Kurenkov Data'''
    FILE_NAME = 'dataset_usa_reference_ru_kurenkov_yu_v.csv'
    data_control = pd.read_csv(FILE_NAME, index_col=0)
    # =============================================================================
    # Production
    # =============================================================================
    data_a = pd.concat(
        [
            data_control.iloc[:, [0]],
            data_testing.loc[:, ['A191RX1']],
            get_data_usa_frb_ip(),
        ],
        axis=1, sort=True).dropna(how='all')
    data_a = data_a.div(data_a.loc[1950, :]).mul(100)
    # =============================================================================
    # Labor
    # =============================================================================
    data_b = pd.concat(
        [
            data_control.iloc[:, [1]],
            data_testing.loc[:, ['mfg_labor']],
        ],
        axis=1, sort=True).dropna(how='all')
    # =============================================================================
    # Capital
    # =============================================================================
    data_c = pd.concat(
        [
            data_control.iloc[:, [2]],
            data_testing.loc[:, ['K160491']],
        ],
        axis=1, sort=True).dropna(how='all')
    data_c = data_c.div(data_c.loc[1951, :]).mul(100)
    # =============================================================================
    # Capacity Utilization
    # =============================================================================
    data_d = pd.concat(
        [
            data_control.iloc[:, [3]],
            get_data_usa_frb_cu(),
        ],
        axis=1, sort=True)
    return data_a, data_b, data_c, data_d


def plot_approx_linear(df: pd.DataFrame):
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Real Values for Price Deflator
    df.iloc[:, 1]      Nominal Values for Price Deflator
    df.iloc[:, 2]      Regressor
    df.iloc[:, 3]      Regressand
    ================== =================================
    '''
    df.iloc[:, -1] = pd.to_numeric(df.iloc[:, -1], errors='coerce')
    df.dropna(inplace=True)
    # =========================================================================
    # TODO: Separate Basic Year Function
    # =========================================================================
    df['__deflator'] = df.iloc[:, 0].div(df.iloc[:, 1]).sub(1).abs()
    _b = df.iloc[:, -1].astype(float).argmin()
    df.drop(df.columns[-1], axis=1, inplace=True)
    # =========================================================================
    # Deflator
    # =========================================================================
    df['deflator'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df[f'{df.columns[2]}_bas'] = df.iloc[:, 2].mul(df.iloc[:, 4]).div(
        df.iloc[0, 2]).div(df.iloc[0, 4]).astype(float)
    df[f'{df.columns[3]}_bas'] = df.iloc[:, 3].mul(df.iloc[:, 4]).div(
        df.iloc[0, 3]).div(df.iloc[0, 4]).astype(float)
    _p1 = np.polyfit(
        df.iloc[:, -2],
        df.iloc[:, -1],
        deg=1
    )
    # =========================================================================
    # Yhat
    # =========================================================================
    df[f'{df.columns[3]}_estimate'] = df.iloc[:, -2].mul(_p1[0]).add(_p1[1])
    print('Period From: {} Through: {}'.format(df.index[0], df.index[-1]))
    print('Prices: {}=100'.format(df.index[_b]))
    print('Model: Yhat = {:.4f} + {:.4f}*X'.format(*_p1[::-1]))
    print('Model Parameter: A_0 = {:.4f}'.format(_p1[1]))
    print('Model Parameter: A_1 = {:.4f}'.format(_p1[0]))
    plt.figure()
    plt.title(
        '$Y(X)$, {}=100, {}$-${}'.format(
            df.index[_b], df.index[0], df.index[-1]
        )
    )
    plt.xlabel(
        'Gross Private Domestic Investment, $X(\\tau)$, {}=100, {}=100'.format(
            df.index[_b], df.index[0]
        )
    )
    plt.ylabel(
        'Gross Domestic Product, $Y(\\tau)$, {}=100, {}=100'.format(
            df.index[_b], df.index[0]
        )
    )
    plt.plot(df.iloc[:, -3], df.iloc[:, -2])
    plt.plot(
        df.iloc[:, -3], df.iloc[:, -1],
        label='$\\hat Y = {:.4f}+{:.4f}X$'.format(*_p1[::-1])
    )
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_approx_log_linear(df: pd.DataFrame):
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Real Values for Price Deflator
    df.iloc[:, 1]      Nominal Values for Price Deflator
    df.iloc[:, 2]      Regressor
    df.iloc[:, 3]      Regressand
    ================== =================================
    '''
    MAP_DESC = {
        'A032RC1': 'National Income',
        'A191RC1': 'Gross Domestic Product',
    }
    df.iloc[:, -1] = pd.to_numeric(df.iloc[:, -1], errors='coerce')
    df.dropna(inplace=True)
    # =========================================================================
    # TODO: Separate Basic Year Function
    # =========================================================================
    df['__deflator'] = df.iloc[:, 0].div(df.iloc[:, 1]).sub(1).abs()
    _b = df.iloc[:, -1].astype(float).argmin()
    df.drop(df.columns[-1], axis=1, inplace=True)
    # =========================================================================
    # Deflator
    # =========================================================================
    df['deflator'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df[f'{df.columns[2]}_log_bas'] = np.log(df.iloc[:, 2].div(df.iloc[0, 2]))
    df[f'{df.columns[3]}_log_bas'] = np.log(df.iloc[:, 3].mul(df.iloc[:, 4]).div(
        df.iloc[0, 3]).div(df.iloc[0, 4]).astype(float))
    _p1 = np.polyfit(
        df.iloc[:, -2],
        df.iloc[:, -1],
        deg=1
    )
    # =========================================================================
    # Yhat
    # =========================================================================
    df[f'{df.columns[3]}_estimate'] = df.iloc[:, -2].mul(_p1[0]).add(_p1[1])
    # =========================================================================
    # Delivery Block
    # =========================================================================
    print('Period From: {} Through: {}'.format(df.index[0], df.index[-1]))
    print('Prices: {}=100'.format(df.index[_b]))
    print('Model: Yhat = {:.4f} + {:.4f}*Ln(X)'.format(*_p1[::-1]))
    print('Model Parameter: A_0 = {:.4f}'.format(_p1[1]))
    print('Model Parameter: A_1 = {:.4f}'.format(_p1[0]))
    plt.figure()
    plt.title(
        '$Y(X)$, {}=100, {}$-${}'.format(
            df.index[_b], df.index[0], df.index[-1]
        )
    )
    plt.xlabel('Logarithm Prime Rate, $X(\\tau)$, {}=100'.format(df.index[0]))
    plt.ylabel(
        'Logarithm {}, $Y(\\tau)$, {}=100, {}=100'.format(
            MAP_DESC[df.columns[3]], df.index[_b], df.index[0]
        )
    )
    plt.plot(df.iloc[:, -3], df.iloc[:, -2])
    plt.plot(
        df.iloc[:, -3], df.iloc[:, -1],
        label='$\\hat Y = {:.4f}+{:.4f}X$'.format(*_p1[::-1])
    )
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_a(df: pd.DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Gross Domestic Investment
    df.iloc[:, 1]      National Income
    df.iloc[:, 2]      Nominal Gross Domestic Product
    df.iloc[:, 3]      Real Gross Domestic Product
    ================== =================================
    '''
    _df = df.copy()
    # =========================================================================
    # `Real` Investment
    # =========================================================================
    _df['inv'] = _df.iloc[:, 0].mul(_df.iloc[:, 3]).div(_df.iloc[:, 2])
    # =========================================================================
    # `Real` Production
    # =========================================================================
    _df['prd'] = _df.iloc[:, 1].mul(_df.iloc[:, 3]).div(_df.iloc[:, 2])
    _df['inv_roll_mean'] = _df.iloc[:, -2].rolling(2).mean()
    _df['prd_roll_mean'] = _df.iloc[:, -2].rolling(2).mean()
    plt.figure()
    plt.title(
        'Gross Private Domestic Investment & National Income, {}$-${}'.format(
            _df.index[0], _df.index[-1]
        )
    )
    plt.plot(_df.iloc[:, -4:-2], label=[
        'Gross Private Domestic Investment',
        'National Income',
    ])
    plt.xlabel('Period')
    plt.ylabel('Index')
    _df.index = _df.index.to_series().rolling(2).mean()
    plt.plot(
        _df.index, _df.iloc[:, -2], '--',
        _df.index, _df.iloc[:, -1], '--'
    )
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_b(df: pd.DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Gross Domestic Investment,
    df.iloc[:, 1]      Nominal Gross Domestic Product,
    df.iloc[:, 2]      Real Gross Domestic Product,
    df.iloc[:, 3]      Prime Rate
    ================== =================================
    '''
    _df = df.copy()
    # =========================================================================
    # `Real` Investment
    # =========================================================================
    _df['inv'] = _df.iloc[:, 0].mul(_df.iloc[:, 2]).div(_df.iloc[:, 1])
    plt.figure()
    plt.plot(_df.iloc[:, 3], _df.iloc[:, -1])
    plt.title(
        'Gross Private Domestic Investment, A006RC, {}$-${}'.format(
            _df.index[0], _df.index[-1]
        )
    )
    plt.xlabel('Percentage')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.show()


def plot_c(df: pd.DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Gross Domestic Investment
    df.iloc[:, 1]      Nominal Gross Domestic Product
    df.iloc[:, 2]      Real Gross Domestic Product
    df.iloc[:, 3]      M1
    ================== =================================
    '''
    # =========================================================================
    # `Real` Investment
    # =========================================================================
    df['inv'] = df.iloc[:, 0].mul(df.iloc[:, 2]).div(df.iloc[:, 1])
    plt.figure()
    plt.plot(df.iloc[:, range(2, 5)], label=[
        'Real Gross Domestic Product',
        'Money Supply',
        '`Real` Gross Domestic Investment',
    ])
    plt.title('Indexes, {}$-${}'.format(df.index[0], df.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_d(df: pd.DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period,
    df.iloc[:, 0]      Gross Domestic Investment,
    df.iloc[:, 1]      Gross Domestic Investment Price Index,
    df.iloc[:, 2]      Fixed Investment,
    df.iloc[:, 3]      Fixed Investment Price Index,
    df.iloc[:, 4]      Real Gross Domestic Product
    ================== =================================
    '''
    # =========================================================================
    # Basic Year
    # =========================================================================
    df['__deflator'] = df.iloc[:, 1].sub(100).abs()
    _b = df.iloc[:, -1].astype(float).argmin()
    df.drop(df.columns[-1], axis=1, inplace=True)
    _title = (df.index[_b], df.index[0], df.index[-1])
    # =========================================================================
    # Convert to Billions
    # =========================================================================
    df.iloc[:, -1] = df.iloc[:, -1].div(1000)
    # =========================================================================
    # Real Investment, Billions
    # =========================================================================
    df['invmnt'] = df.iloc[:, 1].mul(df.iloc[_b, 0]).div(100).div(1000)
    # =========================================================================
    # Real Fixed Investment, Billions
    # =========================================================================
    df['fxd_invmnt'] = df.iloc[:, 3].mul(df.iloc[_b, 2]).div(100).div(1000)
    plt.figure(1)
    plt.semilogy(
        df.iloc[:, -2],
        label='Real Gross Private Domestic Investment $GPDI$'
    )
    plt.semilogy(
        df.iloc[:, -1],
        color='red',
        label='Real Gross Private Fixed Investment, Nonresidential $GPFI(n)$'
    )
    plt.title('Real Indexes, {}=100, {}$-${}'.format(*_title))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars')
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(df.iloc[:, 4])
    plt.title(
        'Real Gross Domestic Product $GDP$, {}=100, {}$-${}'.format(*_title))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.figure(3)
    plt.plot(df.iloc[:, -2], df.iloc[:, 4])
    plt.title('$GPDI$ & $GPFI(n)$, {}=100, {}$-${}'.format(*_title))
    plt.xlabel('Billions of Dollars')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.figure(4)
    plt.plot(df.iloc[:, -1], df.iloc[:, 4])
    plt.title('$GPFI(n)$ & $GDP$, {}=100, {}$-${}'.format(*_title))
    plt.xlabel('Billions of Dollars')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.show()


def plot_block_zer(df: pd.DataFrame) -> None:
    '''
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Labor,
    df.iloc[:, 2]: Product
    '''
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    df['log_lab_c'] = np.log(df.iloc[:, 0].div(df.iloc[:, 1]))
    df['log_lab_p'] = np.log(df.iloc[:, 2].div(df.iloc[:, 1]))
    plot_simple_linear(
        *simple_linear_regression(df.iloc[:, [3, 4]])
    )
    plot_simple_log(
        *simple_linear_regression(df.iloc[:, [5, 6]])
    )


def plot_block_one(df: pd.DataFrame) -> None:
    '''
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Labor,
    df.iloc[:, 2]: Product
    '''
    # =========================================================================
    # TODO: Increase Cohesion
    # =========================================================================
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Valid Only for _k = 2
    # =========================================================================
    _k = 2
    # =========================================================================
    # Odd Frame
    # =========================================================================
    data_frame_o = pd.concat(
        [
            df.iloc[:, [-1]],
            rolling_mean_filter(df.iloc[:, [-1]], _k)[0].iloc[:, [-1]],
            kol_zur_filter(df.iloc[:, [-1]], _k)[0].iloc[:, [-1]],
            df.iloc[:, [-1]].ewm(alpha=0.25, adjust=False).mean(),
        ],
        axis=1,
    )
    # =========================================================================
    # Even Frame
    # =========================================================================
    data_frame_e = pd.concat(
        [
            rolling_mean_filter(df.iloc[:, [-1]], _k)[1].iloc[:, [-1]],
            kol_zur_filter(df.iloc[:, [-1]], _k)[1].iloc[:, [-1]],
        ],
        axis=1,
    )
    plt.figure()
    plt.plot(
        data_frame_o.iloc[:, 0],
        linewidth=3,
        label='Labor Capital Intensity'
    )
    plt.plot(
        data_frame_o.iloc[:, 1],
        label=f'Rolling Mean, {1+_k}'
    )
    plt.plot(
        data_frame_o.iloc[:, 2],
        label=f'Kolmogorov--Zurbenko Filter, {1+_k}'
    )
    plt.plot(
        data_frame_o.iloc[:, 3],
        label='Single Exponential Smoothing, Alpha={:,.2f}'.format(0.25)
    )
    plt.plot(
        data_frame_e,
        label=[
            f'Rolling Mean, {_k}',
            f'Kolmogorov--Zurbenko Filter, {_k}',
        ]
    )
    plt.title(
        'Labor Capital Intensity: Rolling Mean Filter, Kolmogorov--Zurbenko Filter &\n\
        Single Exponential Smoothing'
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_block_two(df: pd.DataFrame) -> None:
    '''
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Labor,
    df.iloc[:, 2]: Product
    '''
    # =========================================================================
    # TODO: Increase Cohesion
    # =========================================================================
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    _k = 3
    # =========================================================================
    # Odd Frame
    # =========================================================================
    data_frame_o = pd.concat(
        [
            df.iloc[:, [-1]],
            rolling_mean_filter(df.iloc[:, [-1]], _k)[0].iloc[:, [-1]],
            kol_zur_filter(df.iloc[:, [-1]], _k)[0].iloc[:, [1]],
            df.iloc[:, [-1]].ewm(alpha=0.25, adjust=False).mean(),
            df.iloc[:, [-1]].ewm(alpha=0.35, adjust=False).mean(),
            df.iloc[:, [-1]].ewm(alpha=0.45, adjust=False).mean(),
        ],
        axis=1,
    )
    # =========================================================================
    # Even Frame
    # =========================================================================
    data_frame_e = pd.concat(
        [
            rolling_mean_filter(df.iloc[:, [-1]], _k)[1],
            kol_zur_filter(df.iloc[:, [-1]], _k)[1],
        ],
        axis=1,
    )
    plt.figure()
    plt.plot(
        data_frame_o.iloc[:, 0],
        linewidth=3,
        label='Labor Productivity'
    )
    plt.plot(
        data_frame_o.iloc[:, 1],
        label=f'Rolling Mean, {_k}'
    )
    plt.plot(
        data_frame_o.iloc[:, 2],
        label=f'Kolmogorov--Zurbenko Filter, {_k}'
    )
    plt.plot(
        data_frame_o.iloc[:, 3],
        label='Single Exponential Smoothing, Alpha={:,.2f}'.format(0.25)
    )
    plt.plot(
        data_frame_o.iloc[:, 4],
        label='Single Exponential Smoothing, Alpha={:,.2f}'.format(0.35)
    )
    plt.plot(
        data_frame_o.iloc[:, 5],
        label='Single Exponential Smoothing, Alpha={:,.2f}'.format(0.45)
    )
    plt.plot(
        data_frame_e,
        label=[
            f'Rolling Mean, {_k-1}',
            f'Rolling Mean, {_k+1}',
            f'Kolmogorov--Zurbenko Filter, {_k-1}',
            f'Kolmogorov--Zurbenko Filter, {_k+1}',
        ]
    )
    plt.title(
        'Labor Capital Intensity: Rolling Mean Filter, Kolmogorov--Zurbenko Filter &\n\
        Single Exponential Smoothing'
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_built_in(module: callable):
    # =========================================================================
    # TODO: Rework
    # =========================================================================
    FILE_NAMES = (
        'datasetAutocorrelation.txt',
        'CHN_TUR_GDP.zip',
    )
    data = pd.read_csv(FILE_NAMES[0])
    for _, series_id in enumerate(sorted(set(data.iloc[:, 1])), start=1):
        plt.figure(_)
        module(fetch_world_bank(data, series_id))
        plt.grid(True)

    data = pd.read_csv(FILE_NAMES[1])
    for _, series_id in enumerate(sorted(set(data.iloc[:, 1])), start=1):
        plt.figure(_)
        module(fetch_world_bank(data, series_id))
        plt.grid(True)

    plt.show()


def data_preprocessing_cobb_douglas(df: pd.DataFrame) -> tuple[pd.DataFrame, tuple[float]]:
    '''
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Labor,
    df.iloc[:, 2]: Product
    '''
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    # =========================================================================
    # Original: k=0.25
    # =========================================================================
    k, b = np.polyfit(
        np.log(df.iloc[:, -2]),
        np.log(df.iloc[:, -1]),
        deg=1
    )
    # =========================================================================
    # Scipy Signal Median Filter, Non-Linear Low-Pass Filter
    # =========================================================================
    # =========================================================================
    # k, b = np.polyfit(
    #     np.log(signal.medfilt(df.iloc[:, -2])),
    #     np.log(signal.medfilt(df.iloc[:, -1])),
    #     deg=1
    # )
    # =========================================================================
    # =========================================================================
    # Description
    # =========================================================================
    df['cap_to_lab'] = df.iloc[:, 1].div(df.iloc[:, 0])
    # =========================================================================
    # Fixed Assets Turnover
    # =========================================================================
    df['c_turnover'] = df.iloc[:, 2].div(df.iloc[:, 0])
    # =========================================================================
    # Product Trend Line=3 Year Moving Average
    # =========================================================================
    df['prod_roll'] = df.iloc[:, 2].rolling(window=3, center=True).mean()
    df['prod_roll_sub'] = df.iloc[:, 2].sub(df.iloc[:, -1])
    # =========================================================================
    # Computed Product
    # =========================================================================
    df['prod_comp'] = df.iloc[:, 0].pow(k).mul(
        df.iloc[:, 1].pow(1-k)).mul(np.exp(b))
    # =========================================================================
    # Computed Product Trend Line=3 Year Moving Average
    # =========================================================================
    df['prod_comp_roll'] = df.iloc[:, -1].rolling(window=3, center=True).mean()
    df['prod_comp_roll_sub'] = df.iloc[:, -2].sub(df.iloc[:, -1])
    # =========================================================================
    #     print(r2_score(df.iloc[:, 2], df.iloc[:, 3]))
    #     print(df.iloc[:, 3].div(df.iloc[:, 2]).sub(1).abs().mean())
    # =========================================================================
    return df, (k, np.exp(b),)


def data_preprocessing_cobb_douglas_alt(df: pd.DataFrame) -> tuple[pd.DataFrame, tuple[float]]:
    '''
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Labor,
    df.iloc[:, 2]: Product,
    df.iloc[:, 3]: Product Alternative,
    '''
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    # =========================================================================
    # Original: k=0.25
    # =========================================================================
    k, b = np.polyfit(
        np.log(df.iloc[:, -2]),
        np.log(df.iloc[:, -1]),
        deg=1
    )
    # =========================================================================
    # Description
    # =========================================================================
    df['cap_to_lab'] = df.iloc[:, 1].div(df.iloc[:, 0])
    # =========================================================================
    # Fixed Assets Turnover
    # =========================================================================
    df['c_turnover'] = df.iloc[:, 2].div(df.iloc[:, 0])
    # =========================================================================
    # Product Trend Line=3 Year Moving Average
    # =========================================================================
    df['prod_roll'] = df.iloc[:, 2].rolling(window=3, center=True).mean()
    df['prod_roll_sub'] = df.iloc[:, 2].sub(df.iloc[:, -1])
    # =========================================================================
    # Computed Product
    # =========================================================================
    df['prod_comp'] = df.iloc[:, 0].pow(k).mul(
        df.iloc[:, 1].pow(1-k)).mul(np.exp(b))
    # =========================================================================
    # Computed Product Trend Line=3 Year Moving Average
    # =========================================================================
    df['prod_comp_roll'] = df.iloc[:, -1].rolling(window=3, center=True).mean()
    df['prod_comp_roll_sub'] = df.iloc[:, -2].sub(df.iloc[:, -1])
    # =========================================================================
    # Labor Productivity Alternative
    # =========================================================================
    df['_lab_product'] = df.iloc[:, 3].div(df.iloc[:, 1])
    # =========================================================================
    # Original: _k=0.25
    # =========================================================================
    _k, _b = np.polyfit(
        np.log(df.iloc[:, 4]),
        np.log(df.iloc[:, -1]),
        deg=1
    )
    # =========================================================================
    # Fixed Assets Turnover Alternative
    # =========================================================================
    df['_c_turnover'] = df.iloc[:, 3].div(df.iloc[:, 0])
    # =========================================================================
    # Product Alternative Trend Line=3 Year Moving Average
    # =========================================================================
    df['_prod_roll'] = df.iloc[:, 3].rolling(window=3, center=True).mean()
    df['_prod_roll_sub'] = df.iloc[:, 3].sub(df.iloc[:, -1])
    # =========================================================================
    # Computed Product Alternative
    # =========================================================================
    df['_prod_comp'] = df.iloc[:, 0].pow(_k).mul(
        df.iloc[:, 1].pow(1-_k)).mul(np.exp(_b))
    # =========================================================================
    # Computed Product Alternative Trend Line=3 Year Moving Average
    # =========================================================================
    df['_prod_comp_roll'] = df.iloc[:, -
                                    1].rolling(window=3, center=True).mean()
    df['_prod_comp_roll_sub'] = df.iloc[:, -2].sub(df.iloc[:, -1])
    return df, (k, np.exp(b),), (_k, np.exp(_b),)


FIG_MAP = {
    'fg_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
    'fg_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
    'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
    'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
    'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
    'year_price': 1899,
}


def plot_cobb_douglas(data_frame: pd.DataFrame, params: tuple[float], mapping: dict) -> None:
    '''
    Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    '''
    assert data_frame.shape[1] == 12

    def lab_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
        return np.multiply(np.power(array, -k), b)

    def cap_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
        return np.multiply(np.power(array, 1-k), b)

    plt.figure(1)
    plt.semilogy(data_frame.iloc[:, range(3)], label=[
        'Fixed Capital',
        'Labor Force',
        'Physical Product',
    ])
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(mapping['fg_a'].format(data_frame.index[0],
                                     data_frame.index[-1],
                                     mapping['year_price']))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.semilogy(data_frame.iloc[:, [2, 9]], label=[
        'Actual Product',
        'Computed Product, $P\' = {:,.4f}L^{{{:,.4f}}}C^{{{:,.4f}}}$'.format(
            params[1],
            1-params[0],
            params[0],
        ),
    ])
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(mapping['fg_b'].format(data_frame.index[0],
                                     data_frame.index[-1],
                                     mapping['year_price']))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(data_frame.iloc[:, [8, 11]], label=[
        'Deviations of $P$',
        'Deviations of $P\'$',
        # =========================================================================
        #      TODO: ls=['solid','dashed',]
        # =========================================================================
    ])
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(mapping['fg_c'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(data_frame.iloc[:, 9].div(data_frame.iloc[:, 2]).sub(1))
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(mapping['fg_d'].format(data_frame.index[0],
                                     data_frame.index[-1]))
    plt.grid(True)
    plt.figure(5, figsize=(5, 8))
    lc = np.arange(0.2, 1.0, 0.005)
    plt.scatter(data_frame.iloc[:, 5], data_frame.iloc[:, 4])
    plt.scatter(data_frame.iloc[:, 5], data_frame.iloc[:, 6])
    plt.plot(lc, lab_productivity(lc, *params),
             label='$\\frac{3}{4}\\frac{P}{L}$')
    plt.plot(lc, cap_productivity(lc, *params),
             label='$\\frac{1}{4}\\frac{P}{C}$')
    plt.xlabel('$\\frac{L}{C}$')
    plt.ylabel('Indexes')
    plt.title(mapping['fg_e'])
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_cobb_douglas_alt(data_frame: pd.DataFrame, params: tuple[float], mapping: dict) -> None:
    '''
    Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    '''
    assert data_frame.shape[1] == 20

    def lab_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
        return np.multiply(np.power(array, -k), b)

    def cap_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
        return np.multiply(np.power(array, 1-k), b)

    plt.figure(1)
    plt.semilogy(data_frame.iloc[:, range(4)], label=[
        'Fixed Capital',
        'Labor Force',
        'Physical Product',
        'Physical Product, Alternative',
    ])
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(mapping['fg_a'].format(data_frame.index[0],
                                     data_frame.index[-1],
                                     mapping['year_price']))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(data_frame.iloc[:, [3, 17]], label=[
        'Actual Product',
        'Computed Product, $P\' = {:,.4f}L^{{{:,.4f}}}C^{{{:,.4f}}}$'.format(
            params[1],
            1-params[0],
            params[0],
        ),
    ])
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(mapping['fg_b'].format(data_frame.index[0],
                                     data_frame.index[-1],
                                     mapping['year_price']))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(data_frame.iloc[:, [15, 18]], label=[
        'Deviations of $P$',
        'Deviations of $P\'$',
        # =========================================================================
        #      TODO: ls=['solid','dashed',]
        # =========================================================================
    ])
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(mapping['fg_c'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(data_frame.iloc[:, 17].div(data_frame.iloc[:, 3]).sub(1))
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(mapping['fg_d'].format(data_frame.index[0],
                                     data_frame.index[-1]))
    plt.grid(True)
    plt.figure(5, figsize=(5, 8))
    lc = np.arange(0.2, 1.0, 0.005)
    plt.scatter(data_frame.iloc[:, 6], data_frame.iloc[:, 13])
    plt.scatter(data_frame.iloc[:, 6], data_frame.iloc[:, 14])
    plt.plot(lc, lab_productivity(lc, *params),
             label='$\\frac{3}{4}\\frac{P}{L}$')
    plt.plot(lc, cap_productivity(lc, *params),
             label='$\\frac{1}{4}\\frac{P}{C}$')
    plt.xlabel('$\\frac{L}{C}$')
    plt.ylabel('Indexes')
    plt.title(mapping['fg_e'])
    plt.legend()
    plt.grid(True)
    plt.show()


# def data_preprocessing_cobb_douglas(df: pd.DataFrame) -> tuple[pd.DataFrame, tuple[float]]:
# =============================================================================
#     TODO: Implement Additional Features
# =============================================================================
#     '''
#     df.index: Period,
#     df.iloc[:, 0]: Capital,
#     df.iloc[:, 1]: Labor,
#     df.iloc[:, 2]: Product
#     '''
#     from sklearn.linear_model import Lasso
#     from sklearn.linear_model import LassoCV
#     from sklearn.linear_model import LinearRegression
#     from sklearn.linear_model import Ridge
#     # =========================================================================
#     # Labor Capital Intensity
#     # =========================================================================
#     df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
#     # =========================================================================
#     # Labor Productivity
#     # =========================================================================
#     df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
#     # # =========================================================================
#     # # TODO: Refresh
#     # # =========================================================================
#     # df['_lab_cap_int'] = np.vstack(
#     #     (np.zeros((df.shape[0], 1)).T,
#     #      np.log(df.iloc[:, [-2]])))

# # # =============================================================================
# # #     las = Lasso(alpha=0.01).fit(df['_lab_cap_int'], np.log(df.iloc[:, -1]))
# # #     reg = LinearRegression().fit(df['_lab_cap_int'], np.log(df.iloc[:, -1]))
# # # =============================================================================
# #     las = LassoCV(cv=4, random_state=0).fit(
# #         df['_lab_cap_int'], np.log(df.iloc[:, -1]))
# #     print(las)
# # # =============================================================================
# # #     tik = Ridge(alpha=0.01).fit(df['_lab_cap_int'], np.log(df.iloc[:, -1]))
# # #     print('Lasso: a_0 = {0:.12f} & a_1 = {1:.12f}'.format(las.intercept_, las.coef_[1]))
# # #     print('Linear Regression: a_0 = {0:.12f} & a_1 = {1:.12f}'.format(reg.intercept_, reg.coef_[1]))
# # #     print('Ridge Regression: a_0 = {0:.12f} & a_1 = {1:.12f}'.format(tik.intercept_, tik.coef_[1]))
# # # =============================================================================
# #     b = np.exp(las.intercept_)
# # #     # =========================================================================
# # #     # Original: k=0.25
# # #     # =========================================================================
# # #     k, b = np.polyfit(
# # #         np.log(df.iloc[:, -2]),
# # #         np.log(df.iloc[:, -1]),
# # #         deg=1
# # #     )
#     # =========================================================================
#     # Description
#     # =========================================================================
#     df['cap_to_lab'] = df.iloc[:, 1].div(df.iloc[:, 0])
#     # =========================================================================
#     # Fixed Assets Turnover
#     # =========================================================================
#     df['c_turnover'] = df.iloc[:, 2].div(df.iloc[:, 0])
#     # =========================================================================
#     # Product Trend Line=3 Year Moving Average
#     # =========================================================================
#     df['prod_roll'] = df.iloc[:, 2].rolling(window=3, center=True).mean()
#     # df['prod_roll_sub'] = df.iloc[:, 2].sub(df.iloc[:, -1])
#     # =========================================================================
#     # Computed Product
#     # =========================================================================
# #     df['prod_comp'] = df.iloc[:, 0].pow(las.coef_[1]).mul(
# #         df.iloc[:, 1].pow(1-las.coef_[1])).mul(b)
#     # =========================================================================
#     # Computed Product Trend Line=3 Year Moving Average
#     # =========================================================================
#     df['prod_comp_roll'] = df.iloc[:, -1].rolling(window=3, center=True).mean()
#     df['prod_comp_roll_sub'] = df.iloc[:, -2].sub(df.iloc[:, -1])
# # #     return df, (k, np.exp(b),)


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


def plot_cobb_douglas_3d(data_frame: pd.DataFrame) -> None:
    '''
    Cobb--Douglas 3D-Plotting
    '''
    assert data_frame.shape[1] == 3

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(data_frame.iloc[:, 0],
            data_frame.iloc[:, 1], data_frame.iloc[:, 2])
    ax.set_xlabel('Capital')
    ax.set_ylabel('Labor')
    ax.set_zlabel('Production')
    ax.view_init(30, 45)
    plt.show()


# =============================================================================
# Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928 & P.H. Douglas. The Theory of Wages, 1934;
# =============================================================================
FIG_MAP = {
    'fg_a': 'Chart 15 Relative Increase in Capital, Labor, and Physical Product in Manufacturing Industries of Massachussets, {}$-${} ({}=100',
    'fg_b': 'Chart 16 Theoretical and Actual Curves of Production, Massachusetts, {}$-${} ({}=100',
    'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines, Massachusetts\nTrend Lines = 3 Year Moving Average',
    'fg_d': 'Chart 17 The Percentage Deviations of the Computed Product ($P\'$) from the Actual Product ($P$) in Massachusetts Manufacturing, {}$-${}',
    'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
    'year_price': 1899
}


def plot_cobb_douglas_tight_layout(data_frame: pd.DataFrame, params: tuple[float], mapping: dict) -> None:
    '''
    Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    '''
    assert data_frame.shape[1] == 12

    def lab_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
        return np.multiply(np.power(array, -k), b)

    def cap_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
        return np.multiply(np.power(array, 1-k), b)

    fig, axs = plt.subplots(5, 1)
    axs[0].plot(data_frame.iloc[:, range(3)], label=[
        'Fixed Capital',
        'Labor Force',
        'Physical Product',
    ])
    axs[0].set_xlabel('Period')
    axs[0].set_ylabel('Indexes')
    axs[0].set_title(mapping['fg_a'].format(data_frame.index[0],
                                            data_frame.index[-1],
                                            mapping['year_price']))
    axs[0].legend()
    axs[0].grid(True)
    axs[1].plot(data_frame.iloc[:, [2, 5]], label=[
        'Actual Product',
        'Computed Product, $P\' = {:,.4f}L^{{{:,.4f}}}C^{{{:,.4f}}}$'.format(
            params[1], 1-params[0], params[0]),
    ])
    axs[1].set_xlabel('Period')
    axs[1].set_ylabel('Production')
    axs[1].set_title(mapping['fg_b'].format(data_frame.index[0],
                                            data_frame.index[-1],
                                            mapping['year_price']))
    axs[1].legend()
    axs[1].grid(True)
    axs[2].plot(data_frame.iloc[:, [8, 9]],
                label=[
                    'Deviations of $P$',
                    'Deviations of $P\'$',
    ],
        # =========================================================================
        #      TODO: ls=['solid','dashed',]
        # =========================================================================
    )
    axs[2].set_xlabel('Period')
    axs[2].set_ylabel('Percentage Deviation')
    axs[2].set_title(mapping['fg_c'])
    axs[2].legend()
    axs[2].grid(True)
    axs[3].plot(data_frame.iloc[:, 5].div(data_frame.iloc[:, 2]).sub(1))
    axs[3].set_xlabel('Period')
    axs[3].set_ylabel('Percentage Deviation')
    axs[3].set_title(mapping['fg_d'].format(data_frame.index[0],
                                            data_frame.index[-1]))
    axs[3].grid(True)
    lc = np.arange(0.2, 1.0, 0.005)
    axs[4].scatter(data_frame.iloc[:, 10], data_frame.iloc[:, 4])
    axs[4].scatter(data_frame.iloc[:, 10], data_frame.iloc[:, 11])
    axs[4].plot(lc, lab_productivity(lc, *params),
                label='$\\frac{3}{4}\\frac{P}{L}$')
    axs[4].plot(lc, cap_productivity(lc, *params),
                label='$\\frac{1}{4}\\frac{P}{C}$')
    axs[4].set_xlabel('$\\frac{L}{C}$')
    axs[4].set_ylabel('Indexes')
    axs[4].set_title(mapping['fg_e'])
    axs[4].legend()
    axs[4].grid(True)
    plt.tight_layout()
    plt.show()


def test_procedure(kwargs_list: list[dict]) -> None:
    data_frame = pd.concat(
        [
            fetch_usa_bea(**_kwargs) for _kwargs in kwargs_list
        ],
        axis=1,
        sort=True
    )
    data_frame['diff_abs'] = data_frame.iloc[:, 0].sub(
        data_frame.iloc[:, 1]).sub(data_frame.iloc[:, 2])
    data_frame.iloc[:, [-1]].dropna(axis=0).plot(grid=True)


def test_sub_a(data_frame):
    data_frame['delta_sm'] = data_frame.iloc[:, 0].sub(
        data_frame.iloc[:, [3, 4, 5]].sum(axis=1))
    data_frame.dropna(axis=0, inplace=True)
    autocorrelation_plot(data_frame.iloc[:, [-1]])


def test_sub_b(data_frame):
    # data_frame['delta_eq'] = data_frame.iloc[:, 0].sub(data_frame.iloc[:, -1])
    data_frame['delta_eq'] = data_frame.iloc[:, 0].mul(4).div(
        data_frame.iloc[:, 0].add(data_frame.iloc[:, -1])).sub(2)
    data_frame.dropna(axis=0, inplace=True)
    data_frame.iloc[:, [-1]].plot(grid=True)


def plot_can_test(data_frame):
    plt.figure()
    data_frame.plot(logy=True)
    plt.title('Discrepancy')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.show()


def plot_usa_nber_manager():
    FILE_NAMES = (
        'dataset_usa_nber_ces_mid_sic5811.csv',
        'dataset_usa_nber_ces_mid_naics5811.csv',
    )
    aggs = ('mean', 'sum')
    for _agg in aggs:
        sic = fetch_usa_nber(FILE_NAMES[0], _agg)
        naics = fetch_usa_nber(FILE_NAMES[1], _agg)
        plot_usa_nber(sic, naics, _agg)


def fetch_usa_nber(file_name: str, agg: str) -> pd.DataFrame:
    _df = pd.read_csv(file_name)
    _df.drop(_df.columns[0], axis=1, inplace=True)
    if agg == 'mean':
        return _df.groupby(_df.columns[0]).mean()
    elif agg == 'sum':
        return _df.groupby(_df.columns[0]).sum()


def plot_usa_nber(df_sic: pd.DataFrame, df_naics: pd.DataFrame, agg: str) -> None:
    '''Project V: USA NBER Data Plotting'''
    for _, (sic_id, naics_id) in enumerate(zip(df_sic.columns, df_naics.columns)):
        # =====================================================================
        # Ensures Columns in Two DataFrames Are in the Same Ordering
        # =====================================================================
        series_id = tuple(set((sic_id, naics_id)))
        plt.plot(df_sic.iloc[:, _], label='sic_{}'.format(*series_id))
        plt.plot(df_naics.iloc[:, _], label='naics_{}'.format(*series_id))
        plt.title('NBER CES: {} {}'.format(*series_id, agg))
        plt.xlabel('Period')
        plt.ylabel('Dimension')
        plt.grid(True)
        plt.legend()
        plt.show()


def test_data_consistency_a():
    '''Project I: Canada Gross Domestic Product Data Comparison'''
    # =========================================================================
    # Expenditure-Based Gross Domestic Product Series Used
    # Income-Based Gross Domestic Product Series Not Used
    # =========================================================================
    ARGS = (
        # =====================================================================
        # Series A: Equals Series D, However, Series D Is Preferred Over Series A As It Is Yearly:
        # v62307282 - 380-0066 Price indexes, gross domestic product; Canada; Implicit price indexes; Gross domestic product at market prices (quarterly, 1961-03-01 to 2017-09-01)
        # =====================================================================
        (3800066, 'v62307282'),
        # =====================================================================
        # Series B: Equals Both Series C & Series E, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306896 - 380-0084 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Seasonally adjusted at annual rates; Gross domestic product at market prices (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)
        # =====================================================================
        (3800084, 'v62306896'),
        # =====================================================================
        # Series C: Equals Both Series B & Series E, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306938 - 380-0084 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Unadjusted; Gross domestic product at market prices (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)
        # =====================================================================
        (3800084, 'v62306938'),
        # =====================================================================
        # Series D: Equals Series A, However, Series D Is Preferred Over Series A As It Is Yearly: v62471023 - 380-0102 Gross domestic product indexes; Canada; Implicit price indexes; Gross domestic product at market prices (annual, 1961 to 2016)
        # =====================================================================
        (3800102, 'v62471023'),
        # =====================================================================
        # Series E: Equals Both Series B & Series C, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62471340 - 380-0106 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Gross domestic product at market prices (x 1,000,000) (annual, 1961 to 2016)
        # =====================================================================
        (3800106, 'v62471340'),
        (3800518, 'v96411770'),
        (3800566, 'v96391932'),
        (3800567, 'v96730304'),
        (3800567, 'v96730338'),
    )
    data_frame = pd.concat(
        [
            pd.concat(
                [
                    fetch_can_quarterly(*_args) for _args in ARGS[:3]
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    fetch_can_annually(*_args) for _args in ARGS[3:]
                ],
                axis=1,
                sort=True
            ),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    data_frame['series_0x0'] = data_frame.iloc[:, 0].div(data_frame.iloc[0, 0])
    data_frame['series_0x1'] = data_frame.iloc[:, 4].div(data_frame.iloc[0, 4])
    data_frame['series_0x2'] = data_frame.iloc[:, 5].div(data_frame.iloc[0, 5])
    data_frame['series_0x3'] = data_frame.iloc[:, 7].div(
        data_frame.iloc[:, 6]).div(data_frame.iloc[:, 5]).mul(100)
    data_frame['series_0x4'] = data_frame.iloc[:, 8].div(data_frame.iloc[0, 8])
    # =========================================================================
    # Option 1
    # =========================================================================
    plot_can_test(data_frame.iloc[:, [-5, -3]])
    # =========================================================================
    # Option 2
    # =========================================================================
    plot_can_test(data_frame.iloc[:, [-2, -1]])
    # =========================================================================
    # Option 3
    # =========================================================================
    plot_can_test(data_frame.iloc[:, [-4, -1]])
    # =========================================================================
    # Option 4: What?
    # =========================================================================
    # plot_can_test(data_frame.iloc[:, -1].div(data_frame.iloc[:, -1]), data_frame.iloc[:, -3])


def test_data_consistency_b():
    '''Project II: USA Fixed Assets Data Comparison'''
    # =========================================================================
    # Fixed Assets Series: k1ntotl1si000, 1925--2016
    # Fixed Assets Series: kcntotl1si000, 1925--2016
    # Not Used: Fixed Assets: k3ntotl1si000, 1925--2016, Table 2.3. Historical-Cost Net Stock of Private Fixed Assets, Equipment, Structures, and Intellectual Property Products by Type
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WB_NAME = 'Section2ALL_xls.xls'
    SH_NAMES = (
        '201 Ann',
        '202 Ann',
        '203 Ann',
    )
    SERIES_IDS = (
        'k1ntotl1si000',
        'kcntotl1si000',
        'k3ntotl1si000',
    )
    data_frame = pd.concat(
        [
            fetch_usa_bea(ARCHIVE_NAME, WB_NAME, sh, _id)
            for sh, _id in zip(SH_NAMES, SERIES_IDS)
        ],
        axis=1,
        sort=True
    )
    print(data_frame)


def test_data_consistency_c():
    '''Project III: USA BLS Unemployment Rate & Producer Price Index Manufacturing'''
    FILE_NAMES = (
        'dataset_usa_bls-2015-02-23-ln.data.1.AllData',
        'dataset_usa_bls-2017-07-06-ln.data.1.AllData',
        'dataset_usa_bls-pc.data.0.Current',
    )
    SERIES_IDS = (
        # =====================================================================
        # LNU04000000: Bureau of Labor Statistics Unemployment Rate
        # LNU04000000: Bureau of Labor Statistics Unemployment Rate
        # PCUOMFG--OMFG--: Bureau of Labor Statistics Producer Price Index Manufacturing
        # =====================================================================
        'LNU04000000',
        'LNU04000000',
        'PCUOMFG--OMFG',
    )
    [print(fetch_usa_bls(file_name, series_id))
     for file_name, series_id in zip(FILE_NAMES, SERIES_IDS)]


def test_data_consistency_d():
    '''Project IV: USA Macroeconomic & Fixed Assets Data Tests'''
    # =========================================================================
    # Macroeconomic Data Tests
    # =========================================================================
    def generate_kwargs_list(
            archive_name: str,
            wb_name: str,
            sheet_names: tuple[str],
            series_ids: tuple[str]
    ) -> list[dict]:
        return [
            {
                'archive_name': archive_name,
                'wb_name': wb_name,
                'sh_name': _sh,
                'series_id': _id,
            } for _sh, _id in zip(sheet_names, series_ids)
        ]

    # =========================================================================
    # Tested: `A051RC1` != `A052RC1` + `A262RC1`
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10705-A', 'T11200-A', 'T10705-A',)
    SERIES_IDS = ('A051RC', 'A052RC', 'A262RC',)
    test_procedure(generate_kwargs_list(
        ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS))
    # =========================================================================
    # Tested: `Government` = `Federal` + `State and local`
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10105-A', 'T10105-A', 'T10105-A',)
    SERIES_IDS = ('A822RC', 'A823RC', 'A829RC',)
    test_procedure(generate_kwargs_list(
        ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS))
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section3all_xls.xlsx'
    SH_NAMES = ('T30100-A', 'T30200-A', 'T30300-A',)
    SERIES_IDS = ('A955RC', 'A957RC', 'A991RC',)
    test_procedure(generate_kwargs_list(
        ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS))
    # # =========================================================================
    # # Tested: `Federal` = `National defense` + `Nondefense`
    # # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10105-A', 'T10105-A', 'T10105-A',)
    SERIES_IDS = ('A823RC', 'A824RC', 'A825RC',)
    test_procedure(generate_kwargs_list(
        ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS))
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section3all_xls.xlsx'
    SH_NAMES = ('T30200-A', 'T30905-A', 'T30905-A',)
    SERIES_IDS = ('A957RC', 'A997RC', 'A542RC',)
    test_procedure(generate_kwargs_list(
        ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS))
    # =========================================================================
    # Fixed Assets Data Tests
    # =========================================================================
    result_frame = fetch_usa_bea_sfat_series()
    # =========================================================================
    # Tested: `k3n31gd1es000` = `k3n31gd1eq000` + `k3n31gd1ip000` + `k3n31gd1st000`
    # =========================================================================
    test_sub_a(result_frame)
    # =========================================================================
    # Comparison of `k3n31gd1es000` out of control_frame with `k3n31gd1es000` out of test_frame
    # =========================================================================
    test_sub_b(result_frame)
    # =========================================================================
    # Future Project: Test Ratio of Manufacturing Fixed Assets to Overall Fixed Assets
    # =========================================================================
    # =========================================================================
    # TODO:
    # =========================================================================


def save_zip(data_frame, file_name):
    data_frame.to_csv(f'{file_name}.csv', index=True, encoding='utf-8-sig')
    with zipfile.ZipFile(f'{file_name}.zip', 'w') as archive:
        archive.write(f'{file_name}.csv', compress_type=zipfile.ZIP_DEFLATED)
        os.unlink(f'{file_name}.csv')


def plot_increment(frame):
    fig, axs = plt.subplots(2, 1)  # fig, axs = plt.subplots()
    axs[0].plot(frame.iloc[:, 0], frame.iloc[:, 1], label='Description Here')
    axs[0].set_xlabel('Labor Capital Intensity')
    axs[0].set_ylabel('Labor Productivity')
    axs[0].set_title('Description')
    axs[0].legend()
    axs[0].grid(True)
    axs[1].plot(frame.iloc[:, 2], frame.iloc[:, 3], label='Description Here')
    axs[1].set_xlabel('Labor Capital Intensity Increment')
    axs[1].set_ylabel('Labor Productivity Increment')
    axs[1].set_title('Description')
    axs[1].grid(True)
    axs[1].legend()
    for i in range(3, frame.shape[0], 5):
        axs[1].annotate(frame.index[i], (frame.iloc[i, 2], frame.iloc[i, 3]))
#    os.chdir('/media/alexander/321B-6A94')
#    plt.tight_layout()
#    fig.set_size_inches(10., 25.)
#    fig.savefig('name_figure_a.pdf', format='pdf', dpi=900)
    plt.show()


def calculate_plot_uspline(df: pd.DataFrame):
    '''
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Labor,
    df.iloc[:, 2]: Product
    '''
    # =========================================================================
    # TODO: Increase Cohesion
    # =========================================================================
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    chunk = df.iloc[:, -2:]
    chunk.sort_values(chunk.columns[0], inplace=True)
    spl = UnivariateSpline(chunk.iloc[:, [0]], chunk.iloc[:, [1]])
    # =========================================================================
    # _new_axis = np.linspace(chunk.iloc[:, [0]].min(), chunk.iloc[:, [0]].max(), chunk.shape[0] - 1)
    # =========================================================================
    plt.figure()
    plt.scatter(chunk.iloc[:, [0]], chunk.iloc[:, [1]], label='Original')
    plt.plot(
        chunk.iloc[:, 0],
        spl(chunk.iloc[:, 0]),
        'g',
        lw=3,
        label='Spline'
    )
    plt.title(
        'Labor Capital Intensity & Labor Productivity, {}$-${}'.format(
            df.index[0],
            df.index[-1]
        )
    )
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    # =========================================================================
    # TODO: Figure Out How It Works
    # =========================================================================
    print(spl.antiderivative())
    # =========================================================================
    # TODO: Figure Out How It Works
    # =========================================================================
    print(spl.derivative())
    print(spl.derivatives(1))
    print(spl.ext)
    print(spl.get_coeffs())
    print(spl.get_knots())
    print(spl.get_residual())
    print(spl.integral(1., 1.75))
    print(spl.roots())
    print(spl.set_smoothing_factor(0.25))
    plt.show()


def price_inverse_single(data_series):
    '''Intent: Returns Prices Icrement Series from Cumulative Deflator Series;
    source: pandas DataFrame'''
    return data_series.div(data_series.shift(1)).sub(1)


def strip_cumulated_deflator(data_frame):
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    return price_inverse_single(data_frame.dropna()).dropna()


def price_direct(data_frame, base):
    '''Intent: Returns Cumulative Price Index for Base Year;
    data_frame.iloc[:, 0]: Growth Rate;
    base: Base Year'''
    '''Cumulative Price Index'''
    data_frame['p_i'] = data_frame.iloc[:, 0].add(1).cumprod()
    '''Cumulative Price Index for the Base Year'''
    data_frame['cpi'] = data_frame.iloc[:, 1].div(
        data_frame.iloc[base-data_frame.index[0], 1])
    return data_frame.iloc[:, [2]]


def price_inverse(data_frame):
    '''Intent: Returns Growth Rate from Cumulative Price Index for Some Base Year;
    data_frame.iloc[:, 0]: Cumulative Price Index for Some Base Year'''
    data_frame['gri'] = data_frame.iloc[:, [-1]].div(
        data_frame.iloc[:, [-1]].shift(1)).sub(1)
    return data_frame.iloc[:, [-1]].dropna(axis=0)


def price_inverse_double(data_frame):
    '''Intent: Returns Growth Rate from Nominal & Real Prices Series;
    data_frame.iloc[:, 0]: Nominal Prices;
    data_frame.iloc[:, 1]: Real Prices'''
    data_frame['cpi'] = data_frame.iloc[:, 0].div(data_frame.iloc[:, 1])
    data_frame['gri'] = data_frame.iloc[:, [-1]].div(
        data_frame.iloc[:, [-1]].shift(1)).sub(1)
    return data_frame.iloc[:, [-1]].dropna(axis=0)


def get_price_base(df: pd.DataFrame) -> int:
    '''
    Determine Base Year

    Parameters
    ----------
    df : pd.DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Deflator
    ================== =================================

    Returns
    -------
    int
        Base Year.

    '''
    df['__deflator'] = df.iloc[:, 0].sub(100).abs()
    _b = df.iloc[:, -1].astype(float).argmin()
    df.drop(df.columns[-1], axis=1, inplace=True)
    return int(df.index[_b])


def price_cobb_douglas():
    ARCHIVE_NAME = 'dataset_usa_cobb-douglas.zip'
    data = pd.read_csv(ARCHIVE_NAME)
    SERIES_IDS = ('CDT2S1', 'CDT2S3')
    combined = pd.DataFrame()
    for series_id in SERIES_IDS:
        chunk = data[data.iloc[:, 5] == series_id].iloc[:, [6, 7]]
        chunk.set_index(chunk.columns[0], inplace=True)
        chunk.rename_axis('REF_DATE', inplace=True)
        chunk.columns = [series_id]
        combined = pd.concat([combined, chunk],
                             axis=1,
                             sort=False)
    combined['def'] = combined.iloc[:, 0].div(combined.iloc[:, 1])
    combined['prc'] = combined.iloc[:, 2].div(
        combined.iloc[:, 2].shift(1)).sub(1)
    combined.dropna(axis=0, inplace=True)
    return combined.iloc[:, [3]]


def price_census():
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    data = pd.read_csv(ARCHIVE_NAME)
    SERIES_IDS = ('P0107', 'P0110')
    combined = pd.DataFrame()
    for series_id in SERIES_IDS:
        chunk = data[data.iloc[:, 8] == series_id].iloc[:, [9, 10]]
        chunk = chunk.apply(pd.to_numeric)
        chunk.set_index(chunk.columns[0], inplace=True)
        chunk.sort_index(inplace=True)
        chunk.rename_axis('REF_DATE', inplace=True)
        chunk.columns = [series_id]
        combined = pd.concat([combined, chunk],
                             axis=1,
                             sort=False)
    combined['def'] = combined.iloc[:, 0].div(combined.iloc[:, 1])
    combined['prc'] = combined.iloc[:, 2].div(
        combined.iloc[:, 2].shift(1)).sub(1)
    combined.dropna(axis=0, inplace=True)
    return combined.iloc[:, [3]]


def price_can_a():
    FILE_NAME = '/home/alexander/projects/stat_can_cap.xlsx'
    data = pd.read_excel(FILE_NAME)
    data.set_index(data.columns[0], inplace=True)
    groups = [[[i, 5 + i] for i in range(5)],
              # [[i, 10 + i] for i in range(5)],
              [[i, 5 + i] for i in range(35, 39)],
              # [[i, 10 + i] for i in range(35, 40)],
              ]
    combined = pd.DataFrame()
    for pairs in groups:
        for pair in pairs:
            chunk = data.iloc[:, pair].dropna(axis=0)
            chunk['def'] = chunk.iloc[:, 0].div(chunk.iloc[:, 1])
            chunk['prc'] = chunk.iloc[:, 2].div(
                chunk.iloc[:, 2].shift(1)).sub(1)
            chunk.dropna(axis=0, inplace=True)
            combined = pd.concat([combined, chunk.iloc[:, [3]]],
                                 axis=1,
                                 sort=False)
            combined.plot(grid=True)
    # return combined


def price_can_b():
    FILE_NAME = '/home/alexander/projects/stat_can_cap.xlsx'
    data = pd.read_excel(FILE_NAME)
    data.set_index(data.columns[0], inplace=True)
    combined = pd.DataFrame()
    for i in [i for i in range(21, 24)]:
        chunk = data.iloc[:, [i]].dropna(axis=0)
        chunk[f'{data.columns[i]}_prc'] = chunk.iloc[:, 0].div(
            chunk.iloc[:, 0].shift(1)).sub(1)
        chunk.dropna(axis=0, inplace=True)
        combined = pd.concat([combined, chunk.iloc[:, [1]]],
                             axis=1,
                             sort=False)
    return combined


def plot_capital_purchases(df: pd.DataFrame) -> None:
    assert df.shape[1] == 27, 'Works on DataFrame Produced with `get_data_capital_purchases()`'
    plt.figure()
    plt.semilogy(
        df.loc[:, [df.columns[0], *df.columns[-3:]]],
        label=[
            '$s^{2;1}_{Cobb-Douglas}$',
            'Total',
            'Structures',
            'Equipment', ]
    )
    plt.title('Fixed Assets Purchases, {}$-${}'.format(df.index[0], df.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.legend()
    plt.grid(True)
    plt.show()


def calculate_curve_fit_params(data_frame: pd.DataFrame) -> None:
    '''
    data_frame.index: Period,
    data_frame.iloc[:, 0]: Capital,
    data_frame.iloc[:, 1]: Labor,
    data_frame.iloc[:, 2]: Product
    '''
    def _curve(regressor: pd.Series, b: float, k: float) -> pd.Series:
        return regressor.pow(k).mul(b)

    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    data_frame['lab_cap_int'] = data_frame.iloc[:, 0].div(
        data_frame.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    data_frame['lab_product'] = data_frame.iloc[:, 2].div(
        data_frame.iloc[:, 1])
    params, matrix = optimization.curve_fit(
        _curve,
        data_frame.iloc[:, -2],
        data_frame.iloc[:, -1],
        np.array([1.0, 0.5])
    )
    print('Factor, b: {:,.4f}; Index, k: {:,.4f}'.format(*params))


def plot_lab_prod_polynomial(df: pd.DataFrame) -> None:
    '''Static Labor Productivity Approximation
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Labor,
    df.iloc[:, 2]: Product
    '''
    # =========================================================================
    # TODO: Increase Cohesion
    # =========================================================================

    def _r2_scores():
        for _ in range(5):
            yield r2_score(df.iloc[:, -1], _df.iloc[:, _])

    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    # =========================================================================
    # Power Function: Labor Productivity
    # =========================================================================
    k, b = np.polyfit(np.log(df.iloc[:, -2]), np.log(df.iloc[:, -1]), deg=1)
    # =========================================================================
    # Polynomials 1, 2, 3 & 4: Labor Productivity
    # =========================================================================
    _p1 = np.polyfit(df.iloc[:, -2], df.iloc[:, -1], deg=1)
    _p2 = np.polyfit(df.iloc[:, -2], df.iloc[:, -1], deg=2)
    _p3 = np.polyfit(df.iloc[:, -2], df.iloc[:, -1], deg=3)
    _p4 = np.polyfit(df.iloc[:, -2], df.iloc[:, -1], deg=4)
    # =========================================================================
    # DataFrame for Approximation Results
    # =========================================================================
    _df = pd.DataFrame()
    _df['pow'] = df.iloc[:, -2].pow(k).mul(np.exp(b))
    _df['p_1'] = _p1[1] + df.iloc[:, -2].mul(_p1[0])
    _df['p_2'] = _p2[2] + df.iloc[:, -
                                  2].mul(_p2[1]) + df.iloc[:, -2].pow(2).mul(_p2[0])
    _df['p_3'] = _p3[3] + df.iloc[:, -2].mul(_p3[2]) + df.iloc[:, -2].pow(
        2).mul(_p3[1]) + df.iloc[:, -2].pow(3).mul(_p3[0])
    _df['p_4'] = _p4[4] + df.iloc[:, -2].mul(_p4[3]) + df.iloc[:, -2].pow(2).mul(
        _p4[2]) + df.iloc[:, -2].pow(3).mul(_p4[1]) + df.iloc[:, -2].pow(4).mul(_p4[0])
    # =========================================================================
    # Deltas
    # =========================================================================
    _df['d_pow'] = _df.iloc[:, 0].div(df.iloc[:, -1]).sub(1).abs()
    _df['d_p_1'] = _df.iloc[:, 1].div(df.iloc[:, -1]).sub(1).abs()
    _df['d_p_2'] = _df.iloc[:, 2].div(df.iloc[:, -1]).sub(1).abs()
    _df['d_p_3'] = _df.iloc[:, 3].div(df.iloc[:, -1]).sub(1).abs()
    _df['d_p_4'] = _df.iloc[:, 4].div(df.iloc[:, -1]).sub(1).abs()
    r = _r2_scores()
    plt.figure(1)
    plt.scatter(
        df.iloc[:, [-1]].index,
        df.iloc[:, [-1]],
        label='Labor Productivity'
    )
    plt.plot(
        _df.iloc[:, 0],
        label='$\\hat Y = {:.2f}X^{{{:.2f}}}, R^2 = {:.4f}$'.format(
            np.exp(b),
            k,
            next(r),
        )
    )
    plt.plot(
        _df.iloc[:, 1],
        label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X, R^2 = {:.4f}$'.format(
            1,
            *_p1[::-1],
            next(r),
        )
    )
    plt.plot(
        _df.iloc[:, 2], label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2, R^2 = {:.4f}$'.format(
            2,
            *_p2[::-1],
            next(r),
        )
    )
    plt.plot(
        _df.iloc[:, 3], label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2+{:.2f}X^3, R^2 = {:.4f}$'.format(
            3,
            *_p3[::-1],
            next(r),
        )
    )
    plt.plot(
        _df.iloc[:, 4], label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2+{:.2f}X^3 {:.2f}X^4, R^2 = {:.4f}$'.format(
            4,
            *_p4[::-1],
            next(r),
        )
    )
    plt.title('Labor Capital Intensity & Labor Productivity, {}$-${}'.format(
        df.index[0], df.index[-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(
        _df.iloc[:, 5],
        ':',
        label='$\\|\\frac{{\\hat Y-Y}}{{Y}}\\|, \\bar S = {:.4f}$'.format(
            _df.iloc[:, 5].mean()
        )
    )
    plt.plot(
        _df.iloc[:, 6],
        ':',
        label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4f}$'.format(
            1,
            _df.iloc[:, 6].mean()
        )
    )
    plt.plot(
        _df.iloc[:, 7],
        ':',
        label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4f}$'.format(
            2,
            _df.iloc[:, 7].mean()
        )
    )
    plt.plot(
        _df.iloc[:, 8],
        ':',
        label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4f}$'.format(
            3,
            _df.iloc[:, 8].mean()
        )
    )
    plt.plot(
        _df.iloc[:, 9],
        ':',
        label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4f}$'.format(
            4,
            _df.iloc[:, 9].mean()
        )
    )
    plt.title(
        'Deltas of Labor Capital Intensity & Labor Productivity, {}$-${}'.format(
            df.index[0],
            df.index[-1]
        )
    )
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_simple_linear(df: pd.DataFrame, params: tuple[float]) -> None:
    '''
    Labor Productivity on Labor Capital Intensity Plot;
    Predicted Labor Productivity Plot
    '''
    plt.figure(1)
    plt.plot(
        df.iloc[:, 0],
        df.iloc[:, 1],
        label='Original'
    )
    plt.title(
        '$Labor\ Capital\ Intensity$, $Labor\ Productivity$ Relation, {}$-${}'.format(
            df.index[0],
            df.index[-1]
        )
    )
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(
        df.iloc[:, 2],
        # =====================================================================
        # TODO:
        # label='$\\frac{{Y}{Y_{0}} = {{:,.4f}}\\frac{{L}{L_{0}}+{{:,.4f}}\\frac{{K}{K_{0}}$'.format(
        #     *params[::-1]
        # )
        # =====================================================================
        label='TBA'
    )
    plt.title(
        'Model: $\\hat Y = {:.4f}+{:.4f}\\times X$, {}$-${}'.format(
            *params[::-1],
            df.index[0],
            df.index[-1]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('$\\hat Y = Labor\ Productivity$, $X = Labor\ Capital\ Intensity$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_simple_log(df: pd.DataFrame, params: tuple[float]) -> None:
    '''
    Log Labor Productivity on Log Labor Capital Intensity Plot;
    Predicted Log Labor Productivity Plot
    '''
    plt.figure(1)
    plt.plot(
        df.iloc[:, 0],
        df.iloc[:, 1],
        label='Logarithm'
    )
    plt.title(
        '$\\ln(Labor\ Capital\ Intensity), \\ln(Labor\ Productivity)$ Relation, {}$-${}'.format(
            df.index[0],
            df.index[-1]
        )
    )
    plt.xlabel('$\\ln(Labor\ Capital\ Intensity)$')
    plt.ylabel('$\\ln(Labor\ Productivity)$')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(
        df.iloc[:, 2],
        # =====================================================================
        # TODO
        # =====================================================================
        label='$\\ln(\\frac{Y}{Y_{0}}) = %f+%f\\ln(\\frac{K}{K_{0}})+%f\\ln(\\frac{L}{L_{0}})$' % (
            *params[::-1],
            1 - params[0]
        )
    )
    plt.title('Model: $\\ln(\\hat Y) = {:.4f}+{:.4f}\\times \\ln(X)$, {}$-${}'.format(
        *params[::-1],
        df.index[0],
        df.index[-1]
        )
    )
    plt.xlabel('Period')
    plt.ylabel(
        '$\\hat Y = \\ln(Labor\ Productivity)$, $X = \\ln(Labor\ Capital\ Intensity)$'
    )
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_turnover(df: pd.DataFrame) -> None:
    '''Static Fixed Assets Turnover Approximation
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Product
    '''
    # =========================================================================
    # Fixed Assets Turnover
    # =========================================================================
    df['c_turnover'] = df.iloc[:, 1].div(df.iloc[:, 0])
    # =========================================================================
    # Linear: Fixed Assets Turnover
    # =========================================================================
    _lin = np.polyfit(df.index, df.iloc[:, -1], deg=1)
    # =========================================================================
    # Exponential: Fixed Assets Turnover
    # =========================================================================
    _exp = np.polyfit(df.index, np.log(df.iloc[:, -1]), deg=1)
    df['c_turnover_lin'] = df.index.to_series().mul(_lin[0]).add(_lin[1])
    df['c_turnover_exp'] = np.exp(df.index.to_series().mul(_exp[0]).add(_exp[1]))
    # =========================================================================
    # Deltas
    # =========================================================================
    df['d_lin'] = df.iloc[:, -2].div(df.iloc[:, -3]).sub(1).abs()
    df['d_exp'] = df.iloc[:, -2].div(df.iloc[:, -4]).sub(1).abs()
    plt.figure(1)
    plt.plot(df.iloc[:, 2], df.iloc[:, 0])
    plt.title(
        'Fixed Assets Volume to Fixed Assets Turnover, {}$-${}'.format(
            df.index[0],
            df.index[-1]
        )
    )
    plt.xlabel('Fixed Assets Turnover')
    plt.ylabel('Fixed Assets Volume')
    plt.grid(True)
    plt.figure(2)
    plt.scatter(
        df.index,
        df.iloc[:, -5],
        label='Fixed Assets Turnover'
    )
    plt.plot(
        df.iloc[:, [-4]],
        label='$\\hat K_{{l}} = {:.2f} {:.2f} t, R^2 = {:.4f}$'.format(
            *_lin[::-1],
            r2_score(df.iloc[:, -5], df.iloc[:, -4])
        )
    )
    plt.plot(
        df.iloc[:, [-3]],
        label='$\\hat K_{{e}} = \\exp ({:.2f} {:.2f} t), R^2 = {:.4f}$'.format(
            *_exp[::-1],
            r2_score(df.iloc[:, -5], df.iloc[:, -3])
        )
    )
    plt.title(
        'Fixed Assets Turnover Approximation, {}$-${}'.format(
            df.index[0],
            df.index[-1]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.plot(
        df.iloc[:, [-2]],
        ':',
        label='$\\|\\frac{{\\hat K_{{l}}-K}}{{K}}\\|, \\bar S = {:.4%}$'.format(
            df.iloc[:, -2].mean()
        )
    )
    plt.plot(
        df.iloc[:, [-1]],
        ':',
        label='$\\|\\frac{{\\hat K_{{e}}-K}}{{K}}\\|, \\bar S = {:.4%}$'.format(
            df.iloc[:, -1].mean()
        )
    )
    plt.title(
        'Deltas of Fixed Assets Turnover Approximation, {}$-${}'.format(
            df.index[0],
            df.index[-1]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.show()


def simple_linear_regression(df: pd.DataFrame):
    '''Determining of Coefficients of Regression
    df.index: Period,
    df.iloc[:, 0]: Regressor,
    df.iloc[:, 1]: Regressand
    '''
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    params, _ess, *_ = np.polyfit(
        df.iloc[:, 0],
        df.iloc[:, 1],
        deg=1,
        full=True
    )
    # =========================================================================
    # Approximation
    # =========================================================================
    df[f'{df.columns[1]}_estimate'] = df.iloc[:, 0].mul(
        params[0]).add(params[1])
    _r = r2_score(df.iloc[:, 1], df.iloc[:, -1])
    _tss = _ess[0] / (1 - _r)
    # =========================================================================
    # Delivery Block
    # =========================================================================
    print('Period From {} Through {}'.format(df.index[0], df.index[-1]))
    print('Model: Yhat = {:,.4f} + {:,.4f}*X'.format(*params[::-1]))
    print('Model Parameter: A_0 = {:,.4f}'.format(params[1]))
    print('Model Parameter: A_1 = {:,.4f}'.format(params[0]))
    print('Model Result: ESS = {:,.4f}; TSS = {:,.4f}; R^2 = {:,.4f}'.format(
        _ess[0],
        _tss,
        _r
    ))
    return df, params


def plot_cobb_douglas_complex(source_frame):
    modified_frame_a = source_frame.reset_index(level=0)
    modified_frame_b = source_frame.iloc[:, [0, 2]]
    modified_frame_b = modified_frame_b.reset_index(level=0)
    plot_cobb_douglas(source_frame)
    plot_cobb_douglas_3d(source_frame)
    plot_lab_prod_polynomial(source_frame)
    plot_block_zer(source_frame)
    plot_block_one(modified_frame_a)
    plot_block_two(modified_frame_a)
    plot_turnover(modified_frame_b)


def plot_is_lm():
    # =========================================================================
    # Read Data
    # =========================================================================
    ARCHIVE_NAME = 'dataset_rus_m1.zip'
    df = pd.read_csv(
        ARCHIVE_NAME,
        names=['period', 'prime_rate', 'm1'],
        index_col=0,
        skiprows=1,
        parse_dates=True
    )
    # =========================================================================
    # Plotting
    # =========================================================================
    plt.figure()
    plt.plot(df.iloc[:, 0], df.iloc[:, 1])
    plt.xlabel('Percentage')
    plt.ylabel('RUB, Millions')
    plt.title('M1 Dependency on Prime Rate')
    plt.grid(True)
    plt.show()


def plot_grigoriev():
    FILE_NAME = 'dataset_rus_grigoriev_v.csv'
    data_frame = pd.read_csv(FILE_NAME, index_col=1, usecols=range(2, 5))
    for series_id in sorted(set(data_frame.iloc[:, 0])):
        chunk = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1]]
        chunk.columns = [series_id]
        chunk.sort_index(inplace=True)
        chunk.plot(grid=True)


def zip_pack(archive_name, file_names):
    with zipfile.ZipFile(f'{archive_name}.zip', 'w') as z:
        for file_name in file_names:
            z.write(f'{file_name}', compress_type=zipfile.ZIP_DEFLATED)
            os.unlink(file_name)


def string_to_numeric(string):
    y, m = string.split('-')
    return int(y) + (int(m)-0.5)/12


def procedure(output_name, criteria):
    result = pd.DataFrame()
    for item in criteria:
        data = fetch_can_from_url(string_to_url(item['file_name']))
        data = data[data['VECTOR'].isin(item['series_ids'])]
        data = data[['REF_DATE', 'VECTOR', 'VALUE']]
        for series_id in item['series_ids']:
            chunk = data[data['VECTOR'] == series_id]
            chunk.set_index(chunk.columns[0], inplace=True)
            chunk = chunk.iloc[:, [1]]
            chunk = mean_by_year(chunk)
            chunk.rename(columns={'VALUE': series_id}, inplace=True)
            result = pd.concat([result, chunk], axis=1, sort=True)
    result.to_excel(output_name)


def plot_census_a(source_frame, base):
    plt.figure()
    plt.plot(source_frame.iloc[:, 0], label='Fabricant S., Shiskin J., NBER')
    plt.plot(source_frame.iloc[:, 1], color='red',
             linewidth=4, label='W.M. Persons')
    plt.plot(source_frame.iloc[:, 2], label='E. Frickey')
    plt.axvline(x=source_frame.index[base], linestyle=':')
    plt.title('US Manufacturing Indexes Of Physical Production Of Manufacturing, {}=100'.format(
        source_frame.index[base]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_b(capital_frame, deflator_frame):
    """Census Manufacturing Fixed Assets Series"""
    plt.figure(1)
    plt.semilogy(capital_frame.iloc[:, 0], label='Total')
    plt.semilogy(capital_frame.iloc[:, 1], label='Structures')
    plt.semilogy(capital_frame.iloc[:, 2], label='Equipment')
    plt.title('Manufacturing Fixed Assets, {}$-${}'.format(
        capital_frame.index[0],
        capital_frame.index[-1])
    )
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(deflator_frame)
    plt.title('Census Fused Capital Deflator, {}$-${}'.format(
        deflator_frame.index[0],
        deflator_frame.index[-1])
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.show()


def plot_census_c(source_frame, base):
    plt.figure(1)
    plt.semilogy(
        source_frame.iloc[:, 1], label='P265 - Raw Steel Produced - Total, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(
        source_frame.iloc[:, 2], label='P266 - Raw Steel Produced - Bessemer, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(
        source_frame.iloc[:, 3], label='P267 - Raw Steel Produced - Open Hearth, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(
        source_frame.iloc[:, 4], label='P268 - Raw Steel Produced - Crucible, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(
        source_frame.iloc[:, 5], label='P269 - Raw Steel Produced - Electric and All Other, {}=100'.format(source_frame.index[base[2]]))
    plt.axvline(x=source_frame.index[base[0]], linestyle=':')
    plt.axvline(x=source_frame.index[base[2]], linestyle=':')
    plt.title('Steel Production')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.semilogy(
        source_frame.iloc[:, 0], label='P262 - Rails Produced, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(
        source_frame.iloc[:, 6], label='P293 - Locomotives Produced, {}=100'.format(source_frame.index[base[1]]))
    plt.semilogy(
        source_frame.iloc[:, 7], label='P294 - Railroad Passenger Cars Produced, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(
        source_frame.iloc[:, 8], label='P295 - Railroad Freight Cars Produced, {}=100'.format(source_frame.index[base[0]]))
    plt.axvline(x=source_frame.index[base[0]], linestyle=':')
    plt.axvline(x=source_frame.index[base[1]], linestyle=':')
    plt.title('Rails & Cars Production')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_d(series_ids):
    '''series_ids: List for Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    result_frame = pd.DataFrame()
    for series_id in series_ids:
        title = fetch_usa_census_description(ARCHIVE_NAME, series_id)
        print(f'<{series_id}> {title}')
        data_frame = fetch_usa_census(ARCHIVE_NAME, series_id)
        data_frame = data_frame.div(data_frame.iloc[0, :]).mul(100)
        result_frame = pd.concat([result_frame, data_frame], axis=1, sort=True)

    plt.figure()
    plt.semilogy(result_frame)
    plt.title('Series P 231$-$300. Physical Output of Selected Manufactured Commodities: {}$-${}'.format(
        result_frame.index[0], result_frame.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend(series_ids)
    plt.show()


def plot_census_e(source_frame):
    plt.figure()
    plt.plot(source_frame.iloc[:, 0])
    plt.title('Total Immigration, {}$-${}'.format(
        source_frame.index[0],
        source_frame.index[-1])
    )
    plt.xlabel('Period')
    plt.ylabel('People')
    plt.grid(True)
    plt.show()


def plot_census_f_a(source_frame):
    plt.figure(1)
    source_frame.iloc[:, 1].plot()
    plt.title('Unemployment, Percent of Civilian Labor Force')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.figure(2)
    plt.plot(source_frame.iloc[:, 2], label='Bureau of Labour')
    plt.plot(source_frame.iloc[:, 3], label='Wolman')
    plt.title('All Manufacturing, Average Full-Time Weekly Hours, 1890-1899=100')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    source_frame.iloc[:, 6].plot()
    plt.title('Implicit Number of Workers')
    plt.xlabel('Period')
    plt.ylabel('Persons')
    plt.grid(True)
    plt.show()


def plot_census_f_b(source_frame):
    fig, axs_a = plt.subplots()
    color = 'tab:red'
    axs_a.set_xlabel('Period')
    axs_a.set_ylabel('Number', color=color)
    axs_a.plot(source_frame.iloc[:, 4], color=color, label='Stoppages')
    axs_a.set_title('Work Conflicts')
    axs_a.grid(True)
    axs_a.legend(loc=2)
    axs_a.tick_params(axis='y', labelcolor=color)
    axs_b = axs_a.twinx()
    color = 'tab:blue'
    axs_b.set_ylabel('1,000 People', color=color)
    axs_b.plot(source_frame.iloc[:, 5], color=color, label='Workers Involved')
    axs_b.legend(loc=1)
    axs_b.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()
    plt.show()


def plot_census_g(source_frame):
    plt.figure()
    plt.plot(source_frame.iloc[:, 0], label='Gross National Product')
    plt.plot(source_frame.iloc[:, 1],
             label='Gross National Product Per Capita')
    plt.title('Gross National Product, Prices {}=100, {}=100'.format(
        1958, source_frame.index[0]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_h():
    '''Census 1975, Land in Farms'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    result_frame = fetch_usa_census(ARCHIVE_NAME, 'K0005')
    plt.figure()
    plt.plot(result_frame.iloc[:, 0])
    plt.title('Land in Farms')
    plt.xlabel('Period')
    plt.ylabel('1,000 acres')
    plt.grid(True)
    plt.show()


def plot_census_i(source_frame_a, source_frame_b, source_frame_c):
    plt.figure(1)
    plt.plot(source_frame_a.iloc[:, 0], label='Exports, U1')
    plt.plot(source_frame_a.iloc[:, 1], label='Imports, U8')
    plt.plot(source_frame_a.iloc[:, 0].sub(
        source_frame_a.iloc[:, 1]), label='Net Exports')
    plt.title('Exports & Imports of Goods and Services, {}$-${}'.format(
        source_frame_a.index[0], source_frame_a.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(source_frame_b.iloc[:, 0], label='Exports, U187')
    plt.plot(source_frame_b.iloc[:, 1], label='Imports, U188')
    plt.plot(source_frame_b.iloc[:, 2], label='Net Exports, U189')
    plt.title('Total Merchandise, Gold and Silver, {}$-${}'.format(
        source_frame_b.index[0], source_frame_b.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.plot(source_frame_c.iloc[:, 0].sub(
        source_frame_c.iloc[:, 14]), label='America-Canada')
    plt.plot(source_frame_c.iloc[:, 1].sub(
        source_frame_c.iloc[:, 15]), label='America-Cuba')
    plt.plot(source_frame_c.iloc[:, 2].sub(
        source_frame_c.iloc[:, 16]), label='America-Mexico')
    plt.plot(source_frame_c.iloc[:, 3].sub(
        source_frame_c.iloc[:, 17]), label='America-Brazil')
    plt.plot(source_frame_c.iloc[:, 4].sub(
        source_frame_c.iloc[:, 18]), label='America-Other')
    plt.plot(source_frame_c.iloc[:, 5].sub(
        source_frame_c.iloc[:, 19]), label='Europe-United Kingdom')
    plt.plot(source_frame_c.iloc[:, 6].sub(
        source_frame_c.iloc[:, 20]), label='Europe-France')
    plt.plot(source_frame_c.iloc[:, 7].sub(
        source_frame_c.iloc[:, 21]), label='Europe-Germany')
    plt.plot(source_frame_c.iloc[:, 8].sub(
        source_frame_c.iloc[:, 22]), label='Europe-Other')
    plt.plot(source_frame_c.iloc[:, 9].sub(
        source_frame_c.iloc[:, 23]), label='Asia-Mainland China')
    plt.plot(source_frame_c.iloc[:, 10].sub(
        source_frame_c.iloc[:, 24]), label='Asia-Japan')
    plt.plot(source_frame_c.iloc[:, 11].sub(
        source_frame_c.iloc[:, 25]), label='Asia-Other')
    plt.plot(source_frame_c.iloc[:, 12].sub(
        source_frame_c.iloc[:, 26]), label='Australia and Oceania-All')
    plt.plot(source_frame_c.iloc[:, 13].sub(
        source_frame_c.iloc[:, 27]), label='Africa-All')
    plt.title('Net Exports')
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.legend()
    plt.figure(4)
    plt.plot(source_frame_c.iloc[:, 0].sub(source_frame_c.iloc[:, 14]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Canada')
    plt.plot(source_frame_c.iloc[:, 1].sub(source_frame_c.iloc[:, 15]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Cuba')
    plt.plot(source_frame_c.iloc[:, 2].sub(source_frame_c.iloc[:, 16]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Mexico')
    plt.plot(source_frame_c.iloc[:, 3].sub(source_frame_c.iloc[:, 17]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Brazil')
    plt.plot(source_frame_c.iloc[:, 4].sub(source_frame_c.iloc[:, 18]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='America-Other')
    plt.plot(source_frame_c.iloc[:, 5].sub(source_frame_c.iloc[:, 19]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Europe-United Kingdom')
    plt.plot(source_frame_c.iloc[:, 6].sub(source_frame_c.iloc[:, 20]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Europe-France')
    plt.plot(source_frame_c.iloc[:, 7].sub(source_frame_c.iloc[:, 21]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Europe-Germany')
    plt.plot(source_frame_c.iloc[:, 8].sub(source_frame_c.iloc[:, 22]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Europe-Other')
    plt.plot(source_frame_c.iloc[:, 9].sub(source_frame_c.iloc[:, 23]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Asia-Mainland China')
    plt.plot(source_frame_c.iloc[:, 10].sub(source_frame_c.iloc[:, 24]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Asia-Japan')
    plt.plot(source_frame_c.iloc[:, 11].sub(source_frame_c.iloc[:, 25]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Asia-Other')
    plt.plot(source_frame_c.iloc[:, 12].sub(source_frame_c.iloc[:, 26]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Australia and Oceania-All')
    plt.plot(source_frame_c.iloc[:, 13].sub(source_frame_c.iloc[:, 27]).div(
        source_frame_c.iloc[:, 28].sub(source_frame_c.iloc[:, 29])), label='Africa-All')
    plt.title('Net Exports')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_j(data_frame, base):
    plt.figure()
    plt.semilogy(data_frame,
                 label=['Currency Held by the Public',
                        'M1 Money Supply (Currency Plus Demand Deposits)',
                        'M2 Money Supply (M1 Plus Time Deposits)'])
    plt.axvline(x=data_frame.index[base], linestyle=':')
    plt.title('Currency Dynamics, {}=100'.format(data_frame.index[base]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_k():
    """Census Financial Markets & Institutions Series"""
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = (
        'X0410', 'X0411', 'X0412', 'X0413', 'X0414', 'X0415', 'X0416',
        'X0417', 'X0418', 'X0419', 'X0420', 'X0421', 'X0422', 'X0423',
        'X0580', 'X0581', 'X0582', 'X0583', 'X0584', 'X0585', 'X0586',
        'X0587', 'X0610', 'X0611', 'X0612', 'X0613', 'X0614', 'X0615',
        'X0616', 'X0617', 'X0618', 'X0619', 'X0620', 'X0621', 'X0622',
        'X0623', 'X0624', 'X0625', 'X0626', 'X0627', 'X0628', 'X0629',
        'X0630', 'X0631', 'X0632', 'X0633', 'X0741', 'X0742', 'X0743',
        'X0744', 'X0745', 'X0746', 'X0747', 'X0748', 'X0749', 'X0750',
        'X0751', 'X0752', 'X0753', 'X0754', 'X0755', 'X0879', 'X0880',
        'X0881', 'X0882', 'X0883', 'X0884', 'X0885', 'X0886', 'X0887',
        'X0888', 'X0889', 'X0890', 'X0891', 'X0892', 'X0893', 'X0894',
        'X0895', 'X0896', 'X0897', 'X0898', 'X0899', 'X0900', 'X0901',
        'X0902', 'X0903', 'X0904', 'X0905', 'X0906', 'X0907', 'X0908',
        'X0909', 'X0910', 'X0911', 'X0912', 'X0913', 'X0914', 'X0915',
        'X0916', 'X0917', 'X0918', 'X0919', 'X0920', 'X0921', 'X0922',
        'X0923', 'X0924', 'X0925', 'X0926', 'X0927', 'X0928', 'X0929',
        'X0930', 'X0931', 'X0932', 'X0947', 'X0948', 'X0949', 'X0950',
        'X0951', 'X0952', 'X0953', 'X0954', 'X0955', 'X0956',
    )
    for _, series_id in enumerate(SERIES_IDS, start=1):
        title = fetch_usa_census_description(ARCHIVE_NAME, series_id)
        data_frame = fetch_usa_census(ARCHIVE_NAME, series_id)
        data_frame = data_frame.div(data_frame.iloc[0, :]).mul(100)
        plt.figure(_)
        plt.plot(data_frame, label=f'{series_id}')
        plt.title('{}, {}$-${}'.format(title,
                  data_frame.index[0], data_frame.index[-1]))
        plt.xlabel('Period')
        plt.ylabel('Percentage')
        plt.grid(True)
        plt.legend()
        plt.show()


def plot_growth_elasticity(df: pd.DataFrame) -> None:
    '''Growth Elasticity Plotting
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    # =========================================================================
    # TODO: Increase Cohesion of This Code: Send Plotting to Separate Function
    # =========================================================================
    df.reset_index(level=0, inplace=True)
    _df = pd.DataFrame()
    # =========================================================================
    # Period, Centered
    # =========================================================================
    _df[f'{df.columns[0]}'] = df.iloc[:, [0]].rolling(2).mean()
    df.index.to_series().rolling(2).mean()
    # =========================================================================
    # Series, Centered
    # =========================================================================
    _df[f'{df.columns[1]}_centered'] = df.iloc[:, [1]].rolling(2).mean()
    # =========================================================================
    # Series, Growth Rate
    # =========================================================================
    _df[f'{df.columns[1]}_growth_rate'] = df.iloc[:, [1]].sub(
        df.iloc[:, [1]].shift(2)).div(df.iloc[:, [1]].rolling(2).sum().shift(1))
    # =========================================================================
    # Series, Elasticity
    # =========================================================================
    _df[f'{df.columns[1]}_elasticity'] = df.iloc[:, [1]].rolling(2).sum(
    ).shift(-1).mul(2).div(df.iloc[:, [1]].rolling(4).sum().shift(-1)).sub(1)
    _df.set_index(_df.columns[0], inplace=True)
    _df.dropna(inplace=True)
    plt.figure()
    plt.plot(_df.iloc[:, [1]], label='Growth Rate')
    plt.plot(_df.iloc[:, [2]], label='Elasticity Rate')
    plt.title('Growth & Elasticity Rates')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_douglas(source, dictionary, num, start, stop, step, title, measure, label=None):
    '''
    source: Source Database,
    dictionary: Dictionary of Series IDs to Series Titles from Source Database,
    num: Plot Number,
    start: Start Series Code,
    stop: Stop Series Code,
    step: Step for Series IDs,
    title: Plot Title,
    measure: Dimenstion for Series,
    label: Additional Sublabels'''
    plt.figure(num)
    for i in range(start, stop, step):
        plt.plot(fetch_usa_classic(
            source, dictionary.iloc[i, 0]), label=dictionary.iloc[i, 1])
    plt.title(title)
    plt.xlabel('Period')
    plt.ylabel(measure)
    plt.grid(True)
    if label is None:
        plt.legend()
    else:
        plt.legend(label)


def _m_spline_print_params(n_spans: int, params: tuple[float]) -> None:
    '''
    Results Delivery Function
    ================== =================================
    n_spans            Number of Spans
    params             Coefficients
    ================== =================================
    '''
    if n_spans == len(params):
        for _, _param in enumerate(params, start=1):
            print(f'Model Parameter: K{_:02d} = {_param:.6f}')
    else:
        # =====================================================================
        # n_spans (1 + N): 1 + Number of Spans
        # =====================================================================
        for _, _param in enumerate(params):
            print(f'Model Parameter: A{_:02n} = {_param:.6f}')


def plot_capital_modelling(df: pd.DataFrame, base) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Investment
    df.iloc[:, 1]      Production
    df.iloc[:, 2]      Capital
    df.iloc[:, 3]      Capital Retirement
    ================== =================================
    '''
    _params_i = np.polyfit(
        df.index.to_series(),
        df.iloc[:, 0].div(df.iloc[:, 1]).astype(float),
        deg=1
    )
    _params_t = np.polyfit(
        df.index.to_series(),
        df.iloc[:, 1].div(df.iloc[:, 2]).astype(float),
        deg=1
    )
    _df = df.copy()
    # =========================================================================
    # Gross Fixed Investment to Gross Domestic Product Ratio
    # =========================================================================
    _df['inv_to_pro'] = _df.index.to_series().mul(
        _params_i[0]).add(_params_i[1])
    # =========================================================================
    # Fixed Assets Turnover
    # =========================================================================
    _df['c_turnover'] = _df.index.to_series().mul(
        _params_t[0]).add(_params_t[1])
    _df['cap_a'] = calculate_capital(df, _params_i, _params_t, 0.875)
    _df['cap_b'] = calculate_capital(df, _params_i, _params_t, 1)
    _df['cap_c'] = calculate_capital(df, _params_i, _params_t, 1.125)
    plt.figure(1)
    plt.title(
        'Fixed Assets Turnover ($\\lambda$) for the US, {}$-${}'.format(
            _df.index[0], _df.index[-1]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(_df.iloc[:, 1].div(_df.iloc[:, 2]), label='$\\lambda$')
    label = '$\\lambda = {1:,.4f}\\ {0:,.4f}\\times t$'.format(
        *_params_t) if _params_t[0] < 0 else '$\\lambda = {1:,.4f} + {0:,.4f} \\times t$'.format(*_params_t)
    plt.plot(_df.iloc[:, -4], label=label)
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title(
        'Gross Fixed Investment as Percentage of GDP ($S$) for the US, {}$-${}'.format(
            _df.index[0], _df.index[-1]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(_df.iloc[:, 0].div(_df.iloc[:, 1]), label='$S$')
    label = '$S = {1:,.4f}\\ {0:,.4f}\\times t$'.format(
        *_params_i) if _params_i[0] < 0 else '$S = {1:,.4f} + {0:,.4f} \\times t$'.format(*_params_i)
    plt.plot(_df.iloc[:, -5], label=label)
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.title(
        '$\\alpha$ for the US, {}$-${}'.format(
            _df.index[0], _df.index[-2]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(_df.iloc[:, 3], label='$\\alpha$')
    plt.grid(True)
    plt.legend()
    plt.figure(4)
    plt.title('$K$ for the US, {}$-${}'.format(_df.index[0], _df.index[-2]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars, {}=100'.format(_df.index[base]))
    plt.semilogy(
        _df.iloc[:, -3:],
        label=['$K\\left(\\pi = \\frac{7}{8}\\right)$',
               '$K\\left(\\pi = 1\\right)$',
               '$K\\left(\\pi = \\frac{9}{8}\\right)$', ]
    )
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_fourier_discrete(df: pd.DataFrame, precision: int = 10) -> None:
    '''
    Discrete Fourier Transform based on Simpson's Rule
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Target Series
    ================== =================================
    '''
    _df = df.copy()
    precision += 1
    _p = np.polyfit(
        _df.index,
        _df.iloc[:, 0].astype(float),
        deg=1
    )
    _df['period_calibrated'] = _df.index.to_series().sub(
        _df.index[0]).div(_df.shape[0]).mul(2).mul(np.pi)
    _df[f'{_df.columns[0]}_line'] = _df.index.to_series().mul(_p[0]).add(_p[1])
    _df[f'{_df.columns[0]}_wave'] = _df.iloc[:, 0].sub(_df.iloc[:, 2])
    # =========================================================================
    # DataFrame for Fourier Coefficients
    # =========================================================================
    _fourier = pd.DataFrame(columns=['cos', 'sin'])
    for _ in range(precision):
        _fourier.loc[_] = [
            _df.iloc[:, 3].mul(np.cos(_df.iloc[:, 1].mul(_))).mul(2).mean(),
            _df.iloc[:, 3].mul(np.sin(_df.iloc[:, 1].mul(_))).mul(2).mean()
        ]
    # =========================================================================
    # First Entry Correction
    # =========================================================================
    _fourier.loc[0, 'cos'] /= 2
    plt.figure()
    plt.title(f'$\\alpha$ for the US, {_df.index[0]}$-${_df.index[-1]}')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(_df.index, _df.iloc[:, 0], label='$\\alpha$')
    _df[f'{_df.columns[0]}_fourier_{0}'] = np.cos(_df.iloc[:, 1].mul(0)).mul(
        _fourier.loc[0, 'cos']).add(np.sin(_df.iloc[:, 1].mul(0)).mul(_fourier.loc[0, 'sin']))
    for _ in range(1, precision):
        _df[f'{_df.columns[0]}_fourier_{_}'] = _df.iloc[:, -1].add(np.cos(_df.iloc[:, 1].mul(_)).mul(
            _fourier.loc[_, 'cos'])).add(np.sin(_df.iloc[:, 1].mul(_)).mul(_fourier.loc[_, 'sin']))
        plt.plot(_df.iloc[:, 2].add(_df.iloc[:, -1]),
                 label=f'$FT_{{{_:02}}}(\\alpha)$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_elasticity(df: pd.DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Real Values for Price Deflator
    df.iloc[:, 1]      Nominal Values for Price Deflator
    df.iloc[:, 2]      Focused Series
    ================== =================================
    '''
    df.iloc[:, -1] = pd.to_numeric(df.iloc[:, -1], errors='coerce')
    df.dropna(inplace=True)
    # =========================================================================
    # TODO: Separate Basic Year Function
    # =========================================================================
    df['__deflator'] = df.iloc[:, 0].div(df.iloc[:, 1]).sub(1).abs()
    _b = df.iloc[:, -1].astype(float).argmin()
    df.drop(df.columns[-1], axis=1, inplace=True)
    _title = (
        'National Income' if df.columns[2] == 'A032RC1' else 'Series',
        df.columns[2],
        df.index[_b],
    )
    df[f'{df.columns[2]}_real'] = df.iloc[:, 0].mul(
        df.iloc[:, 2]).div(df.iloc[:, 1])
    df[f'{df.columns[2]}_centered'] = df.iloc[:, 3].rolling(2).mean()
    # =========================================================================
    # \dfrac{x_{k} - x_{k-1}}{\dfrac{x_{k} + x_{k-1}}{2}}
    # =========================================================================
    df[f'{df.columns[2]}_elasticity_a'] = df.iloc[:, 3].sub(
        df.iloc[:, 3].shift(1)).div(df.iloc[:, -1])
    # =========================================================================
    # \frac{x_{k+1} - x_{k-1}}{2 x_{k}}
    # =========================================================================
    df[f'{df.columns[2]}_elasticity_b'] = df.iloc[:,
                                                  3].shift(-1).sub(df.iloc[:, 3].shift(1)).div(df.iloc[:, 3]).div(2)
    # =========================================================================
    # 2 \times \frac{x_{k+1} - x_{k-1}}{x_{k-1} + 2 x_{k} + x_{k+1}}
    # =========================================================================
    df[f'{df.columns[2]}_elasticity_c'] = df.iloc[:, 3].shift(-1).sub(df.iloc[:, 3].shift(1)).div(
        df.iloc[:, 3].mul(2).add(df.iloc[:, 3].shift(-1)).add(df.iloc[:, 3].shift(1))).mul(2)
    # =========================================================================
    # \frac{-x_{k-1} - x_{k} + x_{k+1} + x_{k+2}}{2 \times (x_{k} + x_{k+1})}
    # =========================================================================
    df[f'{df.columns[2]}_elasticity_d'] = df.iloc[:, 3].shift(-1).add(df.iloc[:, 3].shift(-2)).sub(
        df.iloc[:, 3].shift(1)).sub(df.iloc[:, 3]).div(df.iloc[:, 3].add(df.iloc[:, 3].shift(-1)).mul(2))
    plt.figure(1)
    plt.title('{}, {}, {}=100'.format(*_title))
    plt.xlabel('Period')
    plt.ylabel(f'Billions of Dollars, {_title[2]}=100')
    plt.plot(df.iloc[:, [3]], label=f'{_title[1]}')
    plt.plot(
        df.index.to_series().rolling(2).mean(),
        df.iloc[:, 4],
        label=f'{_title[1]}, Rolling Mean, Window = 2'
    )
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Elasticity: {}, {}, {}=100'.format(*_title))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(
        df.index.to_series().rolling(2).mean(),
        df.iloc[:, 5],
        label='$\\overline{E}_{T+\\frac{1}{2}}$'
    )
    plt.plot(df.iloc[:, [6]], label='$E_{T+1}$')
    plt.plot(df.iloc[:, [7]], label='$\\overline{E}_{T+1}$')
    plt.plot(
        df.index.to_series().rolling(2).mean(),
        df.iloc[:, 8],
        label='$\\overline{\\epsilon(E_{T+\\frac{1}{2}})}$'
    )
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.title('Elasticity: {}, {}, {}=100'.format(*_title))
    plt.xlabel('{}, {}, {}=100'.format(*_title))
    plt.ylabel('Elasticity: {}, {}, {}=100'.format(*_title))
    plt.plot(df.iloc[:, 3], df.iloc[:, 8], label='$\\frac{\\epsilon(X)}{X}$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_kol_zur_filter(data_frame: pd.DataFrame):
    '''Kolmogorov--Zurbenko Filter
        data_frame.index: Period,
        data_frame.iloc[:, 0]: Series
    '''
    data_frame_o, data_frame_e, residuals_o, residuals_e = kol_zur_filter(data_frame)

    plt.figure(1)
    plt.title('Kolmogorov$-$Zurbenko Filter')
    plt.xlabel('Period')
    plt.ylabel('Measure')
    plt.scatter(
        data_frame_o.iloc[:, [0]].index,
        data_frame_o.iloc[:, [0]],
        label='Original Series'
    )
    plt.plot(
        data_frame_o.iloc[:, 1:],
        label=['$KZF(\\lambda = {})$'.format(int(_.split('_')[-1], 16))
               for _ in data_frame_o.columns[1:]]
    )
    plt.plot(
        data_frame_e,
        label=['$KZF(\\lambda = {})$'.format(int(_.split('_')[-1], 16))
               for _ in data_frame_e.columns]
    )
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Kolmogorov$-$Zurbenko Filter Residuals')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(
        residuals_o.iloc[:, [0]].index,
        residuals_o.iloc[:, [0]],
        label='Residuals'
    )
    plt.plot(
        residuals_o.iloc[:, 1:],
        label=['$\\delta KZF(\\lambda = {})$'.format(int(_.split('_')[-1], 16))
               for _ in residuals_o.columns[1:]]
    )
    plt.plot(
        residuals_e,
        label=['$\\delta KZF(\\lambda = {})$'.format(int(_.split('_')[-1], 16))
               for _ in residuals_e.columns]
    )
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_pearson_r_test(df: pd.DataFrame) -> None:
    '''
    Left-Side & Right-Side Rolling Means' Calculation & Plotting
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Target Series
    ================== =================================
    '''
    _pearson = pd.DataFrame(columns=['right_to_left_ratio'])
    for _ in range(1 + df.shape[0] // 2):
        # =====================================================================
        # Shift Mean Values to Left
        # =====================================================================
        _l_frame = df.iloc[:, 0].rolling(1 + _).mean().shift(-_)
        # =====================================================================
        # Shift Mean Values to Right
        # =====================================================================
        _r_frame = df.iloc[:, 0].rolling(1 + _).mean()
        _pearson.loc[_] = [
            stats.pearsonr(df.iloc[:, 0][_r_frame.notna()], _r_frame.dropna())[0] /
            stats.pearsonr(
                df.iloc[:, 0][_l_frame.notna()], _l_frame.dropna())[0]
        ]
    # =========================================================================
    # Plot 'Window' to 'Right-Side to Left-Side Pearson R
    # =========================================================================
    plt.figure()
    plt.title('Right-Side to Left-Side Pearson R Ratio')
    plt.xlabel('`Window`')
    plt.ylabel('Index')
    plt.plot(_pearson, label='Right-Side to Left-Side Pearson R Ratio')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_rolling_mean_filter(data_frame: pd.DataFrame):
    '''Rolling Mean Filter
        data_frame.index: Period;
        data_frame.iloc[:, 0]: Series
    '''
    data_frame_o, data_frame_e, residuals_o, residuals_e = rolling_mean_filter(data_frame)
    plt.figure(1)
    plt.title(
        f'Rolling Mean {data_frame_o.index[0]}$-${data_frame_o.index[-1]}'
    )
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.scatter(
        data_frame_o.iloc[:, [0]].index,
        data_frame_o.iloc[:, [0]],
        label='Original Series'
    )
    plt.plot(
        data_frame_o.iloc[:, 1:],
        label=['$\\hat Y_{{m = {}}}$'.format(int(_.split('_')[-1], 16))
               for _ in data_frame_o.columns[1:]]
    )
    plt.plot(
        data_frame_e,
        label=['$\\hat Y_{{m = {}}}$'.format(int(_.split('_')[-1], 16))
               for _ in data_frame_e.columns]
    )
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title(
        f'Rolling Mean Residuals {data_frame_o.index[0]}$-${data_frame_o.index[-1]}'
    )
    plt.xlabel('Period')
    plt.ylabel('Residuals ($\\delta$), Percent')
    plt.scatter(
        residuals_o.iloc[:, [0]].index,
        residuals_o.iloc[:, [0]],
        label='Residuals'
    )

    plt.plot(
        residuals_o.iloc[:, 1:],
        label=['$\\delta(\\hat Y_{{m = {}}})$'.format(int(_.split('_')[-1], 16))
               for _ in residuals_o.columns[1:]]
    )
    plt.plot(
        residuals_e,
        label=['$\\delta(\\hat Y_{{m = {}}})$'.format(int(_.split('_')[-1], 16))
               for _ in residuals_e.columns]
    )
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_ewm(df: pd.DataFrame, step: float = 0.1) -> None:
    '''Single Exponential Smoothing
    Robert Goodell Brown, 1956
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Target Series
    ================== =================================
    '''
    _alpha = 0.25
    # =========================================================================
    # DataFrame for Exponentially Smoothed Series
    # =========================================================================
    _smooth = df.copy()
    while True:
        if _alpha >= 1:
            break
        _smooth = pd.concat(
            [
                _smooth,
                _smooth.iloc[:, [0]].ewm(alpha=_alpha, adjust=False).mean()
            ],
            axis=1
        )
        _smooth.columns = [
            *_smooth.columns[:-1], f'{_smooth.columns[0]}_{_alpha:,.2f}',
        ]
        _alpha += step
    # =========================================================================
    # DataFrame for Deltas of Exponentially Smoothed Series
    # =========================================================================
    _deltas = pd.concat(
        [
            _smooth.iloc[:, [_]].div(
                _smooth.iloc[:, [_]].shift(-1)).rsub(1).dropna()
            for _ in range(_smooth.shape[1])
        ],
        axis=1
    )
    _deltas.index = _smooth.index.to_series().rolling(2).mean().dropna()
    # =========================================================================
    # Plotting
    # =========================================================================
    _labels = [
        'Original Series',
        *[
            'Smoothing: $\\alpha={:,.2f}$'.format(float(column.split('_')[-1])) for column in _smooth.columns[1:]
        ]
    ]
    plt.figure(1)
    plt.title('Exponentially Smoothed Series')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(_smooth.index, _smooth.iloc[:, 0])
    plt.plot(_smooth.iloc[:, 1:])
    plt.grid(True)
    plt.legend(_labels)
    plt.figure(2)
    plt.title('Deltas of Exponentially Smoothed Series')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(_deltas.index, _deltas.iloc[:, 0])
    plt.plot(_deltas.iloc[:, 1:])
    plt.grid(True)
    plt.legend(_labels)
    plt.show()


def plot_e(df: pd.DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Investment
    df.iloc[:, 1]      Production
    df.iloc[:, 2]      Capital
    ================== =================================
    '''
    # =========================================================================
    # Investment to Production Ratio
    # =========================================================================
    df['inv_to_pro'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Fixed Assets Turnover Ratio
    # =========================================================================
    df['c_turnover'] = df.iloc[:, 1].div(df.iloc[:, 2])
    _params_i = np.polyfit(
        df.iloc[:, 0],
        df.iloc[:, 1],
        deg=1
    )
    _params_t = np.polyfit(
        df.iloc[:, 1].astype(float),
        df.iloc[:, 2].astype(float),
        deg=1
    )
    df['inv_to_pro_lin'] = df.iloc[:, 0].mul(_params_i[0]).add(_params_i[1])
    df['c_turnover_lin'] = df.iloc[:, 2].mul(_params_t[0]).add(_params_t[1])
    plt.figure()
    plt.semilogy(df.iloc[:, 0], df.iloc[:, 1])
    plt.semilogy(df.iloc[:, 0], df.iloc[:, 5])
    plt.title(
        'Investment to Production Ratio, {}$-${}'.format(
            df.index[0],
            df.index[-1]
        )
    )
    plt.xlabel('Investment, Billions of Dollars')
    plt.ylabel('Gross Domestic Product, Billions of Dollars')
    plt.grid(True)
    plt.legend(
        [
            '$P(I)$',
            '$\\hat{{P(I)}} = {:.4f}+{:.4f} I$'.format(*_params_i[::-1])
        ]
    )
    print(df.iloc[:, 3].describe())
    print(_params_i)
    print(df.iloc[:, 4].describe())
    print(_params_t)
    plt.show()


def plot_kurenkov(data_frames: tuple[pd.DataFrame]) -> None:
    '''
    data_frames[0]: Production DataFrame,
    data_frames[1]: Labor DataFrame,
    data_frames[2]: Capital DataFrame,
    data_frames[3]: Capacity Utilization DataFrame'''
    # =========================================================================
    # Plotting
    # =========================================================================
    fig, axs = plt.subplots(4, 1)
    axs[0].plot(
        data_frames[0],
        label=[
            'Kurenkov Data, 1950=100',
            'BEA Data, 1950=100',
            'FRB Data, 1950=100',
        ]
    )
    axs[0].set_title('Production')
    axs[0].set_xlabel('Period')
    axs[0].set_ylabel('Percentage')
    axs[0].legend()
    axs[0].grid(True)
    axs[1].plot(
        data_frames[1],
        label=[
            'Kurenkov Data',
            'BEA Data',
        ]
    )
    axs[1].set_title('Labor')
    axs[1].set_xlabel('Period')
    axs[1].set_ylabel('Thousands of Persons')
    axs[1].legend()
    axs[1].grid(True)
    # =========================================================================
    # Revised Capital
    # =========================================================================
    axs[2].plot(
        data_frames[2],
        label=[
            'Kurenkov Data, 1951=100',
            'BEA Data, 1951=100',
        ]
    )
    axs[2].set_title('Capital')
    axs[2].set_xlabel('Period')
    axs[2].set_ylabel('Percentage')
    axs[2].legend()
    axs[2].grid(True)
    axs[3].plot(
        data_frames[3],
        label=[
            'Kurenkov Data',
            'FRB Data',
        ]
    )
    axs[3].set_title('Capacity Utilization')
    axs[3].set_xlabel('Period')
    axs[3].set_ylabel('Percentage')
    axs[3].legend()
    axs[3].grid(True)
    fig.set_size_inches(10., 20.)


def plot_census_complex(source_frame):
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    plot_pearson_r_test(source_frame)
    plot_kol_zur_filter(source_frame)
    plot_ewm(source_frame)


def m_spline_processing(df: pd.DataFrame, kernel: callable) -> None:
    '''
    Interactive Shell for Processing Make Shift Spline Functions

    Parameters
    ----------
    df : pd.DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Target Series
    ================== =================================
    kernel : callable
        One Out of m_spline_ea(), m_spline_eb(), m_spline_la(), m_spline_lb(), m_spline_lls().

    Returns
    -------
    None
        Draws matplotlib.pyplot Plots.
    '''
    df.reset_index(level=0, inplace=True)
    df.columns = ['Period', 'Original']
    # =========================================================================
    # Number of Periods
    # =========================================================================
    N = int(input('Define Number of Interpolation Spans (N, N >= 2): '))
    print(f'Number of Spans Provided: {N}')
    assert N >= 2, f'N >= 2 is Required, N = {N} Was Provided'
    # =========================================================================
    # Switch Knots
    # =========================================================================
    _knots = [0, ]
    _ = 0
    # =========================================================================
    # Although N >=2, Left for Consistency Purpose Only
    # =========================================================================
    if N == 1:
        _knots.append(df.index[-1])
    elif N >= 2:
        while _ < N:
            if 1 + _ == N:
                _knots.append(df.index[-1])
            else:
                _knot = int(input('Select Row for Year: ')) - 1
                # =============================================================
                # Ensure Knots Are In Ascending Order
                # =============================================================
                if _knot > _knots[_]:
                    _knots.append(_knot)
            _ += 1
    else:
        # =====================================================================
        # Should Never Happen
        # =====================================================================
        print('Error')
    _knots = tuple(_knots)
    splined_frame, _params = kernel(df, N, _knots)
    _m_spline_print_params(N, _params)
    _m_spline_error_metrics(splined_frame)
    plt.figure()
    plt.scatter(splined_frame.iloc[:, 0], splined_frame.iloc[:, 1])
    plt.plot(
        splined_frame.iloc[:, 0],
        splined_frame.iloc[:, 2],
        color='red',
        label='$s_{}(\\tau)$'.format(0,)
    )
    _go_no_go = input('Does the Resulting Series Need an Improvement?, Y: ')
    if _go_no_go.lower() == 'y':
        assert len(_knots) == 1 + N
        _correction_factors = [
            float(input(f'Correction Factor of Knot {1 + _:02d} out of {len(_knots):02d}: '))
            for _, _knot in enumerate(_knots)
        ]
        # =====================================================================
        # Series Modification
        # =====================================================================
        modified = df.copy()
        for _knot, _factor in zip(_knots, _correction_factors):
            modified.iloc[_knot, 1] = modified.iloc[_knot, 1]*_factor

        modified.columns = ['Period', 'Corrected']
        splined_frame, _params = kernel(modified, N, _knots)
        _m_spline_print_params(N, _params)
        _m_spline_error_metrics(splined_frame)
        plt.plot(
            splined_frame.iloc[:, 0],
            splined_frame.iloc[:, 2],
            color='g',
            label='$s_{}(\\tau)$'.format(1,)
        )
    plt.grid(True)
    plt.legend()
    plt.show()


def test_douglas() -> None:
    '''
    Data Consistency Test

    Returns
    -------
    None

    '''
    _kwargs = (
        {
            'archive_name': 'dataset_usa_census1949.zip',
            'series_id': 'J0014',
        },
        {
            'archive_name': 'dataset_douglas.zip',
            'series_id': 'DT24AS01',
        },
    )
    data = pd.concat(
        [
            partial(fetch_usa_census, **_kwargs[0])(),
            partial(fetch_usa_classic, **_kwargs[1])(),
        ],
        axis=1)
    _loc = _kwargs[0]['series_id']
    data.loc[:, [_loc]] = data.loc[:, [_loc]].div(data.loc[1899, [_loc]]).mul(100).round(0)
    data['dif'] = data.iloc[:, 1].sub(data.iloc[:, 0])
    data.dropna().plot(title='Cobb--Douglas Data Comparison', legend=True, grid=True)
    _kwargs = (
        {
            # =================================================================
            # Cobb C.W., Douglas P.H. Capital Series: Total Fixed Capital in 1880 dollars (4)
            # =================================================================
            'archive_name': 'dataset_usa_cobb-douglas.zip',
            'series_id': 'CDT2S4',
        },
        {
            'archive_name': 'dataset_douglas.zip',
            'series_id': 'DT63AS01',
        },
    )
    data = pd.concat(
        [
            partial(fetch_usa_classic, **kwargs)() for kwargs in _kwargs
        ],
        axis=1)
    data['div'] = data.iloc[:, 0].div(data.iloc[:, 1])
    data.dropna().plot(title='Cobb--Douglas Data Comparison', legend=True, grid=True)


def options():
    ARCHIVE_NAME = 'dataset_douglas.zip'
    SERIES_IDS = (
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01',
        # =====================================================================
        # Not Suitable: Total Capital (in millions of 1880 dollars)
        # =====================================================================
        'DT63AS01',
        # =====================================================================
        # Not Suitable: Annual Increase (in millions of 1880 dollars)
        # =====================================================================
        'DT63AS02',
        # =====================================================================
        # Not Suitable: Percentage Rate of Growth
        # =====================================================================
        'DT63AS03',
    )
    [print(fetch_usa_classic(ARCHIVE_NAME, series_id))
     for series_id in SERIES_IDS]
