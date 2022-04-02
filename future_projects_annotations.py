 =============================================================================
# D:\archiveProjectUSACobbDouglasOptions.py
# =============================================================================


def preprocessing_dx_dy(data_frame):
    data_frame.dropna(inplace=True)
    data_frame.iloc[:, 1] = data_frame.iloc[:, 1].div(data_frame.iloc[0, 1])
# =============================================================================
# Labor Capital Intensity
# =============================================================================
    data_frame['lab_cap_int'] = data_frame.iloc[:, 0].div(
        data_frame.iloc[:, 1])
# =============================================================================
# Labor Productivity
# =============================================================================
    data_frame['lab_prod'] = data_frame.iloc[:, 2].div(data_frame.iloc[:, 1])
# =============================================================================
# Labor Capital Intensity Increment
# =============================================================================
    data_frame['lab_cap_int_diff'] = data_frame.iloc[:, -
                                                     2].div(data_frame.iloc[:, -2].shift(1))
# =============================================================================
# Labor Productivity Increment
# =============================================================================
    data_frame['lab_prod_diff'] = data_frame.iloc[:, -
                                                  2].div(data_frame.iloc[:, -2].shift(1))
    return data_frame.iloc[:, [3, 4, 5, 6]]


def preprocessing_dx_dy_service(data_frame):
    """
    data_frame.iloc[:, 0]: Capital Series;
    data_frame.iloc[:, 1]: Labor Series;
    data_frame.iloc[:, 2]: Product Series
    """
# =============================================================================
# Labor Capital Intensity
# =============================================================================
    data_frame['lab_cap_int'] = data_frame.iloc[:, 0].div(
        data_frame.iloc[:, 1])
# =============================================================================
# Labor Productivity
# =============================================================================
    data_frame['lab_prod'] = data_frame.iloc[:, 2].div(data_frame.iloc[:, 1])
# =============================================================================
# Labor Capital Intensity Increment
# =============================================================================
    data_frame['lab_cap_int_diff'] = data_frame.iloc[:, 3].div(
        data_frame.iloc[:, 3].shift(1))
# =============================================================================
# Labor Productivity Increment
# =============================================================================
    data_frame['lab_prod_diff'] = data_frame.iloc[:, 4].div(
        data_frame.iloc[:, 4].shift(1))
    return data_frame.iloc[:, [3, 4, 5, 6]]


def preprocessing_dx_dy(data_frame):
    '''
    data_frame.index: Period
    data_frame.iloc[:,0]: Capital
    data_frame.iloc[:,1]: Labor
    data_frame.iloc[:,2]: Product
    '''
    data_frame.iloc[:, 1] = data_frame.iloc[:, 1].div(data_frame.iloc[0, 1])
# =============================================================================
# Labor Capital Intensity
# =============================================================================
    data_frame['lab_cap_int'] = data_frame.iloc[:, 0].div(
        data_frame.iloc[:, 1])
# =============================================================================
# Labor Productivity
# =============================================================================
    data_frame['lab_prod'] = data_frame.iloc[:, 2].div(data_frame.iloc[:, 1])
# =============================================================================
# Labor Capital Intensity Increment
# =============================================================================
    data_frame['lab_cap_int_diff'] = data_frame.iloc[:, -
                                                     2].div(data_frame.iloc[:, -2].shift(1))
# =============================================================================
# Labor Productivity Increment
# =============================================================================
    data_frame['lab_prod_diff'] = data_frame.iloc[:, -
                                                  2].div(data_frame.iloc[:, -2].shift(1))
    return data_frame.dropna(axis=0)


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
prd_a_b=100*d*data_frame.loc[:, ['A032RC1']
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


def processing(data_frame, column_num):
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    interim_frame = data_frame.iloc[:, [column_num]]
    interim_frame = interim_frame.dropna()
    result_frame = price_inverse_single(interim_frame)
    result_frame = result_frame.dropna()
    return result_frame


def get_dataset_infcf():
    '''Retrieve Yearly Price Rates from `dataset_usa_infcf16652007.zip`'''
    file_name = 'dataset_usa_infcf16652007.zip'
    data_frame = pd.read_csv(file_name, usecols=range(4, 7))
    result_frame = pd.DataFrame()
# =============================================================================
# Retrieve First 14 Series
# =============================================================================
    for series_id in data_frame.iloc[:, 0].unique()[:14]:
        current_frame = data_frame[data_frame.iloc[:, 0]
                                   == series_id].iloc[:, [1, 2]]
        current_frame.columns=[current_frame.columns[0],
                                 series_id.replace(' ', '_').lower()]
        current_frame.set_index(current_frame.columns[0], inplace=True)
        current_frame = current_frame.rdiv(1)
        current_frame=-price_inverse_single(current_frame)
        result_frame = pd.concat(
            [result_frame, current_frame], axis=1, sort=True)
    result_frame['cpiu_fused'] = result_frame.mean(1)
    return result_frame.iloc[:, [-1]].dropna()


def get_dataset_version_c():
    """Data Fetch"""
# =============================================================================
# Data Fetch for Capital
# =============================================================================
    capital_frame_a = get_cobb_douglas_extension_capital()
# =============================================================================
# Data Fetch for Capital Deflator
# =============================================================================
    capital_frame_b = get_cobb_douglas_deflator()
    capital_frame = pd.concat(
        [capital_frame_a, capital_frame_b], axis=1, sort=True)
    capital_frame.dropna(inplace=True)
    capital_frame['capital_real'] = capital_frame.iloc[:, 0].div(
        capital_frame.iloc[:, 1])
# =============================================================================
# Data Fetch for Labor
# =============================================================================
    labor_frame = get_cobb_douglas_extension_labor()
# =============================================================================
# Data Fetch for Product
# =============================================================================
    product_frame = get_cobb_douglas_extension_product()
    result_frame = pd.concat(
        [capital_frame.iloc[:, 2], labor_frame, product_frame], axis=1, sort=True).dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame


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


source_frame = preprocessing_dx_dy_service(get_dataset_version_c())
plot_increment(source_frame)
