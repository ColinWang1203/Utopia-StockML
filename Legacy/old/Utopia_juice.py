# python Utopia_juice.py
# rule X% by year, 500, 3 years up, latest greater than second(not enabled now)
# produce the best_juices.txt in Figs
from Utopia_tools import *

import pandas, sqlite3, requests, calendar, os, urllib.request, sys
import numpy as np
from dateutil import rrule, relativedelta
from datetime import date, datetime
from argparse import ArgumentParser, RawTextHelpFormatter
from time import sleep
from io import StringIO
from subprocess import call,check_output


# ===== Global vars =====

Thresh_increase = 20 #increase X% by second highest year
parse_adb = True

today = datetime.today().strftime("%Y%m%d")

# Databases
Database_squeeze_name = 'DB_Avalon.sqlite'
sql_connection_Database_squeeze_name = sqlite3.connect(Database_squeeze_name)
sql_cursor_Database_squeeze_name = sql_connection_Database_squeeze_name.cursor()
Database_juice_name = 'DB_Juice.sqlite'
sql_connection_Database_juice_name = sqlite3.connect(Database_juice_name)
sql_cursor_Database_juice_name = sql_connection_Database_juice_name.cursor()

Fig_dir = 'Figs'

# =======================

def get_max_juice():
    best_juice = []
    # Get the tables
    sql_cursor_Database_juice_name.execute("SELECT name FROM sqlite_master WHERE type='table'")
    sql_tables_Database_juice_name = sql_cursor_Database_juice_name.fetchall()
    
    # Get date for an year
    with open('Processed_juice_date_list.txt') as f:
        content = f.read().splitlines()

    Year_juice_date = []
    # list of year, max to 10 year
    for i in list(range(0,10)):
        if i == 0:
            Year_juice_date.append(content[-12:])
        else:
            Year_juice_date.append(content[-(12+(12*i)):-(12*i)])

    Year_juice_date.reverse()
    '''
    [['201001', '201002', '201003', '201004', '201005', '201006', '201007', '201008', '201009', '201010', '201011', '201012'],
     ['201101', '201102', '201103', '201104', '201105', '201106', '201107', '201108', '201109', '201110', '201111', '201112'],
     ['201201', '201202', '201203', '201204', '201205', '201206', '201207', '201208', '201209', '201210', '201211', '201212'],
     ['201301', '201302', '201303', '201304', '201305', '201306', '201307', '201308', '201309', '201310', '201311', '201312'],
     ...
     ['201901', '201902', '201903', '201904', '201905', '201906', '201907', '201908', '201909', '201910', '201911', '201912']]
    '''

    best_juice = []
    with open('Processed_date_list.txt') as f:
        content_apple = f.read().splitlines()
    latest_date = content_apple[-1]
    latest_date_22 = content_apple[-22:]
    latest_date_range = Year_juice_date[-1][0]+'~'+Year_juice_date[-1][-1]

    for apple in sql_tables_Database_juice_name:
        juice_dict = {}
        apple_str = ''.join(apple)
        # print(apple_str)
        Thresh_increase_flag = False

         # check if > 3 cycle at least by getting a single juice 3 year ago
        Three_year_date = Year_juice_date[-3][0]
        Three_year_date_next = Year_juice_date[-3][1]
        try:
            sql_cursor_Database_juice_name.execute("SELECT current FROM "+apple_str+" WHERE date LIKE "+Three_year_date+"")
            juice_data = sql_cursor_Database_juice_name.fetchall()[0][0]
            # verify it again for next month to ensure it's not just a single month missing
            sql_cursor_Database_juice_name.execute("SELECT current FROM "+apple_str+" WHERE date LIKE "+Three_year_date_next+"")
            juice_data = sql_cursor_Database_juice_name.fetchall()[0][0]
        except IndexError:
            print('Not enought data for '+apple_str)
            continue

        # if latest juice is not greater, skip processing this apple
        # sql_cursor_Database_juice_name.execute("SELECT current FROM "+apple_str+" WHERE date LIKE "+Year_juice_date[-1][-1]+"")
        # try:
        #     latest_juice_data = sql_cursor_Database_juice_name.fetchall()[0][0]
        # except IndexError:
        #     print('Not enought data for '+apple_str)
        #     continue
        # sql_cursor_Database_juice_name.execute("SELECT current FROM "+apple_str+" WHERE date LIKE "+Year_juice_date[-1][-2]+"")
        # try:
        #     second_latest_juice_data = sql_cursor_Database_juice_name.fetchall()[0][0]
        # except IndexError:
        #     print('Not enought data for '+apple_str)
        #     continue
        # if not latest_juice_data > second_latest_juice_data:
        #     continue

        # get customized from this month and a year juice here        
        for dates in Year_juice_date:
            dates_str = dates[0]+'~'+dates[-1]
            juice_data_accu = 0
            for date in dates:
                # Get juice
                sql_cursor_Database_juice_name.execute("SELECT current FROM "+apple_str+" WHERE date LIKE "+date+"")
                try:
                    juice_data = sql_cursor_Database_juice_name.fetchall()[0][0]
                except IndexError:
                    continue
                juice_data_accu += juice_data
            juice_dict[dates_str] = juice_data_accu
        max_key = max(juice_dict, key=juice_dict.get)
        # Note that this coping will fail, juice_dict will also be affect by later operation
        # juice_dict_cp = juice_dict
        juice_dict_cp = juice_dict.copy() # use .copy() to correctly copy a dict
        juice_dict_cp.pop(max_key,None)# pop the max then max again to find the second max
        max_second_key = max(juice_dict_cp, key=juice_dict_cp.get)
        if juice_dict[max_key] > 0 and juice_dict[max_second_key] > 0 \
            and (juice_dict[max_key] / juice_dict[max_second_key] * 100) - 100 > Thresh_increase:
            Thresh_increase_flag = True
        if max_key == latest_date_range and Thresh_increase_flag:
            # Check 500 in 22
            apple_amount_total = 0
            d_count = 0
            for d in latest_date_22:
                sql_cursor_Database_squeeze_name.execute("SELECT amount FROM "+apple_str+" WHERE date LIKE "+d+"")
                # printt(sql_cursor_Database_squeeze_name.fetchall()[0][0])
                try:
                    apple_amount_total += int(str(sql_cursor_Database_squeeze_name.fetchall()[0][0]).replace(',',''))
                except IndexError:
                    continue
                d_count += 1
            try:
                apple_amount_avg = apple_amount_total / d_count
            except ZeroDivisionError:
                continue
            # print(apple_amount_avg)
            if apple_amount_avg > 500000:
                best_juice.append(apple_str)
                
    best_juice.sort()

    if best_juice and parse_adb:
        L()
        print("Parsing data to adb now ...")
        L()
        for i in range(0,min(49,len(best_juice))):

            # parse the result to droid and track
            # keyevent of 0123456789 in number  pad is adb shell input keyevent 7~16
            # chinese keyboard got a different layout so need to switch to eng keyboard first manually
            # check adb device first
            result_adb = check_output(["adb", "devices"]).decode("utf-8").split(' ')#.find('device') will get sub string cant work
            result_adb = str(result_adb[3].split('\t')).split('\\')
            if 'device' not in result_adb[1]:
                args.adb_input_three_bamboo = False
                print("Got Error in adb connection, aborting...")
                C()
            # start auto putting data    
            call(["adb", "shell", "input", "tap" , "790" , "1739"])
            sleep(1)
            # call(["adb", "shell", "input", "tap" , "355" , "929"])
            # call(["adb", "shell", "input", "tap" , "311" , "561"])
            # sleep(1)
            # call(["adb", "shell", "input", "tap" , "102" , "1700"])
            # sleep(1)

            # x_num = ["567","311","567","821","311","567","821","311","567","821"]
            # y_num = ["1690","1150","1150","1150","1346","1346","1346","1551","1551","1551"]
            # num_1 = int(result[i][0].split('_')[1][0])
            # num_2 = int(result[i][0].split('_')[1][1])
            # num_3 = int(result[i][0].split('_')[1][2])
            # num_4 = int(result[i][0].split('_')[1][3])
            # call(["adb", "shell", "input", "tap" , x_num[num_1] , y_num[num_1]])
            # sleep(1)
            # call(["adb", "shell", "input", "tap" , x_num[num_2] , y_num[num_2]])
            # sleep(1)
            # call(["adb", "shell", "input", "tap" , x_num[num_3] , y_num[num_3]])
            # sleep(1)
            # call(["adb", "shell", "input", "tap" , x_num[num_4] , y_num[num_4]])
            # sleep(1)

            # tab first
            call(["adb", "shell", "input", "keyevent" , "61"])
            num = ["7","8","9","10","11","12","13","14","15","16"]
            num_1 = int(best_juice[i].split('_')[1][0])
            num_2 = int(best_juice[i].split('_')[1][1])
            num_3 = int(best_juice[i].split('_')[1][2])
            num_4 = int(best_juice[i].split('_')[1][3])
            call(["adb", "shell", "input", "keyevent" , num[num_1]])
            sleep(1)
            call(["adb", "shell", "input", "keyevent" , num[num_2]])
            sleep(1)
            call(["adb", "shell", "input", "keyevent" , num[num_3]])
            sleep(1)
            call(["adb", "shell", "input", "keyevent" , num[num_4]])
            sleep(1)

            call(["adb", "shell", "input", "tap" , "367" , "710"])
            sleep(2)
            call(["adb", "shell", "input", "tap" , "81" , "365"])
            sleep(1)
            call(["adb", "shell", "input", "tap" , "962" , "87"])
            sleep(2)
    if os.path.exists(Fig_dir+'/best_juices.txt'):
        os.remove(Fig_dir+'/best_juices.txt')
    for j in best_juice:
        Z_write_line(j,Fig_dir+'/best_juices.txt')
    print(best_juice)

def main():
    del_all_fig(Fig_dir)
    get_max_juice()
    
    
if __name__ == '__main__':
    main()
