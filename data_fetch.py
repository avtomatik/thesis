# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 12:13:55 2020

@author: Mastermind
"""


def fetch_usa_bea_filter(series_id):
    # =============================================================================
    # Retrieve Yearly Data for BEA Series' Code
    # =============================================================================
    archive_name='dataset_usa_bea-nipa-2015-05-01.zip'
    data_frame = pd.read_csv(archive_name, usecols=[0, *range(14, 18)])
    query = (data_frame.iloc[:, 1] == series_id) & \
            (data_frame.iloc[:, 3] == 0)
    data_frame = data_frame[query]
    result_frame = pd.DataFrame()
    for source_id in data_frame.iloc[:, 0].unique():
        current_frame = data_frame[data_frame.iloc[:, 0]
                                   == source_id].iloc[:, [2, 4]]
        current_frame.columns=[current_frame.columns[0],
                                 '{}{}'.format(source_id.split()[1].replace('.', '_'), series_id)]
        current_frame.set_index(
            current_frame.columns[0], inplace=True, verify_integrity=True)
    return pd.concat([result_frame, current_frame], axis=1, sort=True)


def get_dataset_brown():
    # =============================================================================
    # Fetch Data from `Reference RU Brown M. 0597_088.pdf`, Page 193
    # Dependent on `fetch_classic`
    # Out of Kendrick J.W. Data & Table 2. of `Reference RU Brown M. 0597_088.pdf`
    # =============================================================================
    FILE_NAMES = ('dataset_usa_brown.zip', 'dataset_usa_kendrick.zip',)
    data_frame = pd.read_csv(FILE_NAMES[0], skiprows=4, usecols=range(3, 6))
    data_frame.columns=['series_id', 'period', 'value']
    _b_frame = pd.concat(
        [fetch_classic(FILE_NAMES[0], series_id)
         for series_id in data_frame.iloc[:, 0].unique()],
        axis=1,
        sort=True)
    _b_frame.columns=['series_{}'.format(
        hex(i)) for i, column in enumerate(_b_frame.columns)]
# =============================================================================
# Валовой продукт (в млн. долл., 1929 г.)
# Чистый основной капитал (в млн. долл., 1929 г.)
# Используемый основной капитал (в млн. долл., 1929 г.)
# Отработанные человеко-часы
# Первая аппроксимация рядов загрузки мощностей, полученная с помощью метода Уортонской школы
# Вторая аппроксимация рядов загрузки мощностей, полученная с помощью итеративного процесса
# =============================================================================
# =============================================================================
# Gross Domestic Product, USD 1,000,000, 1929=100
# Net Fixed Assets, USD 1,000,000, 1929=100
# Utilized Fixed Assets, USD 1,000,000, 1929=100
# Actual Man-Hours Worked
# _
# _
# =============================================================================
    SERIES_IDS = ('KTA03S07', 'KTA03S08', 'KTA10S08', 'KTA15S07', 'KTA15S08',)
    _k_frame = pd.concat(
        [fetch_classic(FILE_NAMES[1], series_id) for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    result_frame = pd.concat(
        [_k_frame[_k_frame.index.get_loc(1889):2+_k_frame.index.get_loc(1952)],
         # =============================================================================
         # Первая аппроксимация рядов загрузки мощностей, полученная с помощью метода Уортонской школы
         # =============================================================================
         _b_frame.iloc[:1+_b_frame.index.get_loc(1953), [4]]],
        axis=1,
        sort=True)
    result_frame = result_frame.assign(
        series_0x0=result_frame.iloc[:, 0].sub(result_frame.iloc[:, 1]),
        series_0x1=result_frame.iloc[:, 3].add(result_frame.iloc[:, 4]),
        series_0x2=result_frame.iloc[:, [3, 4]].sum(axis=1).rolling(
            window=2).mean().mul(result_frame.iloc[:, 5]).div(100),
        series_0x3=result_frame.iloc[:, 2],
    )
    result_frame = result_frame.iloc[:, [6, 7, 8, 9]].dropna()
    return pd.concat(
        [result_frame,
         # =============================================================================
         # Brown M. Numbers Not Found in Kendrick J.W. For Years Starting From 1954 Inclusive
         # =============================================================================
         _b_frame.iloc[1+_b_frame.index.get_loc(1953):, [0, 1, 2, 3]]]
    ).round()


# =============================================================================
# Bureau of Economic Analysis
# =============================================================================
SERIES_IDS = ('A006RC1', 'A019RC1', 'A027RC1', 'A030RC1', 'A032RC1',
              'A051RC1', 'A052RC1', 'A054RC1', 'A061RC1', 'A065RC1',
              'A067RC1', 'A124RC1', 'A191RC1', 'A191RX1', 'A229RC0',
              'A229RX0', 'A262RC1', 'A390RC1', 'A392RC1', 'A399RC1',
              'A400RC1', 'A4601C0', 'A655RC1', 'A822RC1', 'A929RC1',
              'B057RC0', 'B230RC0', 'B394RC1', 'B645RC1', 'DPCERC1',
              'W055RC1', 'W056RC1',)
os.chdir('/media/alexander/321B-6A94')
# =============================================================================
# Yearly Data
# =============================================================================
for series_id in SERIES_IDS:
    result_frame = fetch_usa_bea_filter(series_id)

# =============================================================================
# Bureau of Labor Statistics
# =============================================================================
# fetch_usa_bls('dataset_usa_bls-2015-02-23-ln.data.1.AllData', 'LNU04000000')
# fetch_usa_bls('dataset_usa_bls-2017-07-06-ln.data.1.AllData', 'LNU04000000')
# fetch_usa_bls('dataset_usa_bls-pc.data.0.Current', 'PCUOMFG--OMFG')
# =============================================================================
# FN:Murray Brown
# ORG:University at Buffalo;Economics
# TITLE:Professor Emeritus, Retired
# EMAIL;PREF;INTERNET:mbrown@buffalo.edu
# =============================================================================
print(get_dataset_brown())


def save_zip(data_frame, file_name):
    data_frame.to_csv(f'{file_name}.csv', index=True, encoding='utf-8-sig')
    with zipfile.ZipFile(f'{file_name}.zip', 'w') as archive:
        archive.write(f'{file_name}.csv', compress_type=zipfile.ZIP_DEFLATED)
        os.unlink(f'{file_name}.csv')
