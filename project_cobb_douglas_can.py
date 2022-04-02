

def fetch_can_capital_query(source_frame):
    # =============================================================================
    # '''Fetch `Series series_ids` from Statistics Canada. Table: 36-10-0238-01\
    # (formerly CANSIM 031-0004): Flows and stocks of fixed non-residential\
    # capital, total all industries, by asset, provinces and territories, annual\
    # (dollars x 1,000,000)'''
    # =============================================================================
    query = (source_frame.iloc[:, 3].str.contains('2007 constant prices')) &\
            (source_frame.iloc[:, 5] == 'Straight-line end-year net stock') &\
            (source_frame.iloc[:, 6].str.contains('Industrial'))
    source_frame = source_frame[query]
    source_frame = source_frame.iloc[:, [11]]
    source_frame.drop_duplicates(inplace=True)
    series_ids = source_frame.iloc[:, 0].values.tolist()
    return series_ids


def plot_cobb_douglas_canada(data_frame):
    # =============================================================================
    # '''Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    # data_frame.index: Period,
    # data_frame.iloc[:, 0]: Capital,
    # data_frame.iloc[:, 1]: Labor,
    # data_frame.iloc[:, 2]: Product
    # '''
    # =============================================================================
    def pl(series, k=0.25, b=1.01):
        return b*series**(-k)

    def pc(series, k=0.25, b=1.01):
        return b*series**(1-k)

    FIGURES = {
        'fig_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
        'fig_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
        'fig_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fig_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
        'priceyear': 2007
    }
    X = data_frame.iloc[:, 0].div(data_frame.iloc[:, 1])
    Y = data_frame.iloc[:, 2].div(data_frame.iloc[:, 1])

    X = log(X)
    Y = log(Y)
# =============================================================================
# Original: k=0.25
# =============================================================================
    k, b = np.polyfit(X, Y, 1)
    b = np.exp(b)
    data_frame['prod_comp'] = b * \
        (data_frame.iloc[:, 0]**k)*(data_frame.iloc[:, 1]**(1-k))
    data_frame['prod_roll'] = data_frame.iloc[:,
                                              2].rolling(window=3, center=True).mean()
    data_frame['prod_roll_comp'] = data_frame.iloc[:,
                                                   3].rolling(window=3, center=True).mean()
    data_frame['sub_prod'] = data_frame.iloc[:, 2].sub(data_frame.iloc[:, 4])
    data_frame['sub_comp'] = data_frame.iloc[:, 3].sub(data_frame.iloc[:, 5])
    data_frame['dev_prod'] = data_frame.iloc[:, 3].div(
        data_frame.iloc[:, 2]).sub(1)
    plt.figure(1)
    plt.semilogy(data_frame.iloc[:, 0], label='Fixed Capital')
    plt.semilogy(data_frame.iloc[:, 1], label='Labor Force')
    plt.semilogy(data_frame.iloc[:, 2], label='Physical Product')
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(FIGURES['fig_a'] % (data_frame.index[0],
                                  data_frame.index[-1],
                                  FIGURES['priceyear']))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.semilogy(data_frame.iloc[:, 2], label='Actual Product')
    plt.semilogy(
        data_frame.iloc[:, 3], label='Computed Product, $P\' = %fL^{%f}C^{%f}$' % (b, 1-k, k))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(FIGURES['fig_b'] % (data_frame.index[0],
                                  data_frame.index[-1],
                                  FIGURES['priceyear']))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(data_frame.iloc[:, 6], label='Deviations of $P$')
    plt.plot(data_frame.iloc[:, 7], '--', label='Deviations of $P\'$')
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(FIGURES['fig_c'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(data_frame.iloc[:, 3].div(data_frame.iloc[:, 2]).sub(1))
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(FIGURES['fig_d'].format(data_frame.index[0],
                                      data_frame.index[-1]))
    plt.grid(True)
    plt.figure(5, figsize=(5, 8))
    lc = np.arange(0.2, 1.0, 0.005)
    plt.scatter(data_frame.iloc[:, 1].div(data_frame.iloc[:, 0]),
                data_frame.iloc[:, 2].div(data_frame.iloc[:, 1]))
    plt.scatter(data_frame.iloc[:, 1].div(data_frame.iloc[:, 0]),
                data_frame.iloc[:, 2].div(data_frame.iloc[:, 0]))
    plt.plot(lc, pl(lc, k=k, b=b), label='$\\frac{3}{4}\\frac{P}{L}$')
    plt.plot(lc, pc(lc, k=k, b=b), label='$\\frac{1}{4}\\frac{P}{C}$')
    plt.xlabel('$\\frac{L}{C}$')
    plt.ylabel('Indexes')
    plt.title('Relative Final Productivities of Labor and Capital')
    plt.legend()
    plt.grid(True)
    plt.show()

    print(r2_score(data_frame.iloc[:, 2], data_frame.iloc[:, 3]))
    print(np.absolute(data_frame.iloc[:, 3].sub(
        data_frame.iloc[:, 2]).div(data_frame.iloc[:, 2])).mean())


def plot_cobb_douglas_3d(source_frame):
    # =============================================================================
    # '''Cobb--Douglas 3D-Plotting
    # source_frame.index: Period,
    # source_frame.iloc[:, 0]: Capital,
    # source_frame.iloc[:, 1]: Labor,
    # source_frame.iloc[:, 2]: Product
    # '''
    # =============================================================================
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(source_frame.iloc[:, 0],
            source_frame.iloc[:, 1], source_frame.iloc[:, 2])
    ax.set_xlabel('Capital')
    ax.set_ylabel('Labor')
    ax.set_zlabel('Production')
    ax.view_init(30, 45)
    plt.show()


print(__doc__)
# result_frame = get_dataset_can()
# # plot_cobb_douglas_canada(result_frame)
# # plot_cobb_douglas_3d(result_frame)
# df = fetch_from_url('https://www150.statcan.gc.ca/n1/en/tbl/csv/36100210-eng.zip')
df = fetch_from_url('https://www150.statcan.gc.ca/n1/tbl/csv/18100081-eng.zip')
