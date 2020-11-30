
# 1. download csv
# 2. get date in csv
# 3. compare processed list
# 4. parse the csv data into db or not
# 5. add processed list
# format : date  1 2 ... 15

import requests, sys, sqlite3
import pandas as pd
from datetime import datetime, timedelta, date
from time import sleep
from Utopia_tools import *
from htmltable_df.extractor import Extractor

Database_squeeze_name = 'DB_Avalon.sqlite'
sql_connection_Database_squeeze_name = sqlite3.connect(Database_squeeze_name)
sql_cursor_Database_squeeze_name = sql_connection_Database_squeeze_name.cursor()
sql_cursor_Database_squeeze_name.execute("SELECT name FROM sqlite_master WHERE type='table'")
sql_tables_Database_squeeze_name = sql_cursor_Database_squeeze_name.fetchall()

Database_seeds_name = 'DB_Seeds.sqlite'
sql_connection_Database_seeds_name = sqlite3.connect(Database_seeds_name)
sql_cursor_Database_seeds_name = sql_connection_Database_seeds_name.cursor()

# get the lastest date in processed date and check until today
with open('Processed_date_seeds_list.txt') as f:
    lines = f.read().splitlines()
    start_date = lines[-1]

end_date = datetime.today().strftime('%Y/%m/%d')

d1 = date(int(start_date.split('/')[0]),int(start_date.split('/')[1]),int(start_date.split('/')[2]))
d2 = date(int(end_date.split('/')[0]),int(end_date.split('/')[1]),int(end_date.split('/')[2]))

all_dates = []
for i in range(1,(d2-d1).days + 1):
    day = d1 + timedelta(days=i)
    all_dates.append(day.strftime('%Y%m%d'))

def check_seeds(seed_no, date):

    url='https://www.tdcc.com.tw/smWeb/QryStockAjax.do'

    # prevent excessive access
    sleep(2)

    payload={
        'scaDates': date,
        'scaDate':date,
        'SqlMethod':'StockNo',
        'StockNo':seed_no,
        'radioStockNo':seed_no,
        'StockName':'',
        'REQ_OPR':'SELECT',
        'clkStockNo':seed_no,
        'clkStockName':''
    }

    for i in list(range(10)):
        try:
            html=requests.post(url,data=payload).text
            if html is not None:
                break
        except:
            print('Caught error in openssl, delay and try again...')
            sleep(2)

    if html is None:
        print('Failed getting html after 10 tries')
        return 0
    
    data=Extractor(html,'table.mt:eq(1)').df(1)
    
    if data.iat[0,0] == '無此資料':
        print('Ignoring seeds date : '+date)
        # break
        return 0

    return 1

date_need_process_list = []
for date in all_dates:
    # use 2330 to test
    if check_seeds('2330', date):
        date_need_process_list.append(date)

print(date_need_process_list)



