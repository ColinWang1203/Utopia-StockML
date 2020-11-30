# modulize the bb into a  function :
# apple_list = utopia_bb(start_date) 
# loop the list and calculate the average next month high % until a not_valid_date error is returned
# next try to add parameters in ex: apple_list = utopia_bb(start_date,how_close) 

from Utopia_tools import *
from Utopia_bb import *

import pandas, sqlite3, requests, calendar, os, urllib.request, sys
import numpy as np
from dateutil import rrule, relativedelta
from datetime import date, datetime
from argparse import ArgumentParser, RawTextHelpFormatter
from time import sleep
from io import StringIO

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

# custom error for jumping out only one loop
class ContinueI(Exception):
    pass
continue_i = ContinueI()

shift_start_date = 14 # leave 4 days as some buffer to process
result_bb_dict = {}
for i in range(0,120):
    result = utopia_bb(i)
    result_bb_dict[result[0]] = result[1:]
print(result_bb_dict)
f = open('out.txt','w')
for key,value in result_bb_dict:
    print(result_bb_dict, file=f)
C()
# processed till 0416 , shift_start_date is 16
result_bb_dict = {'20200323': [('apple_1598', -3.926919772414176), ('apple_2106', -6.6249424983092995), ('apple_2499', -18.154320519483328), ('apple_3532', -30.99692906935315)], '20200320': [('apple_2206', 7.052769545642993), ('apple_1707', -0.10951664033129216), ('apple_1598', -3.926919772414176), ('apple_2106', -6.6249424983092995), ('apple_2027', -11.106980045811605), ('apple_2499', -18.154320519483328), ('apple_3532', -30.99692906935315)]}

apple_sweet_dict = {}

for key, value in result_bb_dict.items():
# '''
# key : 20200323
# value : [('apple_1598', -3.926919772414176), ('apple_2106', -6.6249424983092995), ('apple_2499', -18.154320519483328), ('apple_3532', -30.99692906935315)]
# '''
    if value[0] == 'Empty':
        continue

    apple_sweet_list = []
    print('day key is '+key)

    for apple_num,juice_rate in value:
        print(apple_num)
        date_apple_mavg_dict = {}
        bb_down_dict = {}
        # next day get in if open is out
        sql_cursor_Database_squeeze_name.execute("SELECT * FROM "+apple_num+"")
        sql_apple = sql_cursor_Database_squeeze_name.fetchall()
        # > calculte the new bb_low with a new open value
        # >> first get the updated 22 date
        with open('Processed_date_list.txt') as f:
            contents = f.read().splitlines()
        index = contents.index(key)
        shift_date = len(contents) - index - 1
        All_22_date = contents[index-20:index+2]
        apple_len = 0
        date_apple_mavg = 0
        bb_list = []
        latest_day = All_22_date[-1]
        print('Current updated 22 day starts from '+All_22_date[-1])
        for day in All_22_date[:-1]:
            for apple in sql_apple:
                # avoid if any missing data for specific apple
                if compare_string(apple[0],day) and not isinstance(apple[5],str):
                    date_apple_mavg += apple[5]
                    bb_list.append(apple[5])
                    apple_len += 1
                    break
        # use the opening to calculate a new bb low
        for apple in sql_apple:
            # avoid if any missing data for specific apple
            if compare_string(apple[0],latest_day) and not isinstance(apple[2],str):
                date_apple_mavg += apple[2]
                bb_list.append(apple[2])
                apple_len += 1
                break
        date_apple_mavg_divide = date_apple_mavg / apple_len
        date_apple_mavg_dict[latest_day] = date_apple_mavg_divide  
        bb_std = np.std(bb_list)
        new_bb_low = date_apple_mavg_divide - (2 * bb_std)
        # in condition here, skip this apple if not fit
        next_open = float(sql_apple[-1-shift_date+1][2])
        print('open is ' + str(next_open))
        print('new_bb_low is ' + str(new_bb_low))
        if next_open > new_bb_low:
            continue
        # now im in, from next next day if lose 1. just out 2.10% in another
        # > calculate the sweet and mark it
        apple_price = next_open
        print('apple_price is '+str(apple_price))
        # > now do it day by day until max two weeks
        try:
            for i in range(1,11):
                print('Day shift to '+contents[index+2+i-1])
                next_price_end = float(sql_apple[-1-shift_date+1+i][5])
                print('next_price_low is '+str(next_price_end))
                if next_price_end < apple_price or i == 10:
                    # get out, calculate sweet
                    sweet = (next_price_end - apple_price) / apple_price * 100
                    apple_sweet_list += (apple_num,sweet)
                    raise continue_i
        except ContinueI:
            continue
        # close to middle and leave then out
            # get the avg now
            # All_22_date_for_avg = contents[index-20+i:index+2+i]
            # print(All_22_date_for_avg)
            # print(len(All_22_date_for_avg))

            # C()
        # cross middle not next high out

    apple_sweet_dict[key] = apple_sweet_list
print(apple_sweet_dict)
C()




# ===================
# modulize the juice into a  function :
# apple_list = utopia_juice(start_date) 
# loop the list and calculate the average next month high % until a not_valid_date error is returned
