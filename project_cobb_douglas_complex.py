#-*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:17:13 2020

@author: Mastermind
"""


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
        odd_frame = pd.concat([odd_frame, result_frame.iloc[:, i]], axis=1, sort=True)
    for i in range(2, 2 + k, 2):
        even_frame = pd.concat([even_frame, result_frame.iloc[:, i]], axis=1, sort=True)
    even_frame = even_frame.dropna(how='all').reset_index(drop=True)
    odd_frame = odd_frame.set_index('Period')
    even_frame = even_frame.set_index('Period')
    return odd_frame, even_frame


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
        odd_frame = pd.concat([odd_frame, result_frame.iloc[:, i]], axis=1, sort=True)
    for i in range(2, 2 + k, 2):
        even_frame = pd.concat([even_frame, result_frame.iloc[:, i]], axis=1, sort=True)
    even_frame = even_frame.dropna(how='all').reset_index(drop=True)
    odd_frame = odd_frame.set_index('Period')
    even_frame = even_frame.set_index('Period')
    return odd_frame, even_frame


def plot_lab_prod_polynomial(source_frame):
    '''Static Labor Productivity Approximation
    source_frame.index: Period,
    source_frame.iloc[:, 0]: Capital,
    source_frame.iloc[:, 1]: Labor,
    source_frame.iloc[:, 2]: Product
    '''
    X = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1]) # # Labor Capital Intensity
    Y = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]) # # Labor Productivity
    '''Power Function: Labor Productivity'''
    yp1p = sp.polyfit(sp.log(X), sp.log(Y), 1)
    '''Polynomials 1, 2, 3 & 4: Labor Productivity'''
    yl1p = sp.polyfit(X, Y, 1)
    yl2p = sp.polyfit(X, Y, 2)
    yl3p = sp.polyfit(X, Y, 3)
    yl4p = sp.polyfit(X, Y, 4)
    PP = sp.exp(yp1p[1])*X**yp1p[0]
    YAA = yl1p[1] + yl1p[0]*X
    YBB = yl2p[2] + yl2p[1]*X + yl2p[0]*X**2
    YCC = yl3p[3] + yl3p[2]*X + yl3p[1]*X**2 + yl3p[0]*X**3
    YDD = yl4p[4] + yl4p[3]*X + yl4p[2]*X**2 + yl4p[1]*X**3 + yl4p[0]*X**4
    '''Deltas'''
    DPP = sp.absolute((sp.exp(yp1p[1])*X**yp1p[0]-Y).div(Y))
    DYAA = sp.absolute((YAA-Y).div(Y))
    DYBB = sp.absolute((YBB-Y).div(Y))
    DYCC = sp.absolute((YCC-Y).div(Y))
    DYDD = sp.absolute((YDD-Y).div(Y))

    r20 = r2_score(Y, PP)
    r21 = r2_score(Y, YAA)
    r22 = r2_score(Y, YBB)
    r23 = r2_score(Y, YCC)
    r24 = r2_score(Y, YDD)
    plt.figure(1)
    plt.scatter(source_frame.index, Y, label='Labor Productivity')
    plt.plot(source_frame.index, PP, label='$\\hat Y = {:.2f}X^{{{:.2f}}}, R^2 = {:.4f}$'.format(sp.exp(yp1p[1]), yp1p[0], r20))
    plt.plot(source_frame.index, YAA, label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X, R^2 = {:.4f}$'.format(1, yl1p[1], yl1p[0], r21))
    plt.plot(source_frame.index, YBB, label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2, R^2 = {:.4f}$'.format(2, yl2p[2], yl2p[1], yl2p[0], r22))
    plt.plot(source_frame.index, YCC, label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2+{:.2f}X^3, R^2 = {:.4f}$'.format(3, yl3p[3], yl3p[2], yl3p[1], yl3p[0], r23))
    plt.plot(source_frame.index, YDD, label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2+{:.2f}X^3 {:.2f}X^4, R^2 = {:.4f}$'.format(4, yl4p[4], yl4p[3], yl4p[2], yl4p[1], yl4p[0], r24))
    plt.title('Labor Capital Intensity & Labor Productivity, {}$-${}'.format(source_frame.index[0], source_frame.index[-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(source_frame.index, DPP, ':', label='$\\|\\frac{{\\hat Y-Y}}{{Y}}\\|, \\bar S = {:.4%}$'.format(DPP.mean()))
    plt.plot(source_frame.index, DYAA, ':', label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4%}$'.format(1, DYAA.mean()))
    plt.plot(source_frame.index, DYBB, ':', label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4%}$'.format(2, DYBB.mean()))
    plt.plot(source_frame.index, DYCC, ':', label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4%}$'.format(3, DYCC.mean()))
    plt.plot(source_frame.index, DYDD, ':', label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4%}$'.format(4, DYDD.mean()))
    plt.title('Deltas of Labor Capital Intensity & Labor Productivity, {}$-${}'.format(source_frame.index[0], source_frame.index[-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_simple_linear(source_frame, coef1, coef2, E):
    '''
    Labor Productivity on Labor Capital Intensity Plot;
    Predicted Labor Productivity Plot
    '''
    plt.figure(1)
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 1], label='Original')
    plt.title('$Labor\ Capital\ Intensity$, $Labor\ Productivity$ Relation, {}$-${}'.format(source_frame.index[0], source_frame.index[-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(source_frame.index, E, label='$\\frac{Y}{Y_{0}} = %f\\frac{L}{L_{0}}+%f\\frac{K}{K_{0}}$' %(coef1, coef2))
    plt.title('Model: $\\hat Y = {:.4f}+{:.4f}\\times X$, {}$-${}'.format(coef1, coef2, source_frame.index[0], source_frame.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('$\\hat Y = Labor\ Productivity$, $X = Labor\ Capital\ Intensity$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_simple_log(source_frame, coef1, coef2, E):
    '''
    Log Labor Productivity on Log Labor Capital Intensity Plot;
    Predicted Log Labor Productivity Plot
    '''
    plt.figure(1)
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 1], label='Logarithm')
    plt.title('$\\ln(Labor\ Capital\ Intensity), \\ln(Labor\ Productivity)$ Relation, {}$-${}'.format(source_frame.index[0], source_frame.index[-1]))
    plt.xlabel('$\\ln(Labor\ Capital\ Intensity)$')
    plt.ylabel('$\\ln(Labor\ Productivity)$')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(source_frame.index, E, label='$\\ln(\\frac{Y}{Y_{0}}) = %f+%f\\ln(\\frac{K}{K_{0}})+%f\\ln(\\frac{L}{L_{0}})$' %(coef1, coef2, 1-coef2))
    plt.title('Model: $\\ln(\\hat Y) = {:.4f}+{:.4f}\\times \\ln(X)$, {}$-${}'.format(coef1, coef2, source_frame.index[0], source_frame.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('$\\hat Y = \\ln(Labor\ Productivity)$, $X = \\ln(Labor\ Capital\ Intensity)$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_turnover(source_frame):
    '''Static Fixed Assets Turnover Approximation
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Capital,
    source_frame.iloc[:, 2]: Product
    '''
    K = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]) # # Fixed Assets Turnover
    '''Linear: Fixed Assets Turnover'''
    kl1p = sp.polyfit(source_frame.iloc[:, 0], K, 1)
    '''Exponential: Fixed Assets Turnover'''
    ke1p = sp.polyfit(source_frame.iloc[:, 0], sp.log(K), 1)
    K1 = kl1p[1] + kl1p[0]*source_frame.iloc[:, 0]
    K2 = sp.exp(ke1p[1] + ke1p[0]*source_frame.iloc[:, 0])
    '''Deltas'''
    DK1 = sp.absolute((K1-K).div(K))
    DK2 = sp.absolute((K2-K).div(K))

    r21 = r2_score(K, K1)
    r22 = r2_score(K, K2)
    plt.figure(1)
    plt.plot(source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]), source_frame.iloc[:, 1])
    plt.title('Fixed Assets Volume to Fixed Assets Turnover, {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Fixed Assets Turnover')
    plt.ylabel('Fixed Assets Volume')
    plt.grid(True)
    plt.figure(2)
    plt.scatter(source_frame.iloc[:, 0], K, label='Fixed Assets Turnover')
    plt.plot(source_frame.iloc[:, 0], K1, label='$\\hat K_{{l}} = {:.2f} {:.2f} t, R^2 = {:.4f}$'.format(kl1p[1], kl1p[0], r21))
    plt.plot(source_frame.iloc[:, 0], K2, label='$\\hat K_{{e}} = \\exp ({:.2f} {:.2f} t), R^2 = {:.4f}$'.format(ke1p[1], ke1p[0], r22))
    plt.title('Fixed Assets Turnover Approximation, {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.plot(source_frame.iloc[:, 0], DK1, ':', label='$\\|\\frac{{\\hat K_{{l}}-K}}{{K}}\\|, \\bar S = {:.4%}$'.format(DK1.mean()))
    plt.plot(source_frame.iloc[:, 0], DK2, ':', label='$\\|\\frac{{\\hat K_{{e}}-K}}{{K}}\\|, \\bar S = {:.4%}$'.format(DK2.mean()))
    plt.title('Deltas of Fixed Assets Turnover Approximation, {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_block_zero(source_frame):
    '''
    source_frame.index: Period,
    source_frame.iloc[:, 0]: Capital,
    source_frame.iloc[:, 1]: Labor,
    source_frame.iloc[:, 2]: Product
    '''
    pd.options.mode.chained_assignment = None
    source_frame['lab_cap_int'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1]) # # Labor Capital Intensity
    source_frame['lab_product'] = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]) # # Labor Productivity
    source_frame['log_lab_c'] = sp.log(source_frame.iloc[:, 0].div(source_frame.iloc[:, 1]))
    source_frame['log_lab_p'] = sp.log(source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]))
    result_frame_a = source_frame[source_frame.columns[[3, 4]]]
    result_frame_b = source_frame[source_frame.columns[[5, 6]]]
    a0, a1, ea = simple_linear_regression(result_frame_a)
    plot_simple_linear(result_frame_a, a0, a1, ea)
    b0, b1, eb = simple_linear_regression(result_frame_b)
    plot_simple_log(result_frame_b, b0, b1, eb)


def plot_block_one(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Capital,
    source_frame.iloc[:, 2]: Labor,
    source_frame.iloc[:, 3]: Product
    '''
    source_frame['lab_cap_int'] = source_frame.iloc[:, 1].div(source_frame.iloc[:, 2]) # # Labor Capital Intensity
    labcap_frame = source_frame[source_frame.columns[[0, 4]]]
    semi_frame_a, semi_frame_b = RMF(labcap_frame)
    semi_frame_c, semi_frame_d = KZF(labcap_frame)
    semi_frame_e = SES(labcap_frame, 5, 0.25)
    semi_frame_e = semi_frame_e.iloc[:, 1]
    odd_frame = pd.concat([semi_frame_a, semi_frame_e], axis=1, sort=True)
    even_frame = pd.concat([semi_frame_b, semi_frame_d], axis=1, sort=True)
    plt.figure()
    odd_frame.iloc[:, 0].plot(linewidth = 3, label='Labor Capital Intensity')
    odd_frame.iloc[:, 1].plot(label='Single Exponential Smoothing, Window = {}, Alpha = {:, .2f}'.format(5, 0.25))
    even_frame.iloc[:, 0].plot(label='Rolling Mean, {}'.format(2))
    even_frame.iloc[:, 1].plot(label='Kolmogorov--Zurbenko Filter, {}'.format(2))
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
    source_frame['lab_product'] = source_frame.iloc[:, 3].div(source_frame.iloc[:, 2]) # # Labor Productivity
    labpro_frame = source_frame[source_frame.columns[[0, 4]]]
    semi_frame_a, semi_frame_b = RMF(labpro_frame, 3)
    semi_frame_c, semi_frame_d = KZF(labpro_frame, 3)
    semi_frame_c = semi_frame_c.iloc[:, 1]
    semi_frame_e = SES(labpro_frame, 5, 0.25)
    semi_frame_e = semi_frame_e.iloc[:, 1]
    semi_frame_f = SES(labpro_frame, 5, 0.35)
    semi_frame_f = semi_frame_f.iloc[:, 1]
    semi_frame_g = SES(labpro_frame, 5, 0.45)
    semi_frame_g = semi_frame_g.iloc[:, 1]
    odd_frame = pd.concat([semi_frame_a, semi_frame_c, semi_frame_e, semi_frame_f, semi_frame_g], axis=1, sort=True)
    even_frame = pd.concat([semi_frame_b, semi_frame_d], axis=1, sort=True)
    plt.figure()
    odd_frame.iloc[:, 0].plot(linewidth = 3, label='Labor Productivity')
    odd_frame.iloc[:, 1].plot(label='Rolling Mean, {}'.format(3))
    odd_frame.iloc[:, 2].plot(label='Kolmogorov--Zurbenko Filter, {}'.format(3))
    odd_frame.iloc[:, 3].plot(label='Single Exponential Smoothing, Window = {}, Alpha = {:, .2f}'.format(5, 0.25))
    odd_frame.iloc[:, 4].plot(label='Single Exponential Smoothing, Window = {}, Alpha = {:, .2f}'.format(5, 0.35))
    odd_frame.iloc[:, 5].plot(label='Single Exponential Smoothing, Window = {}, Alpha = {:, .2f}'.format(5, 0.45))
    even_frame.iloc[:, 0].plot(label='Rolling Mean, {}'.format(2))
    even_frame.iloc[:, 1].plot(label='Rolling Mean, {}'.format(4))
    even_frame.iloc[:, 2].plot(label='Kolmogorov--Zurbenko Filter, {}'.format(2))
    even_frame.iloc[:, 3].plot(label='Kolmogorov--Zurbenko Filter, {}'.format(4))
    plt.title('Labor Capital Intensity: Rolling Mean Filter, Kolmogorov--Zurbenko Filter &\n\
              Single Exponential Smoothing')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.legend()
    plt.grid(True)
    plt.show()


def simple_linear_regression(source_frame):
    '''Determining of Coefficients of Regression
    source_frame.index: Period,
    source_frame.iloc[:, 0]: Regressor,
    source_frame.iloc[:, 1]: Regressand
    '''
    '''Summarize'''
    S1 = sum(source_frame.iloc[:, 0])
    S2 = sum(source_frame.iloc[:, 1])
    S3 = sum((source_frame.iloc[:, 0])**2)
    S4 = sum(source_frame.iloc[:, 0]*source_frame.iloc[:, 1])
    '''Approximation'''
    A0 = (S2*S3-S1*S4)/(source_frame.shape[0]*S3-S1**2)
    A1 = (source_frame.shape[0]*S4-S1*S2)/(source_frame.shape[0]*S3-S1**2)
    E = A0 + A1*(source_frame.iloc[:, 0])
    MY = sp.mean(source_frame.iloc[:, 1])
    ESS = sum((source_frame.iloc[:, 1]-A0-A1*source_frame.iloc[:, 0])**2)
    TSS = sum((source_frame.iloc[:, 1]-MY)**2)
    R2 = 1-ESS/TSS
    '''Delivery Block'''
    print('Period From {} Through {}'.format(source_frame.index[0], source_frame.index[-1]))
    print('Model: Yhat = {:,.4f}+{:,.4f}*X'.format(A0, A1))
    print('Model Parameter: A0 = {:,.4f}'.format(A0))
    print('Model Parameter: A1 = {:,.4f}'.format(A1))
    print('Model Result: ESS = {:,.4f}; TSS = {:,.4f}; R**2 = {:,.4f}'.format(ESS, TSS, R2))
    return A0, A1, E


def plot_cobb_douglas_complex(source_frame):
    modified_frame_a = source_frame.reset_index(level=0)
    modified_frame_b = source_frame[source_frame.columns[[0, 2]]]
    modified_frame_b = modified_frame_b.reset_index(level=0)
    cobb_douglas_original(source_frame)
    cobb_douglas_3d(source_frame)
    plot_lab_prod_polynomial(source_frame)
    plot_block_zero(source_frame)
    plot_block_one(modified_frame_a)
    plot_block_two(modified_frame_a)
    plot_turnover(modified_frame_b)


'''On Original Dataset'''
source_frame = get_dataset_cobb_douglas()
result_frame_a = source_frame[source_frame.columns[[0, 1, 2]]]
result_frame_b = source_frame[source_frame.columns[[0, 1, 3]]]
result_frame_c = source_frame[source_frame.columns[[0, 1, 4]]]
'''On Expanded Dataset'''
result_frame_d, result_frame_e = get_dataset_version_a()
result_frame_f, result_frame_g, result_frame_h = get_dataset_version_b()
result_frame_i = dataset_version_c()
plot_cobb_douglas_complex(result_frame_a)
plot_cobb_douglas_complex(result_frame_b)
plot_cobb_douglas_complex(result_frame_c)
'''No Capacity Utilization Adjustment'''
plot_cobb_douglas_complex(result_frame_d)
'''Capacity Utilization Adjustment'''
plot_cobb_douglas_complex(result_frame_e)
'''Option: 1929--2013, No Capacity Utilization Adjustment'''
plot_cobb_douglas_complex(result_frame_f)
'''Option: 1967--2013, No Capacity Utilization Adjustment'''
plot_cobb_douglas_complex(result_frame_g)
'''Option: 1967--2012, Capacity Utilization Adjustment'''
plot_cobb_douglas_complex(result_frame_h)
plot_cobb_douglas_complex(result_frame_i)