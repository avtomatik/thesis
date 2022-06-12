#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 12:25:52 2022

@author: alexander
"""


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
            *df.index[[_b, 0, -1]]
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
            *df.index[[_b, 0, -1]]
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
            *df.index[[_b, 0, -1]]
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
            *df.index[[_b, 0, -1]]
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
            *df.index[[_b, 0, -1]]
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
    plt.title('Product, {}=100, {}$-${}'.format(*df.index[[_b, 0, -1]]))
    plt.xlabel('Period')
    plt.ylabel(f'Product, {_df.index[_b]}=100')
    plt.plot(_df.iloc[:, 2])
    plt.grid(True)
    plt.figure(2)
    plt.title('Capital, {}=100, {}$-${}'.format(*df.index[[_b, 0, -1]]))
    plt.xlabel('Period')
    plt.ylabel(f'Capital, {_df.index[_b]}=100')
    plt.plot(_df.iloc[:, 3])
    plt.grid(True)
    plt.figure(3)
    plt.title(
        'Fixed Assets Turnover ($\\lambda$), {}=100, {}$-${}'.format(*
                                                                     df.index[[_b, 0, -1]])
    )
    plt.xlabel('Period')
    plt.ylabel(f'Fixed Assets Turnover ($\\lambda$), {_df.index[_b]}=100')
    plt.plot(_df.iloc[:, 2].div(_df.iloc[:, 3]))
    plt.grid(True)
    plt.figure(4)
    plt.title(
        'Investment to Gross Domestic Product Ratio, {}=100, {}$-${}'.format(
            *df.index[[_b, 0, -1]])
    )
    plt.xlabel('Period')
    plt.ylabel(
        f'Investment to Gross Domestic Product Ratio, {_df.index[_b]}=100'
    )
    plt.plot(_df.iloc[:, 7])
    plt.grid(True)
    plt.figure(5)
    plt.title(
        '$\\alpha(t)$, Fixed Assets Retirement Ratio, {}=100, {}$-${}'.format(*
                                                                              df.index[[_b, 0, -1]])
    )
    plt.xlabel('Period')
    plt.ylabel(f'$\\alpha(t)$, {_df.index[_b]}=100')
    plt.plot(_df.iloc[:, 9])
    plt.grid(True)
    plt.figure(6)
    plt.title(
        'Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, {}=100, {}$-${}'.format(
            *df.index[[_b, 0, -1]])
    )
    plt.xlabel(f'$\\alpha(t)$, {_df.index[_b]}=100')
    plt.ylabel(f'Fixed Assets Retirement Value, {_df.index[_b]}=100')
    plt.plot(_df.iloc[:, 9], _df.iloc[:, 8])
    plt.grid(True)
    plt.figure(7)
    plt.title(
        'Labor Capital Intensity, {}=100, {}$-${}'.format(*df.index[[_b, 0, -1]]))
    plt.xlabel(f'Labor Capital Intensity, {_df.index[_b]}=100')
    plt.ylabel(f'Labor Productivity, {_df.index[_b]}=100')
    plt.plot(np.exp(_df.iloc[:, 5]), np.exp(_df.iloc[:, 6]))
    plt.grid(True)
    plt.show()


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
            *df.index[[0, -1]]
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
    print(
        f'Model Parameter: A: = (U_2-U_1)/(TAU_2-TAU_1)**Alpha = {_param:,.4f};')
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
    df[f'estimate_{df.columns[-1]}'] = df.iloc[:,
                                               0].rdiv(params[0]).pow(_alpha).mul(params[2])
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


def kol_zur_filter(df: pd.DataFrame, k: int = None) -> tuple[pd.DataFrame]:
    '''Kolmogorov--Zurbenko Filter
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Target Series
    ================== =================================
    '''
    if k is None:
        k = df.shape[0] // 2
    df.reset_index(level=0, inplace=True)
    # =========================================================================
    # DataFrame for Kolmogorov--Zurbenko Filter Results: Odd
    # =========================================================================
    df_o = pd.concat(
        [
            # =================================================================
            # No Period Shift
            # =================================================================
            df,
        ],
        axis=1
    )
    # =========================================================================
    # DataFrame for Kolmogorov--Zurbenko Filter Results: Even
    # =========================================================================
    df_e = pd.concat(
        [
            # =================================================================
            # Period Shift
            # =================================================================
            df.iloc[:, [0]].rolling(2).mean(),
        ],
        axis=1
    )
    # =========================================================================
    # DataFrame for Kolmogorov--Zurbenko Filter Residuals: Odd
    # =========================================================================
    residuals_o = pd.concat(
        [
            # =================================================================
            # Period Shift
            # =================================================================
            df.iloc[:, [0]].rolling(2).mean(),
        ],
        axis=1
    )
    # =========================================================================
    # DataFrame for Kolmogorov--Zurbenko Filter Residuals: Even
    # =========================================================================
    residuals_e = pd.concat(
        [
            # =================================================================
            # No Period Shift
            # =================================================================
            df.iloc[:, [0]],
        ],
        axis=1
    )
    chunk = df.iloc[:, [1]]
    for _ in range(k):
        chunk = chunk.rolling(2).mean()
        if _ % 2 == 1:
            # =================================================================
            # DataFrame for Kolmogorov--Zurbenko Filter Results: Odd
            # =================================================================
            df_o = pd.concat(
                [
                    df_o,
                    chunk.shift(-((1 + _) // 2)),
                ],
                axis=1
            )
            df_o.columns = [*df_o.columns[:-1],
                            f'{df.columns[1]}_{hex(2 + _)}', ]
            # =================================================================
            # DataFrame for Kolmogorov--Zurbenko Filter Residuals: Odd
            # =================================================================
            residuals_o = pd.concat(
                [
                    residuals_o,
                    df_o.iloc[:, [-2]
                              ].div(df_o.iloc[:, [-2]].shift(1)).sub(1),
                ],
                axis=1
            )
        else:
            # =================================================================
            # DataFrame for Kolmogorov--Zurbenko Filter Results: Even
            # =================================================================
            df_e = pd.concat(
                [
                    df_e,
                    chunk.shift(-((1 + _) // 2)),
                ],
                axis=1
            )
            df_e.columns = [*df_e.columns[:-1],
                            f'{df.columns[1]}_{hex(2 + _)}', ]
            # =================================================================
            # DataFrame for Kolmogorov--Zurbenko Filter Residuals: Even
            # =================================================================
            residuals_e = pd.concat(
                [
                    residuals_e,
                    df_e.iloc[:, [-1]
                              ].shift(-1).div(df_e.iloc[:, [-1]]).sub(1),
                ],
                axis=1
            )
    df_o.set_index(df_o.columns[0], inplace=True)
    df_e.set_index(df_e.columns[0], inplace=True)
    residuals_o.set_index(residuals_o.columns[0], inplace=True)
    residuals_e.set_index(residuals_e.columns[0], inplace=True)
    df_o.dropna(how='all', inplace=True)
    df_e.dropna(how='all', inplace=True)
    residuals_o.dropna(how='all', inplace=True)
    residuals_e.dropna(how='all', inplace=True)
    return df_o, df_e, residuals_o, residuals_e


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


def _m_spline_error_metrics(df: pd.DataFrame) -> None:
    '''Error Metrics Function'''
    print('Criterion, C: {:.6f}'.format(
        df.iloc[:, 2].div(df.iloc[:, 1]).sub(1).abs().mean()))


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


def m_spline_manager(df: pd.DataFrame, kernel: callable) -> None:
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
            float(
                input(f'Correction Factor of Knot {1 + _:02d} out of {len(_knots):02d}: '))
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


def price_inverse_single(data_series):
    '''Intent: Returns Prices Icrement Series from Cumulative Deflator Series;
    source: pandas DataFrame'''
    return data_series.div(data_series.shift(1)).sub(1)


def strip_cumulated_deflator(data_frame):
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    return price_inverse_single(data_frame.dropna()).dropna()


def procedure(output_name, criteria):
    # =========================================================================
    # TODO: Add Description
    # =========================================================================
    result = pd.DataFrame()
    for item in criteria:
        data = extract_can_from_url(string_to_url(item['file_name']))
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
    print('Period From {} Through {}'.format(*df.index[[0, -1]]))
    print('Model: Yhat = {:,.4f} + {:,.4f}*X'.format(*params[::-1]))
    print('Model Parameter: A_0 = {:,.4f}'.format(params[1]))
    print('Model Parameter: A_1 = {:,.4f}'.format(params[0]))
    print('Model Result: ESS = {:,.4f}; TSS = {:,.4f}; R^2 = {:,.4f}'.format(
        _ess[0],
        _tss,
        _r
    ))
    return df, params