#-*- coding: utf-8 -*-
"""
Created on Mon Mar  9 12:13:55 2020

@author: Mastermind
"""


def fetch_usa_bea_filter(data_frame, series_id):
# =============================================================================
# Retrieve Yearly Data for BEA Series' Code
# =============================================================================
    data_frame = data_frame[data_frame.iloc[:, 14] == series_id]
    result_frame = pd.DataFrame()
    for source_id in data_frame.iloc[:, 0].unique().tolist():
        current_frame = data_frame[data_frame.iloc[:, 0] == source_id].iloc[:,[15, 17]]
        current_frame.columns = [current_frame.columns[0],
                                 '{}{}'.format(source_id.split()[1].replace('.', '_'), series_id),]
        current_frame.set_index(current_frame.columns[0], inplace=True)
        current_frame.drop_duplicates(inplace=True)
        result_frame = pd.concat([result_frame, current_frame], axis=1, sort=True)
    return result_frame


def fetch_brown():
# =============================================================================
# Fetch Data from `Reference RU Brown M. 0597_088.pdf`, Page 193
# Dependent on `fetch_classic`
# Out of Kendrick J.W. Data & Table 2. of `Reference RU Brown M. 0597_088.pdf`
# =============================================================================
    file_name = 'dataset_usa_brown.zip'
    data_frame = pd.read_csv(file_name, skiprows=4, usecols=range(3, 6))
    data_frame.rename(columns={'Данные по отработанным человеко-часам заимствованы из: Kendrick, op. cit., pp. 311-313, Table A. 10.':'series',
                        'Unnamed: 4':'period',
                        'Unnamed: 5':'value'}, inplace=True)
    series_ids = data_frame.iloc[:, 0].sort_values().unique()
    file_name = 'dataset_usa_brown.zip'
    semi_frame_a = fetch_classic(file_name, series_ids[0])
    file_name = 'dataset_usa_brown.zip'
    semi_frame_b = fetch_classic(file_name, series_ids[1])
    file_name = 'dataset_usa_brown.zip'
    semi_frame_c = fetch_classic(file_name, series_ids[2])
    file_name = 'dataset_usa_brown.zip'
    semi_frame_d = fetch_classic(file_name, series_ids[3])
    file_name = 'dataset_usa_brown.zip'
    semi_frame_e = fetch_classic(file_name, series_ids[4])
    file_name = 'dataset_usa_brown.zip'
    semi_frame_f = fetch_classic(file_name, series_ids[5])

    Brown_frame = pd.concat([semi_frame_a, semi_frame_f, semi_frame_c, semi_frame_d, semi_frame_e, semi_frame_b], axis=1, sort=True)
    Brown_frame.rename(columns={
                                'Валовой продукт (в млн. долл., 1929 г.)':'XAA', # # Gross Domestic Product, USD 1,000,000, 1929=100;
                                'Чистый основной капитал (в млн. долл., 1929 г.)':'XBB', # # Net Fixed Assets, USD 1,000,000, 1929=100;
                                'Используемый основной капитал (в млн. долл., 1929 г.)':'XCC', # # Utilized Fixed Assets, USD 1,000,000, 1929=100;
                                'Отработанные человеко-часы':'XDD', # # Actual Man-Hours Worked.
                                'Первая аппроксимация рядов загрузки мощностей, полученная с помощью метода Уортонской школы':'XEE',
                                'Вторая аппроксимация рядов загрузки мощностей, полученная с помощью итеративного процесса':'XFF'
                                }, inplace=True)

    file_name = 'dataset_usa_kendrick.zip'
    semi_frame_a = fetch_classic(file_name, 'KTA03S07')
    file_name = 'dataset_usa_kendrick.zip'
    semi_frame_b = fetch_classic(file_name, 'KTA03S08')
    file_name = 'dataset_usa_kendrick.zip'
    semi_frame_c = fetch_classic(file_name, 'KTA10S08')
    file_name = 'dataset_usa_kendrick.zip'
    semi_frame_d = fetch_classic(file_name, 'KTA15S07')
    file_name = 'dataset_usa_kendrick.zip'
    semi_frame_e = fetch_classic(file_name, 'KTA15S08')
    Kendrick_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e], axis=1, sort=True)
    semi_frame_a = Kendrick_frame[20:-2]
# =============================================================================
# Первая аппроксимация рядов загрузки мощностей, полученная с помощью метода Уортонской школы
# =============================================================================
    semi_frame_b = Brown_frame[Brown_frame.columns[[4]]][:-7]
# =============================================================================
# Brown M. Numbers Not Found in Kendrick J.W. For Years Starting From 1954 Inclusive
# =============================================================================
    semi_frame_c = Brown_frame[Brown_frame.columns[[0, 1, 2, 3]]][-7:]
    result_frame = pd.concat([semi_frame_a, semi_frame_b], axis=1, sort=True)
    result_frame = result_frame.assign(XAA = result_frame.iloc[:, 0]-result_frame.iloc[:, 1],
                                   XBB = result_frame.iloc[:, 3] + result_frame.iloc[:, 4],
                                   XCC = result_frame.iloc[:, 5]*(result_frame.iloc[:, 3].rolling(window=2).mean() + result_frame.iloc[:, 4].rolling(window=2).mean())/100,
                                   XDD = result_frame.iloc[:, 2])
    result_frame = result_frame[result_frame.columns[[6, 7, 8, 9]]]
    result_frame = result_frame.dropna()
    result_frame = result_frame.append(semi_frame_c)
    result_frame = result_frame.round()
    return result_frame


# =============================================================================
# Bureau of Economic Analysis
# =============================================================================
series_ids = ('A006RC1', 'A019RC1', 'A027RC1', 'A030RC1', 'A032RC1',
              'A051RC1', 'A052RC1', 'A054RC1', 'A061RC1', 'A065RC1',
              'A067RC1', 'A124RC1', 'A191RC1', 'A191RX1', 'A229RC0',
              'A229RX0', 'A262RC1', 'A390RC1', 'A392RC1', 'A399RC1',
              'A400RC1', 'A4601C0', 'A655RC1', 'A822RC1', 'A929RC1',
              'B057RC0', 'B230RC0', 'B394RC1', 'B645RC1', 'DPCERC1',
              'W055RC1', 'W056RC1',)
os.chdir('/media/alexander/321B-6A94')
file_name = 'dataset_usa_bea-nipa-2015-05-01.zip'
data_frame = pd.read_csv(file_name)
# =============================================================================
# Yearly Data
# =============================================================================
data_frame = data_frame[data_frame.iloc[:, 16] == 0]
for series_id in series_ids:
    result_frame = fetch_usa_bea_filter(data_frame, series_id)

# =============================================================================
# Bureau of Labor Statistics
# =============================================================================
# fetch_usa_bls_lnu('dataset USA BLS 2015-02-23 ln.data.1.AllData')
# fetch_usa_bls_lnu('dataset USA BLS 2017-07-06 ln.data.1.AllData')
# fetch_usa_bls_ppi('dataset USA BLS pc.data.0.Current')
# =============================================================================
# FN:Murray Brown
# ORG:University at Buffalo;Economics
# TITLE:Professor Emeritus, Retired
# EMAIL;PREF;INTERNET:mbrown@buffalo.edu
# =============================================================================
print(fetch_brown())

def save_zip(data_frame, file_name):
    data_frame.to_csv(f'{file_name}.csv', index=True, encoding='utf-8-sig')
    with zipfile.ZipFile(f'{file_name}.zip', 'w') as archive:
        archive.write(f'{file_name}.csv', compress_type=zipfile.ZIP_DEFLATED)
        os.unlink(f'{file_name}.csv')