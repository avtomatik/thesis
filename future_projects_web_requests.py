##https://download.bls.gov/pub/time.series/cu/
## 9/13/2018  8:31 AM     38073676 cu.data.0.Current
## 9/13/2018  8:31 AM      2791094 cu.data.1.AllItems
## 9/13/2018  8:31 AM     10208894 cu.data.10.OtherWest
## 9/13/2018  8:31 AM      6361894 cu.data.11.USFoodBeverage
## 9/13/2018  8:31 AM      2542094 cu.data.12.USHousing
## 9/13/2018  8:31 AM      1388694 cu.data.13.USApparel
## 9/13/2018  8:31 AM      2138344 cu.data.14.USTransportation
## 9/13/2018  8:31 AM       949294 cu.data.15.USMedical
## 9/13/2018  8:31 AM      1247044 cu.data.16.USRecreation
## 9/13/2018  8:31 AM       762294 cu.data.17.USEducationAndCommunication
## 9/13/2018  8:31 AM       690994 cu.data.18.USOtherGoodsAndServices
## 9/13/2018  8:31 AM      1770694 cu.data.19.PopulationSize
## 9/13/2018  8:31 AM     11500144 cu.data.2.Summaries
## 9/13/2018  8:31 AM      3632544 cu.data.20.USCommoditiesServicesSpecial
## 9/13/2018  8:31 AM       824394 cu.data.3.AsizeNorthEast
## 9/13/2018  8:31 AM      3004744 cu.data.4.AsizeNorthCentral
## 9/13/2018  8:31 AM       562944 cu.data.5.AsizeSouth
## 9/13/2018  8:31 AM      2259044 cu.data.6.AsizeWest
## 9/13/2018  8:31 AM      8575094 cu.data.7.OtherNorthEast
## 9/13/2018  8:31 AM      9964697 cu.data.8.OtherNorthCentral
## 9/13/2018  8:31 AM     11327673 cu.data.9.OtherSouth
## 9/13/2018  8:46 AM           40 cu.footnote
## 9/13/2018  8:46 AM        16479 cu.item
## 2/25/1994  5:29 PM          323 cu.period
## 9/13/2018  8:46 AM           61 cu.periodicity
## 9/13/2018  8:31 AM      1367281 cu.series
import pandas as pd
import requests
from io import StringIO
url = 'https://download.bls.gov/pub/time.series/wp/wp.data.0.Current'
url = 'https://download.bls.gov/pub/time.series/pc/pc.data.0.Current'
url = 'https://download.bls.gov/pub/time.series/compressed/tape.format/bls.wp.date201807.gz'
url = 'https://download.bls.gov/pub/time.series/compressed/tape.format/bls.pc.date201807.gz'
url = 'https://www.bls.gov/opub/ted/2011/ted_20110224.htm'
url = 'https://thecode.media/einstein/'
url = 'https://www.rfbr.ru/rffi/ru/books/o_58886#213'
request = requests.get(url).text
print(request)
####for i in range(1):
####    file.retrieve(f[i], 'wp.data.0.Current')
source_frame = pd.read_csv(StringIO(request), compression = 'gzip',  header = 0,  sep = ' ',  quotechar = '"',  error_bad_lines = False)
print(source_frame)
source_frame.to_csv('dataset_USA_BLS_pc_data_0_Current.csv', index = False)