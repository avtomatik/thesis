#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 20:54:06 2022

@author: alexander
"""


# =============================================================================
# TODO: Replace `.set_index('period')`
# =============================================================================
# =============================================================================
# TODO: result.div(result.iloc[result.index.get_loc(2001), :]).mul(100)
# =============================================================================
def append_series_ids(source_frame, data_frame, series_ids):
    for series_id in series_ids:
        chunk = source_frame.loc[:, [series_id]]
        chunk.dropna(inplace=True)
        data_frame = pd.concat([data_frame, chunk], axis=1, sort=False)
    return data_frame


def append_series_ids_sum(source_frame, data_frame, series_ids):
    chunk = pd.DataFrame()
    for series_id in series_ids:
        _ = source_frame.loc[:, [series_id]]
        _.dropna(inplace=True)
        chunk = pd.concat([chunk, _], axis=1, sort=False)
    series_ids.extend(['sum'])
    chunk['_'.join(series_ids)] = chunk.sum(1)
    data_frame = pd.concat(
        [data_frame, chunk.iloc[:, [-1]]], axis=1, sort=False)
    return data_frame


def approx_power_function_a(source_frame, q_1, q_2, alpha):
    '''
    source_frame.iloc[:, 0]: Regressor: = Period,
    source_frame.iloc[:, 1]: Regressand,
    q_1, q_2, alpha: Parameters
    '''
    # =========================================================================
    # DataFrame for Based Log-Linear Approximation Results
    # =========================================================================
    result_frame = source_frame.iloc[:, 0]
    # =========================================================================
    # Blank List for Calculation Results
    # =========================================================================
    calcul_frame = []

    for i in range(source_frame.shape[0]):
        # {RESULT}(Yhat) = Y_0 + A*(T-T_0)**alpha
        XAA = q_1 + q_2 * \
            (1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha
        XBB = (q_1 + q_2*(1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])
               ** alpha-source_frame.iloc[i, 1])**2  # (Yhat-Y)**2
        # (T-T_0)**(alpha-1)
        XCC = (1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**(alpha-1)
        # (T-T_0)**alpha
        XDD = (1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha
        XEE = ((1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha)*math.log(
            1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])  # ((T-T_0)**alpha)*LN(T-T_0)
        # Y*(T-T_0)**alpha
        XFF = source_frame.iloc[i, 1] * \
            (1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha
        XGG = source_frame.iloc[i, 1]*((1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha)*math.log(
            1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])  # Y*((T-T_0)**alpha)*LN(T-T_0)
        # (T-T_0)**(2*alpha)
        XHH = (1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**(2*alpha)
        XII = (1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**(2*alpha)*math.log(
            1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])  # (T-T_0)**(2*alpha)*LN(T-T_0)
        # (T-T_0)**(2*alpha-1)
        XJJ = (1 + source_frame.iloc[i, 0] -
               source_frame.iloc[0, 0])**(2*alpha-1)
        calcul_frame.append({'XAA': XAA, 'XBB': XBB, 'XCC': XCC, 'XDD': XDD,
                            'XEE': XEE, 'XFF': XFF, 'XGG': XGG, 'XHH': XHH, 'XII': XII, 'XJJ': XJJ})
    # =========================================================================
    # Convert List to Dataframe
    # =========================================================================
    calcul_frame = pd.DataFrame(calcul_frame)
    result_frame = pd.concat([result_frame, calcul_frame], axis=1, sort=True)

    Z = q_1 + q_2 * \
        (source_frame.iloc[:, 0].add(1).sub(source_frame.iloc[0, 0]))**alpha

    print('Model Parameter: T_0 = {}'.format((source_frame.iloc[0, 0]-1)))
    print('Model Parameter: Y_0 = {}'.format(q_1))
    print('Model Parameter: A = {:.4f}'.format(q_2))
    print('Model Parameter: Alpha = {:.4f}'.format(alpha))
    print('Estimator Result: Mean Value: {:,.4f}'.format(sp.mean(Z)))
    print('Estimator Result: Mean Squared Deviation, MSD: {:,.4f}'.format(
        mean_squared_error(source_frame.iloc[:, 1], Z)))
    print('Estimator Result: Root-Mean-Square Deviation, RMSD: {:,.4f}'.format(
        math.sqrt(mean_squared_error(source_frame.iloc[:, 1], Z))))


def approx_power_function_b(source_frame, q_1, q_2, q_3, q_4, alpha):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Regressor,
    source_frame.iloc[:, 2]: Regressand,
    q_1, q_2, q_3, q_4, alpha: Parameters
    '''
    # =========================================================================
    # DataFrame for Approximation Results
    # =========================================================================
    result_frame = source_frame.iloc[:, 0]
    # =========================================================================
    # Blank List for Calculation Results
    # =========================================================================
    calcul_frame = []
    for i in range(source_frame.shape[0]):
        XAA = source_frame.iloc[i, 1]  # '{X}'
        # '{RESULT}(Yhat) = U_1 + ((U_2-U_1)/(TAU_2-TAU_1)**Alpha)*({X}-TAU_1)**Alpha'
        XBB = q_3 + ((q_4-q_3)/(q_2-q_1)**alpha) * \
            (source_frame.iloc[i, 1]-q_1)**alpha
        XCC = (source_frame.iloc[i, 2]-(q_3 + ((q_4-q_3)/(q_2-q_1)**alpha)
               * (source_frame.iloc[i, 1]-q_1)**alpha))**2  # '(Yhat-Y)**2'
        XDD = abs(source_frame.iloc[i, 2]-(q_3 + ((q_4-q_3)/(q_2-q_1)**alpha)
                  * (source_frame.iloc[i, 1]-q_1)**alpha))  # 'ABS(Yhat-Y)'
        calcul_frame.append({'XAA': XAA, 'XBB': XBB, 'XCC': XCC, 'XDD': XDD})
    # =========================================================================
    # Convert List to Dataframe
    # =========================================================================
    calcul_frame = pd.DataFrame(calcul_frame)
    result_frame = pd.concat([result_frame, calcul_frame], axis=1, sort=True)

    Z = q_3 + ((q_4-q_3)/(q_2-q_1)**alpha)*(source_frame.iloc[:, 1]-q_1)**alpha

    print('Model Parameter: TAU_1 = {}'.format(q_1))
    print('Model Parameter: TAU_2 = {}'.format(q_2))
    print('Model Parameter: U_1 = {}'.format(q_3))
    print('Model Parameter: U_2 = {}'.format(q_4))
    print('Model Parameter: Alpha = {:.4f}'.format(alpha))
    print(
        'Model Parameter: A: = (U_2-U_1)/(TAU_2-TAU_1)**Alpha = {:,.4f}'.format((q_4-q_3)/(q_2-q_1)**alpha))
    print('Estimator Result: Mean Value: {:,.4f}'.format(sp.mean(Z)))
    print('Estimator Result: Mean Squared Deviation, MSD: {:,.4f}'.format(
        mean_squared_error(source_frame.iloc[:, 2], Z)))
    print('Estimator Result: Root-Mean-Square Deviation, RMSD: {:,.4f}'.format(
        math.sqrt(mean_squared_error(source_frame.iloc[:, 2], Z))))


def approx_power_function_c(source_frame, q_1, q_2, q_3, q_4):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Regressor,
    source_frame.iloc[:, 2]: Regressand,
    q_1, q_2, q_3, q_4: Parameters
    '''

    alpha = math.log(q_4/q_3)/math.log(q_1/q_2)
    # =========================================================================
    # DataFrame for Approximation Results
    # =========================================================================
    result_frame = source_frame.iloc[:, 0]
    # =========================================================================
    # Blank List for Calculation Results
    # =========================================================================
    calcul_frame = []
    for i in range(source_frame.shape[0]):
        XAA = source_frame.iloc[i, 1]  # '{X}'
        # '{RESULT}{Hat}{Y} = Y_1*(X_1/{X})**Alpha'
        XBB = q_3*(q_1/source_frame.iloc[i, 1])**alpha
        XCC = source_frame.iloc[i, 2]-q_3 * \
            (q_1/source_frame.iloc[i, 1])**alpha  # '{Hat-1}{Y}'
        # 'ABS({Hat-1}{Y})'
        XDD = abs(source_frame.iloc[i, 2]-q_3 *
                  (q_1/source_frame.iloc[i, 1])**alpha)
        # '({Hat-1}{Y})**2'
        XEE = (source_frame.iloc[i, 2]-q_3 *
               (q_1/source_frame.iloc[i, 1])**alpha)**2
        calcul_frame.append(
            {'XAA': XAA, 'XBB': XBB, 'XCC': XCC, 'XDD': XDD, 'XEE': XEE})
    # =========================================================================
    # Convert List to Dataframe
    # =========================================================================
    calcul_frame = pd.DataFrame(calcul_frame)
    result_frame = pd.concat([result_frame, calcul_frame], axis=1, sort=True)

    Z = q_3*(source_frame.iloc[:, 1].rdiv(q_1))**alpha

    print('Model Parameter: X_1 = {:.4f}'.format(q_1))
    print('Model Parameter: X_2 = {}'.format(q_2))
    print('Model Parameter: Y_1 = {:.4f}'.format(q_3))
    print('Model Parameter: Y_2 = {}'.format(q_4))
    print(
        'Model Parameter: Alpha: = LN(Y_2/Y_1)/LN(X_1/X_2) = {:.4f}'.format(alpha))
    print('Estimator Result: Mean Value: {:,.4f}'.format(sp.mean(Z)))
    print('Estimator Result: Mean Squared Deviation, MSD: {:,.4f}'.format(
        mean_squared_error(source_frame.iloc[:, 2], Z)))
    print('Estimator Result: Root-Mean-Square Deviation, RMSD: {:,.4f}'.format(
        math.sqrt(mean_squared_error(source_frame.iloc[:, 2], Z))))


def calculate_capital(source_frame, A, B, C, D, Pi):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Investment,
    source_frame.iloc[:, 2]: Production,
    source_frame.iloc[:, 3]: Capital,
    source_frame.iloc[:, 4]: Capital Retirement,
    A: S - Gross Fixed Investment to Gross Domestic Product Ratio - Absolute Term over Period,
    B: S - Gross Fixed Investment to Gross Domestic Product Ratio - Slope over Period,
    C: Λ - Fixed Assets Turnover Ratio - Absolute Term over Period,
    D: Λ - Fixed Assets Turnover Ratio - Slope over Period,
    Pi: Investment to Capital Conversion Ratio
    '''
    series = source_frame.iloc[:, 3].shift(1)*(1 + (B*source_frame.iloc[:, 0].shift(1) + A)*(
        D*source_frame.iloc[:, 0].shift(1) + C)*Pi-source_frame.iloc[:, 4].shift(1))
    return series


def capital_aquisition(source_frame):
    '''
    source_frame.iloc[:, 0]: Period
    source_frame.iloc[:, 1]: Nominal Investment
    source_frame.iloc[:, 2]: Nominal Production
    source_frame.iloc[:, 3]: Real Production
    source_frame.iloc[:, 4]: Maximum Real Production
    source_frame.iloc[:, 5]: Nominal Capital
    source_frame.iloc[:, 6]: Labor
    '''
    i = source_frame.shape[0]-1
    while abs(source_frame.iloc[i, 2]-source_frame.iloc[i, 3]) > 1:
        i -= 1
        base = i  # Basic Year
    '''Calculate Static Values'''
    XAA = source_frame.iloc[:, 3].div(
        source_frame.iloc[:, 5])  # Fixed Assets Turnover Ratio
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I_0/Y_0)
    XBB = source_frame.iloc[:, 1].div(source_frame.iloc[:, 3])
    XCC = source_frame.iloc[:, 5].div(
        source_frame.iloc[:, 6])  # Labor Capital Intensity
    XDD = source_frame.iloc[:, 3].div(
        source_frame.iloc[:, 6])  # Labor Productivity
    XBB = XBB.div(XBB[0])
    XCC = XCC.div(XCC[0])
    XDD = XDD.div(XDD[0])
    XEE = np.log(XCC)  # Log Labor Capital Intensity, LN((K/L)/(K_0/L_0))
    XFF = np.log(XDD)  # Log Labor Productivity, LN((Y/L)/(Y_0/L_0))
    # Max: Fixed Assets Turnover Ratio
    XGG = source_frame.iloc[:, 4].div(source_frame.iloc[:, 5])
    # Max: Investment to Gross Domestic Product Ratio
    XHH = source_frame.iloc[:, 1].div(source_frame.iloc[:, 4])
    XII = source_frame.iloc[:, 4].div(
        source_frame.iloc[:, 6])  # Max: Labor Productivity
    XHH = XHH.div(XHH[0])
    XII = XII.div(XII[0])
    XJJ = np.log(XII)  # Max: Log Labor Productivity
    XEE = pd.DataFrame(XEE, columns=['XEE'])  # Convert List to Dataframe
    XFF = pd.DataFrame(XFF, columns=['XFF'])  # Convert List to Dataframe
    XJJ = pd.DataFrame(XJJ, columns=['XJJ'])  # Convert List to Dataframe
    '''Calculate Dynamic Values'''
    N = int(input('Define Number of Line Segments for Pi: '))  # Number of Periods
    if N >= 1:
        print('Number of Periods Provided: {}'.format(N))
        pi, knt = [], []  # Pi Switch Points & Pi
        knt.append(0)
        i = 0
        if N == 1:
            knt.append(source_frame.shape[0]-1)
            pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i]-1, 0]))))
        elif N >= 2:
            while i < N:
                if i == N-1:
                    knt.append(source_frame.shape[0]-1)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                        source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i]-1, 0]))))
                    i += 1
                else:
                    y = int(input('Select Row for Year, Should Be More Than {}: = {}: '.format(
                        0, source_frame.iloc[0, 0])))
                    if y > knt[i]:
                        knt.append(y)
                        pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                            source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i], 0]))))
                        i += 1
        else:
            print('Error')
        XKK = []
        for i in range(1):
            XKK.append(sp.nan)
        if N == 1:
            j = 0
            for i in range(knt[j], knt[1 + j]):
                # Estimate: GCF[-] or CA[ + ]
                XKK.append(
                    source_frame.iloc[1 + i, 5]-source_frame.iloc[i, 5] + pi[j]*source_frame.iloc[1 + i, 1])
        else:
            for j in range(N):
                if j == N-1:
                    for i in range(knt[j], knt[1 + j]):
                        # Estimate: GCF[-] or CA[ + ]
                        XKK.append(
                            source_frame.iloc[1 + i, 5]-source_frame.iloc[i, 5] + pi[j]*source_frame.iloc[1 + i, 1])
                else:
                    for i in range(knt[j], knt[1 + j]):
                        # Estimate: GCF[-] or CA[ + ]
                        XKK.append(
                            source_frame.iloc[1 + i, 5]-source_frame.iloc[i, 5] + pi[j]*source_frame.iloc[1 + i, 1])
        XKK = pd.DataFrame(XKK, columns=['XKK'])  # Convert List to Dataframe
        result_frame = pd.DataFrame(
            source_frame.iloc[:, 0], columns=['Period'])
        result_frame = pd.concat(
            [result_frame, XAA, XBB, XCC, XDD, XEE, XFF, XGG, XHH, XII, XJJ, XKK], axis=1)
        result_frame.columns = [
            'Period', 'XAA', 'XBB', 'XCC', 'XDD', 'XEE', 'XFF', 'XGG', 'XHH',
            'XII', 'XJJ', 'XKK'
        ]
        '''
        `-` Gross Capital Formation
        `+` Capital Acquisitions
        '''
        for i in range(N):
            if i == N-1:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(
                    source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i]-1, 0], pi[i]))
            else:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(
                    source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i], 0], pi[i]))
        plt.figure(1)
        plt.plot(XCC, XDD)
        plt.plot(XCC, XII)
        plt.title('Labor Productivity, Observed & Max, {}=100, {}$-${}'.format(
            source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N]-1, 0]))
        plt.xlabel('Labor Capital Intensity')
        plt.ylabel('Labor Productivity, {}=100'.format(
            source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.figure(2)
        plt.plot(XEE, XFF)
        plt.plot(XEE, XJJ)
        plt.title('Log Labor Productivity, Observed & Max, {}=100, {}$-${}'.format(
            source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N]-1, 0]))
        plt.xlabel('Log Labor Capital Intensity')
        plt.ylabel('Log Labor Productivity, {}=100'.format(
            source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.figure(3)
        plt.plot(source_frame.iloc[:, 0], XAA)
        plt.plot(source_frame.iloc[:, 0], XGG)
        plt.title('Fixed Assets Turnover ($\\lambda$), Observed & Max, {}=100, {}$-${}'.format(
            source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N]-1, 0]))
        plt.xlabel('Period')
        plt.ylabel('Fixed Assets Turnover ($\\lambda$), {}=100'.format(
            source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.figure(4)
        plt.plot(source_frame.iloc[:, 0], XBB)
        plt.plot(source_frame.iloc[:, 0], XHH)
        plt.title('Investment to Gross Domestic Product Ratio, \nObserved & Max, {}=100, {}$-${}'.format(
            source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Investment to Gross Domestic Product Ratio, {}=100'.format(
            source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.figure(5)
        plt.plot(source_frame.iloc[:, 0], XKK)
        plt.title('Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), {}=100, {}$-${}'.format(
            source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N]-1, 0]))
        plt.xlabel('Period')
        plt.ylabel('GCF or CA, {}=100'.format(source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.show()
    else:
        print('N >= 1 is Required, N = {} Was Provided'.format(N))


def capital_retirement(source_frame):
    '''
    source_frame.iloc[:, 0]: Period
    source_frame.iloc[:, 1]: Nominal Investment
    source_frame.iloc[:, 2]: Nominal Production
    source_frame.iloc[:, 3]: Real Production
    source_frame.iloc[:, 4]: Nominal Capital
    source_frame.iloc[:, 5]: Labor
    '''
    # =========================================================================
    # Define Basic Year for Deflator
    # =========================================================================
    i = source_frame.shape[0]-1
    while abs(source_frame.iloc[i, 2]-source_frame.iloc[i, 3]) > 1:
        i -= 1
        base = i  # Basic Year
    '''Calculate Static Values'''
    YAA = source_frame.iloc[:, 4].div(source_frame.iloc[:, 5])
    # Log Labor Capital Intensity, LN((K/L)/(K_0/L_0))
    YAA = np.log(YAA.div(YAA[0]))
    YBB = source_frame.iloc[:, 3].div(source_frame.iloc[:, 5])
    # Log Labor Productivity, LN((Y/L)/(Y_0/L_0))
    YBB = np.log(YBB.div(YBB[0]))
    YCC = source_frame.iloc[:, 1].div(source_frame.iloc[:, 3])
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I_0/Y_0)
    YCC = YCC.div(YCC[0])
    YDD = source_frame.iloc[:, 3].div(
        source_frame.iloc[:, 4])  # Fixed Assets Turnover Ratio
    YAA = pd.DataFrame(YAA, columns=['YAA'])  # Convert List to Dataframe
    YBB = pd.DataFrame(YBB, columns=['YBB'])  # Convert List to Dataframe
    # =========================================================================
    # Number of Periods
    # =========================================================================
    N = int(input('Define Number of Line Segments for Pi: '))
    if N >= 1:
        print('Number of Periods Provided: {}'.format(N))
        pi, knt = [], []  # Pi Switch Points & Pi
        knt.append(0)
        i = 0
        if N == 1:
            knt.append(source_frame.shape[0]-1)
            pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                source_frame.iloc[knt[i], 0], source_frame.iloc[:, 0][knt[1 + i]]))))
        elif N >= 2:
            while i < N:
                if i == N-1:
                    knt.append(source_frame.shape[0]-1)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                        source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i], 0]))))
                    i += 1
                else:
                    y = int(input('Select Row for Year: '))
                    if y > knt[i]:
                        knt.append(y)
                        pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                            source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i], 0]))))
                        i += 1
        else:
            print('Error')
        YEE = []
        YFF = []
        YEE.append(sp.nan)  # Fixed Assets Retirement Value
        YFF.append(sp.nan)  # Fixed Assets Retirement Ratio
        '''Calculate Dynamic Values'''
        if N == 1:
            j = 0
            for i in range(knt[j], knt[1 + j]):
                # Fixed Assets Retirement Value
                YEE.append(
                    source_frame.iloc[i, 4]-source_frame.iloc[1 + i, 4] + pi[j]*source_frame.iloc[i, 1])
                YFF.append((source_frame.iloc[i, 4]-source_frame.iloc[1 + i, 4] + pi[j] *
                           source_frame.iloc[i, 1])/source_frame.iloc[1 + i, 4])  # Fixed Assets Retirement Ratio
        else:
            for j in range(N):
                if j == N-1:
                    for i in range(knt[j], knt[1 + j]):
                        # Fixed Assets Retirement Value
                        YEE.append(
                            source_frame.iloc[i, 4]-source_frame.iloc[1 + i, 4] + pi[j]*source_frame.iloc[i, 1])
                        # Fixed Assets Retirement Ratio
                        YFF.append((source_frame.iloc[i, 4]-source_frame.iloc[1 + i, 4] +
                                   pi[j]*source_frame.iloc[i, 1])/source_frame.iloc[1 + i, 4])
                else:
                    for i in range(knt[j], knt[1 + j]):
                        # Fixed Assets Retirement Value
                        YEE.append(
                            source_frame.iloc[i, 4]-source_frame.iloc[1 + i, 4] + pi[j]*source_frame.iloc[i, 1])
                        # Fixed Assets Retirement Ratio
                        YFF.append((source_frame.iloc[i, 4]-source_frame.iloc[1 + i, 4] +
                                   pi[j]*source_frame.iloc[i, 1])/source_frame.iloc[1 + i, 4])
        YEE = pd.DataFrame(YEE, columns=['YEE'])  # Convert List to Dataframe
        YFF = pd.DataFrame(YFF, columns=['YFF'])  # Convert List to Dataframe
        result_frame = pd.DataFrame(
            source_frame.iloc[:, 0], columns=['Period'])
        result_frame = pd.concat(
            [result_frame, YAA, YBB, YCC, YDD, YEE, YFF], axis=1, sort=True)
        result_frame.columns = [
            'Period', 'YAA', 'YBB', 'YCC', 'YDD', 'YEE', 'YFF'
        ]
        result_frame['YGG'] = result_frame['YFF']-result_frame['YFF'].mean()
        result_frame['YGG'] = result_frame['YGG'].abs()
        result_frame['YHH'] = result_frame['YFF']-result_frame['YFF'].shift(1)
        result_frame['YHH'] = result_frame['YHH'].abs()
        for i in range(N):
            if i == N-1:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(
                    source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i], 0], pi[i]))
            else:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(
                    source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i], 0], pi[i]))
        plt.figure(1)
        plt.title('Product, {}=100, {}$-${}'.format(
            source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Product, {}=100'.format(source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 3])
        plt.grid(True)
        plt.figure(2)
        plt.title('Capital, {}=100, {}$-${}'.format(
            source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Capital, {}=100'.format(source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 4])
        plt.grid(True)
        plt.figure(3)
        plt.title('Fixed Assets Turnover ($\\lambda$), {}=100, {}$-${}'.format(
            source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Fixed Assets Turnover ($\\lambda$), {}=100'.format(
            source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 3].div(
            source_frame.iloc[:, 4]))
        plt.grid(True)
        plt.figure(4)
        plt.title('Investment to Gross Domestic Product Ratio, {}=100, {}$-${}'.format(
            source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Investment to Gross Domestic Product Ratio, {}=100'.format(
            source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0], YCC)
        plt.grid(True)
        plt.figure(5)
        plt.title('$\\alpha(t)$, Fixed Assets Retirement Ratio, {}=100, {}$-${}'.format(
            source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('$\\alpha(t)$, {}=100'.format(source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0], YFF)
        plt.grid(True)
        plt.figure(6)
        plt.title('Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, {}=100, {}$-${}'.format(
            source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('$\\alpha(t)$, {}=100'.format(source_frame.iloc[base, 0]))
        plt.ylabel('Fixed Assets Retirement Value, {}=100'.format(
            source_frame.iloc[base, 0]))
        plt.plot(YFF, YEE)
        plt.grid(True)
        plt.figure(7)
        plt.title('Labor Capital Intensity, {}=100, {}$-${}'.format(
            source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Labor Capital Intensity, {}=100'.format(
            source_frame.iloc[base, 0]))
        plt.ylabel('Labor Productivity, {}=100'.format(
            source_frame.iloc[base, 0]))
        plt.plot(sp.exp(YAA), sp.exp(YBB))
        plt.grid(True)
        plt.show()
    else:
        print('N >= 1 is Required, N = {} Was Provided'.format(N))


def convert_url(string):
    return '/'.join(('https://www150.statcan.gc.ca/n1/tbl/csv', '{}-eng.zip'.format(string.split('=')[1][:-2])))


def string_to_url(string):
    return f'https://www150.statcan.gc.ca/n1/tbl/csv/{string}'


def data_select(data, query):
    for column, value in query['filter'].items():
        data = data[data.iloc[:, column] == value]
    return data


def error_metrics(data_frame):
    '''Error Metrics Module'''
    print('Criterion, C: {:.6f}'.format(
        sp.mean(data_frame.iloc[:, 2].div(data_frame.iloc[:, 1]).sub(1).abs())))


def fetch_can_annually(file_id, series_id):
    # =========================================================================
    # Data Frame Fetching from CANSIM Zip Archives
    # =========================================================================
    usecols = {
        2820012: (5, 7,),
        3800102: (4, 6,),
        3800106: (3, 5,),
        3800518: (4, 6,),
        3800566: (3, 5,),
        3800567: (4, 6,),
    }
    data_frame = pd.read_csv(
        f'dataset_can_{file_id:08n}-eng.zip', usecols=[0, *usecols[file_id]]
    )
    data_frame = data_frame[data_frame.iloc[:, 1] == series_id].iloc[:, [0, 2]]
    data_frame.columns = [data_frame.columns[0].upper(), series_id]
    data_frame.set_index(data_frame.columns[0], inplace=True)
    data_frame.iloc[:, 0] = pd.to_numeric(data_frame.iloc[:, 0])
    return data_frame


def fetch_can_capital_query():
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
    return df.iloc[:, -1].unique().tolist()


def fetch_can_capital_query_archived():
    # =========================================================================
    # TODO: Consider Using sqlalchemy
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
    return df.iloc[:, -1].unique().tolist()


def fetch_can_capital_query(source_frame):
    # =========================================================================
    # '''Fetch `Series series_ids` from Statistics Canada. Table: 36-10-0238-01\
    # (formerly CANSIM 031-0004): Flows and stocks of fixed non-residential\
    # capital, total all industries, by asset, provinces and territories, annual\
    # (dollars x 1,000,000)'''
    # =========================================================================
    query = (source_frame.iloc[:, 3].str.contains('2007 constant prices')) &\
            (source_frame.iloc[:, 5] == 'Straight-line end-year net stock') &\
            (source_frame.iloc[:, 6].str.contains('Industrial'))
    source_frame = source_frame[query]
    source_frame = source_frame.iloc[:, [11]]
    source_frame.drop_duplicates(inplace=True)
    series_ids = source_frame.iloc[:, 0].values.tolist()
    return series_ids


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


def fetch_usa_bea(archive_name, wb_name, sh_name, series_id):
    # =========================================================================
    # Data Frame Fetching from Bureau of Economic Analysis Zip Archives
    # =========================================================================
    with pd.ExcelFile(ZipFile(archive_name, 'r').open(wb_name)) as xl_file:
        # =====================================================================
        # Load
        # =====================================================================
        data_frame = pd.read_excel(xl_file, sh_name, skiprows=7)
        # =========================================================================
        # Re-Load
        # =========================================================================
        data_frame = pd.read_excel(xl_file,
                                   sh_name,
                                   usecols=range(2, data_frame.shape[1]),
                                   skiprows=7)
    data_frame.dropna(inplace=True)
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
    result_frame = pd.DataFrame()
    for source_id in data_frame.iloc[:, 0].unique():
        chunk = data_frame[data_frame.iloc[:, 0] == source_id].iloc[:, [2, 4]]
        chunk.columns = [chunk.columns[0],
                         '{}{}'.format(source_id.split()[1].replace('.', '_'), series_id)]
        chunk.set_index(chunk.columns[0], inplace=True, verify_integrity=True)
    return pd.concat([result_frame, chunk], axis=1, sort=True)


def fetch_usa_bea_from_loaded(data_frame, series_id):
    '''`NipaDataA.txt`: U.S. Bureau of Economic Analysis'''
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    data_frame.columns = [data_frame.columns[0].lower(), series_id]
    return data_frame.set_index(data_frame.columns[0], verify_integrity=True)


def fetch_usa_bea_from_url(url: str) -> pd.DataFrame:
    '''Retrieves U.S. Bureau of Economic Analysis DataFrame from URL'''
    r = requests.get(url)
    return pd.read_csv(io.BytesIO(r.content), thousands=',')


def fetch_usa_bea_sfat_series():
    ARCHIVE_NAME = 'dataset_usa_bea-nipa-selected.zip'
    series_id = 'k3n31gd1es000'
    data_frame = pd.read_csv(ARCHIVE_NAME, usecols=[0, *range(8, 11)])
    data_frame = data_frame[data_frame.iloc[:, 1] == series_id]
    control_frame = pd.DataFrame()
    for source_id in data_frame.iloc[:, 0].unique():
        chunk = data_frame[data_frame.iloc[:, 0] == source_id].iloc[:, [2, 3]]
        chunk.columns = [chunk.columns[0],
                         '{}{}'.format(source_id.split()[1].replace('.', '_'), series_id)]
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


def fetch_usa_census(file_name: str, series_id: str) -> pd.DataFrame:
    # =========================================================================
    # Selected Series by U.S. Bureau of the Census
    # U.S. Bureau of the Census, Historical Statistics of the United States,
    # 1789--1945, Washington, D.C., 1949.
    # U.S. Bureau of the Census. Historical Statistics of the United States,
    # Colonial Times to 1970, Bicentennial Edition. Washington, D.C., 1975.
    # =========================================================================
    data_frame = pd.read_csv(file_name,
                             usecols=range(8, 11),
                             dtype=str)
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].str[:4].astype(int)
    data_frame.iloc[:, 1] = data_frame.iloc[:, 1].astype(float)
    data_frame.columns = [data_frame.columns[0], series_id]
    data_frame.sort_values(data_frame.columns[0], inplace=True)
    return data_frame.groupby(data_frame.columns[0]).mean()


def fetch_usa_classic(file_id: str, series_id: str) -> pd.DataFrame:
    # =========================================================================
    # Data Fetch Procedure for Enumerated Classical Datasets
    # =========================================================================
    usecols = {
        'dataset_douglas.zip': (4, 7,),
        'dataset_usa_brown.zip': (3, 6,),
        'dataset_usa_cobb-douglas.zip': (5, 8,),
        'dataset_usa_kendrick.zip': (4, 7,),
    }
    data_frame = pd.read_csv(
        file_id,
        skiprows=(None, 4)[file_id == 'dataset_usa_brown.zip'],
        usecols=range(*usecols[file_id])
    )
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].astype(int)
    data_frame.iloc[:, 1] = pd.to_numeric(
        data_frame.iloc[:, 1], errors='coerce')
    data_frame.columns = ['period', series_id]
    return data_frame.set_index(data_frame.columns[0])


def fetch_usa_mcconnel(series_id):
    '''Data Frame Fetching from McConnell C.R. & Brue S.L.'''
    ARCHIVE_NAME = 'dataset_usa_mc-connell-brue.zip'
    data_frame = pd.read_csv(ARCHIVE_NAME, usecols=range(1, 4))
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    data_frame.sort_values(data_frame.columns[0], inplace=False)
    return data_frame.set_index(data_frame.columns[0], verify_integrity=True)


def fetch_world_bank(file_name, series_id):
    data_frame = pd.read_csv(file_name)
    data_frame = data_frame[data_frame.iloc[:, 1] == series_id].iloc[:, [0, 2]]
    data_frame.columns = ['period', series_id]
    data_frame.set_index(data_frame.columns[0], inplace=True)
    return data_frame.reset_index(level=0, inplace=True)


def get_data_archived() -> pd.DataFrame:
    ARCHIVES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WBS = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SHS = (
        '10105 Ann',
        '10106 Ann',
        '50900 Ann',
    )
    IDS = (
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
                    fetch_usa_bea(ARCHIVES[0], _wb, _sh, _id)
                    for _wb, _sh, _id in zip(tuple(WBS[2*(_ // 2)] for _ in range(len(IDS))), SHS, IDS)
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVES[1], _wb, _sh, _id)
                    for _wb, _sh, _id in zip(tuple(WBS[1 + 2*(_ // 2)] for _ in range(len(IDS))), SHS, IDS)
                ],
                axis=1,
                sort=True
            ),
        ],
        sort=True
    ).drop_duplicates()
    _df = pd.concat([
        # =====================================================================
        # Do Not Use As It Is CPI-U Not PPI
        # =====================================================================
        get_data_usa_bls_cpiu(),
        _data_bea],
        axis=1, sort=True).dropna()
    # =========================================================================
    # Deflator, 2005=100
    # =========================================================================
    _df['def'] = np.cumprod(_df.iloc[:, 0].add(1))
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
    _df['rto'] = _df.iloc[:, -2].mul(1).sub(_df.iloc[:, -1].shift(-1)).div(
        _df.iloc[:, -1]).add(1)
    return (_df.loc[:, ['inv', 'A191RX1', 'cap', 'rto']].dropna().reset_index(level=0),
            _df.loc[:, ['rto']].dropna().reset_index(level=0),
            _df.index.get_loc(2005)
            )


def get_data_bea_def():
    '''Intent: Returns Cumulative Price Index for Some Base Year from Certain Type BEA Deflator File'''
    FILE_NAME = 'dataset_usa_bea-GDPDEF.xls'
    data_frame = pd.read_excel(FILE_NAME, skiprows=15, parse_dates=[0])
    data_frame['period'] = data_frame.iloc[:, 0].dt.year
    return data_frame.groupby(data_frame.columns[-1]).prod().pow(1/4)


def get_data_bea_gdp():
    ARCHIVES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WBS = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
    )
    SHS = (
        '10105 Ann',
        '10106 Ann',
    )
    IDS = (
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
                    fetch_usa_bea(ARCHIVES[0], WBS[0], sh, _id)
                    for sh, _id in zip(SHS, IDS)
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVES[1], WBS[1], sh, _id)
                    for sh, _id in zip(SHS, IDS)
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
        [fetch_usa_classic(ARCHIVE_NAMES[0], series_id)
         for series_id in data_frame.iloc[:, 0].unique()],
        axis=1,
        sort=True)
    _b_frame.columns = ['series_{}'.format(
        hex(i)) for i, column in enumerate(_b_frame.columns)]
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
        [_k_frame[_k_frame.index.get_loc(1889):2+_k_frame.index.get_loc(1952)],
         # ====================================================================
         # Первая аппроксимация рядов загрузки мощностей, полученная с помощью метода Уортонской школы
         # ====================================================================
         _b_frame.iloc[:1+_b_frame.index.get_loc(1953), [4]]],
        axis=1,
        sort=True)
    result_frame = result_frame.assign(
        series_0x0=result_frame.iloc[:, 0].sub(result_frame.iloc[:, 1]),
        series_0x1=result_frame.iloc[:, 3].add(result_frame.iloc[:, 4]),
        series_0x2=result_frame.iloc[:, [3, 4]].sum(axis=1).rolling(
            window=2).mean().mul(result_frame.iloc[:, 5]).div(100),
        series_0x3=result_frame.iloc[:, 2],
    )
    result_frame = result_frame.iloc[:, [6, 7, 8, 9]].dropna()
    return pd.concat(
        [result_frame,
         # ====================================================================
         # Brown M. Numbers Not Found in Kendrick J.W. For Years Starting From 1954 Inclusive
         # ====================================================================
         _b_frame.iloc[1+_b_frame.index.get_loc(1953):, [0, 1, 2, 3]]]
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
    # result_frame = result_frame.dropna()
    result_frame.columns = ['capital', 'labor', 'product']
    # result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame


def get_data_can():
    '''A. Fixed Assets Block: `Industrial buildings`, `Industrial machinery` for `Newfoundland and Labrador`, `Prince Edward Island`, `Nova Scotia`, `New Brunswick`, \
    `Quebec`, `Ontario`, `Manitoba`, `Saskatchewan`, `Alberta`, `British Columbia`, `Yukon`, `Northwest Territories`, `Nunavut`'''
    '''2007 constant prices'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1,000,000): `v43975603`, `v43977683`, `v43978099`, `v43978515`, `v43978931`, `v43979347`, `v43979763`, `v43980179`, `v43980595`, \
    `v43976019`, `v43976435`, `v43976851`, `v43977267`'''
    '''Industrial machinery (x 1,000,000): `v43975594`, `v43977674`, `v43978090`, `v43978506`, `v43978922`, `v43979338`, `v43979754`, `v43980170`, `v43980586`, \
    `v43976010`,  `v43976426`, `v43976842`, `v43977258`'''
    capital = fetch_can_fixed_assets(fetch_can_capital_query_archived())
    '''B. Labor Block: `v2523012`, Preferred Over `v3437501` Which Is Quarterly'''
    '''`v2523012` - 282-0012 Labour Force Survey Estimates (LFS), employment by class of worker, North American Industry Classification System (NAICS)\
    and sex; Canada; Total employed, all class of workers; Manufacturing; Both sexes (x 1,000) (annual, 1987 to 2017)'''
    labor = fetch_can_annually(2820012, 'v2523012')
    '''C. Production Block: `v65201809`'''
    '''`v65201809` - 379-0031 Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS); Canada; Trading-day\
    adjusted; 2007 constant prices; Manufacturing (x 1,000,000) (monthly, 1997-01-01 to 2017-10-01)'''
    product = fetch_can_quarterly(3790031, 'v65201809')
    result_frame = pd.concat([capital, labor, product], axis=1, sort=True)
    result_frame = result_frame.dropna()
    result_frame.rename(
        columns={0: 'capital', 'v2523012': 'labor', 'v65201809': 'product'}, inplace=True)
    return result_frame


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
    # # fetch_can_quarterly(2820011, 'v3437501')
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
    # # fetch_can_quarterly(3790031, 'v65201536')

    result_frame = pd.concat([labor, capital, product], axis=1, sort=True)
    result_frame = result_frame.dropna()
    result_frame.rename(
        columns={'v2523012': 'labor', 0: 'capital', 'v65201809': 'product'}, inplace=True)
    return result_frame.reset_index(level=0, inplace=True)


def get_data_capital_combined_archived():
    ARCHIVES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WBS = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SHS = (
        '10105 Ann',
        '10106 Ann',
        '50900 Ann',
    )
    IDS = (
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
        # U.S. Bureau of Economic Analysis, Produced assets, closing balance: Fixed assets (DISCONTINUED) [K160491A027NBEA], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/K160491A027NBEA, August 23, 2018.
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
                    fetch_usa_bea(ARCHIVES[0], _wb, _sh, _id)
                    for _wb, _sh, _id in zip(
                        tuple(WBS[2*(_ // len(SHS))] for _ in range(len(IDS))),
                        tuple(SHS[2*(_ // len(SHS)) + ((_ - 1) % len(SHS)) *
                                  (2 - ((_ - 1) % len(SHS)))] for _ in range(len(IDS))),
                        IDS,
                    )
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVES[1], _wb, _sh, _id)
                    for _wb, _sh, _id in zip(
                        tuple(WBS[1 + 2*(_ // len(SHS))]
                              for _ in range(len(IDS))),
                        tuple(SHS[2*(_ // len(SHS)) + ((_ - 1) % len(SHS)) *
                                  (2 - ((_ - 1) % len(SHS)))] for _ in range(len(IDS))),
                        IDS,
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
        'CDT2S1', 'J0149', 'P0107']].mean(1)
    data_frame['struc'] = data_frame.loc[:, ['J0150', 'P0108']].mean(1)
    data_frame['equip'] = data_frame.loc[:, ['J0151', 'P0109']].mean(1)
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
        # HSUS 1949 Page 179, J13
        # =====================================================================
        'J0013',
        # =====================================================================
        # HSUS 1949 Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
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
    data_frame['total'] = data_frame.loc[:, ['J0149', 'P0107']].mean(1)
    data_frame['struc'] = data_frame.loc[:, ['J0150', 'P0108']].mean(1)
    data_frame['equip'] = data_frame.loc[:, ['J0151', 'P0109']].mean(1)
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
    data_frame['census_fused'] = data_frame.mean(1)
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
    SERIES_ID_YEAR_MAP = {_: base_year for _,
                          base_year in enumerate(BASE_YEARS)}
    data_frame = pd.concat(
        [fetch_usa_census(ARCHIVE_NAME, series_id)
         for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    for i in range(data_frame.shape[1]):
        base_year = data_frame.index.get_loc(SERIES_ID_YEAR_MAP[i])
        data_frame.iloc[:, i] = data_frame.iloc[:, i].div(
            data_frame.iloc[base_year, i]).mul(100)
    return data_frame, SERIES_ID_YEAR_MAP


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
    base = (84, 177, 216)  # 2009, 1970, 2009
    '''Combine L2, L15, E7, E23, E40, E68 & P107/P110'''
    '''Bureau of Labor Statistics
    Data Not Used As It Covers Only Years of 1998--2017'''
    '''Results:
        ARCHIVE_NAME = 'dataset_usa_census1949.zip'
    fetch_usa_census(ARCHIVE_NAME, 'L0036') Offset with\
        ARCHIVE_NAME = 'dataset_usa_census1975.zip'
        fetch_usa_census(ARCHIVE_NAME, 'E0183')
        ARCHIVE_NAME = 'dataset_usa_census1949.zip'
    fetch_usa_census(ARCHIVE_NAME, 'L0038') Offset with\
        ARCHIVE_NAME = 'dataset_usa_census1975.zip'
        fetch_usa_census(ARCHIVE_NAME, 'E0184')
        ARCHIVE_NAME = 'dataset_usa_census1949.zip'
    fetch_usa_census(ARCHIVE_NAME, 'L0039') Offset with\
        ARCHIVE_NAME = 'dataset_usa_census1975.zip'
        fetch_usa_census(ARCHIVE_NAME, 'E0185')
        ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    fetch_usa_census(ARCHIVE_NAME, 'E0052') Offset With\
        ARCHIVE_NAME = 'dataset_usa_census1949.zip'
        fetch_usa_census(ARCHIVE_NAME, 'L0002')'''
    '''Cost-Of-Living Indexes'''
    '''E183: Federal Reserve Bank, 1913=100'''
    '''E184: Burgess, 1913=100'''
    '''E185: Douglas, 1890-99=100'''
    ARCHIVE_NAME = 'dataset_usa_cobb-douglas.zip'
    sub_frame_a = fetch_usa_classic(ARCHIVE_NAME, 'CDT2S1')
    ARCHIVE_NAME = 'dataset_usa_cobb-douglas.zip'
    sub_frame_b = fetch_usa_classic(ARCHIVE_NAME, 'CDT2S3')
    ARCHIVE_NAME = 'dataset_usa_census1949.zip'
    sub_frame_c = fetch_usa_census(ARCHIVE_NAME, 'L0001')
    ARCHIVE_NAME = 'dataset_usa_census1949.zip'
    sub_frame_d = fetch_usa_census(ARCHIVE_NAME, 'L0002')
    ARCHIVE_NAME = 'dataset_usa_census1949.zip'
    sub_frame_e = fetch_usa_census(ARCHIVE_NAME, 'L0015')
    ARCHIVE_NAME = 'dataset_usa_census1949.zip'
    sub_frame_f = fetch_usa_census(ARCHIVE_NAME, 'L0037')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    sub_frame_g = fetch_usa_census(ARCHIVE_NAME, 'E0007')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    sub_frame_h = fetch_usa_census(ARCHIVE_NAME, 'E0008')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    sub_frame_i = fetch_usa_census(ARCHIVE_NAME, 'E0009')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    sub_frame_j = fetch_usa_census(ARCHIVE_NAME, 'E0023')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    sub_frame_k = fetch_usa_census(ARCHIVE_NAME, 'E0040')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    sub_frame_l = fetch_usa_census(ARCHIVE_NAME, 'E0068')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    sub_frame_m = fetch_usa_census(ARCHIVE_NAME, 'E0183')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    sub_frame_n = fetch_usa_census(ARCHIVE_NAME, 'E0184')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    sub_frame_o = fetch_usa_census(ARCHIVE_NAME, 'E0185')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    sub_frame_p = fetch_usa_census(ARCHIVE_NAME, 'E0186')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    sub_frame_q = fetch_usa_census(ARCHIVE_NAME, 'P0107')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    sub_frame_r = fetch_usa_census(ARCHIVE_NAME, 'P0110')
    sub_frame_s = get_data_usa_frb_fa_def()
    sub_frame_q = sub_frame_q[22:]
    sub_frame_r = sub_frame_r[22:]
    basis_frame = pd.concat([sub_frame_a, sub_frame_b, sub_frame_c,
                             sub_frame_d, sub_frame_e, sub_frame_f,
                             sub_frame_g, sub_frame_h, sub_frame_i,
                             sub_frame_j, sub_frame_k, sub_frame_l,
                             sub_frame_m, sub_frame_n, sub_frame_o,
                             sub_frame_p, sub_frame_q, sub_frame_r,
                             sub_frame_s], axis=1, sort=True)
    basis_frame['fa_def_cd'] = basis_frame.iloc[:, 0].div(
        basis_frame.iloc[:, 1])
    basis_frame['fa_def_cn'] = basis_frame.iloc[:, 16].div(
        basis_frame.iloc[:, 17])
    '''Cobb--Douglas'''
    semi_frame_a = processing(basis_frame.iloc[:, [19]])
    '''Bureau of Economic Analysis'''
    URL = 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    loaded_frame = fetch_usa_bea_from_url(URL)
    '''Fixed Assets: k1n31gd1es00, 1925--2019, Table 4.1. Current-Cost Net\
        Stock of Private Nonresidential Fixed Assets by Industry Group and\
            Legal Form of Organization'''
    sub_frame_a = fetch_usa_bea_from_loaded(loaded_frame, 'k1n31gd1es00')
    '''Fixed Assets: kcn31gd1es00, 1925--2019, Table 4.2. Chain-Type Quantity\
        Indexes for Net Stock of Private Nonresidential Fixed Assets by\
            Industry Group and Legal Form of Organization'''
    sub_frame_b = fetch_usa_bea_from_loaded(loaded_frame, 'kcn31gd1es00')
    '''Not Used: Not Used: Fixed Assets: k3n31gd1es00, 1925--2019, Table 4.3.\
        Historical-Cost Net Stock of Private Nonresidential Fixed Assets by\
            Industry Group and Legal Form of Organization'''
    sub_frame_c = fetch_usa_bea_from_loaded(loaded_frame, 'k3n31gd1es00')
    '''Not Used: Fixed Assets: k3ntotl1si00, 1925--2019, Table 2.3.\
        Historical-Cost Net Stock of Private Fixed Assets, Equipment,\
            Structures, and Intellectual Property Products by Type'''
    sub_frame_d = fetch_usa_bea_from_loaded(loaded_frame, 'k3ntotl1si00')
    '''Not Used: mcn31gd1es00, 1925--2019, Table 4.5. Chain-Type Quantity\
        Indexes for Depreciation of Private Nonresidential Fixed Assets by\
            Industry Group and Legal Form of Organization'''
    sub_frame_e = fetch_usa_bea_from_loaded(loaded_frame, 'mcn31gd1es00')
    '''Not Used: mcntotl1si00, 1925--2019, Table 2.5. Chain-Type Quantity\
        Indexes for Depreciation of Private Fixed Assets, Equipment,\
            Structures, and Intellectual Property Products by Type'''
    sub_frame_f = fetch_usa_bea_from_loaded(loaded_frame, 'mcntotl1si00')
    '''Real Values'''
    semi_frame_b = pd.concat([sub_frame_a, sub_frame_b], axis=1, sort=True)
    semi_frame_b['ppi_bea'] = 100*semi_frame_b.iloc[:,
                                                    0].div(semi_frame_b.iloc[base[0], 0]*semi_frame_b.iloc[:, 1])
    semi_frame_b.iloc[:, 2] = processing(semi_frame_b.iloc[:, [2]])
    semi_frame_b = semi_frame_b.iloc[:, [2]]
    '''Bureau of the Census'''
    '''Correlation Test:
    `kendall_frame = result_frame.corr(method='kendall')`
    `pearson_frame = result_frame.corr(method='pearson')`
    `spearman_frame = result_frame.corr(method='spearman')`
    Correlation Test Result: kendall & pearson & spearman: L2, L15, E7, E23, E40, E68'''
    sub_frame_a = processing(basis_frame.iloc[:, [3]])
    sub_frame_b = processing(basis_frame.iloc[:, [4]])
    sub_frame_c = processing(basis_frame.iloc[:, [6]])
    sub_frame_d = processing(basis_frame.iloc[:, [9]])
    sub_frame_e = processing(basis_frame.iloc[:, [10]])
    sub_frame_f = processing(basis_frame.iloc[:, [11]])
    sub_frame_g = processing(basis_frame.iloc[:, [20]])
    semi_frame_c = pd.concat([sub_frame_a, sub_frame_b, sub_frame_c,
                              sub_frame_d, sub_frame_e, sub_frame_f,
                              sub_frame_g], axis=1, sort=True)
    semi_frame_c['ppi_census_fused'] = semi_frame_c.mean(1)
    semi_frame_c = semi_frame_c.iloc[:, [7]]
    '''Federal Reserve'''
    semi_frame_d = processing(basis_frame.iloc[:, [18]])
    '''Robert C. Sahr, 2007'''
    semi_frame_e = get_data_infcf()
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c,
                              semi_frame_d, semi_frame_e], axis=1, sort=True)

    result_frame = result_frame[128:]
    result_frame['def_cum_bea'] = np.cumprod(result_frame.iloc[:, 1].add(1))
    result_frame['def_cum_cen'] = np.cumprod(result_frame.iloc[:, 2].add(1))
    result_frame['def_cum_frb'] = np.cumprod(result_frame.iloc[:, 3].add(1))
    result_frame['def_cum_sah'] = np.cumprod(result_frame.iloc[:, 4].add(1))
    result_frame.iloc[:, 5] = result_frame.iloc[:, 5].div(
        result_frame.iloc[base[1], 5])
    result_frame.iloc[:, 6] = result_frame.iloc[:, 6].div(
        result_frame.iloc[base[1], 6])
    result_frame.iloc[:, 7] = result_frame.iloc[:, 7].div(
        result_frame.iloc[base[1], 7])
    result_frame.iloc[:, 8] = result_frame.iloc[:, 8].div(
        result_frame.iloc[base[1], 8])
    result_frame['def_cum_com'] = result_frame.iloc[:, [5, 6, 7]].mean(1)
    result_frame['fa_def_com'] = processing(result_frame.iloc[:, [9]])
    result_frame.iloc[:, 9] = result_frame.iloc[:, 9].div(
        result_frame.iloc[base[2], 9])
    result_frame = result_frame.iloc[:, [9]]
    result_frame.dropna(inplace=True)
    return result_frame


def get_data_cobb_douglas(series_number: int = 3) -> pd.DataFrame:
    '''Original Cobb--Douglas Data Preprocessing Extension'''
    ARCHIVE_NAMES = (
        'dataset_usa_cobb-douglas.zip',
        'dataset_usa_census1949.zip',
        'dataset_douglas.zip',
    )
    data_frame = pd.concat(
        [
            fetch_usa_classic(ARCHIVE_NAMES[0], 'CDT2S4'),
            fetch_usa_classic(ARCHIVE_NAMES[0], 'CDT3S1'),
            fetch_usa_census(ARCHIVE_NAMES[1], 'J0014'),
            # =================================================================
            # Description
            # =================================================================
            fetch_usa_census(ARCHIVE_NAMES[1], 'J0013'),
            # =================================================================
            # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
            # =================================================================
            fetch_usa_classic(ARCHIVE_NAMES[2], 'DT24AS01')
        ], axis=1, sort=True
    ).dropna()
    data_frame.columns = [
        'capital', 'labor', 'product', 'product_nber', 'product_rev'
    ]
    return data_frame.div(data_frame.iloc[0, :]).iloc[:, range(series_number)]


def get_data_cobb_douglas_extension_capital():
    '''Existing Capital Dataset'''
    source_frame = get_data_usa_capital()
    '''Convert Capital Series into Current (Historical) Prices'''
    source_frame['nominal_cbb_dg'] = source_frame.iloc[:, 0] * \
        source_frame.iloc[:, 2].div(1000*source_frame.iloc[:, 1])
    source_frame['nominal_census'] = source_frame.iloc[:, 5] * \
        source_frame.iloc[:, 7].div(source_frame.iloc[:, 6])
    source_frame['nominal_dougls'] = source_frame.iloc[:, 0] * \
        source_frame.iloc[:, 9].div(1000*source_frame.iloc[:, 1])
    source_frame['nominal_kndrck'] = source_frame.iloc[:, 5] * \
        source_frame.iloc[:, 8].div(1000*source_frame.iloc[:, 6])
    source_frame.iloc[:, 15] = source_frame.iloc[66, 6] * \
        source_frame.iloc[:, 15].div(source_frame.iloc[66, 5])
    '''Douglas P.H. -- Kendrick J.W. (Blended) Series'''
    source_frame['nominal_doug_kndrck'] = source_frame.iloc[:, 14:16].mean(1)
    '''Cobb C.W., Douglas P.H. -- FRB (Blended) Series'''
    source_frame['nominal_cbb_dg_frb'] = source_frame.iloc[:, [12, 10]].mean(1)
    '''Capital Structure Series: `Cobb C.W., Douglas P.H. -- FRB (Blended)\
    Series` to `Douglas P.H. -- Kendrick J.W. (Blended) Series`'''
    source_frame['struct_ratio'] = source_frame.iloc[:, 17].div(
        source_frame.iloc[:, 16])
    '''Filling the Gaps within Capital Structure Series'''
    source_frame.iloc[6:36, 18].fillna(source_frame.iloc[36, 18], inplace=True)
    source_frame.iloc[36:, 18].fillna(0.275, inplace=True)
    '''Patch Series `Douglas P.H. -- Kendrick J.W. (Blended) Series`\
    Multiplied by `Capital Structure Series`'''
    source_frame['nominal_patch'] = source_frame.iloc[:, 16].mul(
        source_frame.iloc[:, 18])
    '''`Cobb C.W., Douglas P.H. -- FRB (Blended) Series` Patched with `Patch Series`'''
    source_frame['nominal_extended'] = source_frame.iloc[:, [17, 19]].mean(1)
    source_frame = source_frame.iloc[:, [20]]
    source_frame.dropna(inplace=True)
    return source_frame


def get_data_cobb_douglas_extension_labor():
    BASE = 14  # 1899
    '''Manufacturing Laborers` Series Comparison
    semi_frame_a: Cobb C.W., Douglas P.H. Labor Series
    semi_frame_b: Census Bureau 1949, D69
    semi_frame_c: Census Bureau 1949, J4
    semi_frame_d: Census Bureau 1975, D130
    semi_frame_e: Census Bureau 1975, P5
    semi_frame_f: Census Bureau 1975, P62
    semi_frame_g: Bureau of Economic Analysis, H4313C & J4313C & A4313C & N4313C
    semi_frame_h: J.W. Kendrick, Productivity Trends in the United States,\
        Table D-II, `Persons Engaged` Column, pp. 465--466
    semi_frame_i: Yu.V. Kurenkov
    Bureau of Labor Statistics
    Federal Reserve Board'''
    ARCHIVE_NAME = 'dataset_usa_cobb-douglas.zip'
    # Average Number Employed (in thousands)
    semi_frame_a = fetch_usa_classic(ARCHIVE_NAME, 'CDT3S1')
    ARCHIVE_NAME = 'dataset_usa_census1949.zip'
    semi_frame_b = fetch_usa_census(ARCHIVE_NAME, 'D0069')
    ARCHIVE_NAME = 'dataset_usa_census1949.zip'
    semi_frame_c = fetch_usa_census(ARCHIVE_NAME, 'J0004')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    semi_frame_d = fetch_usa_census(ARCHIVE_NAME, 'D0130')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    semi_frame_e = fetch_usa_census(ARCHIVE_NAME, 'P0005')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    semi_frame_f = fetch_usa_census(ARCHIVE_NAME, 'P0062')
    URL = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    loaded_frame = fetch_usa_bea_from_url(URL)
    sub_frame_a = fetch_usa_bea_from_loaded(loaded_frame, 'H4313C')
    sub_frame_b = fetch_usa_bea_from_loaded(loaded_frame, 'J4313C')
    sub_frame_c = fetch_usa_bea_from_loaded(loaded_frame, 'A4313C')
    sub_frame_d = fetch_usa_bea_from_loaded(loaded_frame, 'N4313C')
    semi_frame_g = pd.concat([sub_frame_a, sub_frame_b, sub_frame_c, sub_frame_d],
                             axis=1, sort=True)

    semi_frame_g = semi_frame_g.mean(1)
    semi_frame_g = semi_frame_g.to_frame(name='BEA')
    ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
    semi_frame_h = fetch_usa_classic(ARCHIVE_NAME, 'KTD02S02')
    ARCHIVE_NAME = 'dataset_usa_reference_ru_kurenkov-yu-v.csv'
    semi_frame_i = pd.read_csv(ARCHIVE_NAME, index_col=0, usecols=[0, 2])
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c,
                              semi_frame_d, semi_frame_e, semi_frame_f,
                              semi_frame_g, semi_frame_h, semi_frame_i],
                             axis=1, sort=True)
    result_frame['kendrick'] = result_frame.iloc[BASE, 0] * \
        result_frame.iloc[:, 7].div(result_frame.iloc[BASE, 7])
    result_frame['labor'] = result_frame.iloc[:, [0, 1, 3, 6, 8, 9]].mean(1)
    result_frame = result_frame.iloc[:, [10]]
    result_frame.dropna(inplace=True)
    result_frame = result_frame[2:]
    return result_frame


def get_data_cobb_douglas_extension_product():
    base = (109, 149)  # 1899, 1939
    '''Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic\
        Research Index of Physical Output, All Manufacturing Industries.'''
    ARCHIVE_NAME = 'dataset_usa_census1949.zip'
    semi_frame_a = fetch_usa_census(ARCHIVE_NAME, 'J0013')
    '''Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of\
        Physical Production of Manufacturing'''
    ARCHIVE_NAME = 'dataset_usa_census1949.zip'
    semi_frame_b = fetch_usa_census(ARCHIVE_NAME, 'J0014')
    '''Bureau of the Census, 1975, Page 667, P17: Edwin Frickey Index of\
        Manufacturing Production'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    semi_frame_c = fetch_usa_census(ARCHIVE_NAME, 'P0017')
    '''The Revised Index of Physical Production for All Manufacturing In the\
        United States, 1899--1926'''
    ARCHIVE_NAME = 'dataset_douglas.zip'
    semi_frame_d = fetch_usa_classic(ARCHIVE_NAME, 'DT24AS01')
    '''Federal Reserve, AIPMASAIX'''
    semi_frame_e = get_data_usa_frb_ip()
    '''Joseph H. Davis Production Index'''
    ARCHIVE_NAME = 'dataset_usa_davis-j-h-ip-total.xls'
    semi_frame_f = pd.read_excel(ARCHIVE_NAME, index_col=0, skiprows=4)
    semi_frame_f.index.rename('period', inplace=True)
    semi_frame_f.columns = ['davis_index']
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c,
                              semi_frame_d, semi_frame_e, semi_frame_f],
                             axis=1, sort=True)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].div(
        result_frame.iloc[base[0], 1]).mul(100)
    result_frame.iloc[:, 5] = result_frame.iloc[:, 5].div(
        result_frame.iloc[base[0], 5]).mul(100)
    result_frame['fused_classic'] = result_frame.iloc[:,
                                                      [0, 1, 2, 3, 5]].mean(1)
    result_frame.iloc[:, 4] = result_frame.iloc[:, 4].div(
        result_frame.iloc[base[1], 4]).mul(100)
    result_frame.iloc[:, 6] = result_frame.iloc[:, 6].div(
        result_frame.iloc[base[1], 6]).mul(100)
    result_frame['fused'] = result_frame.iloc[:, [4, 6]].mean(1)
    result_frame = result_frame.iloc[:, [7]]
    return result_frame


def get_data_combined():
    '''Most Up-To-Date Version'''
    # =========================================================================
    # TODO: Refactor It
    # =========================================================================
    URL = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    _data = fetch_usa_bea_from_url(URL)
    IDS = (
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
            fetch_usa_bea_from_loaded(_data, _id) for _id in IDS
        ],
        axis=1,
        sort=True
    )
    IDS = (
        'H4313C',
        'J4313C',
        'A4313C',
        'N4313C',
    )
    _labor_frame = pd.concat(
        [
            fetch_usa_bea_from_loaded(_data, _id) for _id in IDS
        ],
        axis=1,
        sort=True
    )
    _labor_frame['mfg_labor'] = _labor_frame.mean(1)
    _labor_frame = _labor_frame.iloc[:, [-1]]
    ARCHIVES = (
        'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
    )
    WBS = (
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH, ID = ('51000 Ann', 'K100701',)
    # =========================================================================
    # Fixed Assets Series: K100701, 1951--2013
    # =========================================================================
    _data_sfat = pd.concat(
        [
            fetch_usa_bea(_archive, _wb, SH, ID) for _archive, _wb in zip(ARCHIVES, WBS)
        ],
        sort=True
    ).drop_duplicates()
    # =========================================================================
    # US BEA Fixed Assets Series Tests
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WBS = (
        'Section1ALL_xls.xls',
        'Section2ALL_xls.xls',
    )
    SHS = (
        '105 Ann',
        '106 Ann',
        '101 Ann',
        '203 Ann',
        '202 Ann',
    )
    IDS = (
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
                tuple(WBS[_ // 3] for _ in range(len(IDS))), SHS, IDS)
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
    ARCHIVES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WBS = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SHS = (
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
    IDS = (
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
                    fetch_usa_bea(ARCHIVES[0], _wb, _sh, _id) for _wb, _sh, _id in zip(
                        tuple(WBS[2*(_ // 8)] for _ in range(len(IDS))), SHS, IDS)
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVES[1], _wb, _sh, _id) for _wb, _sh, _id in zip(
                        tuple(WBS[1 + 2*(_ // 8)] for _ in range(len(IDS))), SHS, IDS)
                ],
                axis=1,
                sort=True
            ),
        ],
        sort=True
    ).drop_duplicates()
    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2012-08-15-SectionAll_xls.zip'
    WBS = (
        'Section1ALL_xls.xls',
        'Section2ALL_xls.xls',
    )
    SHS = (
        '105 Ann',
        '106 Ann',
        '101 Ann',
        '203 Ann',
        '202 Ann',
    )
    IDS = (
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
                tuple(WBS[_ // 3] for _ in range(len(IDS))), SHS, IDS)
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
    ARCHIVES = (
        'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
    )
    WBS = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SHS = (
        '10105 Ann',
        '10106 Ann',
        '10109 Ann',
        '11200 Ann',
        '51000 Ann',
    )
    IDS = (
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
                    fetch_usa_bea(ARCHIVES[0], _wb, _sh, _id) for _wb, _sh, _id in zip(
                        tuple(WBS[2*(_ // 4)] for _ in range(len(IDS))), SHS, IDS)
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    fetch_usa_bea(ARCHIVES[1], _wb, _sh, _id) for _wb, _sh, _id in zip(
                        tuple(WBS[1 + 2*(_ // 4)] for _ in range(len(IDS))), SHS, IDS)
                ],
                axis=1,
                sort=True
            ),
        ],
        sort=True
    ).drop_duplicates()
    _data_nipa.loc[:, [IDS[2]]] = _data_nipa.loc[:, [IDS[2]]].rdiv(100)

    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WBS = (
        'Section2ALL_xls.xls',
        'Section4ALL_xls.xls',
    )
    SHS = (
        '201 Ann',
        '203 Ann',
        '401 Ann',
        '403 Ann',
    )
    IDS = (
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
                tuple(WBS[_ // 2] for _ in range(len(IDS))), SHS, IDS)
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


def get_data_infcf():
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
    result_frame['cpiu_fused'] = result_frame.mean(1)
    return result_frame.iloc[:, [-1]].dropna()


def get_data_local():
    ARCHIVES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WBS = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SHS = (
        '10105 Ann',
        '10105 Ann',
        '10106 Ann',
        '50900 Ann',
    )
    IDS = (
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
                [fetch_usa_bea(ARCHIVES[0], _wb, _sh, _id)
                 for _wb, _sh, _id in zip(tuple(WBS[2*(_ // 3)] for _ in range(len(IDS))), SHS, IDS)],
                axis=1,
                sort=True,
            ),
            pd.concat(
                [fetch_usa_bea(ARCHIVES[1], _wb, _sh, _id)
                 for _wb, _sh, _id in zip(tuple(WBS[1 + 2*(_ // 3)] for _ in range(len(IDS))), SHS, IDS)],
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


def get_dataset():
    '''Data Fetch'''
    '''Data Fetch for Capital'''
    capital_frame_a = get_data_cobb_douglas_extension_capital()
    '''Data Fetch for Capital Deflator'''
    capital_frame_b = get_data_cobb_douglas_deflator()
    capital_frame = pd.concat(
        [capital_frame_a, capital_frame_b], axis=1, sort=True)
    capital_frame.dropna(inplace=True)
    capital_frame['capital_real'] = capital_frame.iloc[:, 0].div(
        capital_frame.iloc[:, 1])
    '''Data Fetch for Labor'''
    labor_frame = get_data_cobb_douglas_extension_labor()
    '''Data Fetch for Product'''
    product_frame = get_data_cobb_douglas_extension_product()
    result_frame = pd.concat([capital_frame.iloc[:, 2], labor_frame, product_frame],
                             axis=1, sort=True).dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame


def get_data_updated():
    URL = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    _data = fetch_usa_bea_from_url(URL)
    IDS = (
        'A006RC',
        'A006RD',
        'A191RC',
        'A191RX',
    )
    _data_nipa = pd.concat(
        [
            fetch_usa_bea_from_loaded(_data, _id) for _id in IDS
        ],
        axis=1,
        sort=True
    )
    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WB = 'Section4ALL_xls.xls'
    SHS = (
        '403 Ann',
        '402 Ann',
    )
    IDS = (
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
            fetch_usa_bea(ARCHIVE_NAME, WB, _sh, _id) for _sh, _id in zip(SHS, IDS)
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
    _data['_rto'] = _data.iloc[:, -
                               2].mul(1).sub(_data.iloc[:, -1].shift(-1)).div(_data.iloc[:, -1]).add(1)
    return (
        _data.loc[:, ['_inv', 'A191RX', '_cap', '_rto']].dropna(),
        _data.loc[:, ['_rto']].dropna(),
        _data.index.get_loc(2012)
    )


def get_data_usa_bea_labor():
    # =========================================================================
    # Labor Series: A4601C0, 1929--2011
    # =========================================================================
    ARCHIVES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WBS = (
        'Section6ALL_Hist.xls',
        'Section6ALL_Hist.xls',
        'Section6all_xls.xls',
        'Section6all_xls.xls',
        'Section6all_xls.xls',
    )
    SHS = (
        '60800A Ann',
        '60800B Ann',
        '60800B Ann',
        '60800C Ann',
        '60800D Ann',
    )
    ID = 'A4601C0'
    data_frame = pd.concat(
        [fetch_usa_bea(archive, wb, sh, ID)
         for archive, wb, sh in zip(ARCHIVES, WBS, SHS)],
        axis=1,
        sort=True)
    data_frame[ID] = data_frame.mean(1)
    return data_frame.iloc[:, [-1]].dropna()


def get_data_usa_bea_labor_mfg():
    # =========================================================================
    # Manufacturing Labor Series: H4313C0, 1929--1948
    # Manufacturing Labor Series: J4313C0, 1948--1969
    # Manufacturing Labor Series: J4313C0, 1969--1987
    # Manufacturing Labor Series: A4313C0, 1987--2000
    # Manufacturing Labor Series: N4313C0, 1998--2011
    # =========================================================================
    ARCHIVES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WBS = (
        'Section6ALL_Hist.xls',
        'Section6ALL_Hist.xls',
        'Section6all_xls.xls',
        'Section6all_xls.xls',
        'Section6all_xls.xls',
    )
    SHS = (
        '60500A Ann',
        '60500B Ann',
        '60500B Ann',
        '60500C Ann',
        '60500D Ann',
    )
    IDS = (
        'H4313C0',
        'J4313C0',
        'J4313C0',
        'A4313C0',
        'N4313C0',
    )
    data_frame = pd.concat(
        [fetch_usa_bea(archive, wb, sh, _id)
         for archive, wb, sh, _id in zip(ARCHIVES, WBS, SHS, IDS)],
        axis=1,
        sort=True)
    data_frame['mfg_labor'] = data_frame.mean(1)
    return data_frame.iloc[:, [-1]].dropna()


def get_data_usa_bls_cpiu():
    '''BLS CPI-U Price Index Fetch'''
    FILE_NAME = 'dataset_usa_bls_cpiai.txt'
    data_frame = pd.read_csv(FILE_NAME,
                             sep='\s+',
                             index_col=0,
                             usecols=range(13),
                             skiprows=16)
    data_frame.rename_axis('period', inplace=True)
    data_frame['mean'] = data_frame.mean(1)
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
    return data_frame.iloc[:, [-1]].dropna()


def get_data_usa_capital():
    '''Series Not Used - `k3ntotl1si00`'''
    ARCHIVE_NAME = 'dataset_usa_cobb-douglas.zip'
    # Annual Increase in Terms of Cost Price (1)
    semi_frame_a = fetch_usa_classic(ARCHIVE_NAME, 'CDT2S1')
    ARCHIVE_NAME = 'dataset_usa_cobb-douglas.zip'
    # Annual Increase in Terms of 1880 dollars (3)
    semi_frame_b = fetch_usa_classic(ARCHIVE_NAME, 'CDT2S3')
    ARCHIVE_NAME = 'dataset_usa_cobb-douglas.zip'
    # Total Fixed Capital in 1880 dollars (4)
    semi_frame_c = fetch_usa_classic(ARCHIVE_NAME, 'CDT2S4')
    URL = 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    loaded_frame = fetch_usa_bea_from_url(URL)
    '''Fixed Assets: k1n31gd1es00, 1925--2019, Table 4.1. Current-Cost Net\
    Stock of Private Nonresidential Fixed Assets by Industry Group and\
    Legal Form of Organization'''
    semi_frame_d = fetch_usa_bea_from_loaded(loaded_frame, 'k1n31gd1es00')
    '''Not Used: Fixed Assets: k3n31gd1es00, 1925--2019, Table 4.3.\
    Historical-Cost Net Stock of Private Nonresidential Fixed Assets by\
    Industry Group and Legal Form of Organization'''
    semi_frame_e = fetch_usa_bea_from_loaded(loaded_frame, 'k3n31gd1es00')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    semi_frame_f = fetch_usa_census(ARCHIVE_NAME, 'P0107')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    semi_frame_g = fetch_usa_census(ARCHIVE_NAME, 'P0110')
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    semi_frame_h = fetch_usa_census(ARCHIVE_NAME, 'P0119')
    '''Kendrick J.W., Productivity Trends in the United States, Page 320'''
    ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
    semi_frame_i = fetch_usa_classic(ARCHIVE_NAME, 'KTA15S08')
    '''Douglas P.H., Theory of Wages, Page 332'''
    ARCHIVE_NAME = 'dataset_douglas.zip'
    semi_frame_j = fetch_usa_classic(ARCHIVE_NAME, 'DT63AS01')
    '''FRB Data'''
    semi_frame_k = get_data_usa_frb_fa()
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c,
                              semi_frame_d, semi_frame_e, semi_frame_f,
                              semi_frame_g, semi_frame_h, semi_frame_i,
                              semi_frame_j, semi_frame_k], axis=1, sort=True)
    return result_frame


def get_data_usa_frb_cu():
    '''Indexed Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
    CAPUTL.B50001.A Fetching'''
    FILE_NAME = 'dataset_usa_FRB_G17_All_Annual 2013-06-23.csv'
    series_id = 'CAPUTLB50001A'
    data_frame = pd.read_csv(FILE_NAME, skiprows=1, usecols=range(5, 100))
    data_frame.columns = ['period', *data_frame.columns[1:]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].str.replace(r"[,@\'?\.$%_]",
                                                              '',
                                                              regex=True)
    data_frame = data_frame.set_index(data_frame.columns[0]).transpose()
    data_frame.index = pd.to_numeric(data_frame.index, downcast='integer')
    return data_frame.loc[:, [series_id]].dropna()


def get_data_usa_frb_fa():
    '''Returns Frame of Manufacturing Fixed Assets Series, Billion USD:
    data_frame.iloc[:,0]: Nominal;
    data_frame.iloc[:,1]: Real
    '''
    FILE_NAME = 'dataset_usa_frb-invest_capital.csv'
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
    FILE_NAME = 'dataset_usa_frb-invest_capital.csv'
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
    FILE_NAME = 'dataset_usa_frb-US3_IP 2018-09-02.csv'
    series_id = 'AIPMA_SA_IX'
    data_frame = pd.read_csv(FILE_NAME, skiprows=7, parse_dates=[0])
    data_frame.columns = [column.strip() for column in data_frame.columns]
    data_frame = data_frame.loc[:, [data_frame.columns[0], series_id]]
    data_frame['period'] = data_frame.iloc[:, 0].dt.year
    return data_frame.groupby(data_frame.columns[-1]).mean()


def get_data_usa_frb_ms():
    """Indexed Money Stock Measures (H.6) Series:
    https://www.federalreserve.gov/datadownload/Download.aspx?rel=h6&series=5398d8d1734b19f731aba3105eb36d47&filetype=csv&label=include&layout=seriescolumn&from=01/01/1959&to=12/31/2018"""
    FILE_NAME = 'dataset_usa_FRB_H6.csv'
    data_frame = pd.read_csv(FILE_NAME, skiprows=5, usecols=range(2))
    data_frame[['period',
                'month', ]] = data_frame.iloc[:, 0].str.split('-', expand=True)
    data_frame.columns = [re.sub(r"[,@\'?\.$%_]",
                                 "",
                                 column) for column in data_frame.columns]
    data_frame.iloc[:, -2] = data_frame.iloc[:, -2].astype(int)
    return data_frame.groupby(data_frame.columns[-2]).mean()


def get_data_usa_mcconnel_a():
    SERIES_ID = 'Валовой внутренний продукт, млрд долл. США'
    data_frame = fetch_usa_mcconnel(SERIES_ID)
    return data_frame[data_frame.index.get_loc(1980):].reset_index(level=0)


def get_data_usa_mcconnel_b():
    SERIES_IDS = {
        'Ставка прайм-рейт, %': 'prime_rate',
        'Национальный доход, млрд долл. США': 'A032RC1',
    }
    data_frame = pd.concat([fetch_usa_mcconnel(series_id)
                           for series_id in SERIES_IDS.keys()],
                           axis=1,
                           sort=True)
    data_frame.columns = list(SERIES_IDS.values())
    return data_frame[data_frame.index.get_loc(1980):].reset_index(level=0)


def get_data_usa_mcconnel_c():
    SERIES_IDS = {
        'Ставка прайм-рейт, %': 'prime_rate',
        'Валовой объем внутренних частных инвестиций, млрд долл. США': 'A006RC1',
    }
    data_frame = pd.concat([fetch_usa_mcconnel(series_id)
                           for series_id in SERIES_IDS.keys()],
                           axis=1,
                           sort=True)
    data_frame.columns = list(SERIES_IDS.values())
    return data_frame[data_frame.index.get_loc(1980):].reset_index(level=0)


def get_data_usa_xlsm():
    ARCHIVES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WBS = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
    )
    SHS = (
        '10105 Ann',
        '10105 Ann',
        '10106 Ann',
        '10705 Ann',
    )
    IDS = (
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
                [fetch_usa_bea(ARCHIVES[0], WBS[0], _sh, _id)
                 for _sh, _id in zip(SHS, IDS)],
                axis=1,
                sort=True
            ),
            pd.concat(
                [fetch_usa_bea(ARCHIVES[1], WBS[1], _sh, _id)
                 for _sh, _id in zip(SHS, IDS)],
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
    ARCHIVES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WBS = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
    )
    SH, ID = ('10106 Ann', 'A191RX1')
    ARGS = (
        'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
        'Section4ALL_xls.xls',
        '402 Ann',
        'kcn31gd1es000',
    )
    _data_a = pd.concat(
        [
            # =================================================================
            # Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
            # =================================================================
            fetch_usa_bea(*ARGS),
            # =================================================================
            # Labor
            # =================================================================
            get_data_usa_bea_labor_mfg(),
            # =================================================================
            # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
            # =================================================================
            pd.concat(
                [
                    fetch_usa_bea(_archive, _wb, SH, ID) for _archive, _wb in zip(ARCHIVES, WBS)
                ],
                sort=True).drop_duplicates(),
        ],
        axis=1, sort=True).dropna()
    _data_b = pd.concat(
        [
            # =================================================================
            # Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
            # =================================================================
            fetch_usa_bea(*ARGS),
            # =================================================================
            # Labor
            # =================================================================
            get_data_usa_bea_labor_mfg(),
            # =================================================================
            # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
            # =================================================================
            pd.concat(
                [
                    fetch_usa_bea(_archive, _wb, SH, ID) for _archive, _wb in zip(ARCHIVES, WBS)
                ],
                sort=True).drop_duplicates(),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            get_data_usa_frb_cu(),
        ],
        axis=1, sort=True).dropna()
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
    ).dropna()
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
    ).dropna()
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
        axis=1, sort=True).dropna()
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
    SERIES_IDS = [
        'v123355112',
        'v1235071986',
        'v2057609',
        'v2057818',
        'v2523013',
    ]
    for series_id in SERIES_IDS:
        chunk = _.loc[:, [series_id]]
        chunk.dropna(inplace=True)
        result = pd.concat([result, chunk], axis=1, sort=False)
    result.dropna(inplace=True)
    result['std'] = result.std(axis=1)
    return (result.iloc[:, [-1]].idxmin()[0],
            result.loc[result.iloc[:, [-1]].idxmin()[0], :][:-1].mean())


def get_series_ids(archive_name):
    '''Returns Dictionary for Series from Douglas's & Kendrick's Databases'''
    data_frame = pd.read_csv(archive_name, usecols=[3, 4, ])
    return dict(zip(data_frame.iloc[:, 1], data_frame.iloc[:, 0]))


def KZF(source_frame, k=1):
    '''Kolmogorov--Zurbenko Filter
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Series
    '''
    series = source_frame.iloc[:, 1]
    result_frame = source_frame
    for i in range(1, 1 + k):
        series = series.rolling(window=2).mean()
        skz = series.shift(-(i//2))
        result_frame = pd.concat([result_frame, skz], axis=1, sort=True)
    odd_frame = result_frame.iloc[:, 0]
    even_frame = result_frame.iloc[:, 0].rolling(window=2).mean()
    for i in range(1, 2 + k, 2):
        odd_frame = pd.concat(
            [odd_frame, result_frame.iloc[:, i]], axis=1, sort=True)
    for i in range(2, 2 + k, 2):
        even_frame = pd.concat(
            [even_frame, result_frame.iloc[:, i]], axis=1, sort=True)
    even_frame = even_frame.dropna(how='all').reset_index(drop=True)
    odd_frame = odd_frame.set_index('Period')
    even_frame = even_frame.set_index('Period')
    return odd_frame, even_frame


def RMF(source_frame, k=1):
    '''Rolling Mean Filter
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Series
    '''
    series = source_frame.iloc[:, 1]
    result_frame = source_frame
    for i in range(1, 1 + k):
        rmf = series.rolling(window=1 + i, center=True).mean()
        result_frame = pd.concat([result_frame, rmf], axis=1, sort=True)
    odd_frame = result_frame.iloc[:, 0]
    even_frame = result_frame.iloc[:, 0].rolling(window=2).mean()
    for i in range(1, 2 + k, 2):
        odd_frame = pd.concat(
            [odd_frame, result_frame.iloc[:, i]], axis=1, sort=True)
    for i in range(2, 2 + k, 2):
        even_frame = pd.concat(
            [even_frame, result_frame.iloc[:, i]], axis=1, sort=True)
    even_frame = even_frame.dropna(how='all').reset_index(drop=True)
    odd_frame = odd_frame.set_index('Period')
    even_frame = even_frame.set_index('Period')
    return odd_frame, even_frame


def lookup(data_frame):
    for i, series_id in enumerate(data_frame.columns):
        series = data_frame.iloc[:, i].sort_values().unique()
        print('{:*^50}'.format(series_id))
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
        width = max(len('{}'.format(item)), width)
    if width > 4:
        data[['YEAR', 'Q']] = data.index.to_series().str.split('-', expand=True)
        data = data.iloc[:, [1, 0]]
        data = data.apply(pd.to_numeric)
        data = data.groupby('YEAR').mean()
        data.index.rename('REF_DATE', inplace=True)
    return data


def m_spline_ea(source_frame, intervals, k):
    '''Exponential Spline, Type A
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Target Series,
    intervals: Number of Intervals,
    k: Interpolation Knots'''
    A, K, S = [], [], []
    for j in range(intervals):  # Coefficient Section
        A.append(((source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[0], 0])*np.log(source_frame.iloc[k[j], 1])-(source_frame.iloc[k[j], 0] -
                 source_frame.iloc[k[0], 0])*np.log(source_frame.iloc[k[1 + j], 1]))/(source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0]))
        if j == 0:
            K.append((np.log(source_frame.iloc[k[1 + j], 1])-np.log(source_frame.iloc[k[j], 1]))/(
                source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0]))
        else:
            K.append(K[j-1] + np.log(source_frame.iloc[k[1 + j], 1])/(source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0]) -
                     (source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j-1], 0])*np.log(source_frame.iloc[k[j], 1])/((source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0])*(source_frame.iloc[k[j], 0]-source_frame.iloc[k[j-1], 0])) +
                     np.log(source_frame.iloc[k[j-1], 1])/(source_frame.iloc[k[j], 0]-source_frame.iloc[k[j-1], 0]))
        if j == intervals-1:  # Spline Section
            for i in range(k[j], 1 + k[1 + j]):
                S.append(
                    sp.exp(A[j] + K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[0, 0])))
        else:
            for i in range(k[j], k[1 + j]):
                S.append(
                    sp.exp(A[j] + K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[0, 0])))
    S = pd.DataFrame(S, columns=['Spline'])  # Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis=1, sort=True)
    return K, result_frame


def m_spline_eb(source_frame, intervals, k):
    '''Exponential Spline, Type B
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Target Series,
    intervals: Number of Intervals,
    k: Interpolation Knots'''
    K, S = [], []
    for j in range(intervals):  # Coefficient Section
        K.append((np.log(source_frame.iloc[k[1 + j], 1])-np.log(source_frame.iloc[k[j], 1]))/(
            source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0]))
        if j == intervals-1:  # Spline Section
            for i in range(k[j], 1 + k[1 + j]):
                S.append(source_frame.iloc[k[j], 1]*sp.exp(K[j] *
                         (source_frame.iloc[i, 0]-source_frame.iloc[k[j], 0])))
        else:
            for i in range(k[j], k[1 + j]):
                S.append(source_frame.iloc[k[j], 1]*sp.exp(K[j] *
                         (source_frame.iloc[i, 0]-source_frame.iloc[k[j], 0])))
    S = pd.DataFrame(S, columns=['Spline'])  # Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis=1, sort=True)
    return K, result_frame


def m_spline_la(source_frame, intervals, k):
    '''Linear Spline, Type A
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Target Series,
    intervals: Number of Intervals,
    k: Interpolation Knots'''
    A, K, S = [], [], []
    for j in range(intervals):
        A.append(((source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[0], 0])*source_frame.iloc[k[j], 1]-(source_frame.iloc[k[j], 0] -
                 source_frame.iloc[k[0], 0])*source_frame.iloc[k[1 + j], 1])/(source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0]))
        if j == 0:
            K.append((source_frame.iloc[k[1 + j], 1]-source_frame.iloc[k[j], 1])/(
                source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0]))
        else:
            K.append(K[j-1] + source_frame.iloc[k[1 + j], 1]/(source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0]) -
                     (source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j-1], 0])*source_frame.iloc[k[j], 1]/((source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0])*(source_frame.iloc[k[j], 0]-source_frame.iloc[k[j-1], 0])) +
                     source_frame.iloc[k[j-1], 1]/(source_frame.iloc[k[j], 0]-source_frame.iloc[k[j-1], 0]))
        if j == intervals-1:
            for i in range(k[j], 1 + k[1 + j]):
                S.append(A[j] + K[j]*(source_frame.iloc[i, 0] -
                         source_frame.iloc[0, 0]))
        else:
            for i in range(k[j], k[1 + j]):
                S.append(A[j] + K[j]*(source_frame.iloc[i, 0] -
                         source_frame.iloc[0, 0]))
    S = pd.DataFrame(S, columns=['Spline'])  # Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis=1, sort=True)
    return K, result_frame


def m_spline_lb(source_frame, intervals, k):
    '''Linear Spline, Type B
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Target Series,
    intervals: Number of Intervals,
    k: Interpolation Knots'''
    K, S = [], []
    for j in range(intervals):
        K.append((source_frame.iloc[k[1 + j], 1]-source_frame.iloc[k[j], 1])/(
            source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0]))
        if j == intervals-1:
            for i in range(k[j], 1 + k[1 + j]):
                S.append(source_frame.iloc[k[j], 1] + K[j] *
                         (source_frame.iloc[i, 0]-source_frame.iloc[k[j], 0]))
        else:
            for i in range(k[j], k[1 + j]):
                S.append(source_frame.iloc[k[j], 1] + K[j] *
                         (source_frame.iloc[i, 0]-source_frame.iloc[k[j], 0]))
    S = pd.DataFrame(S, columns=['Spline'])  # Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis=1, sort=True)
    return K, result_frame


def m_spline_lls(source_frame, intervals, k):
    '''Linear Spline, Linear Regression Kernel
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Target Series,
    intervals: Number of Intervals,
    k: Interpolation Knots'''
    A, K, S = [], [], []
    for j in range(intervals):
        s_1, s_2, s_3, s_4 = 0, 0, 0, 0  # X, Y, X**2, XY # # Summarize
        if j == intervals-1:
            for i in range(k[j], 1 + k[1 + j]):
                S_1 += source_frame.iloc[i, 0]
                S_2 += source_frame.iloc[i, 1]
                S_3 += (source_frame.iloc[i, 0])**2
                S_4 += source_frame.iloc[i, 0]*source_frame.iloc[i, 1]
            A.append(((1 + k[1 + j]-k[j])*S_4-S_1*S_2) /
                     ((1 + k[1 + j]-k[j])*S_3-S_1**2))
        else:
            for i in range(k[j], k[1 + j]):
                S_1 += source_frame.iloc[i, 0]
                S_2 += source_frame.iloc[i, 1]
                S_3 += (source_frame.iloc[i, 0])**2
                S_4 += source_frame.iloc[i, 0]*source_frame.iloc[i, 1]
            if j == 0:
                A.append((S_2*S_3-S_1*S_4)/((k[1 + j]-k[j])*S_3-S_1**2))
            A.append(((k[1 + j]-k[j])*S_4-S_1*S_2) /
                     ((k[1 + j]-k[j])*S_3-S_1**2))
    for j in range(intervals):
        if j == 0:
            K.append(A[j])
        else:
            K.append(K[j-1] + (A[j]-A[1 + j])*source_frame.iloc[k[j], 0])
        if j == intervals-1:
            for i in range(k[j], 1 + k[1 + j]):
                S.append(K[j] + A[1 + j]*source_frame.iloc[i, 0])
        else:
            for i in range(k[j], k[1 + j]):
                S.append(K[j] + A[1 + j]*source_frame.iloc[i, 0])
    S = pd.DataFrame(S, columns=['Spline'])  # Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis=1, sort=True)
    return A, result_frame


def period_centering(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Series
    '''
    '''Variables Initialised'''
    result_frame = source_frame  # DataFrame for Results
    period = result_frame.iloc[:, 0]
    series = result_frame.iloc[:, 1]
    '''Loop'''
    for i in range(1, 1 + result_frame.shape[0]//2):
        period = period.rolling(window=2).mean()
        series = series.rolling(window=2).mean()
        period_roll = period.shift(-(i//2))
        series_roll = series.shift(-(i//2))
        series_frac = series_roll.div(result_frame.iloc[:, 1])
        series_diff = (series_roll.shift(-2) -
                       series_roll).div(2*series_roll.shift(-1))
        result_frame = pd.concat(
            [result_frame, period_roll, series_roll, series_frac, series_diff], axis=1, sort=True)
    return result_frame


def preprocessing_a(source_frame):
    source_frame = source_frame.iloc[:, [0, 4, 6, 7]]
    source_frame = source_frame.dropna()
    source_frame = source_frame.div(source_frame.iloc[0, :])
    source_frame.reset_index(level=0, inplace=True)
    return source_frame


def preprocessing_b(source_frame):
    source_frame = source_frame.iloc[:, [0, 6, 7, 20]]
    source_frame = source_frame.dropna()
    source_frame.reset_index(level=0, inplace=True)
    return source_frame


def preprocessing_c(source_frame):
    source_frame_production = source_frame.iloc[:, [0, 6, 7]]
    source_frame_production = source_frame_production.dropna()
    source_frame_production = source_frame_production.div(
        source_frame_production.iloc[0, :])
    source_frame_money = source_frame.iloc[:, 18:20]
    source_frame_money = source_frame_money.mean(1)
    source_frame_money = pd.DataFrame(source_frame_money, columns=[
                                      'M1'])  # Convert Series to Dataframe
    source_frame_money = source_frame_money.dropna()
    source_frame_money = source_frame_money.div(source_frame_money.iloc[0, :])
    result_frame = pd.concat(
        [source_frame_production, source_frame_money], axis=1)
    result_frame = result_frame.dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    result_frame.reset_index(level=0, inplace=True)
    return result_frame


def preprocessing_d(source_frame):
    source_frame = source_frame.iloc[:, [0, 1, 2, 3, 7]]
    source_frame = source_frame.dropna()
    source_frame.reset_index(level=0, inplace=True)
    return source_frame


def preprocessing_e(data_frame):
    '''Works on Result of `get_data_combined_archived()`'''
    # =========================================================================
    # `Real` Investment
    # =========================================================================
    data_frame['inv'] = data_frame.iloc[:, 0].mul(
        data_frame.iloc[:, 7]).div(data_frame.iloc[:, 6])
    # =========================================================================
    # `Real` Capital
    # =========================================================================
    data_frame['cap'] = data_frame.iloc[:, 11].mul(
        data_frame.iloc[:, 7]).div(data_frame.iloc[:, 6])
    # =========================================================================
    # Nominal DataSet
    # =========================================================================
    nominal_frame = data_frame.iloc[:, [0, 6, 11]].dropna()
    # =========================================================================
    # `Real` DataSet
    # =========================================================================
    real_frame = data_frame.iloc[:, [21, 7, 22]].dropna()
    return nominal_frame, real_frame


def preprocessing_f(testing_frame):
    '''testing_frame: test _frame'''
    '''control _frame'''
    FILE_NAME = 'dataset_usa_reference_ru_kurenkov-yu-v.csv'
    control_frame = pd.read_csv(FILE_NAME, index_col=0)
    '''Data Fetch'''
    '''Production'''
    semi_frame_a_a = control_frame.iloc[:, [0]]
    semi_frame_a_b = testing_frame.iloc[:, [7]].dropna()
    semi_frame_a_c = get_data_usa_frb_ip()
    result_frame_a = pd.concat(
        [semi_frame_a_a, semi_frame_a_b, semi_frame_a_c], axis=1, sort=True)
    result_frame_a = result_frame_a.div(result_frame_a.iloc[31, :]).mul(100)
    '''Labor'''
    semi_frame_b_a = control_frame.iloc[:, [1]]
    semi_frame_b_b = testing_frame.iloc[:, [8]].dropna()
    result_frame_b = pd.concat(
        [semi_frame_b_a, semi_frame_b_b], axis=1, sort=True)
    '''Capital'''
    semi_frame_c_a = control_frame.iloc[:, [2]]
    semi_frame_c_b = testing_frame.iloc[:, [11]].dropna()
    result_frame_c = pd.concat(
        [semi_frame_c_a, semi_frame_c_b], axis=1, sort=True)
    result_frame_c = result_frame_c.div(result_frame_c.iloc[1, :]).mul(100)
    '''Capacity Utilization'''
    semi_frame_d_a = control_frame.iloc[:, [3]]
    semi_frame_d_b = get_data_usa_frb_cu()
    result_frame_d = pd.concat(
        [semi_frame_d_a, semi_frame_d_b], axis=1, sort=True)
    return result_frame_a, result_frame_b, result_frame_c, result_frame_d


def plot_approx_linear(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Real Values for Price Deflator,
    source_frame.iloc[:, 2]: Nominal Values for Price Deflator,
    source_frame.iloc[:, 3]: Regressor,
    source_frame.iloc[:, 4]: Regressand
    '''
    i = source_frame.shape[0]-1
    while abs(source_frame.iloc[i, 2]-source_frame.iloc[i, 1]) > 1:
        i -= 1
        base = i  # Basic Year
    D = source_frame.iloc[:, 1].div(source_frame.iloc[:, 2])  # Deflator
    # DataFrame for Based Linear Approximation Results
    result_frame = source_frame.iloc[:, 0]
    calcul_frame = []  # Blank List for Calculation Results
    for i in range(source_frame.shape[0]):
        X = source_frame.iloc[i, 3]*D[i]/(source_frame.iloc[0, 3]*D[0])
        Y = source_frame.iloc[i, 4]*D[i]/(source_frame.iloc[0, 4]*D[0])
        calcul_frame.append({'X': X, 'Y': Y})

    calcul_frame = pd.DataFrame(calcul_frame)  # Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis=1, sort=True)

    S_1, S_2, S_3, S_4 = 0, 0, 0, 0  # X, Y, X**2, XY # # Summarize
    for i in range(source_frame.shape[0]):
        S_1 += source_frame.iloc[i, 3]*D[i]/(source_frame.iloc[0, 3]*D[0])
        S_2 += source_frame.iloc[i, 4]*D[i]/(source_frame.iloc[0, 4]*D[0])
        S_3 += (source_frame.iloc[i, 3]*D[i]/(source_frame.iloc[0, 3]*D[0]))**2
        S_4 += source_frame.iloc[i, 3]*source_frame.iloc[i, 4]*(D[i])**2/(
            source_frame.iloc[0, 3]*source_frame.iloc[0, 4]*(D[0]**2))
    '''Approximation'''
    A_0 = (S_2*S_3-S_1*S_4)/(source_frame.shape[0]*S_3-S_1**2)
    A_1 = (source_frame.shape[0]*S_4-S_1*S_2) / \
        (source_frame.shape[0]*S_3-S_1**2)
    calcul_frame = []  # Blank List for Calculation Results
    for i in range(source_frame.shape[0]):
        Y = A_0 + A_1*source_frame.iloc[i, 3] * \
            D[i]/(source_frame.iloc[0, 3]*D[0])
        calcul_frame.append({'YH': Y})

    calcul_frame = pd.DataFrame(calcul_frame)  # Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis=1, sort=True)

    print('Period From: {} Through: {}'.format(
        source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    print('Prices: {}=100'.format(source_frame.iloc[base, 0]))
    print('Model: Yhat = {:.4f}+{:.4f}*X'.format(A_0, A_1))
    print('Model Parameter: A_0 = {:.4f}'.format(A_0))
    print('Model Parameter: A_1 = {:.4f}'.format(A_1))
    plt.figure()
    plt.title('$Y(X)$, {}=100, {}$-${}'.format(
        source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Gross Private Domestic Investment, $X(\\tau)$, {}=100, {}=100'.format(
        source_frame.iloc[base, 0], source_frame.iloc[0, 0]))
    plt.ylabel('Gross Domestic Product, $Y(\\tau)$, {}=100, {}=100'.format(
        source_frame.iloc[base, 0], source_frame.iloc[0, 0]))
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:, 2])
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:, 3],
             label='$\\hat Y = {:.4f}+{:.4f}X$'.format(A_0, A_1))
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_approx_log_linear(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Real Values for Price Deflator,
    source_frame.iloc[:, 2]: Nominal Values for Price Deflator,
    source_frame.iloc[:, 3]: Regressor,
    source_frame.iloc[:, 4]: Regressand
    '''
    i = source_frame.shape[0]-1
    while abs(source_frame.iloc[i, 2]-source_frame.iloc[i, 1]) > 1:
        i -= 1
        base = i  # Basic Year
    D = source_frame.iloc[:, 1].div(source_frame.iloc[:, 2])  # Deflator
    # DataFrame for Based Log-Linear Approximation Results
    result_frame = source_frame.iloc[:, 0]
    calcul_frame = []  # Blank List for Calculation Results

    for i in range(source_frame.shape[0]):
        X = math.log(source_frame.iloc[i, 3])-math.log(source_frame.iloc[0, 3])
        Y = math.log(source_frame.iloc[i, 4]) + math.log(D[i]) - \
            math.log(source_frame.iloc[0, 4])-math.log(D[0])
        calcul_frame.append({'X': X, 'Y': Y})

    calcul_frame = pd.DataFrame(calcul_frame)  # Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis=1, sort=True)

    S_1, S_2, S_3, S_4 = 0, 0, 0, 0  # Summarize
    for i in range(source_frame.shape[0]):
        S_1 += math.log(source_frame.iloc[i, 3]) - \
            math.log(source_frame.iloc[0, 3])
        S_2 += math.log(source_frame.iloc[i, 4]) + math.log(D[i]) - \
            math.log(source_frame.iloc[0, 4])-math.log(D[0])
        S_3 += (math.log(source_frame.iloc[i, 3]) -
                math.log(source_frame.iloc[0, 3]))**2
        S_4 += (math.log(source_frame.iloc[i, 3])-math.log(source_frame.iloc[0, 3]))*(math.log(
            D[i]) + math.log(source_frame.iloc[i, 4])-math.log(D[0])-math.log(source_frame.iloc[0, 4]))
    '''Approximation'''
    A_0 = (S_2*S_3-S_1*S_4)/(source_frame.shape[0]*S_3-S_1**2)
    A_1 = (source_frame.shape[0]*S_4-S_1*S_2) / \
        (source_frame.shape[0]*S_3-S_1**2)
    calcul_frame = []  # Blank List for Calculation Results
    for i in range(source_frame.shape[0]):
        Y = A_0 + A_1 * \
            (math.log(source_frame.iloc[i, 3]) -
             math.log(source_frame.iloc[0, 3]))  # Yhat
        calcul_frame.append({'YH': Y})

    calcul_frame = pd.DataFrame(calcul_frame)  # Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis=1, sort=True)

    print('Period From: {} Through: {}'.format(
        source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    print('Prices: {}=100'.format(source_frame.iloc[base, 0]))
    print('Model: Yhat = {:.4f}+{:.4f}*Ln(X)'.format(A_0, A_1))
    print('Model Parameter: A_0 = {:.4f}'.format(A_0))
    print('Model Parameter: A_1 = {:.4f}'.format(A_1))
    plt.figure()
    plt.title('$Y(X)$, {}=100, {}$-${}'.format(
        source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Logarithm Prime Rate, $X(\\tau)$, {}=100'.format(
        source_frame.iloc[0, 0]))
    # =========================================================================
    # TODO: What?
    # =========================================================================
    if source_frame.columns[4][:7] == 'A032RC1':
        desc = 'National Income'
    elif source_frame.columns[4][:7] == 'A191RC1':
        desc = 'Gross Domestic Product'
    plt.ylabel('Logarithm {}, $Y(\\tau)$, {}=100, {}=100'.format(
        desc, source_frame.iloc[base, 0], source_frame.iloc[0, 0]))
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:, 2])
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:, 3],
             label='$\\hat Y = {:.4f}+{:.4f}X$'.format(A_0, A_1))
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_a(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Gross Domestic Investment,
    source_frame.iloc[:, 2]: National Income,
    source_frame.iloc[:, 3]: Nominal Gross Domestic Product,
    source_frame.iloc[:, 4]: Real Gross Domestic Product
    '''
    '''`Real` Investment'''
    source_frame['inv'] = source_frame.iloc[:, 1] * \
        source_frame.iloc[:, 4].div(source_frame.iloc[:, 3])
    '''`Real` Production'''
    source_frame['prd'] = source_frame.iloc[:, 2] * \
        source_frame.iloc[:, 4].div(source_frame.iloc[:, 3])
    plt.figure()
    plt.title('Gross Private Domestic Investment & National Income, {}$-${}'.format(
        source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:,
             5], label='Gross Private Domestic Investment')
    plt.plot(source_frame.iloc[:, 0],
             source_frame.iloc[:, 6], label='National Income')
    plt.xlabel('Period')
    plt.ylabel('Index')
    source_frame.iloc[:, 0] = source_frame.iloc[:,
                                                0].shift(-1).add(source_frame.iloc[:, 0]).div(2)
    X = source_frame.iloc[:, 5].shift(-1).add(source_frame.iloc[:, 5]).div(2)
    Y = source_frame.iloc[:, 6].shift(-1).add(source_frame.iloc[:, 6]).div(2)
    plt.plot(source_frame.iloc[:, 0], X, '--',
             source_frame.iloc[:, 0], Y, '--')
    plt.grid()
    plt.legend()
    plt.show()


def plot_b(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Gross Domestic Investment,
    source_frame.iloc[:, 2]: Nominal Gross Domestic Product,
    source_frame.iloc[:, 3]: Real Gross Domestic Product,
    source_frame.iloc[:, 4]: Prime Rate
    '''
    '''`Real` Investment'''
    source_frame['inv'] = source_frame.iloc[:, 1].mul(
        source_frame.iloc[:, 3]).div(source_frame.iloc[:, 2])
    plt.figure()
    plt.plot(source_frame.iloc[:, 4], source_frame.iloc[:, 5])
    plt.title('Gross Private Domestic Investment, A006RC, {}$-${}'.format(
        source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Percentage')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.show()


def plot_c(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Gross Domestic Investment,
    source_frame.iloc[:, 2]: Nominal Gross Domestic Product,
    source_frame.iloc[:, 3]: Real Gross Domestic Product,
    source_frame.iloc[:, 4]: M1
    '''
    '''`Real` Investment'''
    source_frame['inv'] = source_frame.iloc[:, 1].mul(
        source_frame.iloc[:, 3]).div(source_frame.iloc[:, 2])
    plt.figure()
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:,
             3], label='Real Gross Domestic Product')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:,
             5], label='`Real` Gross Domestic Investment')
    plt.plot(source_frame.iloc[:, 0],
             source_frame.iloc[:, 4], label='Money Supply')
    plt.title('Indexes, {}$-${}'.format(
        source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_d(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Gross Domestic Investment,
    source_frame.iloc[:, 2]: Gross Domestic Investment Price Index,
    source_frame.iloc[:, 3]: Fixed Investment,
    source_frame.iloc[:, 4]: Fixed Investment Price Index,
    source_frame.iloc[:, 5]: Real Gross Domestic Product
    '''
    i = source_frame.shape[0]-1
    while abs(source_frame.iloc[i, 2]-100) > 0.1:
        i -= 1
        base = i  # Basic Year
    '''Real Investment, Billions'''
    source_frame['inv'] = source_frame.iloc[base, 1] * \
        source_frame.iloc[:, 2].div(100*1000)
    '''Real Fixed Investment, Billions'''
    source_frame['fnv'] = source_frame.iloc[base, 3] * \
        source_frame.iloc[:, 4].div(100*1000)
    source_frame.iloc[:, 5] = source_frame.iloc[:, 5].div(1000)
    plt.figure(1)
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 6],
                 label='Real Gross Private Domestic Investment $GPDI$')
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 7], color='red',
                 label='Real Gross Private Fixed Investment, Nonresidential $GPFI(n)$')
    plt.title('Real Indexes, {}=100, {}$-${}'.format(
        source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars')
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 5])
    plt.title('Real Gross Domestic Product $GDP$, {}=100, {}$-${}'.format(
        source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.figure(3)
    plt.plot(source_frame.iloc[:, 6], source_frame.iloc[:, 5])
    plt.title('$GPDI$ & $GPFI(n)$, {}=100, {}$-${}'.format(
        source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Billions of Dollars')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.figure(4)
    plt.plot(source_frame.iloc[:, 7], source_frame.iloc[:, 5])
    plt.title('$GPFI(n)$ & $GDP$, {}=100, {}$-${}'.format(
        source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Billions of Dollars')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.show()


def plot_block_zer(source_frame):
    '''
    source_frame.index: Period,
    source_frame.iloc[:, 0]: Capital,
    source_frame.iloc[:, 1]: Labor,
    source_frame.iloc[:, 2]: Product
    '''
    pd.options.mode.chained_assignment = None
    source_frame['lab_cap_int'] = source_frame.iloc[:, 0].div(
        source_frame.iloc[:, 1])  # Labor Capital Intensity
    source_frame['lab_product'] = source_frame.iloc[:, 2].div(
        source_frame.iloc[:, 1])  # Labor Productivity
    source_frame['log_lab_c'] = np.log(
        source_frame.iloc[:, 0].div(source_frame.iloc[:, 1]))
    source_frame['log_lab_p'] = np.log(
        source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]))
    result_frame_a = source_frame.iloc[:, [3, 4]]
    result_frame_b = source_frame.iloc[:, [5, 6]]
    a_0, a_1, ea = simple_linear_regression(result_frame_a)
    plot_simple_linear(result_frame_a, a_0, a_1, ea)
    b_0, b_1, eb = simple_linear_regression(result_frame_b)
    plot_simple_log(result_frame_b, b_0, b_1, eb)


def plot_block_one(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Capital,
    source_frame.iloc[:, 2]: Labor,
    source_frame.iloc[:, 3]: Product
    '''
    source_frame['lab_cap_int'] = source_frame.iloc[:, 1].div(
        source_frame.iloc[:, 2])  # Labor Capital Intensity
    labcap_frame = source_frame.iloc[:, [0, 4]]
    semi_frame_a, semi_frame_b = RMF(labcap_frame)
    semi_frame_c, semi_frame_d = KZF(labcap_frame)
    semi_frame_e = SES(labcap_frame, 5, 0.25)
    semi_frame_e = semi_frame_e.iloc[:, 1]
    odd_frame = pd.concat([semi_frame_a, semi_frame_e], axis=1, sort=True)
    even_frame = pd.concat([semi_frame_b, semi_frame_d], axis=1, sort=True)
    plt.figure()
    odd_frame.iloc[:, 0].plot(linewidth=3, label='Labor Capital Intensity')
    odd_frame.iloc[:, 1].plot(
        label='Single Exponential Smoothing, Window = {}, Alpha = {:, .2f}'.format(5, 0.25))
    even_frame.iloc[:, 0].plot(label='Rolling Mean, {}'.format(2))
    even_frame.iloc[:, 1].plot(
        label='Kolmogorov--Zurbenko Filter, {}'.format(2))
    plt.title('Labor Capital Intensity: Rolling Mean Filter, Kolmogorov--Zurbenko Filter &\n\
              Single Exponential Smoothing')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_block_two(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Capital,
    source_frame.iloc[:, 2]: Labor,
    source_frame.iloc[:, 3]: Product
    '''
    source_frame['lab_product'] = source_frame.iloc[:, 3].div(
        source_frame.iloc[:, 2])  # Labor Productivity
    labpro_frame = source_frame.iloc[:, [0, 4]]
    semi_frame_a, semi_frame_b = RMF(labpro_frame, 3)
    semi_frame_c, semi_frame_d = KZF(labpro_frame, 3)
    semi_frame_c = semi_frame_c.iloc[:, 1]
    semi_frame_e = SES(labpro_frame, 5, 0.25)
    semi_frame_e = semi_frame_e.iloc[:, 1]
    semi_frame_f = SES(labpro_frame, 5, 0.35)
    semi_frame_f = semi_frame_f.iloc[:, 1]
    semi_frame_g = SES(labpro_frame, 5, 0.45)
    semi_frame_g = semi_frame_g.iloc[:, 1]
    odd_frame = pd.concat([semi_frame_a, semi_frame_c, semi_frame_e,
                          semi_frame_f, semi_frame_g], axis=1, sort=True)
    even_frame = pd.concat([semi_frame_b, semi_frame_d], axis=1, sort=True)
    plt.figure()
    odd_frame.iloc[:, 0].plot(linewidth=3, label='Labor Productivity')
    odd_frame.iloc[:, 1].plot(label='Rolling Mean, {}'.format(3))
    odd_frame.iloc[:, 2].plot(
        label='Kolmogorov--Zurbenko Filter, {}'.format(3))
    odd_frame.iloc[:, 3].plot(
        label='Single Exponential Smoothing, Window = {}, Alpha = {:, .2f}'.format(5, 0.25))
    odd_frame.iloc[:, 4].plot(
        label='Single Exponential Smoothing, Window = {}, Alpha = {:, .2f}'.format(5, 0.35))
    odd_frame.iloc[:, 5].plot(
        label='Single Exponential Smoothing, Window = {}, Alpha = {:, .2f}'.format(5, 0.45))
    even_frame.iloc[:, 0].plot(label='Rolling Mean, {}'.format(2))
    even_frame.iloc[:, 1].plot(label='Rolling Mean, {}'.format(4))
    even_frame.iloc[:, 2].plot(
        label='Kolmogorov--Zurbenko Filter, {}'.format(2))
    even_frame.iloc[:, 3].plot(
        label='Kolmogorov--Zurbenko Filter, {}'.format(4))
    plt.title('Labor Capital Intensity: Rolling Mean Filter, Kolmogorov--Zurbenko Filter &\n\
              Single Exponential Smoothing')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_built_in(module):
    FILE_NAME = 'datasetAutocorrelation.txt'
    source_frame = pd.read_csv(FILE_NAME)
    source_frame = source_frame.iloc[:, [1, 0, 2]]
    SERIES_IDS = source_frame.iloc[:, 0].sort_values().unique()

    for i, series_id in enumerate(SERIES_IDS):
        current = fetch_world_bank('datasetAutocorrelation.txt', series_id)
        plt.figure(1 + i)
        module(current.iloc[:, 1])
        plt.grid(True)

    ARCHIVE_NAME = 'chn_tur_gdp.zip'
    source_frame = pd.read_csv(ARCHIVE_NAME)
    source_frame = source_frame.iloc[:, [1, 0, 2]]
    SERIES_IDS = source_frame.iloc[:, 0].sort_values().unique()

    for i, series_id in enumerate(SERIES_IDS):
        current = fetch_world_bank('chn_tur_gdp.zip', series_id)
        plt.figure(5 + i)
        module(current.iloc[:, 1])
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
        1
    )
    # =========================================================================
    # Scipy Signal Median Filter, Non-Linear Low-Pass Filter
    # =========================================================================
    # =========================================================================
    # k, b = np.polyfit(
    #     np.log(signal.medfilt(df.iloc[:, -2])),
    #     np.log(signal.medfilt(df.iloc[:, -1])),
    #     1
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
    #     print(np.absolute(df.iloc[:, 3].sub(df.iloc[:, 2]).div(df.iloc[:, 2])).mean())
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
        1
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
        1
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
# # #         1
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
    data_frame.iloc[:, [-1]].dropna().plot(grid=True)


def test_sub_a(data_frame):
    data_frame['delta_sm'] = data_frame.iloc[:, 0].sub(
        data_frame.iloc[:, [3, 4, 5]].sum(axis=1))
    data_frame.dropna(inplace=True)
    autocorrelation_plot(data_frame.iloc[:, [-1]])


def test_sub_b(data_frame):
    # data_frame['delta_eq'] = data_frame.iloc[:, 0].sub(data_frame.iloc[:, -1])
    data_frame['delta_eq'] = data_frame.iloc[:, 0].mul(4).div(
        data_frame.iloc[:, 0].add(data_frame.iloc[:, -1])).sub(2)
    data_frame.dropna(inplace=True)
    data_frame.iloc[:, [-1]].plot(grid=True)


def plot_can_test(control, test):
    plt.figure()
    control.plot(logy=True)
    test.plot(logy=True)
    plt.title('Discrepancy')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.show()


def plot_usa_nber(file_name, method):
    data_frame = pd.read_csv(file_name)
    if method == 'mean':
        data_frame = data_frame.groupby('year').mean()
        title = 'Mean NBER-CES'
    elif method == 'sum':
        data_frame = data_frame.groupby('year').sum()
        title = 'Sum NBER-CES'
    else:
        return
    if 'sic' in file_name:
        data_frame.drop(['sic'], axis=1, inplace=True)
    elif 'naics' in file_name:
        data_frame.drop(['naics'], axis=1, inplace=True)
    else:
        return
    plt.figure()
    for i, series_id in enumerate(data_frame.columns):
        plt.plot(data_frame.iloc[:, i], label=series_id)
        plt.title(title)
        plt.xlabel('Period')
        plt.ylabel('Dimension')
        plt.grid(True)
        plt.legend()
        plt.show()


def test_data_consistency_a():
    '''Project I: Canada Gross Domestic Product Data Comparison'''
    '''Expenditure-Based Gross Domestic Product Series Used'''
    '''Income-Based Gross Domestic Product Series Not Used'''
    '''Series A Equals Series D, However, Series D Is Preferred Over Series A As It Is Yearly: v62307282 - 380-0066 Price indexes, gross domestic product; Canada; Implicit price indexes; Gross domestic product at market prices (quarterly, 1961-03-01 to 2017-09-01)'''
    semi_frame_a = fetch_can_quarterly(3800066, 'v62307282')
    '''Series B Equals Both Series C & Series E, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306896 - 380-0084 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Seasonally adjusted at annual rates; Gross domestic product at market prices (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)'''
    semi_frame_b = fetch_can_quarterly(3800084, 'v62306896')
    '''Series C Equals Both Series B & Series E, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306938 - 380-0084 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Unadjusted; Gross domestic product at market prices (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)'''
    semi_frame_c = fetch_can_quarterly(3800084, 'v62306938')
    '''Series D Equals Series A, However, Series D Is Preferred Over Series A As It Is Yearly: v62471023 - 380-0102 Gross domestic product indexes; Canada; Implicit price indexes; Gross domestic product at market prices (annual, 1961 to 2016)'''
    semi_frame_d = fetch_can_annually(3800102, 'v62471023')
    '''Series E Equals Both Series B & Series C, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62471340 - 380-0106 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Gross domestic product at market prices (x 1,000,000) (annual, 1961 to 2016)'''
    semi_frame_e = fetch_can_annually(3800106, 'v62471340')
    semi_frame_f = fetch_can_annually(3800518, 'v96411770')
    semi_frame_g = fetch_can_annually(3800566, 'v96391932')
    semi_frame_h = fetch_can_annually(3800567, 'v96730304')
    semi_frame_i = fetch_can_annually(3800567, 'v96730338')
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e,
                              semi_frame_f, semi_frame_g, semi_frame_h, semi_frame_i], axis=1, sort=True)
    result_frame = result_frame.dropna()
    ser_a = result_frame.iloc[:, 0].div(result_frame.iloc[0, 0])
    ser_b = result_frame.iloc[:, 4].div(result_frame.iloc[0, 4])
    ser_c = result_frame.iloc[:, 5].div(result_frame.iloc[0, 5])
    ser_d = result_frame.iloc[:, 7].div(
        result_frame.iloc[:, 6]).div(result_frame.iloc[:, 5]).mul(100)
    ser_e = result_frame.iloc[:, 8].div(result_frame.iloc[0, 8])
    # =========================================================================
    # Option 1
    # =========================================================================
    plot_can_test(ser_a, ser_c)
    # =========================================================================
    # Option 2
    # =========================================================================
    plot_can_test(ser_d, ser_e)
    # =========================================================================
    # Option 3
    # =========================================================================
    plot_can_test(ser_b, ser_e)
    # =========================================================================
    # Option 4
    # =========================================================================
    plot_can_test(ser_e.div(ser_e), ser_c)


def test_data_consistency_b():
    '''Project II: USA Fixed Assets Data Comparison'''
    # =========================================================================
    # Fixed Assets Series: k1ntotl1si000, 1925--2016
    # Fixed Assets Series: kcntotl1si000, 1925--2016
    # Not Used: Fixed Assets: k3ntotl1si000, 1925--2016, Table 2.3. Historical-Cost Net Stock of Private Fixed Assets, Equipment, Structures, and Intellectual Property Products by Type
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WB_NAME = 'Section2ALL_xls.xls'
    SHS = (
        '201 Ann',
        '202 Ann',
        '203 Ann',
    )
    IDS = (
        'k1ntotl1si000',
        'kcntotl1si000',
        'k3ntotl1si000',
    )
    data_frame = pd.concat(
        [
            fetch_usa_bea(ARCHIVE_NAME, WB_NAME, sh, _id)
            for sh, _id in zip(SHS, IDS)
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
    SHS = ('T10705-A', 'T11200-A', 'T10705-A',)
    SERIES_IDS = ('A051RC', 'A052RC', 'A262RC',)
    test_procedure(generate_kwargs_list(
        ARCHIVE_NAME, WB_NAME, SHS, SERIES_IDS))
    # =========================================================================
    # Tested: `Government` = `Federal` + `State and local`
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SHS = ('T10105-A', 'T10105-A', 'T10105-A',)
    SERIES_IDS = ('A822RC', 'A823RC', 'A829RC',)
    test_procedure(generate_kwargs_list(
        ARCHIVE_NAME, WB_NAME, SHS, SERIES_IDS))
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section3all_xls.xlsx'
    SHS = ('T30100-A', 'T30200-A', 'T30300-A',)
    SERIES_IDS = ('A955RC', 'A957RC', 'A991RC',)
    test_procedure(generate_kwargs_list(
        ARCHIVE_NAME, WB_NAME, SHS, SERIES_IDS))
    # # =========================================================================
    # # Tested: `Federal` = `National defense` + `Nondefense`
    # # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SHS = ('T10105-A', 'T10105-A', 'T10105-A',)
    SERIES_IDS = ('A823RC', 'A824RC', 'A825RC',)
    test_procedure(generate_kwargs_list(
        ARCHIVE_NAME, WB_NAME, SHS, SERIES_IDS))
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section3all_xls.xlsx'
    SHS = ('T30200-A', 'T30905-A', 'T30905-A',)
    SERIES_IDS = ('A957RC', 'A997RC', 'A542RC',)
    test_procedure(generate_kwargs_list(
        ARCHIVE_NAME, WB_NAME, SHS, SERIES_IDS))
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


def test_data_consistency_e():
    '''Project V: USA NBER Data Plotting'''
    plot_usa_nber('dataset USA NBER-CES MID sic5811.csv', 'mean')
    plot_usa_nber('dataset USA NBER-CES MID sic5811.csv', 'sum')
    plot_usa_nber('dataset USA NBER-CES MID naics5811.csv', 'mean')
    plot_usa_nber('dataset USA NBER-CES MID naics5811.csv', 'sum')


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


def spline_procedure(source_frame):
    '''
    source_frame.index: Period,
    source_frame.iloc[:, 0]: Capital,
    source_frame.iloc[:, 1]: Labor,
    source_frame.iloc[:, 2]: Product
    '''
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    data_frame['lab_cap_int'] = source_frame.iloc[:, 0].div(
        source_frame.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    Y = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1])
    data_frame['lab_cap_int'] = data_frame['lab_cap_int'].sort_values()
    spl = UnivariateSpline(data_frame['lab_cap_int'], Y)

    Z = np.linspace(data_frame['lab_cap_int'].min(
    ), data_frame['lab_cap_int'].max(), source_frame.shape[0]-1)

    plt.figure()
    plt.scatter(data_frame['lab_cap_int'], Y, label='Original')
    plt.plot(Z, spl(Z))
    plt.title('Labor Capital Intensity & Labor Productivity, {}$-${}'.format(source_frame.index[0],
                                                                             source_frame.index[-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    # # print(spl.antiderivative())
    # # print(spl.derivative())
    # # print(spl.derivatives())
    # # print(spl.ext)
    # # print(spl.get_coeffs)
    # # print(spl.get_knots)
    # # print(spl.get_residual)
    # # print(spl.integral)
    # # print(spl.roots)
    # # print(spl.set_smoothing_factor)
    plt.show()


def price_inverse_single(data_series):
    '''Intent: Returns Prices Icrement Series from Cumulative Deflator Series;
    source: pandas DataFrame'''
    return data_series.div(data_series.shift(1)).sub(1)


def processing(data_frame):
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    return price_inverse_single(data_frame.dropna()).dropna()


def price_direct(data_frame, base):
    '''Intent: Returns Cumulative Price Index for Base Year;
    data_frame.iloc[:, 0]: Growth Rate;
    base: Base Year'''
    '''Cumulative Price Index'''
    data_frame['p_i'] = np.cumprod(data_frame.iloc[:, 0].add(1))
    '''Cumulative Price Index for the Base Year'''
    data_frame['cpi'] = data_frame.iloc[:, 1].div(
        data_frame.iloc[base-data_frame.index[0], 1])
    return data_frame.iloc[:, [2]]


def price_inverse(data_frame):
    '''Intent: Returns Growth Rate from Cumulative Price Index for Some Base Year;
    data_frame.iloc[:, 0]: Cumulative Price Index for Some Base Year'''
    data_frame['gri'] = data_frame.iloc[:, [-1]].div(
        data_frame.iloc[:, [-1]].shift(1)).sub(1)
    return data_frame.iloc[:, [-1]].dropna()


def price_inverse_double(data_frame):
    '''Intent: Returns Growth Rate from Nominal & Real Prices Series;
    data_frame.iloc[:, 0]: Nominal Prices;
    data_frame.iloc[:, 1]: Real Prices'''
    data_frame['cpi'] = data_frame.iloc[:, 0].div(data_frame.iloc[:, 1])
    data_frame['gri'] = data_frame.iloc[:, [-1]].div(
        data_frame.iloc[:, [-1]].shift(1)).sub(1)
    return data_frame.iloc[:, [-1]].dropna()


def price_base(source_frame):
    '''Returns Base Year'''
    i = source_frame.shape[0]-1
    while abs(source_frame.iloc[i, 0]-100) > 1/1000:
        # #    while abs(source_frame.iloc[i, 0]-source_frame.iloc[i, 1])>10:
        #    while abs(source_frame.iloc[i, 0]-source_frame.iloc[i, 1])>1:
        i -= 1
        base = i  # Basic Year
    base = source_frame.index[base]


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
    combined.dropna(inplace=True)
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
    combined.dropna(inplace=True)
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
            chunk = data.iloc[:, pair].dropna()
            chunk['def'] = chunk.iloc[:, 0].div(chunk.iloc[:, 1])
            chunk['prc'] = chunk.iloc[:, 2].div(
                chunk.iloc[:, 2].shift(1)).sub(1)
            chunk.dropna(inplace=True)
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
        chunk = data.iloc[:, [i]].dropna()
        chunk[f'{data.columns[i]}_prc'] = chunk.iloc[:, 0].div(
            chunk.iloc[:, 0].shift(1)).sub(1)
        chunk.dropna(inplace=True)
        combined = pd.concat([combined, chunk.iloc[:, [1]]],
                             axis=1,
                             sort=False)
    return combined


def plot_capital_purchases(source_frame):
    plt.figure()
    plt.semilogy(source_frame.iloc[:, 0], linewidth=3,
                 label='$s^{2;1}_{Cobb-Douglas}$')
    plt.semilogy(source_frame.iloc[:, 24], label='Total')
    plt.semilogy(source_frame.iloc[:, 25], label='Structures')
    plt.semilogy(source_frame.iloc[:, 26], label='Equipment')
    plt.title('Fixed Assets Purchases')
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.legend()
    plt.grid(True)
    plt.show()


def procedure_numbers(data_frame):
    '''
    data_frame.index: Period,
    data_frame.iloc[:, 0]: Capital,
    data_frame.iloc[:, 1]: Labor,
    data_frame.iloc[:, 2]: Product
    '''
    data_frame.reset_index(level=0, inplace=True)
    T = data_frame.iloc[:, 0]
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    data_frame['lab_cap_int'] = data_frame.iloc[:, 1].div(
        data_frame.iloc[:, 2])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    data_frame['lab_product'] = data_frame.iloc[:, 3].div(
        data_frame.iloc[:, 2])
    YP_1P_0 = np.array([1.0, 1.0])

    def func(T, A_1, A_0):
        return A_1*T**A_0

    numbers, matrix = optimization.curve_fit(
        func, data_frame['lab_cap_int'], data_frame['lab_product'], YP_1P_0)
    print('Factor: {:,.4f}; Index: {:,.4f}'.format(numbers[0], numbers[1]))


def plot_lab_prod_polynomial(source_frame):
    '''Static Labor Productivity Approximation
    source_frame.index: Period,
    source_frame.iloc[:, 0]: Capital,
    source_frame.iloc[:, 1]: Labor,
    source_frame.iloc[:, 2]: Product
    '''
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    data_frame['lab_cap_int'] = source_frame.iloc[:, 0].div(
        source_frame.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    data_frame['lab_product'] = source_frame.iloc[:, 2].div(
        source_frame.iloc[:, 1])
    # =========================================================================
    # Power Function: Labor Productivity
    # =========================================================================
    yp_1p = np.polyfit(np.log(data_frame['lab_cap_int']), np.log(
        data_frame['lab_product']), 1)
    # =========================================================================
    # Polynomials 1, 2, 3 & 4: Labor Productivity
    # =========================================================================
    yl_1p = np.polyfit(data_frame['lab_cap_int'], data_frame['lab_product'], 1)
    yl_2p = np.polyfit(data_frame['lab_cap_int'], data_frame['lab_product'], 2)
    yl_3p = np.polyfit(data_frame['lab_cap_int'], data_frame['lab_product'], 3)
    yl_4p = np.polyfit(data_frame['lab_cap_int'], data_frame['lab_product'], 4)
    PP = sp.exp(yp_1p[1])*data_frame['lab_cap_int']**yp_1p[0]
    y_a_a = yl_1p[1] + yl_1p[0]*data_frame['lab_cap_int']
    y_b_b = yl_2p[2] + yl_2p[1]*data_frame['lab_cap_int'] + \
        yl_2p[0]*data_frame['lab_cap_int']**2
    y_c_c = yl_3p[3] + yl_3p[2]*data_frame['lab_cap_int'] + yl_3p[1] * \
        data_frame['lab_cap_int']**2 + yl_3p[0]*data_frame['lab_cap_int']**3
    y_d_d = yl_4p[4] + yl_4p[3]*data_frame['lab_cap_int'] + yl_4p[2] * \
        data_frame['lab_cap_int']**2 + yl_4p[1] * \
        data_frame['lab_cap_int']**3 + yl_4p[0]*data_frame['lab_cap_int']**4
    # =========================================================================
    # Deltas
    # =========================================================================
    d_p_p = sp.absolute((sp.exp(yp_1p[1])*data_frame['lab_cap_int'] **
                        yp_1p[0]-data_frame['lab_product']).div(data_frame['lab_product']))
    d_y_a_a = sp.absolute(
        (YAA-data_frame['lab_product']).div(data_frame['lab_product']))
    d_y_b_b = sp.absolute(
        (YBB-data_frame['lab_product']).div(data_frame['lab_product']))
    d_y_c_c = sp.absolute(
        (YCC-data_frame['lab_product']).div(data_frame['lab_product']))
    d_y_d_d = sp.absolute(
        (YDD-data_frame['lab_product']).div(data_frame['lab_product']))

    r_20 = r2_score(y, pp)
    r_21 = r2_score(y, yaa)
    r_22 = r2_score(y, ybb)
    r_23 = r2_score(y, ycc)
    r_24 = r2_score(y, ydd)
    plt.figure(1)
    plt.scatter(data_frame['lab_product'], label='Labor Productivity')
    plt.plot(PP, label='$\\hat Y = {:.2f}X^{{{:.2f}}}, R^2 = {:.4f}$'.format(
        sp.exp(yp_1p[1]), yp_1p[0], r_20))
    plt.plot(
        YAA, label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X, R^2 = {:.4f}$'.format(1, yl_1p[1], yl_1p[0], r_21))
    plt.plot(YBB, label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2, R^2 = {:.4f}$'.format(
        2, yl_2p[2], yl_2p[1], yl_2p[0], r_22))
    plt.plot(YCC, label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2+{:.2f}X^3, R^2 = {:.4f}$'.format(
        3, yl_3p[3], yl_3p[2], yl_3p[1], yl_3p[0], r_23))
    plt.plot(YDD, label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2+{:.2f}X^3 {:.2f}X^4, R^2 = {:.4f}$'.format(
        4, yl_4p[4], yl_4p[3], yl_4p[2], yl_4p[1], yl_4p[0], r_24))
    plt.title('Labor Capital Intensity & Labor Productivity, {}$-${}'.format(
        source_frame.index[0], source_frame.index[-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(
        DPP, ':', label='$\\|\\frac{{\\hat Y-Y}}{{Y}}\\|, \\bar S = {:.4%}$'.format(DPP.mean()))
    plt.plot(
        DYAA, ':', label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4%}$'.format(1, DYAA.mean()))
    plt.plot(
        DYBB, ':', label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4%}$'.format(2, DYBB.mean()))
    plt.plot(
        DYCC, ':', label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4%}$'.format(3, DYCC.mean()))
    plt.plot(
        DYDD, ':', label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4%}$'.format(4, DYDD.mean()))
    plt.title('Deltas of Labor Capital Intensity & Labor Productivity, {}$-${}'.format(
        source_frame.index[0], source_frame.index[-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_simple_linear(source_frame, coef_1, coef_2, E):
    '''
    Labor Productivity on Labor Capital Intensity Plot;
    Predicted Labor Productivity Plot
    '''
    plt.figure(1)
    plt.plot(source_frame.iloc[:, 0],
             source_frame.iloc[:, 1], label='Original')
    plt.title('$Labor\ Capital\ Intensity$, $Labor\ Productivity$ Relation, {}$-${}'.format(
        source_frame.index[0], source_frame.index[-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(
        E, label='$\\frac{Y}{Y_{0}} = %f\\frac{L}{L_{0}}+%f\\frac{K}{K_{0}}$' % (coef_1, coef_2))
    plt.title('Model: $\\hat Y = {:.4f}+{:.4f}\\times X$, {}$-${}'.format(
        coef_1, coef_2, source_frame.index[0], source_frame.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('$\\hat Y = Labor\ Productivity$, $X = Labor\ Capital\ Intensity$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_simple_log(source_frame, coef_1, coef_2, e):
    '''
    Log Labor Productivity on Log Labor Capital Intensity Plot;
    Predicted Log Labor Productivity Plot
    '''
    plt.figure(1)
    plt.plot(source_frame.iloc[:, 0],
             source_frame.iloc[:, 1], label='Logarithm')
    plt.title('$\\ln(Labor\ Capital\ Intensity), \\ln(Labor\ Productivity)$ Relation, {}$-${}'.format(
        source_frame.index[0], source_frame.index[-1]))
    plt.xlabel('$\\ln(Labor\ Capital\ Intensity)$')
    plt.ylabel('$\\ln(Labor\ Productivity)$')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(
        e, label='$\\ln(\\frac{Y}{Y_{0}}) = %f+%f\\ln(\\frac{K}{K_{0}})+%f\\ln(\\frac{L}{L_{0}})$' % (coef_1, coef_2, 1-coef_2))
    plt.title('Model: $\\ln(\\hat Y) = {:.4f}+{:.4f}\\times \\ln(X)$, {}$-${}'.format(
        coef_1, coef_2, source_frame.index[0], source_frame.index[-1]))
    plt.xlabel('Period')
    plt.ylabel(
        '$\\hat Y = \\ln(Labor\ Productivity)$, $X = \\ln(Labor\ Capital\ Intensity)$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_turnover(source_frame):
    '''Static Fixed Assets Turnover Approximation
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Capital,
    source_frame.iloc[:, 2]: Product
    '''
    # =========================================================================
    # Fixed Assets Turnover
    # =========================================================================
    K = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1])
    # =========================================================================
    # Linear: Fixed Assets Turnover
    # =========================================================================
    kl_1p = np.polyfit(source_frame.iloc[:, 0], K, 1)
    # =========================================================================
    # Exponential: Fixed Assets Turnover
    # =========================================================================
    ke_1p = np.polyfit(source_frame.iloc[:, 0], np.log(K), 1)
    K_1 = kl_1p[1] + kl_1p[0]*source_frame.iloc[:, 0]
    K_2 = sp.exp(ke_1p[1] + ke_1p[0]*source_frame.iloc[:, 0])
    # =========================================================================
    # Deltas
    # =========================================================================
    DK_1 = sp.absolute((K_1-K).div(K))
    DK_2 = sp.absolute((K_2-K).div(K))

    r_21 = r2_score(K, K_1)
    r_22 = r2_score(K, K_2)
    plt.figure(1)
    plt.plot(source_frame.iloc[:, 2].div(
        source_frame.iloc[:, 1]), source_frame.iloc[:, 1])
    plt.title('Fixed Assets Volume to Fixed Assets Turnover, {}$-${}'.format(
        source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Fixed Assets Turnover')
    plt.ylabel('Fixed Assets Volume')
    plt.grid(True)
    plt.figure(2)
    plt.scatter(source_frame.iloc[:, 0], K, label='Fixed Assets Turnover')
    plt.plot(source_frame.iloc[:, 0], K_1, label='$\\hat K_{{l}} = {:.2f} {:.2f} t, R^2 = {:.4f}$'.format(
        kl_1p[1], kl_1p[0], r_21))
    plt.plot(source_frame.iloc[:, 0], K_2, label='$\\hat K_{{e}} = \\exp ({:.2f} {:.2f} t), R^2 = {:.4f}$'.format(
        ke_1p[1], ke_1p[0], r_22))
    plt.title('Fixed Assets Turnover Approximation, {}$-${}'.format(source_frame.iloc[0, 0],
                                                                    source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.plot(source_frame.iloc[:, 0], DK_1, ':',
             label='$\\|\\frac{{\\hat K_{{l}}-K}}{{K}}\\|, \\bar S = {:.4%}$'.format(DK_1.mean()))
    plt.plot(source_frame.iloc[:, 0], DK_2, ':',
             label='$\\|\\frac{{\\hat K_{{e}}-K}}{{K}}\\|, \\bar S = {:.4%}$'.format(DK_2.mean()))
    plt.title('Deltas of Fixed Assets Turnover Approximation, {}$-${}'.format(source_frame.iloc[0, 0],
                                                                              source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.show()


def simple_linear_regression(source_frame):
    '''Determining of Coefficients of Regression
    source_frame.index: Period,
    source_frame.iloc[:, 0]: Regressor,
    source_frame.iloc[:, 1]: Regressand
    '''
    '''Summarize'''
    s_1 = sum(source_frame.iloc[:, 0])
    s_2 = sum(source_frame.iloc[:, 1])
    s_3 = sum((source_frame.iloc[:, 0])**2)
    s_4 = sum(source_frame.iloc[:, 0]*source_frame.iloc[:, 1])
    '''Approximation'''
    a_0 = (s_2*s_3-s_1*s_4)/(source_frame.shape[0]*s_3-s_1**2)
    a_1 = (source_frame.shape[0]*s_4-s_1*s_2) / \
        (source_frame.shape[0]*s_3-s_1**2)
    e = a_0 + a_1*(source_frame.iloc[:, 0])
    my = sp.mean(source_frame.iloc[:, 1])
    ess = sum((source_frame.iloc[:, 1]-a_0-a_1*source_frame.iloc[:, 0])**2)
    TSS = sum((source_frame.iloc[:, 1]-MY)**2)
    R_2 = 1-ESS/TSS
    '''Delivery Block'''
    print('Period From {} Through {}'.format(
        source_frame.index[0], source_frame.index[-1]))
    print('Model: Yhat = {:,.4f}+{:,.4f}*X'.format(A_0, A_1))
    print('Model Parameter: A_0 = {:,.4f}'.format(A_0))
    print('Model Parameter: A_1 = {:,.4f}'.format(A_1))
    print(
        'Model Result: ESS = {:,.4f}; TSS = {:,.4f}; R**2 = {:,.4f}'.format(ESS, TSS, R_2))
    return A_0, A_1, E


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
    """Data Fetch"""
    ARCHIVE_NAME = 'dataset_rus_m1.zip'
    source_frame = pd.read_csv(ARCHIVE_NAME)
    """Plotting"""
    plt.figure()
    plt.plot(source_frame.iloc[:, 1], source_frame.iloc[:, 2])
    plt.xlabel('Percentage')
    plt.ylabel('RUB, Millions')
    plt.title('M1 Dependency on Prime Rate')
    plt.grid(True)
    plt.show()


def plot_grigoriev():
    FILE_NAME = 'dataset_rus_Grigoriev-V.csv'
    data_frame = pd.read_csv(FILE_NAME)
    for series_id in sorted(set(data_frame.iloc[:, 2])):
        chunk = data_frame[data_frame.iloc[:, 2] == series_id].iloc[:, [3, 4]]
        chunk.columns = [chunk.columns[0], series_id]
        chunk.set_index(chunk.columns[0],
                        inplace=True,
                        verify_integrity=True)
        chunk.sort_index(inplace=True)
        chunk.plot(grid=True)


def zip_pack(archive, members):
    with zipfile.ZipFile('{}.zip'.format(archive), 'w') as z:
        for file in members:
            z.write('{}'.format(file), compress_type=zipfile.ZIP_DEFLATED)
            os.unlink(file)


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
    plt.grid()
    plt.legend()
    plt.show()


def plot_census_b(capital_frame, deflator_frame):
    """Census Manufacturing Fixed Assets Series"""
    plt.figure(1)
    plt.semilogy(capital_frame.iloc[:, 0], label='Total')
    plt.semilogy(capital_frame.iloc[:, 1], label='Structures')
    plt.semilogy(capital_frame.iloc[:, 2], label='Equipment')
    plt.title('Manufacturing Fixed Assets, {}$-${}'.format(capital_frame.index[0],
                                                           capital_frame.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.plot(deflator_frame)
    plt.title('Census Fused Capital Deflator, {}$-${}'.format(deflator_frame.index[0],
                                                              deflator_frame.index[-1]))
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
    plt.title('Total Immigration, {}$-${}'.format(source_frame.index[0],
                                                  source_frame.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('People')
    plt.grid()
    plt.show()


def plot_census_f_a(source_frame):
    plt.figure(1)
    source_frame.iloc[:, 1].plot()
    plt.title('Unemployment, Percent of Civilian Labor Force')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.figure(2)
    plt.plot(source_frame.iloc[:, 2], label='Bureau of Labour')
    plt.plot(source_frame.iloc[:, 3], label='Wolman')
    plt.title('All Manufacturing, Average Full-Time Weekly Hours, 1890-1899=100')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.figure(3)
    source_frame.iloc[:, 6].plot()
    plt.title('Implicit Number of Workers')
    plt.xlabel('Period')
    plt.ylabel('Persons')
    plt.grid()
    plt.show()


def plot_census_f_b(source_frame):
    fig, axs_a = plt.subplots()
    color = 'tab:red'
    axs_a.set_xlabel('Period')
    axs_a.set_ylabel('Number', color=color)
    axs_a.plot(source_frame.iloc[:, 4], color=color, label='Stoppages')
    axs_a.set_title('Work Conflicts')
    axs_a.grid()
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
    plt.grid()
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
    plt.grid()
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
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.plot(source_frame_b.iloc[:, 0], label='Exports, U187')
    plt.plot(source_frame_b.iloc[:, 1], label='Imports, U188')
    plt.plot(source_frame_b.iloc[:, 2], label='Net Exports, U189')
    plt.title('Total Merchandise, Gold and Silver, {}$-${}'.format(
        source_frame_b.index[0], source_frame_b.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
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
    plt.grid()
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
    plt.grid()
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
    plt.grid()
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
    for i, series_id in enumerate(SERIES_IDS):
        title = fetch_usa_census_description(ARCHIVE_NAME, series_id)
        data_frame = fetch_usa_census(ARCHIVE_NAME, series_id)
        data_frame = data_frame.div(data_frame.iloc[0, :]).mul(100)
        plt.figure(1+i)
        plt.plot(data_frame, label=f'{series_id}')
        plt.title('{}, {}$-${}'.format(title,
                  data_frame.index[0], data_frame.index[-1]))
        plt.xlabel('Period')
        plt.ylabel('Percentage')
        plt.grid(True)
        plt.legend()
        plt.show()


def plot_growth_elasticity(source_frame):
    '''Growth Elasticity Plotting
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Series
    '''
    result_list = []  # Create List Results
    for i in range(source_frame.shape[0]-3):
        '''
        `period`: Period, Centered
        `value_a`: Value, Centered
        `value_b`: Value, Growth Rate
        `value_c`: Value, Elasticity
        '''
        result_list.append({'period': (source_frame.iloc[1 + i, 0] + source_frame.iloc[2 + i, 0])/2,
                            'value_a': (source_frame.iloc[1 + i, 1] + source_frame.iloc[2 + i, 1])/2,
                            'value_b': (source_frame.iloc[2 + i, 1]-source_frame.iloc[i, 1])/(source_frame.iloc[i, 1] + source_frame.iloc[1 + i, 1]),
                            'value_c': (source_frame.iloc[2 + i, 1] + source_frame.iloc[3 + i, 1]-source_frame.iloc[i, 1]-source_frame.iloc[1 + i, 1])/(source_frame.iloc[i, 1] + source_frame.iloc[1 + i, 1] + source_frame.iloc[2 + i, 1] + source_frame.iloc[3 + i, 1])})
    result_frame = pd.DataFrame(result_list)  # Convert List to Dataframe

    result_frame = result_frame.set_index('Period')
    plt.figure()
    result_frame.iloc[:, 1].plot(label='Growth Rate')
    result_frame.iloc[:, 2].plot(label='Elasticity Rate')
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
    if label == None:
        plt.legend()
    else:
        plt.legend(label)


def SES(source_frame, window=5, alpha=0.5):
    '''Single Exponential Smoothing
    Robert Goodell Brown, 1956
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Series
    '''
    S = source_frame.iloc[:window, 1]
    S = S.mean()  # Average of Window-First Entries
    ses = []
    ses.append(alpha*source_frame.iloc[0, 1] + (1-alpha)*S)
    for i in range(1, source_frame.shape[0]):
        ses.append(alpha*source_frame.iloc[i, 1] + (1-alpha)*ses[i-1])
    cap = 'ses{:02d}_{:, .6f}'.format(window, alpha)
    ses = pd.DataFrame(ses, columns=[cap])
    result_frame = pd.concat([source_frame, ses], axis=1, sort=True)
    result_frame = result_frame.set_index('Period')
    return result_frame


def results_delivery_a(intervals, coefficients):
    '''Results Delivery Module
    intervals (1 + N): 1 + Number of Intervals
    coefficients: A-Coefficients'''
    for i in range(1 + intervals):
        print('Model Parameter: A{:02d} = {:.6f}'.format(i, coefficients[i]))


def results_delivery_k(intervals, coefficients):
    '''Results Delivery Module
    intervals: Number of Intervals
    coefficients: K-Coefficients'''
    for i in range(intervals):
        print('Model Parameter: K{:02d} = {:.6f}'.format(
            1 + i, coefficients[i]))


def plot_capital_modelling(source_frame, base):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Investment,
    source_frame.iloc[:, 2]: Production,
    source_frame.iloc[:, 3]: Capital,
    source_frame.iloc[:, 4]: Capital Retirement
    '''
    QS = np.polyfit(source_frame.iloc[:, 0], source_frame.iloc[:, 1].div(
        source_frame.iloc[:, 2]), 1)
    QL = np.polyfit(source_frame.iloc[:, 0], source_frame.iloc[:, 2].div(
        source_frame.iloc[:, 3]), 1)
    '''Gross Fixed Investment to Gross Domestic Product Ratio'''
    S = QS[1] + QS[0]*source_frame.iloc[:, 0]
    '''Fixed Assets Turnover'''
    L = QL[1] + QL[0]*source_frame.iloc[:, 0]
    KA = calculate_capital(source_frame, QS[1], QS[0], QL[1], QL[0], 0.875)
    KB = calculate_capital(source_frame, QS[1], QS[0], QL[1], QL[0], 1)
    KC = calculate_capital(source_frame, QS[1], QS[0], QL[1], QL[0], 1.125)
    plt.figure(1)
    plt.title('Fixed Assets Turnover ($\\lambda$) for the US, {}$-${}'.format(
        source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 2].div(
        source_frame.iloc[:, 3]), label='$\\lambda$')
    if QL[0] < 0:
        plt.plot(source_frame.iloc[:, 0], L, label='$\\lambda = {1:, .4f}\\ {0:, .4f}\\times t$'.format(
            QL[0], QL[1]))
    else:
        plt.plot(source_frame.iloc[:, 0], L,
                 label='$\\lambda = {1:, .4f} + {0:, .4f} \\times t$'.format(QL[0], QL[1]))
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Gross Fixed Investment as Percentage of GDP ($S$) for the US, {}$-${}'.format(
        source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 1].div(
        source_frame.iloc[:, 2]), label='$S$')
    if QS[0] < 0:
        plt.plot(source_frame.iloc[:, 0], S, label='$S = {1:, .4f}\\ {0:, .4f}\\times t$'.format(
            QS[0], QS[1]))
    else:
        plt.plot(source_frame.iloc[:, 0], S,
                 label='$S = {1:, .4f} + {0:, .4f} \\times t$'.format(QS[0], QS[1]))
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.title('$\\alpha$ for the US, {}$-${}'.format(
        source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-2, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(source_frame.iloc[:, 0],
             source_frame.iloc[:, 4], label='$\\alpha$')
    plt.grid(True)
    plt.legend()
    plt.figure(4)
    plt.title('$K$ for the US, {}$-${}'.format(
        source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-2, 0]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars, {}=100'.format(
        source_frame.iloc[base, 0]))
    plt.semilogy(source_frame.iloc[:, 0], KA,
                 label='$K\\left(\\pi = \\frac{7}{8}\\right)$')
    plt.semilogy(source_frame.iloc[:, 0], KB,
                 label='$K\\left(\\pi = 1\\right)$')
    plt.semilogy(source_frame.iloc[:, 0], KC,
                 label='$K\\left(\\pi = \\frac{9}{8}\\right)$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_fourier_discrete(source_frame, precision=10):
    '''
    source_frame.iloc[:, 0]: Period;
    source_frame.iloc[:, 1]: Series
    Discrete Fourier Transform based on Simpson's Rule
    '''
    f_1p = np.polyfit(source_frame.iloc[:, 0], source_frame.iloc[:, 1], 1)
    LX = f_1p[1] + f_1p[0]*source_frame.iloc[:, 0]
    Q = []  # Blank List for Fourier Coefficients
    for i in range(1 + precision):
        c = 2*(source_frame.iloc[:, 1]-LX)*sp.cos(2*sp.pi*i*(
            source_frame.iloc[:, 0].sub(source_frame.iloc[0, 0])).div(source_frame.shape[0]))
        s = 2*(source_frame.iloc[:, 1]-LX)*sp.sin(2*sp.pi*i*(
            source_frame.iloc[:, 0].sub(source_frame.iloc[0, 0])).div(source_frame.shape[0]))
        Q.append({'cos': c.mean(), 'sin': s.mean()})

    Q = pd.DataFrame(Q)  # Convert List to Dataframe
    Q['cos'][0] = Q['cos'][0]/2
    EX = pd.DataFrame(1, index=range(
        1 + source_frame.shape[0]), columns=['EX'])
    EX = Q['cos'][0]
    plt.figure()
    plt.title('$\\alpha$ for the US, {}$-${}'.format(
        source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(source_frame.iloc[:, 0],
                source_frame.iloc[:, 1], label='$\\alpha$')
    for i in range(1, 1 + precision):
        EX = EX + Q['cos'][i]*sp.cos(2*sp.pi*i*(source_frame.iloc[:, 0].sub(source_frame.iloc[0, 0])).div(source_frame.shape[0])) + \
            Q['sin'][i]*sp.sin(2*sp.pi*i*(source_frame.iloc[:, 0] -
                               source_frame.iloc[0, 0]).div(source_frame.shape[0]))
        plt.plot(source_frame.iloc[:, 0], LX + EX,
                 label='$FT_{{{:02}}}(\\alpha)$'.format(i))
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_elasticity(source):
    '''
    source.iloc[:, 0]: Period,
    source.iloc[:, 1]: Real Values for Price Deflator,
    source.iloc[:, 2]: Nominal Values for Price Deflator,
    source.iloc[:, 3]: Focused Series
    '''
    if source.columns[3] == 'A032RC1':
        desc = 'National Income'
    else:
        desc = 'Series'
    i = source.shape[0]-1
    while abs(source.iloc[i, 2]-source.iloc[i, 1]) > 1:
        i -= 1
        base = i
    source['ser'] = source.iloc[:, 1]*source.iloc[:, 3].div(source.iloc[:, 2])
    # source['sma'] = (source.iloc[:, 4] + source.iloc[:, 4].shift(1))/2
    source['sma'] = source.iloc[:, 4].rolling(window=2).mean()
    source['ela'] = 2*(source.iloc[:, 4]-source.iloc[:, 4].shift(1)
                       ).div(source.iloc[:, 4] + source.iloc[:, 4].shift(1))
    source['elb'] = (source.iloc[:, 4].shift(-1) -
                     source.iloc[:, 4].shift(1)).div(2*source.iloc[:, 4])
    source['elc'] = 2*(source.iloc[:, 4].shift(-1)-source.iloc[:, 4].shift(1)).div(
        source.iloc[:, 4].shift(1) + 2*source.iloc[:, 4] + source.iloc[:, 4].shift(-1))
    source['eld'] = (-source.iloc[:, 4].shift(1)-source.iloc[:, 4] + source.iloc[:, 4].shift(-1) +
                     source.iloc[:, 4].shift(-2)).div(2*source.iloc[:, 4] + 2*source.iloc[:, 4].shift(-1))
    result_frame = source.iloc[:, [0, 4, 5, 6, 7, 8, 9]]
    plt.figure(1)
    plt.title('{}, {}, {}=100'.format(
        desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars, {}=100'.format(
        result_frame.iloc[base, 0]))
    plt.plot(result_frame.iloc[:, 0], result_frame.iloc[:,
             1], label='{}'.format(source.columns[3]))
    plt.plot(result_frame.iloc[:, 0].rolling(window=2).mean(
    ), result_frame.iloc[:, 2], label='A032RC1, Rolling Mean, Window = 2')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Elasticity: {}, {}, {}=100'.format(
        desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(result_frame.iloc[:, 0].rolling(window=2).mean(
    ), result_frame.iloc[:, 3], label='$\\overline{E}_{T+\\frac{1}{2}}$')
    plt.plot(result_frame.iloc[:, 0],
             result_frame.iloc[:, 4], label='$E_{T+1}$')
    plt.plot(result_frame.iloc[:, 0], result_frame.iloc[:,
             5], label='$\\overline{E}_{T+1}$')
    plt.plot(result_frame.iloc[:, 0].rolling(window=2).mean(
    ), result_frame.iloc[:, 6], label='$\\overline{\\epsilon(E_{T+\\frac{1}{2}})}$')
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.title('Elasticity: {}, {}, {}=100'.format(
        desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.xlabel('{}, {}, {}=100'.format(
        desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.ylabel('Elasticity: {}, {}, {}=100'.format(
        desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:,
             6], label='$\\frac{\\epsilon(X)}{X}$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_kzf(source_frame):
    '''Kolmogorov--Zurbenko Filter
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Series'''

    '''DataFrame for Kolmogorov--Zurbenko Filter Results'''
    result_frame_a = source_frame
    '''DataFrame for Kolmogorov--Zurbenko Filter Residuals'''
    result_frame_b = pd.concat([source_frame.iloc[:, 0], source_frame.iloc[:, 0].rolling(
        window=2).mean()], axis=1, sort=False)
    result_frame_b = pd.concat([result_frame_b, (source_frame.iloc[:, 1]-source_frame.iloc[:,
                               1].shift(1)).div(source_frame.iloc[:, 1].shift(1))], axis=1, sort=False)
    for k in range(1, 1 + source_frame.shape[0]//2):
        cap = 'col{:02d}'.format(k)
        result_frame_a[cap] = sp.nan
        for j in range(1, 1 + source_frame.shape[0]-k):
            vkz = 0
            for i in range(1 + k):
                vkz += result_frame_a.iloc[i + j-1,
                                           1]*scipy.special.binom(k, i)/(2**k)
            result_frame_a.iloc[i + j-(k//2)-1, 1 + k] = vkz
        if k % 2 == 0:
            result_frame_b = pd.concat([result_frame_b, (source_frame.iloc[:, 1 + k]-source_frame.iloc[:, 1 + k].shift(
                1)).div(source_frame.iloc[:, 1 + k].shift(1))], axis=1, sort=False)
        else:
            result_frame_b = pd.concat([result_frame_b, (source_frame.iloc[:, 1 + k].shift(-1) -
                                       source_frame.iloc[:, 1 + k]).div(source_frame.iloc[:, 1 + k])], axis=1, sort=False)
    plt.figure(1)
    plt.title('Kolmogorov$-$Zurbenko Filter')
    plt.xlabel('Period')
    plt.ylabel('Measure')
    plt.scatter(
        result_frame_a.iloc[:, 0], result_frame_a.iloc[:, 1], label='Original Series')
    for i in range(2, 1 + source_frame.shape[0]//2):
        if i % 2 == 0:
            plt.plot(result_frame_a.iloc[:, 0].rolling(window=2).mean(
            ), result_frame_a.iloc[:, i], label='$KZF(\\lambda = {})$'.format(i-1))
        else:
            plt.plot(result_frame_a.iloc[:, 0], result_frame_a.iloc[:,
                     i], label='$KZF(\\lambda = {})$'.format(i-1))
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Kolmogorov$-$Zurbenko Filter Residuals')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(result_frame_b.iloc[:, 1],
                result_frame_b.iloc[:, 2], label='Residuals')
    for i in range(3, 2 + source_frame.shape[0]//2):
        if i % 2 == 0:
            plt.plot(result_frame_b.iloc[:, 1], result_frame_b.iloc[:, i],
                     label='$\\delta KZF(\\lambda = {})$'.format(i-1))
        else:
            plt.plot(result_frame_b.iloc[:, 0], result_frame_b.iloc[:, i],
                     label='$\\delta KZF(\\lambda = {})$'.format(i-1))
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_pearson_r_test(source_frame):
    '''Left-Side & Right-Side Rolling Means' Calculation & Plotting
    source_frame.index: Period,
    source_frame.iloc[:, 0]: Series'''

    result_frame = pd.DataFrame(columns=['window'])
    for i in range(1 + source_frame.shape[0]//2):
        # =====================================================================
        # Shift Mean Values to Left
        # =====================================================================
        l_frame = source_frame.iloc[:, 0].rolling(
            window=1 + i).mean().shift(-i)
        # =====================================================================
        # Shift Mean Values to Right
        # =====================================================================
        r_frame = source_frame.iloc[:, 0].rolling(window=1 + i).mean()
        numerator = stats.pearsonr(
            source_frame.iloc[:, 0][R_frame.notna()], R_frame.dropna())[0]
        denominator = stats.pearsonr(
            source_frame.iloc[:, 0][L_frame.notna()], L_frame.dropna())[0]
        result_frame = result_frame.append(
            {'window': numerator/denominator}, ignore_index=True)
    '''Plot 'Window' to 'Right-Side to Left-Side Pearson R'''
    plt.figure()
    plt.title('Right-Side to Left-Side Pearson R Ratio')
    plt.xlabel('`Window`')
    plt.ylabel('Index')
    plt.plot(result_frame, label='Right-Side to Left-Side Pearson R Ratio')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_rmf(source_frame):
    '''
    source_frame.iloc[:, 0]: Period;
    source_frame.iloc[:, 1]: Series
    Rolling Mean Filter'''
    plt.figure(1)
    plt.title('Moving Average {}$-${}'.format(
        source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    source_frame['sma'] = source_frame.iloc[:, 1].rolling(
        window=1, center=True).mean()
    plt.scatter(source_frame.iloc[:, 0], source_frame.iloc[:, 2], label='$Y$')
    '''Smoothed Series Calculation'''
    for i in range(1, source_frame.shape[0]//2):
        source_frame.iloc[:, 2] = source_frame.iloc[:, 1].rolling(
            window=1 + i, center=True).mean()
        if i % 2 == 0:
            plt.plot(0.5 + source_frame.iloc[:, 0], source_frame.iloc[:,
                     2], label='$\\bar Y_{{m = {}}}$'.format(i))
        else:
            plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:,
                     2], label='$\\bar Y_{{m = {}}}$'.format(i))
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Moving Average Deviations {}$-${}'.format(
        source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Deviations ($\\delta$), Percent')
    source_frame['del'] = (source_frame.iloc[:, 1].rolling(window=1, center=True).mean().shift(-1)-source_frame.iloc[:,
                           1].rolling(window=1, center=True).mean()).div(source_frame.iloc[:, 1].rolling(window=1, center=True).mean())
    plt.scatter(source_frame.iloc[:, 0],
                source_frame.iloc[:, 3], label='$\\delta(Y)$')
    '''Deviations Calculation'''
    for i in range(1, source_frame.shape[0]//2):
        source_frame.iloc[:, 3] = (source_frame.iloc[:, 1].rolling(window=1 + i, center=True).mean().shift(-1)-source_frame.iloc[:, 1].rolling(
            window=1 + i, center=True).mean()).div(source_frame.iloc[:, 1].rolling(window=1 + i, center=True).mean())
        if i % 2 == 0:
            plt.plot(0.5 + source_frame.iloc[:, 0], source_frame.iloc[:,
                     3], label='$\\delta(\\bar Y_{{m = {}}})$'.format(i))
        else:
            plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 3],
                     label='$\\delta(\\bar Y_{{m = {}}})$'.format(i))
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_ses(source_frame, window, step):
    '''Single Exponential Smoothing
    Robert Goodell Brown, 1956
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Series'''
    '''Average of Window-First Entries'''
    S = source_frame.iloc[:window, 1].mean()
    '''DataFrame for Exponentially Smoothed Series'''
    smooth_frame = pd.DataFrame(source_frame.iloc[:, 0])
    '''DataFrame for Deltas of Exponentially Smoothed Series'''
    deltas_frame = pd.DataFrame(
        0.5 + source_frame.iloc[:(source_frame.shape[0]-1), 0])
    delta = (source_frame.iloc[:, 1].shift(-1) -
             source_frame.iloc[:, 1]).div(source_frame.iloc[:, 1].shift(-1))
    delta = delta[:(len(delta)-1)]
    deltas_frame = pd.concat([deltas_frame, delta], axis=1, sort=False)
    plt.figure()
    plt.title('Deltas of Exponentially Smoothed Series')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(source_frame.iloc[:, 0],
                source_frame.iloc[:, 1], label='Original Series')
    k = 0
    while True:
        k += 1
        alpha = 0.25 + step*(k-1)
        ses, dse = [], []
        ses.append(alpha*source_frame.iloc[0, 1] + (1-alpha)*S)
        for i in range(1, source_frame.shape[0]):
            ses.append(alpha*source_frame.iloc[i, 1] + (1-alpha)*ses[i-1])
            dse.append((ses[i]-ses[i-1])/ses[i-1])
            cap = 'col{:02d}'.format(k)
        ses = pd.DataFrame(ses, columns=[cap])
        dse = pd.DataFrame(dse, columns=[cap])
        smooth_frame = pd.concat([smooth_frame, ses], axis=1, sort=False)
        deltas_frame = pd.concat([deltas_frame, dse], axis=1, sort=False)
        plt.plot(source_frame.iloc[:, 0], ses, label='Smoothing: $w = {}, \\alpha={:, .2f}$'.format(
            window, alpha))

        if k >= 0.5 + 0.75/step:  # 0.25 + step*(k-0.5) >= 1
            break
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_e(source_frame):
    '''
    source_frame.iloc[:, 0]: Investment,
    source_frame.iloc[:, 1]: Production,
    source_frame.iloc[:, 2]: Capital
    '''
    '''Investment to Production Ratio'''
    source_frame['S'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])
    '''Fixed Assets Turnover Ratio'''
    source_frame['L'] = source_frame.iloc[:, 1].div(source_frame.iloc[:, 2])
    QS = np.polyfit(source_frame.iloc[:, 0], source_frame.iloc[:, 1], 1)
    QL = np.polyfit(source_frame.iloc[:, 1], source_frame.iloc[:, 2], 1)
    source_frame['RS'] = QS[1] + QS[0]*source_frame.iloc[:, 0]
    source_frame['RL'] = QL[1] + QL[0]*source_frame.iloc[:, 2]
    plt.figure()
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 1])
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 5])
    plt.title('Investment to Production Ratio, {}$-${}'.format(
        source_frame.index[0], source_frame.index[-1]))
    plt.xlabel('Investment, Billions of Dollars')
    plt.ylabel('Gross Domestic Product, Billions of Dollars')
    plt.grid(True)
    plt.legend(['$P(I)$', '$\\hat P(I) = %.4f+%.4f I$' % (QS[1], QS[0])])
    print(source_frame.iloc[:, 3].describe())
    print(QS)
    print(source_frame.iloc[:, 4].describe())
    print(QL)
    plt.show()


def plot_f(source_frame_a, source_frame_b, source_frame_c, source_frame_d):
    '''
    source_frame_a: Production _frame,
    source_frame_b: Labor _frame,
    source_frame_c: Capital _frame,
    source_frame_d: Capacity Utilization _frame'''
    BASE = (31, 1)
    '''Plotting'''
    fig, axs = plt.subplots(4, 1)
    axs[0].plot(source_frame_a.iloc[:, 0], label='Kurenkov Data, {}=100'.format(
        source_frame_a.index[BASE[0]]))
    axs[0].plot(source_frame_a.iloc[:, 1], label='BEA Data, {}=100'.format(
        source_frame_a.index[BASE[0]]))
    axs[0].plot(source_frame_a.iloc[:, 2], label='FRB Data, {}=100'.format(
        source_frame_a.index[BASE[0]]))
    axs[0].set_title('Production')
    axs[0].set_xlabel('Period')
    axs[0].set_ylabel('Percentage')
    axs[0].legend()
    axs[0].grid(True)
    axs[1].plot(source_frame_b.iloc[:, 0], label='Kurenkov Data')
    axs[1].plot(source_frame_b.iloc[:, 1], label='BEA Data')
    axs[1].set_title('Labor')
    axs[1].set_xlabel('Period')
    axs[1].set_ylabel('Thousands of Persons')
    axs[1].legend()
    axs[1].grid(True)
    '''Revised Capital'''
    axs[2].plot(source_frame_c.iloc[:, 0], label='Kurenkov Data, {}=100'.format(
        source_frame_c.index[BASE[1]]))
    axs[2].plot(source_frame_c.iloc[:, 1], label='BEA Data, {}=100'.format(
        source_frame_c.index[BASE[1]]))
    axs[2].set_title('Capital')
    axs[2].set_xlabel('Period')
    axs[2].set_ylabel('Percentage')
    axs[2].legend()
    axs[2].grid(True)
    axs[3].plot(source_frame_d.iloc[:, 0], label='Kurenkov Data')
    axs[3].plot(source_frame_d.iloc[:, 1], label='FRB Data')
    axs[3].set_title('Capacity Utilization')
    axs[3].set_xlabel('Period')
    axs[3].set_ylabel('Percentage')
    axs[3].legend()
    axs[3].grid(True)
    fig.set_size_inches(10., 20.)


def plot_census_complex(source_frame):
    plot_pearson_r_test(source_frame)
    source_frame.reset_index(level=0, inplace=True)
    plot_kzf(source_frame)
    plot_ses(source_frame, 5, 0.1)


def processing_spline(source_frame, kernelModule, deliveryModule):
    source_frame.columns = ['Period', 'Original']
    # Number of Periods
    N = int(input('Define Number of Interpolation Intervals: '))
    if N >= 2:
        print('Number of Periods Provided: {}'.format(N))
        knt = []  # Switch Points
        knt.append(0)
        i = 0
        if N == 1:
            knt.append(source_frame.shape[0]-1)
        elif N >= 2:
            while i < N:
                if i == N-1:
                    knt.append(source_frame.shape[0]-1)
                    i += 1
                else:
                    y = int(input('Select Row for Year: '))-1
                    if y > knt[i]:
                        knt.append(y)
                        i += 1
        else:
            print('Error')  # Should Never Happen
        K, result_frame = kernelModule(source_frame, N, knt)
        deliveryModule(N, K)
        error_metrics(result_frame)
        plt.figure()
        plt.scatter(result_frame.iloc[:, 0], result_frame.iloc[:, 1])
        plt.plot(result_frame.iloc[:, 0], result_frame.iloc[:, 2],
                 color='red', label='$s_{%d}(\\tau)$' % (0,))
        go_no_go = input('Does the Resulting Value Need an Improvement?, Y: ')
        if go_no_go == 'Y':
            Q = []
            assert len(knt) == 1 + N
            for i in range(len(knt)):
                Q.append(
                    float(input('Correction of Knot {:02d}: '.format(1 + i))))
            modified = source_frame.iloc[:, 1].copy()  # Series Modification
            for i in range(len(knt)):
                modified[knt[i]] = Q[i]*modified[knt[i]]

            source_frame = pd.concat(
                [source_frame.iloc[:, 0], modified], axis=1, sort=True)
            source_frame.columns = ['Period', 'Original']
            K, result_frame = kernelModule(source_frame, N, knt)
            deliveryModule(N, K)
            error_metrics(result_frame)
            plt.plot(result_frame.iloc[:, 0], result_frame.iloc[:,
                     2], color='g', label='$s_{%d}(\\tau)$' % (1,))
            plt.grid(True)
            plt.legend()
            plt.show()
        else:
            plt.grid(True)
            plt.legend()
            plt.show()
            pass
    else:
        print('N >= 2 is Required, N = {} Was Provided'.format(N))


def plot_kzf_b(source_frame):
    """Kolmogorov--Zurbenko Filter
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Series"""

    """DataFrame for Kolmogorov--Zurbenko Filter Results"""
    result_frame_a = source_frame
    """DataFrame for Kolmogorov--Zurbenko Filter Residuals"""
    result_frame_b = pd.concat([source_frame.iloc[:, 0], source_frame.iloc[:, 0].rolling(
        window=2).mean()], axis=1, sort=False)
    result_frame_b = pd.concat([result_frame_b, (source_frame.iloc[:, 1]-source_frame.iloc[:,
                               1].shift(1)).div(source_frame.iloc[:, 1].shift(1))], axis=1, sort=False)
    series = source_frame.iloc[:, 1]
    for i in range(1, 1 + source_frame.shape[0]//2):
        series = series.rolling(window=2).mean()
        skz = series.shift(-(i//2))
        result_frame_a = pd.concat([result_frame_a, skz], axis=1, sort=False)
        if i % 2 == 0:
            result_frame_b = pd.concat(
                [result_frame_b, (skz-skz.shift(1)).div(skz.shift(1))], axis=1, sort=False)
        else:
            result_frame_b = pd.concat(
                [result_frame_b, (skz.shift(-1)-skz).div(skz)], axis=1, sort=False)
    plt.figure(1)
    plt.title('Kolmogorov$-$Zurbenko Filter')
    plt.xlabel('Period')
    plt.ylabel('Measure')
    plt.scatter(
        result_frame_a.iloc[:, 0], result_frame_a.iloc[:, 1], label='Original Series')
    for i in range(2, 1 + source_frame.shape[0]//2):
        if i % 2 == 0:
            plt.plot(result_frame_a.iloc[:, 0].rolling(window=2).mean(
            ), result_frame_a.iloc[:, i], label='$KZF(\\lambda = {})$'.format(i-1))
        else:
            plt.plot(result_frame_a.iloc[:, 0], result_frame_a.iloc[:,
                     i], label='$KZF(\\lambda = {})$'.format(i-1))
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Kolmogorov$-$Zurbenko Filter Residuals')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(result_frame_b.iloc[:, 1],
                result_frame_b.iloc[:, 2], label='Residuals')
    for i in range(3, 2 + source_frame.shape[0]//2):
        if i % 2 == 0:
            plt.plot(result_frame_b.iloc[:, 1], result_frame_b.iloc[:, i],
                     label='$\\delta KZF(\\lambda = {})$'.format(i-1))
        else:
            plt.plot(result_frame_b.iloc[:, 0], result_frame_b.iloc[:, i],
                     label='$\\delta KZF(\\lambda = {})$'.format(i-1))
    plt.grid(True)
    plt.legend()
    plt.show()


def test_douglas(control, series_ids):
    '''control from Original Dataset;
    series_ids from Douglas Theory of Wages'''
    if control == 'CDT2S4':
        # Total Fixed Capital in 1880 dollars (4)
        control_frame = fetch_usa_classic(
            'dataset_usa_cobb-douglas.zip', 'CDT2S4')
    elif control == 'J0014':
        control_frame = fetch_usa_census('dataset_usa_census1949.zip', 'J0014')
    test_frame = fetch_usa_classic('dataset_douglas.zip', series_ids)
    if control == 'J0014':
        control_frame.iloc[:, 0] = 100*control_frame.iloc[:,
                                                          0].div(control_frame.iloc[36, 0])  # 1899=100
        control_frame.iloc[:, 0] = control_frame.iloc[:, 0].round(0)
    else:
        pass
    control_frame = pd.concat([control_frame, test_frame], axis=1, sort=True)
    if control == 'J0014':
        control_frame['dev'] = control_frame.iloc[:, 1].sub(
            control_frame.iloc[:, 0])
    elif control == 'CDT2S4':
        control_frame['dev'] = control_frame.iloc[:, 0].div(
            control_frame.iloc[:, 1])
    else:
        pass
    control_frame = control_frame.dropna()
#    control_frame.plot(title='Cobb--Douglas Data Comparison', legend=True, grid=True)
    print(control_frame)


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
