# =============================================================================
# D:\archiveProjectUSACobbDouglasOptions.py
# =============================================================================


from extract.lib import get_data_version_c
from extract.lib import get_data_usa_sahr_infcf
from toolkit.lib import strip_cumulated_deflator
from toolkit.lib import price_inverse_single
from plot.lib import plot_increment


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
plot_increment(x_a, x_b, x_c, x_d)
# # procedure_b(x_a, x_b, x_c, x_d)
"""Update from `project.py`"""


source_frame = preprocessing_dx_dy_service(get_dataset_version_c())
plot_increment(source_frame)
