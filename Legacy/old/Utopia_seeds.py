# seeds up, apple does not, arrange by juice and show on title
# produce the best_seeds.txt in Figs
from Utopia_tools import *

import pandas, sqlite3, requests, calendar, os, urllib.request, sys
import numpy as np
from dateutil import rrule, relativedelta
from datetime import date, datetime
from argparse import ArgumentParser, RawTextHelpFormatter
from time import sleep
from io import StringIO

# ===== Global vars =====

today = datetime.today().strftime("%Y%m%d")

# Databases
Database_name = 'DB_Utopia.sqlite'
sql_connection_Database_name = sqlite3.connect(Database_name)
sql_cursor_Database_name = sql_connection_Database_name.cursor()
Database_squeeze_name = 'DB_Avalon.sqlite'
sql_connection_Database_squeeze_name = sqlite3.connect(Database_squeeze_name)
sql_cursor_Database_squeeze_name = sql_connection_Database_squeeze_name.cursor()
Database_juice_name = 'DB_Juice.sqlite'
sql_connection_Database_juice_name = sqlite3.connect(Database_juice_name)
sql_cursor_Database_juice_name = sql_connection_Database_juice_name.cursor()
Database_seeds_name = 'DB_Seeds.sqlite'
sql_connection_Database_seeds_name = sqlite3.connect(Database_seeds_name)
sql_cursor_Database_seeds_name = sql_connection_Database_seeds_name.cursor()

Fig_dir = 'Figs'
seed_threshold = 0.05
apple_threshold = 0.05

# =======================
sql_cursor_Database_squeeze_name.execute("SELECT name FROM sqlite_master WHERE type='table'")
sql_tables_Database_name = sql_cursor_Database_squeeze_name.fetchall()

# Get day of an year by apple
with open('Processed_date_list.txt') as f:
    content = f.read().splitlines()
for i in list(range(1,len(content))):
    if Delta_days(content[-1],content[-i]) > 365:
        start_date = content[-i]
        All_apple_date = content[-i:]
        break  

# Use bigger loop to make sure at least 10 result is generated
while True:
    table_str_result_pass_seeds = []
    table_str_result_pass_seeds_pass_apple_slope = []
    # Get 4 seeds , see if rise
    for table in sorted(sql_tables_Database_name):
        # convert tuple into string
        table_str = ''.join(table)
        apple_num = str(table_str.split('_')[1])
        try:
            sql_cursor_Database_seeds_name.execute("SELECT * FROM apple_"+apple_num+"")
            sql_seeds = sql_cursor_Database_seeds_name.fetchall()
        except sqlite3.OperationalError:
            print('No data for '+table_str)
            continue
        try:
            All_seeds_date = [i[0] for i in sql_seeds][-4:]
        except IndexError:
            print('Not enough data for '+table_str)
            continue
        # seeds algo here
        date_seeds_list = []
        for date in All_seeds_date:
            date = str(date)
            for seeds_data in sql_seeds:
                if compare_string(seeds_data[0],date):
                    modified_date = min(map(int,All_apple_date), key=lambda x:abs(x-int(date)))
                    # Get the ratio of big/small seeds
                    # 1~9(100down) 10~15(100up)
                    small_seeds = 0
                    big_seeds = 0
                    for i in list(range(1,16)):
                        if i < 10:
                            small_seeds += seeds_data[i]
                        else:
                            big_seeds += seeds_data[i]
                    try:
                        seeds_ratio = big_seeds/small_seeds
                    except ZeroDivisionError:
                        print('Not valid data for '+table_str)
                        continue
                    date_seeds_list.append(seeds_ratio)    
        # use (last-average)/average > 0.05
        try:
            date_seeds_list_avg = (date_seeds_list[0] + date_seeds_list[1] +\
                    date_seeds_list[2] + date_seeds_list[3])/4 
        except IndexError:
            print('Not valid data for '+table_str)
            continue
        if (date_seeds_list[-1] - date_seeds_list_avg)/date_seeds_list_avg > seed_threshold:
            table_str_result_pass_seeds.append(table_str)
    # print(table_str_result_pass_seeds)

    # Get apple between 4 seeds, see if not rise
    # use apple_22 (last-average)/average < 0.05
    for apple in table_str_result_pass_seeds:
        sql_cursor_Database_squeeze_name.execute("SELECT * FROM "+apple+"")
        sql_apple = sql_cursor_Database_squeeze_name.fetchall()
        # check if not valid for around an year
        if len(sql_apple) < 250:
            continue
        sql_apple_sum = 0
        for i in list(range(1,31)):
            sql_apple_sum += sql_apple[-i][5]
        sql_apple_avg = sql_apple_sum/30
        if (sql_apple[-1][5] - sql_apple_avg)/sql_apple_avg < apple_threshold:
            table_str_result_pass_seeds_pass_apple_slope.append(apple)
    # print(table_str_result_pass_seeds_pass_apple_slope)

    if len(table_str_result_pass_seeds_pass_apple_slope) > 10:
        break

    seed_threshold -= 0.005
    apple_threshold += 0.005


# print(table_str_result_pass_seeds_pass_apple_slope)
table_str_result_pass_seeds_pass_apple_slope.sort()
if os.path.exists(Fig_dir+'/best_seeds.txt'):
    os.remove(Fig_dir+'/best_seeds.txt')
for j in table_str_result_pass_seeds_pass_apple_slope:
    Z_write_line(j,Fig_dir+'/best_seeds.txt')

# Arrange them by juice and print on title

# Get date for an year
with open('Processed_juice_date_list.txt') as f:
    content = f.read().splitlines()

Year_juice_date = []
# list of year, max to 10 year
for i in list(range(0,2)):
    if i == 0:
        Year_juice_date.append(content[-12:])
    else:
        Year_juice_date.append(content[-(12+(12*i)):-(12*i)])

Year_juice_date.reverse()

count = -1
for apple_str in table_str_result_pass_seeds_pass_apple_slope:
    count += 1
    # get customized from this month and a year juice here
    juice_list = []
    for dates in Year_juice_date:
        dates_str = dates[0]+'~'+dates[-1]
        juice_data_accu = 0
        for date in dates:
            # Get juice
            try:
                sql_cursor_Database_juice_name.execute("SELECT current FROM "+apple_str+" WHERE date LIKE "+date+"")
            except sqlite3.OperationalError:
                print('No data for juice in '+apple_str)
                continue
            try:
                juice_data = sql_cursor_Database_juice_name.fetchall()[0][0]
            except IndexError:
                continue
            juice_data_accu += juice_data
        juice_list.append(juice_data_accu)
    # [320562, 495261]
    try:
        Juice_increase = int((juice_list[1] - juice_list[0])/juice_list[0]*100)
    except ZeroDivisionError:
        print('Got error in juice '+apple_str)
        continue

    table_str_result_pass_seeds_pass_apple_slope[count] += ('_'+str(Juice_increase))

# print(table_str_result_pass_seeds_pass_apple_slope)
table_str_result_pass_seeds_pass_apple_slope.sort()
if os.path.exists(Fig_dir+'/best_seeds_with_juice.txt'):
    os.remove(Fig_dir+'/best_seeds_with_juice.txt')
for j in table_str_result_pass_seeds_pass_apple_slope:
    Z_write_line(j,Fig_dir+'/best_seeds_with_juice.txt')
print(table_str_result_pass_seeds_pass_apple_slope)