from Utopia_tools import *

import pandas, sqlite3, requests, calendar, os, urllib.request, sys, math
import numpy as np
import matplotlib.pyplot as plt
from dateutil import rrule
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from argparse import ArgumentParser, RawTextHelpFormatter
from time import sleep
from io import StringIO
from random import randint
from subprocess import call,check_output

# user variable True False
#########################
parse_adb = True
three_up_touch = True
mix_score_with_a_week = False
ignore_must_be_best_juice = True #just compare with the last second year and compare the ratio, ratio  set to max -20%
#########################

# user variable
below_mid_ratio = -0.02 #set the below mid ratio to be 2%
juice_increase_threshhold = 1 #set round compare increase at least 1% compared with max second year
skip_list = [2548, 2348, 2524, 2505, 2851, 2836, 2889, 5521] # skip finance, construction


Database_squeeze_name = 'DB_Avalon.sqlite'
sql_connection_Database_squeeze_name = sqlite3.connect(Database_squeeze_name)
sql_cursor_Database_squeeze_name = sql_connection_Database_squeeze_name.cursor()
Database_juice_name = 'DB_Juice.sqlite'
sql_connection_Database_juice_name = sqlite3.connect(Database_juice_name)
sql_cursor_Database_juice_name = sql_connection_Database_juice_name.cursor()
Database_seeds_name = 'DB_Seeds.sqlite'
sql_connection_Database_seeds_name = sqlite3.connect(Database_seeds_name)
sql_cursor_Database_seeds_name = sql_connection_Database_seeds_name.cursor()

Fig_dir = 'Figs/' 
Fig_dir_dropbox = '/home/colin/Dropbox/Figs/'

# Get the tables
sql_cursor_Database_squeeze_name.execute("SELECT name FROM sqlite_master WHERE type='table'")
sql_tables_Database_squeeze_name = sql_cursor_Database_squeeze_name.fetchall()

apple_alicia = []
apple_alicia_dict = {}

def skip_apple(apple_num):
    for skip_apple in skip_list:
        if compare_string(apple_num,'apple_'+str(skip_apple)):
            print('skip '+'apple_'+str(skip_apple))
            return True
    return False 

def main():

    # Get day of a month by apple and see if above
    with open('Processed_date_list.txt') as f:
        content = f.read().splitlines()
    for i in list(range(1,len(content))):
        if Delta_days(content[-1],content[-i]) > 52: 
            All_apple_date = content[-i:]
            break     

    for apple_num in sql_tables_Database_squeeze_name:
        apple_num = "".join(apple_num)
        # print('now is '+apple_num)
        if skip_apple(apple_num):
            continue
        sql_cursor_Database_squeeze_name.execute("SELECT * FROM "+apple_num+"")
        sql_apple = sql_cursor_Database_squeeze_name.fetchall()
        date_apple_dict = {}
        # if we got an apple that contains missing data like '--' , ignore it
        try :
            for date in All_apple_date:
                date = str(date)
                for apple_data in sql_apple:
                    if compare_string(apple_data[0],date):
                        # handle missing data
                        if compare_string(apple_data[5],'--'):
                            print(apple_num+' got missing data, ignoring it...')
                            raise Exception
                        elif isinstance(apple_data[5],str):
                            if not compare_string(apple_data[5],''):
                                date_apple_dict[date] = float(apple_data[5].replace(',',''))
                            else:
                                date_apple_dict[date] = nan()
                        else: 
                            date_apple_dict[date] = apple_data[5]

            date_apple_mavg_dict = {}
            count = 0
            apple_fit = True

            for date in All_apple_date[::-1]:
                date = str(date)
                date_apple_mavg = 0
                All_22_date = All_apple_date[-(22+count):-(1+count)]
                All_22_date.append(All_apple_date[-(1+count)])
                bb_list = []
                if len(All_22_date) < 22:
                    # print('reach the end of apple index')
                    break
                apple_len = 0
                # print(All_22_date)
                for day in All_22_date:
                    for apple in sql_apple:
                        if compare_string(apple[0],day) and not compare_string(apple[5],''):
                            if type(apple[5]) is str:
                                apple_end = float(apple[5].replace(',',''));
                                apple_high = float(apple[3].replace(',',''));
                            else:
                                apple_end = apple[5];
                                apple_high = apple[3];
                            # capture the latest_apple
                            if day == All_22_date[-1] and count == 0:
                                latest_apple = apple_end
                            date_apple_mavg += apple_end
                            bb_list.append(apple_end)
                            apple_len += 1
                            break
                
                if apple_len < 21:
                    apple_fit = False
                    print(apple_num+' is outdated')
                    break

                date_apple_mavg_dict[date] = date_apple_mavg / apple_len
                if (date_apple_dict[date] - date_apple_mavg_dict[date])/date_apple_mavg_dict[date] < below_mid_ratio :
                    apple_fit = False
                    print(apple_num+" not fit")
                    break
                
                bb_std = np.std(bb_list)
                bb_up = date_apple_mavg_dict[date] + (2 * bb_std)
                # if compare_string(apple_num,'apple_9958'):
                #     L()
                #     print(bb_up)
                #     print(apple_high)
                #     L()
                if three_up_touch and count < 3:
                    #calcuate the up bb and set apple to false if not meet
                    if bb_up > apple_high:
                        apple_fit = False
                        print(apple_num+" not high enough")
                        break
            
                count += 1
            if apple_fit:    
                apple_alicia.append(apple_num)
        except Exception as e:
            print('Error : '+str(e))
            print(apple_num+' got error, abort!')
            continue

    print(apple_alicia)
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
    for apple_num in apple_alicia:
        # print('juice is '+apple_num)
        juice_dict = {}
        apple_str = ''.join(apple_num)
        # print(apple_str)
        # if lesser than 5000w skip
        d_count = 0
        apple_amount_total = 0
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
            print(apple_str+' get amount error, abort')
            continue
        # print(apple_amount_avg)
        if apple_amount_avg * latest_apple < 50000000 or d_count < 21:
            print(apple_str+' not enough amount, abort')
            continue

         # check if > 3 cycle at least by getting a single juice 3 year ago
        Three_year_date = Year_juice_date[-3][0]
        Three_year_date_next = Year_juice_date[-3][1]
        try:
            sql_cursor_Database_juice_name.execute("SELECT current FROM "+apple_str+" WHERE date LIKE "+Three_year_date+"")
            juice_data = sql_cursor_Database_juice_name.fetchall()[0][0]
            # verify it again for next month to ensure it's not just a single month missing
            sql_cursor_Database_juice_name.execute("SELECT current FROM "+apple_str+" WHERE date LIKE "+Three_year_date_next+"")
            juice_data = sql_cursor_Database_juice_name.fetchall()[0][0]
        except (IndexError, sqlite3.OperationalError) :
            print('Not enought data for '+apple_str)
            continue

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
        # if compare_string(apple_str,'apple_2454'):
        #     print(juice_dict)
        #     C()
        
        # print(juice_dict[list(juice_dict)[-1]])
        # print(juice_dict[list(juice_dict)[-2]])
        this_year_juice = juice_dict[list(juice_dict)[-1]]
        if ignore_must_be_best_juice :
            second_year_juice = juice_dict[list(juice_dict)[-2]]
            juice_increase_rate = (this_year_juice - second_year_juice)/ second_year_juice * 100
            if juice_increase_rate < -0.2:
                print(apple_str+' is too bad to eat')
                continue
        else:
            max_key = max(juice_dict, key=juice_dict.get)
            # skip if this year is not the best
            if not compare_string(max_key,latest_date_range):
                print(apple_str+' is not in the best year')
                continue
            juice_dict_cp = juice_dict.copy() # use .copy() to correctly copy a dict
            juice_dict_cp.pop(max_key,None)# pop the max then max again to find the second max
            max_second_key = max(juice_dict_cp, key=juice_dict_cp.get)
            second_max_year_juice = juice_dict[max_second_key]
            ##do not compare only to the previous year but compare to the second best
            # last_yeat_juice = juice_dict[list(juice_dict)[-2]]
            # juice_increase_rate = (this_year_juice - last_yeat_juice)/ last_yeat_juice * 100
            juice_increase_rate = (this_year_juice - second_max_year_juice)/ second_max_year_juice * 100
            
        if ignore_must_be_best_juice or juice_increase_rate > juice_increase_threshhold:
            if mix_score_with_a_week:
                # get the apple a week ago
                sql_cursor_Database_squeeze_name.execute("SELECT * FROM "+apple_num+"")
                sql_apple = sql_cursor_Database_squeeze_name.fetchall()
                try:
                    date = str(latest_date_22[-5])
                    for apple_data in sql_apple:
                        if compare_string(apple_data[0],date):
                            # handle missing data
                            if compare_string(apple_data[5],'--'):
                                print(apple_num+' got missing data, ignoring it...')
                                raise Exception
                            elif isinstance(apple_data[5],str):
                                if not compare_string(apple_data[5],''):
                                    apple_a_week = float(apple_data[5].replace(',',''))
                                else:
                                    apple_a_week = nan()
                            else: 
                                apple_a_week = apple_data[5]
                    date = str(latest_date_22[-1])
                    for apple_data in sql_apple:
                        if compare_string(apple_data[0],date):
                            # handle missing data
                            if compare_string(apple_data[5],'--'):
                                print(apple_num+' got missing data, ignoring it...')
                                raise Exception
                            elif isinstance(apple_data[5],str):
                                if not compare_string(apple_data[5],''):
                                    apple_now = float(apple_data[5].replace(',',''))
                                else:
                                    apple_now = nan()
                            else: 
                                apple_now = apple_data[5]
                except Exception as e:
                    print('Error : '+str(e))
                    print(apple_num+' got error when getting apple a week ago, abort!')
                    continue
                apple_week_rate = apple_now / apple_a_week
                print('The '+str(apple_num)+' apple_week_rate is : '+str(apple_week_rate))
                print('The '+str(apple_num)+' juice_increase_rate is : '+str(juice_increase_rate))
                apple_alicia_dict[apple_num] = juice_increase_rate * apple_week_rate
            else:
                apple_alicia_dict[apple_num] = juice_increase_rate

    # print(apple_alicia_dict)
    result = sorted(apple_alicia_dict.items(), key=lambda x: x[1], reverse=True)
    save_list_to_figs_dir_and_dropbox(result,'best_alicia.txt')
    L()
    print('The Result is : ')
    print(result)

    if result and parse_adb:
        L()
        print("Parsing data to adb now ...")
        L()
        while True:
            result_adb = check_output(["adb", "devices"]).decode("utf-8").split(' ')#.find('device') will get sub string cant work
            # print(result_adb)
            result_adb = str(result_adb[4].split('\t')).split('\\')
            # print(result_adb)
            try:
                if 'device' in result_adb[1]:
                    print("Found adb device!")
                    L()
                    break
            except:
                print("Got Error in adb connection, retrying...")
                sleep(1)
                
        for i in range(0,min(49,len(result))):

            # parse the result to droid and track
            # keyevent of 0123456789 in number  pad is adb shell input keyevent 7~16
            # 61 tab 68 enter 4 back 62 space(can be used to select)
            # chinese keyboard got a different layout so need to switch to eng keyboard first manually
            # check adb device first
            
                
            # start auto putting data    
            call(["adb", "shell", "input", "tap" , "790" , "1739"])
            sleep(2)
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
            # call(["adb", "shell", "input", "keyevent" , "61"]) # no tab is required anymore
            num = ["7","8","9","10","11","12","13","14","15","16"]
            num_1 = int(result[i][0].split('_')[1][0])
            num_2 = int(result[i][0].split('_')[1][1])
            num_3 = int(result[i][0].split('_')[1][2])
            num_4 = int(result[i][0].split('_')[1][3])
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
            sleep(2)
            call(["adb", "shell", "input", "tap" , "962" , "87"])
            sleep(2)

    L()
    print('DONE')
    L()


    
if __name__ == '__main__':
    main()



    