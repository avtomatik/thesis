# =============================================================================
# D:\archiveProjectUSACobbDouglasOptions.py
# =============================================================================
def preprocessing_dx_dy(start, stop, period, capital, labor, product):
    period = period[start:stop].reset_index(drop=True)
    capital = capital[start:stop].reset_index(drop=True)
    labor = labor[start:stop].reset_index(drop=True)
    product = product[start:stop].reset_index(drop=True)
    labor = labor/labor[0]
    X = capital.div(labor) # # Labor Capital Intensity
    Y = product.div(labor) # # Labor Productivity
    DX = X/X.shift(1) # # Labor Capital Intensity Increment
    DY = Y/Y.shift(1) # # Labor Productivity Increment
    return X, Y, DX, DY


def preprocessing_dx_dy_service(source_frame):
    """
    source_frame.iloc[:, 0]: Capital Series;
    source_frame.iloc[:, 1]: Labor Series;
    source_frame.iloc[:, 2]: Product Series
    """
    source_frame['labcap'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])                 # # Labor Capital Intensity
    source_frame['labprd'] = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1])                 # # Labor Productivity
    source_frame['labcap_inc'] = source_frame.iloc[:, 3].div(source_frame.iloc[:, 3].shift(1))    # # Labor Capital Intensity Increment
    source_frame['labprd_inc'] = source_frame.iloc[:, 4].div(source_frame.iloc[:, 4].shift(1))    # # Labor Productivity Increment
    source_frame = source_frame[source_frame.columns[[3, 4, 5, 6]]]
    return source_frame


def preprocessing_dx_dy(data_frame):
    '''
    data_frame.index: Period
    data_frame.iloc[:,0]: Capital
    data_frame.iloc[:,1]: Labor
    data_frame.iloc[:,2]: Product
    '''
    data_frame.iloc[:,1] = data_frame.iloc[:,1].div(data_frame.iloc[0,1])
# =============================================================================
# Labor Capital Intensity
# =============================================================================
    data_frame['lab_cap_int'] = data_frame.iloc[:,0].div(data_frame.iloc[:,1])
# =============================================================================
# Labor Productivity
# =============================================================================
    data_frame['lab_prod'] = data_frame.iloc[:,2].div(data_frame.iloc[:,1])
# =============================================================================
# Labor Capital Intensity Increment
# =============================================================================
    data_frame['lab_cap_int_diff'] = data_frame.iloc[:,-2].div(data_frame.iloc[:,-2].shift(1))
# =============================================================================
# Labor Productivity Increment
# =============================================================================
    data_frame['lab_prod_diff'] = data_frame.iloc[:,-2].div(data_frame.iloc[:,-2].shift(1))
    return data_frame.dropna(axis=0)


def procedure_a(x, y, dx, dy):
    '''Scenario I'''
    # # plt.figure(1)
    # # # # plt.plot(X, Y, '--', X, Y, '+') # Description Here
    # # # # plt.xlabel('Labor Capital Intensity') # # To Do: Add Annotations
    # # # # plt.ylabel('Labor Productivity') # # To Do: Add Annotations
    # # plt.plot(DX, DY, '--', DX, DY, '+') # Description Here
    # # plt.xlabel('Labor Capital Intensity Increment') # # To Do: Add Annotations
    # # plt.ylabel('Labor Productivity Increment') # # To Do: Add Annotations
    # # plt.show()
    '''Scenario II'''
    fig = plt.figure()
    # # plt.plot(X, Y, '--', X, Y, '+') # Description Here
    # # plt.xlabel('Labor Capital Intensity') # # To Do: Add Annotations
    # # plt.ylabel('Labor Productivity') # # To Do: Add Annotations
    plt.plot(DX, DY, '--', DX, DY, '+') # Description Here
    plt.xlabel('Labor Capital Intensity Increment') # # To Do: Add Annotations
    plt.ylabel('Labor Productivity Increment') # # To Do: Add Annotations
    ax = fig.add_subplot(111)
# #    for i in range(0, 90, 5):
# #        ax.annotate(period[i], (DX[i], DY[i]))
    plt.grid()
    # # result_frame = pd.concat([period, capital, labor, product, X, Y, DX, DY], axis=1, sort=False)
    # # result_frame.to_csv('dataset USA Cobb-Douglas Modern Dataset-Out.csv', index=False)
    plt.show()


def procedure_b(x, y, dx, dy):
    '''Scenario I'''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(X, Y)
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
# #    for i in range(4, 90, 5):
# #        ax.annotate(period[i], (X[i], Y[i]))
    plt.grid()
    plt.show()
    '''Scenario II'''
    # # plt.figure()
    # # plt.plot(X, Y, 'o', X, Y, '-')
    # # plt.xlabel('Labor Capital Intensity')
    # # plt.ylabel('Labor Productivity')
    # # plt.show()


# =============================================================================
# TODO: Revise Dataset
# =============================================================================
os.chdir('/media/alexander/321B-6A94')
data_frame = data_fetch_common_archived()
T = data_frame.iloc[:, 0]
d = data_frame.iloc[:, 8].div(data_frame.iloc[:, 7]) # # Deflator, 2009=100
C11 = data_frame.iloc[:, 4]*d # # Fixed Assets, K160491
C12 = data_frame.iloc[:, 2]*d # # Fixed Assets, k3n31gd1es000
C21 = data_frame.iloc[:, 1]*data_frame.iloc[:, 10]
C22 = data_frame.iloc[:, 1]*data_frame.iloc[:, 11].div(data_frame.iloc[:, 9])
C23 = data_frame.iloc[:, 2]*data_frame.iloc[:, 10]
C24 = data_frame.iloc[:, 2]*data_frame.iloc[:, 11].div(data_frame.iloc[:, 9])
L = data_frame.iloc[:, 5]
P11 = d*data_frame.iloc[:, 6] # # Production
P12 = 100*d*data_frame.iloc[:, 6].div(data_frame.iloc[:, 12]) # # Production Maximum
P21 = data_frame.iloc[:, 9]*data_frame.iloc[:, 10]
P22 = data_frame.iloc[:, 11]
P23 = data_frame.iloc[:, 13]*data_frame.iloc[:, 10]
P24 = data_frame.iloc[:, 13]*data_frame.iloc[:, 11].div(data_frame.iloc[:, 9])
# # '''Option 1'''
# # X1, X2, X3, X4 = preprocessing_dx_dy(42, 87, T, C11, L, P11)
# # '''Option 2'''
# # X1, X2, X3, X4 = preprocessing_dx_dy(42, 87, T, C11, L, P12)
# # '''Option 3'''
X1, X2, X3, X4 = preprocessing_dx_dy(42, 87, T, C12, L, P11)
# # '''Option 4'''
# # x1, x2, x3, x4 = preprocessing_dx_dy(42, 87, T, C12, L, P12)
# =============================================================================
# TODO: test `k1ntotl1si000`
# =============================================================================
# # '''Option 1'''
# # X1, X2, X3, X4 = preprocessing_dx_dy(4, 88, T, C21, L, P21)
# # '''Option 2'''
# # X1, X2, X3, X4 = preprocessing_dx_dy(4, 88, T, C22, L, P22)
# # '''Option 3'''
# # X1, X2, X3, X4 = preprocessing_dx_dy(4, 88, T, C21, L, P23)
# # '''Option 4'''
# # X1, X2, X3, X4 = preprocessing_dx_dy(4, 88, T, C22, L, P24)
# # '''Option 5'''
# # X1, X2, X3, X4 = preprocessing_dx_dy(4, 88, T, C23, L, P21)
# # '''Option 6'''
# # X1, X2, X3, X4 = preprocessing_dx_dy(4, 88, T, C24, L, P22)
# # '''Option 7'''
# # X1, X2, X3, X4 = preprocessing_dx_dy(4, 88, T, C23, L, P23)
# # '''Option 8'''
# # X1, X2, X3, X4 = preprocessing_dx_dy(4, 88, T, C24, L, P24)
procedure_a(x1, x2, x3, x4)
# # procedure_b(x1, x2, x3, x4)
"""Update from `project.py`"""


def prices_inverse_single(data_series):
    '''Intent: Returns Prices Icrement Series from Cumulative Deflator Series;
    source: pandas DataFrame'''
    return data_series.div(data_series.shift(1))-1


def processing(data_frame, col):
    interim_frame = data_frame[data_frame.columns[[col]]]
    interim_frame = interim_frame.dropna()
    result_frame = prices_inverse_single(interim_frame)
    result_frame = result_frame.dropna()
    return result_frame


def fetch_infcf():
    '''Retrieve Yearly Price Rates from `dataset_usa_infcf16652007.zip`'''
    os.chdir('/media/alexander/321B-6A94')
    file_name = 'dataset_usa_infcf16652007.zip'
    data_frame = pd.read_csv(file_name, usecols=range(4, 7))
    series_ids = data_frame.iloc[:, 0].unique().tolist()
    result_frame = pd.DataFrame()
# =============================================================================
#     Retrieve First 14 Series
# =============================================================================
    for series_id in series_ids[:14]:
        current_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:,[1, 2]]
        current_frame.columns = [current_frame.columns[0],
                                 series_id.replace(' ', '_').lower()]
        current_frame.set_index(current_frame.columns[0], inplace=True)
        current_frame = current_frame.rdiv(1)
        current_frame = -prices_inverse_single(current_frame)
        result_frame = pd.concat([result_frame, current_frame], axis=1, sort=True)
    result_frame['cpiu_fused'] = result_frame.mean(1)
    return result_frame.iloc[:,[-1]].dropna()


def get_dataset_version_c():
    """Data Fetch"""
    """Data Fetch for Capital"""
    capital_frame_a = cobb_douglas_extension_capital()
    """Data Fetch for Capital Deflator"""
    capital_frame_b = cobb_douglas_deflator()
    capital_frame = pd.concat([capital_frame_a, capital_frame_b], axis=1, sort=True)
    capital_frame.dropna(inplace=True)
    capital_frame['capital_real'] = capital_frame.iloc[:, 0].div(capital_frame.iloc[:, 1])
    """Data Fetch for Labor"""
    labor_frame = cobb_douglas_extension_labor()
    """Data Fetch for Product"""
    product_frame = cobb_douglas_extension_product()
    result_frame = pd.concat([capital_frame.iloc[:, 2], labor_frame, product_frame], axis=1, sort=True).dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame


def plot_increment(frame):
    fig, axs = plt.subplots(2, 1) # # fig, axs = plt.subplots()
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
#    fig.savefig('nameFigure1.pdf', format = 'pdf', dpi = 900)
    plt.show()
source_frame = preprocessing_dx_dy_service(get_dataset_version_c())
plot_increment(source_frame)
