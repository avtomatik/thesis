import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import zipfile


def fetch_from_url(url):
# =============================================================================
#     '''Downloading zip file from url'''
# =============================================================================
    r = requests.get(url)
    with open(url.split('/')[-1],  'wb') as s:
        s.write(r.content)
    with zipfile.ZipFile(url.split('/')[-1],  'r') as z:
        with z.open(url.split('/')[-1].replace('-eng.zip',  '.csv')) as f:
          data_frame = pd.read_csv(f)
    print('{}: Complete'.format(url))
    return data_frame


def fetch_cansim(source_frame,  vector,  index = True):
# =============================================================================
#     '''Data _frame Fetching from CANSIM Zip Archives
#     index ==True -- indexed by `period`;
#     index ==False -- not indexed by `period`'''
# =============================================================================
    source_frame = source_frame[source_frame.iloc[:,  10] ==  vector]
    source_frame = source_frame[source_frame.columns[[0,  12]]]
    source_frame.columns = ['period',  vector]
    source_frame.iloc[:,  1] = pd.to_numeric(source_frame.iloc[:,  1])
    source_frame.reset_index(drop = True,  inplace=True)
    if index:
        source_frame = source_frame.set_index('period')
        return source_frame
    else:
        return source_frame    


def fetch_cansim_q(source_frame,  vector,  index = True):
# =============================================================================
#     '''Data _frame Fetching from Quarterly Data within CANSIM Zip Archives
#     index ==  True -- indexed by `period`;
#     index ==  False -- not indexed by `period`'''
# =============================================================================
    source_frame = source_frame[source_frame.iloc[:,  10] ==  vector]
    source_frame = source_frame[source_frame.columns[[0,  12]]]
    source_frame[['period',  'Q']] = source_frame.iloc[:,  0].str.split('-', 
                                                                      n = 1,  expand = True)
    source_frame = source_frame[source_frame.columns[[2,  1]]]
    source_frame.iloc[:,  0] = source_frame.iloc[:,  0].astype(int)
    source_frame = source_frame.groupby('period').sum()
    source_frame.columns = [ vector ]
    if index:
        return source_frame
    else:
        source_frame.reset_index(level = 0,  inplace=True)
        return source_frame


def fetch_cansim_capital_series(source_frame):
# =============================================================================
#     '''Fetch `Series Sequence` from Statistics Canada. Table: 36-10-0238-01\
#     (formerly CANSIM 031-0004): Flows and stocks of fixed non-residential\
#     capital,  total all industries,  by asset,  provinces and territories,  annual\
#     (dollars x 1, 000, 000)'''
# =============================================================================
    query = (source_frame.iloc[:,  3].str.contains('2007 constant prices')) &\
            (source_frame.iloc[:,  5] ==  'Straight-line end-year net stock') &\
            (source_frame.iloc[:,  6].str.contains('Industrial'))
    source_frame = source_frame[ query ]
    source_frame = source_frame[source_frame.columns[[11]]]
    source_frame.drop_duplicates(inplace=True)
    series_list = source_frame.iloc[:,  0].values.tolist()
    return series_list


def fetch_cansim_capital(source_frame,  sequence):
# =============================================================================
#     '''Fetch `Series` from Statistics Canada. Table: 36-10-0238-01\
#     (formerly CANSIM 031-0004): Flows and stocks of fixed non-residential\
#     capital,  total all industries,  by asset,  provinces and territories,  annual\
#     (dollars x 1, 000, 000)'''
# =============================================================================
    source_frame = source_frame.loc[source_frame.iloc[:,  11].isin(sequence)]
    source_frame = source_frame[source_frame.columns[[11,  0,  13]]]
    vectors = source_frame.iloc[:,  0].unique()
    i = 0 ##Counter
    for vector in vectors:
        current_frame = source_frame[source_frame.iloc[:,  0] ==  vector]
        current_frame = current_frame[current_frame.columns[[1,  2]]]
        current_frame.iloc[:,  1] = current_frame.iloc[:,  1].astype(float)
        current_frame.columns = ['period',  vector]
        current_frame.drop_duplicates(inplace=True)
        current_frame = current_frame.reset_index(drop = True)
        current_frame = current_frame.set_index('period')
        if i ==  0:
            result_frame = current_frame
        elif i > =  1:
            result_frame = pd.concat([current_frame,  result_frame], 
                                      axis = 1,  sort = True)
        del current_frame
        i + =  1
    result_frame = result_frame.sum(axis = 1)
    return result_frame


def dataset_canada():
# =============================================================================
#     '''A. Fixed Assets Block: `Industrial buildings`,  `Industrial machinery`\
#     for `Newfoundland and Labrador`,  `Prince Edward Island`,  `Nova Scotia`, \
#     `New Brunswick`,  `Quebec`,  `Ontario`,  `Manitoba`,  `Saskatchewan`,  `Alberta`, \
#     `British Columbia`,  `Yukon`,  `Northwest Territories`,  `Nunavut`'''
#     '''2007 constant prices'''
#     '''Geometric (infinite) end-year net stock'''
#     '''Industrial buildings (x 1, 000, 000): `v43975603`,  `v43977683`,  `v43978099`, \
#     `v43978515`,  `v43978931`,  `v43979347`,  `v43979763`,  `v43980179`,  `v43980595`, \
#     `v43976019`,  `v43976435`,  `v43976851`,  `v43977267`'''
#     '''Industrial machinery (x 1, 000, 000): `v43975594`,  `v43977674`,  `v43978090`, \
#     `v43978506`,  `v43978922`,  `v43979338`,  `v43979754`,  `v43980170`,  `v43980586`, \
#     `v43976010`,  `v43976426`,  `v43976842`,  `v43977258`'''
#     '''Table: 36-10-0238-01 (formerly CANSIM 031-0004): Flows and stocks of\
#     fixed non-residential capital,  total all industries,  by asset,  provinces\
#     and territories,  annual (dollars x 1, 000, 000)'''
# =============================================================================
    capital = fetch_from_url('https://www150.statcan.gc.ca/n1/tbl/csv/36100238-eng.zip')
    capital = fetch_cansim_capital(capital,  fetch_cansim_capital_series(capital))
# =============================================================================
#     '''B. Labor Block: `v2523012`,  Preferred Over `v3437501` Which Is Quarterly'''
#     '''`v2523012` - Table: 14-10-0027-01 (formerly CANSIM 282-0012): Employment\
#     by class of worker,  annual (x 1, 000)'''
# =============================================================================
    labor = fetch_from_url('https://www150.statcan.gc.ca/n1/tbl/csv/14100027-eng.zip')
    labor = fetch_cansim(labor,  'v2523012')
# =============================================================================
#     '''C. Production Block: `v65201809`'''
#     '''`v65201809` - Table: 36-10-0434-01 (formerly CANSIM 379-0031): Gross\
#     domestic product (GDP) at basic prices,  by industry,  monthly (x 1, 000, 000)'''
# =============================================================================
    product = fetch_from_url('https://www150.statcan.gc.ca/n1/tbl/csv/36100434-eng.zip')
    product = fetch_cansim_q(product,  'v65201809')
    result_frame = pd.concat([capital,  labor,  product],  axis = 1,  sort = True)
    # result_frame = result_frame.dropna()
    result_frame.columns = ['capital',  'labor',  'product']
    # result_frame = result_frame.div(result_frame.iloc[0,  :])
    return result_frame


def cobb_douglas_canada(source_frame):
# =============================================================================
#     '''Cobb--Douglas Algorithm as per C.W. Cobb,  P.H. Douglas. A Theory of Production,  1928;
#     source_frame.index: Period, 
#     source_frame.iloc[:,  0]: Capital, 
#     source_frame.iloc[:,  1]: Labor, 
#     source_frame.iloc[:,  2]: Product
#     '''
# =============================================================================
    def pl(series,  k = 0.25,  b = 1.01):
        return b*series**(-k)
    
    
    def pc(series,  k = 0.25,  b = 1.01):
        return b*series**(1-k)
    
    
    function_dict = {'figure_a':'Chart I Progress in Manufacturing %d$-$%d (%d = 100)', 
                'figure_b':'Chart II Theoretical and Actual Curves of Production %d$-$%d (%d = 100)', 
                'figure_c':'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines = 3 Year Moving Average', 
                'figure_d':'Chart IV Percentage Deviations of Computed from Actual Product %d$-$%d', 
                'priceyear':2007}
    X = source_frame.iloc[:,  0].div(source_frame.iloc[:,  1])
    Y = source_frame.iloc[:,  2].div(source_frame.iloc[:,  1])
    from numpy.lib.scimath import log
    X = log(X)
    Y = log(Y)
    k,  b = np.polyfit(X,  Y,  1) ## Original: k = 0.25
    b = np.exp(b)
    source_frame['prod_comp'] = b*(source_frame.iloc[:,  0]**k)*(source_frame.iloc[:,  1]**(1-k))
    source_frame['prod_roll'] = source_frame.iloc[:,  2].rolling(window = 3,  center = True).mean()
    source_frame['prod_roll_comp'] = source_frame.iloc[:,  3].rolling(window = 3,  center = True).mean()
    source_frame['sub_prod'] = source_frame.iloc[:,  2].sub(source_frame.iloc[:,  4])
    source_frame['sub_comp'] = source_frame.iloc[:,  3].sub(source_frame.iloc[:,  5])
    source_frame['dev_prod'] = source_frame.iloc[:,  3].div(source_frame.iloc[:,  2])-1
    plt.figure(1)
    plt.semilogy(source_frame.iloc[:,  0],  label = 'Fixed Capital')
    plt.semilogy(source_frame.iloc[:,  1],  label = 'Labor Force')
    plt.semilogy(source_frame.iloc[:,  2],  label = 'Physical Product')
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(function_dict['figure_a'] %(source_frame.index[0], 
                                        source_frame.index[len(source_frame)-1], 
                                        function_dict['priceyear']))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.semilogy(source_frame.iloc[:,  2],  label = 'Actual Product')
    plt.semilogy(source_frame.iloc[:,  3],  label = 'Computed Product,  $P\' = %fL^{%f}C^{%f}$' %(b,  1-k,  k))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(function_dict['figure_b'] %(source_frame.index[0], 
                                        source_frame.index[len(source_frame)-1], 
                                        function_dict['priceyear']))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(source_frame.iloc[:,  6],  label = 'Deviations of $P$')
    plt.plot(source_frame.iloc[:,  7],  '--',  label = 'Deviations of $P\'$')
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(function_dict['figure_c'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(source_frame.iloc[:,  3].div(source_frame.iloc[:,  2])-1)
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(function_dict['figure_d'] %(source_frame.index[0], 
                                        source_frame.index[len(source_frame)-1]))
    plt.grid(True)
    plt.figure(5,  figsize = (5,  8))
    lc = np.arange(0.2,  1.0,  0.005)
    plt.scatter(source_frame.iloc[:,  1].div(source_frame.iloc[:,  0]), 
              source_frame.iloc[:,  2].div(source_frame.iloc[:,  1]))
    plt.scatter(source_frame.iloc[:,  1].div(source_frame.iloc[:,  0]), 
              source_frame.iloc[:,  2].div(source_frame.iloc[:,  0]))
    plt.plot(lc,  pl(lc,  k = k,  b = b),  label = '$\\frac{3}{4}\\frac{P}{L}$')
    plt.plot(lc,  pc(lc,  k = k,  b = b),  label = '$\\frac{1}{4}\\frac{P}{C}$')
    plt.xlabel('$\\frac{L}{C}$')
    plt.ylabel('Indexes')
    plt.title('Relative Final Productivities of Labor and Capital')
    plt.legend()
    plt.grid(True)
    plt.show()
    from sklearn.metrics import r2_score
    print(r2_score(source_frame.iloc[:,  2],  source_frame.iloc[:,  3]))
    print(np.absolute(source_frame.iloc[:,  3].sub(source_frame.iloc[:,  2]).div(source_frame.iloc[:,  2])).mean())

def cobb_douglas_3d(source_frame):
# =============================================================================
#     '''Cobb--Douglas 3D-Plotting
#     source_frame.index: Period, 
#     source_frame.iloc[:,  0]: Capital, 
#     source_frame.iloc[:,  1]: Labor, 
#     source_frame.iloc[:,  2]: Product
#     '''
# =============================================================================
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    ax.plot(source_frame.iloc[:,  0],  source_frame.iloc[:,  1],  source_frame.iloc[:,  2])
    ax.set_xlabel('Capital')
    ax.set_ylabel('Labor')
    ax.set_zlabel('Production')
    ax.view_init(30,  45)
    plt.show()


print(__doc__)
# result_frame = dataset_canada()
# result_frame.to_excel('result.xlsx')
# # cobb_douglas_canada(result_frame)
# # cobb_douglas_3d(result_frame)
# df = fetch_from_url('https://www150.statcan.gc.ca/n1/en/tbl/csv/36100210-eng.zip')
df = fetch_from_url('https://www150.statcan.gc.ca/n1/tbl/csv/18100081-eng.zip')
df.to_excel('another.xlsx')
