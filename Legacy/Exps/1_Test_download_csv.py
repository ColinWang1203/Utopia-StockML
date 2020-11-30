import urllib.request
from datetime import date

today = date.today().strftime("%Y%m%d")

_url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date='+today+'&type=ALLBUT0999'

csv_file_name = date.today().strftime("%Y%m%d")+'.csv'

urllib.request.urlretrieve(_url, csv_file_name)
