def fetch_can_capital_query(source_frame):
# =============================================================================
#     '''Fetch `Series series_ids` from Statistics Canada. Table: 36-10-0238-01\
#     (formerly CANSIM 031-0004): Flows and stocks of fixed non-residential\
#     capital, total all industries, by asset, provinces and territories, annual\
#     (dollars x 1,000,000)'''
# =============================================================================
    query = (source_frame.iloc[:, 3].str.contains('2007 constant prices')) &\
            (source_frame.iloc[:, 5] == 'Straight-line end-year net stock') &\
            (source_frame.iloc[:, 6].str.contains('Industrial'))
    source_frame = source_frame[ query ]
    source_frame = source_frame[source_frame.columns[[11]]]
    source_frame.drop_duplicates(inplace=True)
    series_ids = source_frame.iloc[:, 0].values.tolist()
    return series_ids


def cobb_douglas_canada(source_frame):
# =============================================================================
#     '''Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
#     source_frame.index: Period,
#     source_frame.iloc[:, 0]: Capital,
#     source_frame.iloc[:, 1]: Labor,
#     source_frame.iloc[:, 2]: Product
#     '''
# =============================================================================
    def pl(series, k=0.25, b=1.01):
        return b*series**(-k)


    def pc(series, k=0.25, b=1.01):
        return b*series**(1-k)


    function_dict = {'figure_a':'Chart I Progress in Manufacturing %d$-$%d (%d=100)',
                'figure_b':'Chart II Theoretical and Actual Curves of Production %d$-$%d (%d=100)',
                'figure_c':'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines = 3 Year Moving Average',
                'figure_d':'Chart IV Percentage Deviations of Computed from Actual Product %d$-$%d',
                'priceyear':2007}
    X = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])
    Y = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1])

    X = log(X)
    Y = log(Y)
    k, b = np.polyfit(X, Y, 1) # # Original: k = 0.25
    b = np.exp(b)
    source_frame['prod_comp'] = b*(source_frame.iloc[:, 0]**k)*(source_frame.iloc[:, 1]**(1-k))
    source_frame['prod_roll'] = source_frame.iloc[:, 2].rolling(window=3, center=True).mean()
    source_frame['prod_roll_comp'] = source_frame.iloc[:, 3].rolling(window=3, center=True).mean()
    source_frame['sub_prod'] = source_frame.iloc[:, 2].sub(source_frame.iloc[:, 4])
    source_frame['sub_comp'] = source_frame.iloc[:, 3].sub(source_frame.iloc[:, 5])
    source_frame['dev_prod'] = source_frame.iloc[:, 3].div(source_frame.iloc[:, 2])-1
    plt.figure(1)
    plt.semilogy(source_frame.iloc[:, 0], label='Fixed Capital')
    plt.semilogy(source_frame.iloc[:, 1], label='Labor Force')
    plt.semilogy(source_frame.iloc[:, 2], label='Physical Product')
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(function_dict['figure_a'] %(source_frame.index[0],
                                        source_frame.index[-1],
                                        function_dict['priceyear']))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.semilogy(source_frame.iloc[:, 2], label='Actual Product')
    plt.semilogy(source_frame.iloc[:, 3], label='Computed Product, $P\' = %fL^{%f}C^{%f}$' %(b, 1-k, k))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(function_dict['figure_b'] %(source_frame.index[0],
                                        source_frame.index[-1],
                                        function_dict['priceyear']))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(source_frame.iloc[:, 6], label='Deviations of $P$')
    plt.plot(source_frame.iloc[:, 7], '--', label='Deviations of $P\'$')
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(function_dict['figure_c'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(source_frame.iloc[:, 3].div(source_frame.iloc[:, 2])-1)
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(function_dict['figure_d'] %(source_frame.index[0],
                                        source_frame.index[-1]))
    plt.grid(True)
    plt.figure(5, figsize = (5, 8))
    lc = np.arange(0.2, 1.0, 0.005)
    plt.scatter(source_frame.iloc[:, 1].div(source_frame.iloc[:, 0]),
              source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]))
    plt.scatter(source_frame.iloc[:, 1].div(source_frame.iloc[:, 0]),
              source_frame.iloc[:, 2].div(source_frame.iloc[:, 0]))
    plt.plot(lc, pl(lc, k = k, b = b), label='$\\frac{3}{4}\\frac{P}{L}$')
    plt.plot(lc, pc(lc, k = k, b = b), label='$\\frac{1}{4}\\frac{P}{C}$')
    plt.xlabel('$\\frac{L}{C}$')
    plt.ylabel('Indexes')
    plt.title('Relative Final Productivities of Labor and Capital')
    plt.legend()
    plt.grid(True)
    plt.show()

    print(r2_score(source_frame.iloc[:, 2], source_frame.iloc[:, 3]))
    print(np.absolute(source_frame.iloc[:, 3].sub(source_frame.iloc[:, 2]).div(source_frame.iloc[:, 2])).mean())

def cobb_douglas_3d(source_frame):
# =============================================================================
#     '''Cobb--Douglas 3D-Plotting
#     source_frame.index: Period,
#     source_frame.iloc[:, 0]: Capital,
#     source_frame.iloc[:, 1]: Labor,
#     source_frame.iloc[:, 2]: Product
#     '''
# =============================================================================
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    ax.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 1], source_frame.iloc[:, 2])
    ax.set_xlabel('Capital')
    ax.set_ylabel('Labor')
    ax.set_zlabel('Production')
    ax.view_init(30, 45)
    plt.show()


print(__doc__)
# result_frame = dataset_canada()
# # cobb_douglas_canada(result_frame)
# # cobb_douglas_3d(result_frame)
# df = fetch_from_url('https://www150.statcan.gc.ca/n1/en/tbl/csv/36100210-eng.zip')
df = fetch_from_url('https://www150.statcan.gc.ca/n1/tbl/csv/18100081-eng.zip')
