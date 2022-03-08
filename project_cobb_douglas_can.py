'''First Figure: Exact Correspondence with `Note INTH05 2014-07-10.docx`'''
def fetchCANSIMFA(sequence):
    '''Fetch `Series Sequence` from CANSIM Table 031-0004: Flows and stocks of fixed non-residential capital,  total all industries,  by asset,  provinces\
    and territories,  annual (dollars x 1, 000, 000)'''
    source_frame = pd.read_csv('dataset CAN 00310004-eng.zip')
    source_frame = source_frame.loc[source_frame['Vector'].isin(sequence)]
    source_frame = source_frame[source_frame.iloc[:, 8]! = '..']
    source_frame = source_frame[source_frame.columns[[6, 0, 8]]]
    tables = source_frame.iloc[:, 0].unique()
    tables = pd.Series(tables)
    i = 0 ##Counter
    for table in tables:
        current_frame = source_frame[source_frame.iloc[:, 0] == table]
        current_frame = current_frame[current_frame.columns[[1, 2]]]
        current_frame.iloc[:, 1] = current_frame.iloc[:, 1].astype(float)
        current_frame.rename(columns = {'Ref_Date':'Period', 'Value':table}, inplace=True)
        current_frame = current_frame.drop_duplicates()
        current_frame = current_frame.reset_index(drop = True)
        current_frame = current_frame.set_index('Period')
        if i == 0:
            result_frame = current_frame
        elif i> = 1:
            result_frame = pd.concat([current_frame, result_frame], axis = 1, sort = True)
        del current_frame
        i+ = 1
    result_frame = result_frame.sum(axis = 1)
    return result_frame
def fetchCANSIMSeries():
    '''Fetch `Series Sequence` from CANSIM Table 031-0004: Flows and stocks of fixed non-residential capital,  total all industries,  by asset, \
    provinces and territories,  annual (dollars x 1, 000, 000)'''
    source_frame = pd.read_csv('dataset CAN 00310004-eng.zip')
    source_frame = source_frame[source_frame.iloc[:, 2].str.contains('2007 constant prices')]
    source_frame = source_frame[source_frame.iloc[:, 4] == 'Geometric (infinite) end-year net stock']
    source_frame = source_frame[source_frame.iloc[:, 5].str.contains('Industrial')]
    source_frame = source_frame[source_frame.columns[[6]]]
    source_frame = source_frame.drop_duplicates()
    slist = source_frame.iloc[:, 0].values.tolist()
    return slist
def fetchCANSIM(source, vector, index):
    '''Data _frame Fetching from CANSIM Zip Archives
    Should Be [x 7 columns]
    index == True -- indexed by `Period`;
    index == False -- not indexed by `Period`'''
    source_frame = pd.read_csv('dataset CAN {}-eng.zip'.format(source))
    source_frame = source_frame[source_frame.Vector == vector]
    if source == '03800106':
        source_frame = source_frame[source_frame.columns[[0, 5]]]
    elif source == '03800566':
        source_frame = source_frame[source_frame.columns[[0, 5]]]
    elif source == '02820011':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '02820012':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '03790031':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '03800068':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    else:
        source_frame = source_frame[source_frame.columns[[0, 6]]] ##Should Be [x 7 columns]
    source_frame.rename(columns = {'Ref_Date':'Period', 'Value':vector}, inplace=True)
    source_frame.iloc[:, 1] = pd.to_numeric(source_frame.iloc[:, 1])
    source_frame.to_csv('dataset CAN {} {}.csv'.format(source, vector), index = False)
    if index:
        source_frame = source_frame.set_index('Period')
        os.unlink('dataset CAN {} {}.csv'.format(source, vector))
        return source_frame
    else:
        del source_frame
        result_frame = pd.read_csv('dataset CAN {} {}.csv'.format(source, vector))
        os.unlink('dataset CAN {} {}.csv'.format(source, vector))
        return result_frame
def fetchCANSIMQ(source, vector, index):
    '''Data _frame Fetching from Quarterly Data within CANSIM Zip Archives
    Should Be [x 7 columns]
    index == True -- indexed by `Period`;
    index == False -- not indexed by `Period`'''
    source_frame = pd.read_csv('dataset CAN {}-eng.zip'.format(source))
    source_frame = source_frame[source_frame.Vector == vector]
    if source == '02820011':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '02820012':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '03790031':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '03800068':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    else:
        source_frame = source_frame[source_frame.columns[[0, 6]]] ##Should Be [x 7 columns]
    source_frame.rename(columns = {'Value':vector}, inplace=True)
    source_frame['Period'], source_frame['Q'] = source_frame.iloc[:, 0].str.split('/').str
    source_frame = source_frame[source_frame.columns[[2, 1]]]
    source_frame.iloc[:, 0] = source_frame.iloc[:, 0].astype(int)
    source_frame.iloc[:, 1] = pd.to_numeric(source_frame.iloc[:, 1])
    if (source == '03800084' and vector == 'v62306938'):
        source_frame = source_frame.groupby('Period').sum()
    elif (source == '03790031' and vector == 'v65201536'):
        source_frame = source_frame.groupby('Period').mean()
    elif (source == '03790031' and vector == 'v65201809'):
        source_frame = source_frame.groupby('Period').sum()
    else:
        source_frame = source_frame.groupby('Period').mean()
    if index:
        return source_frame
    else:
        source_frame.to_csv('temporary.txt')
        del source_frame
        result_frame = pd.read_csv('temporary.txt')
        os.unlink('temporary.txt')
        return result_frame
def datasetCanada():
    '''A. Fixed Assets Block: `Industrial buildings`, `Industrial machinery` for `Newfoundland and Labrador`, `Prince Edward Island`, `Nova Scotia`, `New Brunswick`, \
    `Quebec`, `Ontario`, `Manitoba`, `Saskatchewan`, `Alberta`, `British Columbia`, `Yukon`, `Northwest Territories`, `Nunavut`'''
    '''2007 constant prices'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1, 000, 000): `v43975603`, `v43977683`, `v43978099`, `v43978515`, `v43978931`, `v43979347`, `v43979763`, `v43980179`, `v43980595`, \
    `v43976019`, `v43976435`, `v43976851`, `v43977267`'''
    '''Industrial machinery (x 1, 000, 000): `v43975594`, `v43977674`, `v43978090`, `v43978506`, `v43978922`, `v43979338`, `v43979754`, `v43980170`, `v43980586`, \
    `v43976010`, `v43976426`, `v43976842`, `v43977258`'''
    capital = fetchCANSIMFA(fetchCANSIMSeries())
    '''B. Labor Block: `v2523012`,  Preferred Over `v3437501` Which Is Quarterly'''
    '''`v2523012` - 282-0012 Labour Force Survey Estimates (LFS),  employment by class of worker,  North American Industry Classification System (NAICS)\
    and sex; Canada; Total employed,  all class of workers; Manufacturing; Both sexes (x 1, 000) (annual,  1987 to 2017)'''
    labor = fetchCANSIM('02820012', 'v2523012', True)
    '''C. Production Block: `v65201809`'''
    '''`v65201809` - 379-0031 Gross domestic product (GDP) at basic prices,  by North American Industry Classification System (NAICS); Canada; Trading-day\
    adjusted; 2007 constant prices; Manufacturing (x 1, 000, 000) (monthly,  1997-01-01 to 2017-10-01)'''
    product = fetchCANSIMQ('03790031', 'v65201809', True)
    result_frame = pd.concat([capital, labor, product], axis = 1, sort = True)
    result_frame = result_frame.dropna()
    result_frame.rename(columns = {0:'capital', 'v2523012':'labor', 'v65201809':'product'}, inplace=True)
    return result_frame
def cd_canada(frame):
    '''Cobb--Douglas Algorithm as per C.W. Cobb,  P.H. Douglas. A Theory of Production,  1928;
    frame.index: Period, 
    frame.iloc[:, 0]: Capital, 
    frame.iloc[:, 1]: Labor, 
    frame.iloc[:, 2]: Product
    '''
    functionDict = {'FigureA':'Chart I Progress in Manufacturing %d$-$%d (%d = 100)', 
                'FigureB':'Chart II Theoretical and Actual Curves of Production %d$-$%d (%d = 100)', 
                'FigureC':'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines = 3 Year Moving Average', 
                'FigureD':'Chart IV Percentage Deviations of Computed from Actual Product %d$-$%d', 
                'priceyear':2007}
    X = frame.iloc[:, 0].div(frame.iloc[:, 1])
    Y = frame.iloc[:, 2].div(frame.iloc[:, 1])
    import scipy as sp
    X = sp.log(X)
    Y = sp.log(Y)
    f1p = sp.polyfit(X, Y, 1)
    a1, a0 = f1p ##Original: a1 = 0.25
    a0 = sp.exp(a0)
    PP = a0*(frame.iloc[:, 1]**(1-a1))*(frame.iloc[:, 0]**a1)
    PR = frame.iloc[:, 2].rolling(window = 3, center = True).mean()
    PPR = PP.rolling(window = 3, center = True).mean()
    plt.figure(1)
    plt.plot(frame.index, frame.iloc[:, 0], label = 'Fixed Capital')
    plt.plot(frame.index, frame.iloc[:, 1], label = 'Labor Force')
    plt.plot(frame.index, frame.iloc[:, 2], label = 'Physical Product')
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(functionDict['FigureA'] %(frame.index[0], frame.index[len(frame)-1], functionDict['priceyear']))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(frame.index, frame.iloc[:, 2], label = 'Actual Product')
    plt.plot(frame.index, PP, label = 'Computed Product,  $P\' = %fL^{%f}C^{%f}$' %(a0, 1-a1, a1))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(functionDict['FigureB'] %(frame.index[0], frame.index[len(frame)-1], functionDict['priceyear']))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(frame.index, frame.iloc[:, 2]-PR, label = 'Deviations of $P$')
    plt.plot(frame.index, PP-PPR, '--', label = 'Deviations of $P\'$')
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(functionDict['FigureC'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(frame.index, PP.div(frame.iloc[:, 2])-1)
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(functionDict['FigureD'] %(frame.index[0], frame.index[len(frame)-1]))
    plt.grid(True)
    plt.show()
def cobbDouglas3D(source_frame):
    '''Cobb--Douglas 3D-Plotting
    source_frame.index: Period, 
    source_frame.iloc[:, 0]: Capital, 
    source_frame.iloc[:, 1]: Labor, 
    source_frame.iloc[:, 2]: Product
    '''
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    ax.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 1], source_frame.iloc[:, 2])
    ax.set_xlabel('Capital')
    ax.set_ylabel('Labor')
    ax.set_zlabel('Production')
    plt.show()
print(__doc__)
import os
import pandas as pd
import matplotlib.pyplot as plt
source_frame = datasetCanada()
cd_canada(source_frame)
cobbDouglas3D(source_frame)