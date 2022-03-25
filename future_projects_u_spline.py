# =============================================================================
# Scipy Univariate Spline
# =============================================================================


def spline_procedure(source_frame):
    '''
    source_frame.index: Period,
    source_frame.iloc[:, 0]: Capital,
    source_frame.iloc[:, 1]: Labor,
    source_frame.iloc[:, 2]: Product
    '''
    X = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1]) # # Labor Capital Intensity
    Y = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]) # # Labor Productivity
    X = X.sort_values()
    spl = UnivariateSpline(X, Y)

    Z = np.linspace(X.min(), X.max(), source_frame.shape[0]-1)

    plt.figure()
    plt.scatter(X, Y, label='Original')
    plt.plot(Z, spl(Z))
    plt.title('Labor Capital Intensity & Labor Productivity, {}$-${}'.format(source_frame.index[0], source_frame.index[-1]))
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


source_frame = get_dataset_cobb_douglas()
spline_procedure(source_frame)

