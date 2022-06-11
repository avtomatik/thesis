# =============================================================================
# D:\archiveProjectUSACobbDouglasOptions.py
# =============================================================================


def preprocessing_dx_dy(df: pd.DataFrame) -> pd.DataFrame:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Capital
    df.iloc[:, 1]      Labor
    df.iloc[:, 2]      Product
    ================== =================================
    '''
    df.dropna(inplace=True)
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Capital Intensity Increment
    # =========================================================================
    df['lab_cap_int_inc'] = df.iloc[:, -2].div(df.iloc[:, -2].shift(1))
    # =========================================================================
    # Labor Productivity Increment
    # =========================================================================
    df['lab_product_inc'] = df.iloc[:, -2].div(df.iloc[:, -2].shift(1))
    return df.iloc[:, range(3, df.shape[1])].dropna(axis=0)


def procedure_a(x, y, dx, dy):
    # =============================================================================
    # Scenario I
    # =============================================================================
    # plt.figure(1)
    # plt.plot(X, Y, '--', X, Y, '+') # Description Here
    # =============================================================================
    # TODO: Add Annotations
    # =============================================================================
    # plt.xlabel('Labor Capital Intensity')
    # =============================================================================
    # TODO: Add Annotations
    # =============================================================================
    # plt.ylabel('Labor Productivity')
    # plt.plot(DX, DY, '--', DX, DY, '+') # Description Here
    # =============================================================================
    # TODO: Add Annotations
    # =============================================================================
    # plt.xlabel('Labor Capital Intensity Increment')
    # =============================================================================
    # TODO: Add Annotations
    # =============================================================================
    # plt.ylabel('Labor Productivity Increment')
    # plt.show()
    # =============================================================================
    # Scenario II
    # =============================================================================
    fig = plt.figure()
    # plt.plot(X, Y, '--', X, Y, '+') # Description Here
# =============================================================================
# TODO: Add Annotations
# =============================================================================
    # plt.xlabel('Labor Capital Intensity')
# =============================================================================
# TODO: Add Annotations
# =============================================================================
    # plt.ylabel('Labor Productivity')
    plt.plot(DX, DY, '--', DX, DY, '+')  # Description Here
# =============================================================================
# TODO: Add Annotations
# =============================================================================
    plt.xlabel('Labor Capital Intensity Increment')
# =============================================================================
# TODO: Add Annotations
# =============================================================================
    plt.ylabel('Labor Productivity Increment')
    ax = fig.add_subplot(111)
    # for i in range(0, 90, 5):
    #     ax.annotate(period[i], (DX[i], DY[i]))
    plt.grid()
    # result_frame = pd.concat([period, capital, labor, product, X, Y, DX, DY], axis=1, sort=False)
    # result_frame.to_csv('dataset-usa-cobb-douglas-modern-dataset-out.csv', index=False)
    plt.show()


def procedure_b(x, y, dx, dy):
    # =============================================================================
    # Scenario I
    # =============================================================================
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(X, Y)
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    # for i in range(4, 90, 5):
    #     ax.annotate(period[i], (X[i], Y[i]))
    plt.grid()
    plt.show()
# =============================================================================
# Scenario II
# =============================================================================
    # plt.figure()
    # plt.plot(X, Y, 'o', X, Y, '-')
    # plt.xlabel('Labor Capital Intensity')
    # plt.ylabel('Labor Productivity')
    # plt.show()


# =============================================================================
# TODO: Revise Dataset
# =============================================================================
os.chdir('/media/alexander/321B-6A94')
data_frame = get_dataset_common_archived()
T = data_frame.iloc[:, 0]
# =============================================================================
# Deflator, 2009=100
# =============================================================================
d = data_frame.loc[:, ['A191RX1']].div(data_frame.loc[:, ['A191RC1']])
# =============================================================================
# Fixed Assets, K160491
# =============================================================================
cap_a_a = data_frame.loc[:, ['K160491']]*d
# =============================================================================
# Fixed Assets, k3n31gd1es000
# =============================================================================
cap_a_b = data_frame.loc[:, ['k3n31gd1es000']]*d
cap_b_a = data_frame.loc[:, ['k1ntotl1si000']].mul(
    data_frame.loc[:, ['A191RD3']])
cap_b_b = data_frame.loc[:, ['k1ntotl1si000']].mul(
    data_frame.loc[:, ['A191RX1']]).div(data_frame.loc[:, ['A191RC1']])
cap_b_c = data_frame.loc[:, ['k3n31gd1es000']].mul(
    data_frame.loc[:, ['A191RD3']])
cap_b_d = data_frame.loc[:, ['k3n31gd1es000']].mul(
    data_frame.loc[:, ['A191RX1']]).div(data_frame.loc[:, ['A191RC1']])
L = data_frame.loc[:, ['Labor']]
# =============================================================================
# Production
# =============================================================================
prd_a_a = d*data_frame.loc[:, ['A032RC1']]
# =============================================================================
# Production Maximum
# =============================================================================
prd_a_b = 100*d*data_frame.loc[:, ['A032RC1']
                               ].div(data_frame.loc[:, ['CAPUTLB50001A']])
prd_b_a = data_frame.loc[:, ['A191RC1']].mul(data_frame.loc[:, ['A191RD3']])
prd_b_b = data_frame.loc[:, ['A191RX1']]
# # =============================================================================
# # Option 1
# # =============================================================================
# x_a, x_b, x_c, x_d = preprocessing_dx_dy(data_frame.index.get_loc(1967),
#                                          data_frame.index.get_loc(2012),
#                                          T, data_frame.loc[:, ['K160491']]*d, L, prd_a_a)
# # =============================================================================
# # Option 2
# # =============================================================================
# x_a, x_b, x_c, x_d = preprocessing_dx_dy(data_frame.index.get_loc(1967),
#                                          data_frame.index.get_loc(2012),
#                                          T, data_frame.loc[:, ['K160491']]*d, L, prd_a_b)
# # =============================================================================
# # Option 3
# # =============================================================================
# x_a, x_b, x_c, x_d = preprocessing_dx_dy(data_frame.index.get_loc(1967),
#                                          data_frame.index.get_loc(2012),
#                                          T, cap_a_b, L, prd_a_a)
# # =============================================================================
# # Option 4
# # =============================================================================
# x_a, x_b, x_c, x_d = preprocessing_dx_dy(data_frame.index.get_loc(1967),
#                                          data_frame.index.get_loc(2012),
#                                          T, cap_a_b, L, prd_a_b)
# # =============================================================================
# # TODO: test `k1ntotl1si000`
# # =============================================================================
# # =============================================================================
# # Option 1
# # =============================================================================
# x_a, x_b, x_c, x_d = preprocessing_dx_dy(data_frame.index.get_loc(1929),
#                                          data_frame.index.get_loc(2013),
#                                          T, cap_b_a, L, prd_b_a)
# # =============================================================================
# # Option 2
# # =============================================================================
# x_a, x_b, x_c, x_d = preprocessing_dx_dy(data_frame.index.get_loc(1929),
#                                          data_frame.index.get_loc(2013),
#                                          T, cap_b_b, L, prd_b_b)
# # =============================================================================
# # Option 5
# # =============================================================================
# x_a, x_b, x_c, x_d = preprocessing_dx_dy(data_frame.index.get_loc(1929),
#                                          data_frame.index.get_loc(2013),
#                                          T, cap_b_c, L, prd_b_a)
# # =============================================================================
# # Option 6
# # =============================================================================
# x_a, x_b, x_c, x_d = preprocessing_dx_dy(data_frame.index.get_loc(1929),
#                                          data_frame.index.get_loc(2013),
#                                          T, cap_b_d, L, prd_b_b)
procedure_a(x_a, x_b, x_c, x_d)
# # procedure_b(x_a, x_b, x_c, x_d)
"""Update from `project.py`"""


def price_inverse_single(data_series):
    '''Intent: Returns Prices Icrement Series from Cumulative Deflator Series;
    source: pandas DataFrame'''
    return data_series.div(data_series.shift(1)).sub(1)


def strip_cumulated_deflator(data_frame):
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    return price_inverse_single(data_frame.dropna()).dropna()


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


def plot_increment(df: pd.DataFrame) -> None:
    FLAG = False
    FOLDER = '/home/alexander/science'
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(df.iloc[:, 0], df.iloc[:, 1], label='Curve')
    axs[0].set_xlabel('Labor Capital Intensity')
    axs[0].set_ylabel('Labor Productivity')
    axs[0].set_title('Labor Capital Intensity to Labor Productivity Relation')
    axs[0].legend()
    axs[0].grid(True)
    axs[1].plot(df.iloc[:, 2], df.iloc[:, 3], label='Curve')
    axs[1].set_xlabel('Labor Capital Intensity Increment')
    axs[1].set_ylabel('Labor Productivity Increment')
    axs[1].set_title(
        'Labor Capital Intensity to Labor Productivity Increments Relation')
    axs[1].grid(True)
    axs[1].legend()
    for _ in range(3, df.shape[0], 5):
        axs[0].annotate(df.index[_], (df.iloc[_, 0], df.iloc[_, 1]))
        axs[1].annotate(df.index[_], (df.iloc[_, 2], df.iloc[_, 3]))
    fig.set_size_inches(10., 20.)
    fig.tight_layout()
    if FLAG:
        fig.savefig(
            os.path.join(FOLDER, 'fig_file_name.pdf'),
            format='pdf', dpi=900
        )
    else:
        plt.show()


source_frame = preprocessing_dx_dy_service(get_dataset_version_c())
plot_increment(source_frame)
