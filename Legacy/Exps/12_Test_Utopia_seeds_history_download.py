# customize the seeds_date.txt to fill in lost data for more than a week!

import requests, sys, sqlite3
import pandas as pd
from datetime import datetime
from datetime import timedelta
from time import sleep
from htmltable_df.extractor import Extractor
from Utopia_tools import *

Database_squeeze_name = 'DB_Avalon.sqlite'
sql_connection_Database_squeeze_name = sqlite3.connect(Database_squeeze_name)
sql_cursor_Database_squeeze_name = sql_connection_Database_squeeze_name.cursor()
sql_cursor_Database_squeeze_name.execute("SELECT name FROM sqlite_master WHERE type='table'")
sql_tables_Database_squeeze_name = sql_cursor_Database_squeeze_name.fetchall()

Database_seeds_name = 'DB_Seeds.sqlite'
# Z_delete(Database_seeds_name)
sql_connection_Database_seeds_name = sqlite3.connect(Database_seeds_name)
sql_cursor_Database_seeds_name = sql_connection_Database_seeds_name.cursor()

url='https://www.tdcc.com.tw/smWeb/QryStockAjax.do'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

# manually get the date by downloading html and get option values, store in seeds_date.txt
dates = Z_read_line('seeds_date.txt')
dates.sort()
# dates = dates[0:]

processed_seeds_f = 'Processed_seeds_apple_date.txt'
# Z_delete(processed_seeds_f)
Z_new_file(processed_seeds_f)

def check_seeds(seed_no):

    skip_seeds_count = 0
    for date in dates:
        # first check if it is already processed
        if date+'_'+seed_no in Z_read_line(processed_seeds_f):
            print(date+'_'+seed_no+' already processed')
            continue

        # if skip seeds count reach continuesly 5 weeks no data, skip the rest
        if skip_seeds_count > 5:
            for date in dates:
                Z_write_line(date+'_'+seed_no, processed_seeds_f)
            break

        print('sleep starts')
        sleep(1)
        print('sleep ends')
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
                html=requests.post(url,data=payload,headers=headers,timeout=5).text
                if html is not None:
                    break
            except :
                print('Caught error in openssl, delay and try again')
                sleep(2)

        if html is None:
            print('Failed getting html after 10 tries')
            return -1

        data=Extractor(html,'table.mt:eq(1)').df(1)
        
        if data.iat[0,0] == '無此資料':
            # sometimes failed to get data but it actually exist, so try again one more
            print('Try saving data...')
            # input()
            sleep(5)
            for i in list(range(5)):
                try :
                    if i == 4:
                        print('ip is blocked')
                        C()
                    html=requests.post(url,data=payload,headers=headers,timeout=5).text
                    if html is not None:
                        break
                except :
                    print('Caught error in openssl, delay and try again')
                    sleep(2)
            data=Extractor(html,'table.mt:eq(1)').df(1)
            if data.iat[0,0] == '無此資料':
                print('Encounter error in seeds date')
                # record the processed date_apple
                Z_write_line(date+'_'+seed_no, processed_seeds_f)
                skip_seeds_count += 1
                continue
            print('Data is saved!')

        df_row_list = data['占集保庫存數比例 (%)'][0:15].values.tolist()
        # insert the date at the front
        df_row_list.insert(0,date)

        sql_create_cmd = 'CREATE TABLE IF NOT EXISTS apple_'+seed_no+' (date INT UNIQUE,\
                    n1 FLOAT, n2 FLOAT, n3 FLOAT, n4 FLOAT, n5 FLOAT, \
                    n6 FLOAT, n7 FLOAT, n8 FLOAT, n9 FLOAT, n10 FLOAT, \
                    n11 FLOAT, n12 FLOAT, n13 FLOAT, n14 FLOAT, n15 FLOAT)'
        sql_cursor_Database_seeds_name.execute(sql_create_cmd)
        sql_write_cmd = 'INSERT OR IGNORE INTO apple_'+seed_no+' (date\
                , n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15) values\
                ("'+str(df_row_list[0])+'","'+str(df_row_list[1])+'",\
                 "'+str(df_row_list[2])+'","'+str(df_row_list[3])+'",\
                 "'+str(df_row_list[4])+'","'+str(df_row_list[5])+'",\
                 "'+str(df_row_list[6])+'","'+str(df_row_list[7])+'",\
                 "'+str(df_row_list[8])+'","'+str(df_row_list[9])+'",\
                 "'+str(df_row_list[10])+'","'+str(df_row_list[11])+'",\
                 "'+str(df_row_list[12])+'","'+str(df_row_list[13])+'",\
                 "'+str(df_row_list[14])+'","'+str(df_row_list[15])+'")'
        sql_cursor_Database_seeds_name.execute(sql_write_cmd)
        sql_connection_Database_seeds_name.commit()

        # record the processed date_apple
        Z_write_line(date+'_'+seed_no, processed_seeds_f)
        
    return 0


for table in sorted(sql_tables_Database_squeeze_name):
    table_str = ''.join(table).split('_')[1]
    print('table is '+table_str)
    if check_seeds(table_str):
        print('Error occurred, aborting...')
        break

# record the processed apple number
# detect key q and stop for completeing a whole loop
