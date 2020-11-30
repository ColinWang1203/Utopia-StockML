import requests, sys, sqlite3
import pandas as pd
from datetime import datetime
from datetime import timedelta
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

def check_seeds(seed_no):

    url='https://www.tdcc.com.tw/smWeb/QryStockAjax.do'

    end_date = datetime.today().strftime('%Y/%m/%d')
    start_date = (datetime.today() - timedelta(weeks=4)).strftime('%Y/%m/%d')
    dates = [d.strftime('%Y%m%d') for d in pd.date_range(start_date, end_date, freq='W-FRI')]

    print('Dates are : '+ str(dates))

    small_seeds_month = []
    big_seeds_month = []

    for date in dates:
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
            try :
                html=requests.post(url,data=payload).text
                print(html)
                if html is not None:
                    break
            except requests.exceptions.SSLError:
                print('Caught error in openssl, delay and try again')
                sleep(2)

        if html is None:
            print('Failed getting html after 10 tries')
            return 0

        data=Extractor(html,'table.mt:eq(1)').df(1)
        
        if data.iat[0,0] == '無此資料':
            print('Encounter error in seeds date')
            # break
            return 0

        # print(data)
        # get small seeds

        small_seeds = []
        for a in list(range(0,8)):
            small_seeds.append(float(data.iat[a,4]))
        
        small_seeds_month.append(sum(small_seeds))

        # get big seeds

        big_seeds_month.append(float(data.iat[14,4]))
        sleep(2)

    small_seeds_month_smaller_slope = True
    big_seeds_month_bigger_slope = True


    for i,k in list(zip(small_seeds_month, small_seeds_month[1:])):
        if k>i:
            small_seeds_month_smaller_slope = False

    for i,k in list(zip(big_seeds_month, big_seeds_month[1:])):
        if k<i:
            big_seeds_month_bigger_slope = False

    if big_seeds_month_bigger_slope and small_seeds_month_smaller_slope:
        print('Seeds condition match!')
        return 1

    return 0


# check_seeds(''.join(sys.argv[1:]))

# now try to find the region that meets the condition and see if it rise

Good_seeds = []

for table in sorted(sql_tables_Database_squeeze_name):
    table_str = ''.join(table).split('_')[1]
    if check_seeds(table_str):
        Good_seeds.append(table_str)
        print(table_str)
    sleep(2)

print(Good_seeds)