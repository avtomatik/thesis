# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 21:22:23 2021

@author: Mastermind
"""


def convert_url(string):
    return '/'.join(('https://www150.statcan.gc.ca/n1/tbl/csv', '{}-eng.zip'.format(string.split('=')[1][:-2])))


def extract_can_from_url(url: str, usecols: list = None) -> pd.DataFrame:
    '''Downloading zip file from url'''
    name = url.split('/')[-1]
    if os.path.exists(name):
        with ZipFile(name, 'r').open(name.replace('-eng.zip', '.csv')) as f:
            return pd.read_csv(f, usecols=usecols)
    else:
        r = requests.get(url)
        with ZipFile(io.BytesIO(r.content)).open(name.replace('-eng.zip', '.csv')) as f:
            return pd.read_csv(f, usecols=usecols)


os.chdir('/media/alexander/321B-6A94')
file_name = '/home/alexander/projects/stat_can_selected.xlsx'
df = pd.read_excel(file_name)
# urls = set()
# for i in range(df.shape[0]):
#     try:
#         urls.add(convert_url(df.iloc[i, 8]))
#     except:
#         pass


# filedict = {url.split('/')[-1]: url for url in urls}


# downloaded = set()
# for file_name in os.listdir():
#     if file_name.endswith(('-eng.zip')):
#         downloaded.add(file_name)


# difference = set(filedict.keys()) - downloaded


# urls = []
# for file_name in difference:
#     urls.append(filedict[file_name])


# with open('output_b.txt', 'w') as f:
#     for url in sorted(urls):
#         data = fetch_from_url(url)
#         print(url, file = f)
#         print('Periods Length {}'.format(len(data['REF_DATE'].unique())), file = f)
#         print(data['REF_DATE'].unique(), file = f)
# # # # urls = sorted(list(urls))
# # # # with open('output.txt', 'w') as f:
# # # #     for url in urls:
# # # #         data = fetch_from_url(url)
# # # #         print(url, file = f)
# # # #         print('Periods Length {}'.format(len(data['REF_DATE'].unique())), file = f)
# # # #         print(data['REF_DATE'].unique(), file = f)
# # # # # df.dropna(how='all', inplace=True)
# # # # # df.to_excel('/home/alexander/projects/stat_can_selected.xlsx', index=False)
