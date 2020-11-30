# produce the low touch in Figs/best_bb.txt
# -a just run now, and once crossed 5% mid in a month, show them
from Utopia_tools import *

import pandas, sqlite3, requests, calendar, os, urllib.request, sys
import numpy as np
from dateutil import rrule, relativedelta
from datetime import date, datetime
from argparse import ArgumentParser, RawTextHelpFormatter
from time import sleep
from io import StringIO
from subprocess import call,check_output


def parse_command_line():
    parser = ArgumentParser(description='-a to just run now\n',
            formatter_class=RawTextHelpFormatter)
    parser.add_argument('-a', dest='just_run_now', default = False, action='store_true')
    parser.add_argument('-b', dest='adb_input_three_bamboo', default = False, action='store_true')
    parser.add_argument('-c', dest='adb_input_assistant', default = False, action='store_true')
    return parser.parse_args()

args = parse_command_line()

def utopia_bb(day_shift):

    if day_shift > 365: 
        print('Only support day shift within 365 days')
        return -1

    # ===== User vars =====
    # drop below middle of middle bb and low bb
    how_close = 2 # set to very close for now
    how_much_mid_cross = 0.05 # 5%
    # =====================

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

    # =======================
    sql_cursor_Database_squeeze_name.execute("SELECT name FROM sqlite_master WHERE type='table'")
    sql_tables_Database_name = sql_cursor_Database_squeeze_name.fetchall()

    # Get day of an year by apple
    with open('Processed_date_list.txt') as f:
        content = f.read().splitlines()
    for i in list(range(1,len(content))):
        if Delta_days(content[-1],content[-i]) > 365:
            All_apple_date = content[-i-22:] # include the 22 in for the 365th day
            break

    # Get the touched low BB
    print("Showing low BB at "+All_apple_date[-1 - day_shift])
    touch_list = []

    for table in sorted(sql_tables_Database_name):
        table_str = ''.join(table)
        apple_num = str(table_str.split('_')[1])
        date_apple_mavg_dict = {}
        bb_up_dict = {}
        bb_down_dict = {}
        sql_cursor_Database_squeeze_name.execute("SELECT * FROM apple_"+apple_num+"")
        sql_apple = sql_cursor_Database_squeeze_name.fetchall()
        if day_shift > 0:
            All_22_date = All_apple_date[-22 - day_shift : -day_shift]
        else:
            All_22_date = All_apple_date[-22:]
        date = All_22_date[-1]
        if len(All_22_date) < 22:
            print('reach the end of apple index')
            continue
        apple_len = 0
        date_apple_mavg = 0
        bb_list = []
        for day in All_22_date:
            for apple in sql_apple:
                # avoid if any missing data for specific apple
                if compare_string(apple[0],day) and not isinstance(apple[5],str):
                    date_apple_mavg += apple[5]
                    bb_list.append(apple[5])
                    apple_len += 1
                    break
        # also need to find the available amount and divide with it
        # print(date_apple_mavg)
        if apple_len is 0 or apple_len < 21:#only accept missing 1 data in 22
            # print("Data not enough for "+apple_num)
            continue
        date_apple_mavg_divide = date_apple_mavg / apple_len
        date_apple_mavg_dict[date] = date_apple_mavg_divide  
        # create the bb
        bb_std = np.std(bb_list)
        # bb_up_dict[date] = date_apple_mavg_divide + (2 * bb_std)
        bb_down_dict[date] = date_apple_mavg_divide - (2 * bb_std)
        # check if touch
        # first check if data is compatible
        if not compare_string(sql_apple[-1 - day_shift][0],date):
            continue
        apple_low = sql_apple[-1 - day_shift][4]
        # print(apple_num)
        # print(apple_low)
        # print(bb_down_dict[date])
        if isinstance(apple_low,float):
            # if apple_low < (bb_down_dict[date] + (date_apple_mavg_dict[date] - bb_down_dict[date])/how_close ):
            if apple_low < bb_down_dict[date]:
                touch_list.append('apple_'+apple_num)
    
    if args.just_run_now:
        L()
        print('Low BB result is : ')
        print(touch_list)
        # save_list_to_figs_dir_and_dropbox(touch_list,'best_bb.txt')
        L()
    
    if touch_list is []:
        print('touch_list is null, aborting...')
        C()

    # Sort filtered apple by juice, compared only with one prev year

    with open('Processed_date_list.txt') as f:
            content_apple = f.read().splitlines()
    latest_date = content_apple[-1 - day_shift]
    if day_shift > 0:
        latest_date_22 = content_apple[-22 - day_shift : - day_shift]
    else:
        latest_date_22 = content_apple[-22:]

    # Get date for an year
    with open('Processed_juice_date_list.txt') as f:
        content = f.read().splitlines()

    # calculate how much juice should shift,
    # for 202003 : 20200415 shift 0 , 20200315 shift 0 , 20200310 shift 1  
    day_of_latest_date = int(latest_date[6:8])
    year_and_month_of_latest_date = latest_date[0:6]
    juice_shift = Delta_months(content[-1],year_and_month_of_latest_date)
    juice_shift += 1 # because current month only get last month
    if day_of_latest_date <= 10:
        juice_shift += 1

    Year_juice_date = []
    # list of year, max to 2 year
    for i in list(range(0,2)):
        if i == 0:
            if juice_shift == 0:
                Year_juice_date.append(content[-12:])
            else:
                Year_juice_date.append(content[-12-juice_shift:-juice_shift])
        else:
            Year_juice_date.append(content[-(12+(12*i))-juice_shift:-(12*i)-juice_shift])

    Year_juice_date.reverse()
    # print(Year_juice_date)

    all_dates_str = []
    for dates in Year_juice_date:
        dates_str = dates[0]+'~'+dates[-1]
        all_dates_str.append(dates_str)

    apple_dict = {}
    for apple in touch_list:
        # print('Processing '+apple)
        # Check 500 in 22
        apple_amount_total = 0
        d_count = 0
        for d in latest_date_22:
            sql_cursor_Database_squeeze_name.execute("SELECT amount FROM "+apple+" WHERE date LIKE "+d+"")
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
        if apple_amount_avg < 500000 or d_count < 21:
            continue
        
        # if latest price lower than 10 abort it
        sql_cursor_Database_squeeze_name.execute("SELECT ends FROM "+apple+" WHERE date LIKE "+latest_date_22[-1]+"")
        if sql_cursor_Database_squeeze_name.fetchall()[0][0] < 10:
            continue
        
        count = 0
        juice_dict = {}
        # get customized from this month and a year juice here        
        for dates in Year_juice_date:
            dates_str = dates[0]+'~'+dates[-1]
            juice_data_accu = 0
            for date in dates:
                # Get juice
                try:
                    sql_cursor_Database_juice_name.execute("SELECT current FROM "+apple+" WHERE date LIKE "+date+"")
                except sqlite3.OperationalError:
                    continue
                try:
                    juice_data = sql_cursor_Database_juice_name.fetchall()[0][0]
                except IndexError:
                    continue
                juice_data_accu += juice_data
                count += 1
            juice_dict[dates_str] = juice_data_accu
        # only accept missing one juice data
        if count < 21:
            continue
        juice_increase = ((juice_dict[all_dates_str[1]] - juice_dict[all_dates_str[0]]) / juice_dict[all_dates_str[0]])*100 
        
        '''
        do not compare juice now
        
        apple_dict[apple] = juice_increase

        '''

        # Also get the trigger target (suspend now)
        # lower than 10 > x.xx
        # 10 ~ 100 > xx.x(0/5)
        # 100 ~ 1000 > xxx.(0/5)
        # 1000 up > xxx(0/5)

        # ================================================================================
        # if over (low_bb - low_price)/low_price > 1% 
        # then calculate the average of (high_price - open_price)/open_price
        # for one year, if get apple fail average = -99 for invalid
        #
        # date_apple_dict = {}

        # for date in All_apple_date:
        #     date = str(date)
        #     for apple_data in sql_apple:
        #         if compare_string(apple_data[0],date):
        #             # handle missing data
        #             if isinstance(apple_data[5],str):
        #                 if not compare_string(apple_data[5],''):
        #                     date_apple_dict[date] = float(apple_data[5].replace(',',''))
        #                 else:
        #                     date_apple_dict[date] = nan()
        #             else: 
        #                 date_apple_dict[date] = apple_data[5]


        print("Calculate bb rate for "+apple+"...")
    
        apple_year_dict = {}
        bb_down_dict = {}
        count = 0
        count_bb = 0
        all_bb = 0
        sql_cursor_Database_squeeze_name.execute("SELECT * FROM "+apple+"")
        sql_apple = sql_cursor_Database_squeeze_name.fetchall()
        # print(All_apple_date)
        try :
            for date in All_apple_date[::-1]:
                date = str(date)
                date_apple_mavg = 0
                All_22_date = All_apple_date[-(22+count):-(1+count)]
                All_22_date.append(All_apple_date[-(1+count)])
                if len(All_22_date) < 22:
                    # print('reach the end of apple index')
                    break
                apple_len = 0
                bb_list = []
                
                for day in All_22_date:
                    for apple_2 in sql_apple:
                        
                        if compare_string(apple_2[0],day) and not compare_string(apple_2[5],''):
                            if type(apple_2[5]) is str:
                                # printt(apple_2[3])
                                apple_high = float(apple_2[3].replace(',',''));
                                apple_open  = float(apple_2[2].replace(',',''));
                                apple_end  = float(apple_2[5].replace(',',''));
                            else:
                                apple_high = apple_2[3];
                                apple_open  = apple_2[2];
                                apple_end  = apple_2[5];
                            date_apple_mavg += apple_end
                            bb_list.append(apple_end)
                            apple_len += 1
                            break

                date_apple_mavg_divide = date_apple_mavg / apple_len
                count += 1   
                # create the bb
                bb_std = np.std(bb_list)
                bb_down_dict[date] = date_apple_mavg_divide - (2 * bb_std)
                apple_year_dict[date] = [apple_high,apple_open]
            
            for key,value in bb_down_dict.items():
                bb_rate = (bb_down_dict[key]-apple_year_dict[key][1])/apple_year_dict[key][1] * 100
                ''' preserve this "how much chance to fill"
                if bb_rate > 1:#set to 1% away from bb_low then calculate the % of (min(high,bb_low)-open)/open
                    diff_high_or_low_bb_and_open = (min(apple_year_dict[key][0],bb_down_dict[key])-apple_year_dict[key][1])/apple_year_dict[key][1] * 100
                    #also get the diff with low_bb and calculate only the per percent of it
                    diff_bb_low_and_open = (bb_down_dict[key] - apple_year_dict[key][1])/apple_year_dict[key][1] * 100
                    #thus we can find out which apple can realy fill the hole between open and low_bb
                    all_bb += diff_high_or_low_bb_and_open / diff_bb_low_and_open
                    count_bb += 1
                '''
                # try to accumulate all the percentage of the drops over 1 %
                if bb_rate > 1:
                    diff_high_or_low_bb_and_open = (min(apple_year_dict[key][0],bb_down_dict[key])-apple_year_dict[key][1])/apple_year_dict[key][1] * 100
                    all_bb += diff_high_or_low_bb_and_open
                    count_bb += 1
            #         if compare_string(apple,'apple_3321'):
            #             print(key)
            #             print(min(apple_year_dict[key][0],bb_down_dict[key]))
            #             print(bb_down_dict[key])
            #             print(diff_high_or_low_bb_and_open)
            #             print(all_bb)

            # if compare_string(apple,'apple_3321'):
            #     C()
                        

            ''' preserve this "how much chance to fill"
            # deal with zero
            try:
                avg_bb = all_bb/count_bb
            except ZeroDivisionError:
                avg_bb = -99
            '''

            # print(avg_bb)
            ''' preserve this "how much chance to fill"
            apple_dict[apple] = [round(avg_bb,2), juice_increase]
            '''
        
            apple_dict[apple] = [all_bb/count_bb, juice_increase]
        except Exception as e:
            print('Error : '+str(e))
            print('Caught error, ignore it...')

        # ======================================================================

    # filter out the "not crossed" for just_run
    apple_dict_just_run = apple_dict.copy()
    if args.just_run_now:
        for apple_num in apple_dict:
            # get the mid bb for this apple for a month
            print(apple_num)
            over_mid = False
            count = 0
            # first check amount
            apple_str = ''.join(apple_num)
            d_count = 0
            apple_amount_total = 0
            latest_date_22 = All_apple_date[-22 : -1]
            latest_date_22.append(All_apple_date[-1])
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
                print('amount is')
                print(apple_amount_avg)
            except ZeroDivisionError:
                print(apple_str+' get amount error, abort')
                del apple_dict_just_run[apple_num]
                continue
            # print(apple_amount_avg)
            
            try:
                sql_cursor_Database_squeeze_name.execute("SELECT * FROM "+apple_num+"")
                sql_apple = sql_cursor_Database_squeeze_name.fetchall()
                for date in All_apple_date[::-1]:
                    if count > 20:#only search for a month
                        break
                    date = str(date)
                    date_apple_mavg = 0
                    All_22_date = All_apple_date[-(22+count):-(1+count)]
                    All_22_date.append(All_apple_date[-(1+count)])
                    if len(All_22_date) < 22:
                        # print('reach the end of apple index')
                        break
                    apple_len = 0
                    for day in All_22_date:
                        for apple in sql_apple:
                            if compare_string(apple[0],day) and not compare_string(apple[5],''):
                                if type(apple[5]) is str:
                                    apple_end = float(apple[5].replace(',',''));
                                else:
                                    apple_end = apple[5];
                                # capture the latest_apple
                                if day == All_22_date[-1] and count == 0:
                                    latest_apple = apple_end
                    
                                date_apple_mavg += apple_end
                                apple_len += 1
                                break
                    if apple_len < 21:
                        apple_fit = False
                        print(apple_num+' is outdated')
                        break
                    if apple_amount_avg * latest_apple < 50000000 or d_count < 21:
                        print(apple_str+' not enough amount, abort')
                        del apple_dict_just_run[apple_num]
                        continue
                    # check apple house
                    date_apple_mavg_dict[date] = date_apple_mavg / apple_len
                    count += 1  
                    if (apple_end - date_apple_mavg_dict[date])/date_apple_mavg_dict[date] > how_much_mid_cross :
                        over_mid = True
                        break
                if over_mid == False:
                    del apple_dict_just_run[apple_num]
            except Exception:
                print(apple_num+' got error in checking over mid, abort!')
                continue


    if args.just_run_now:
        result = sorted(apple_dict_just_run.items(), key=lambda x: x[1][1], reverse=True)
    else:
        result = sorted(apple_dict.items(), key=lambda x: x[1][0], reverse=True)
    
    if result:
        # if adb_input_assistant:
        #     for i in range(0,min(1000,len(result))):
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

        if args.adb_input_three_bamboo:
            L()
            print("Parsing data to adb now ...")
            L()
            for i in range(0,min(49,len(result))):

                # parse the result to droid and track
                # keyevent of 0123456789 in number  pad is adb shell input keyevent 7~16
                # chinese keyboard got a different layout so need to switch to eng keyboard first manually
                
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
                # call(["adb", "shell", "input", "keyevent" , "61"])
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
        print('Chosen low BB result is : ')
        print(result)
        L()
        if args.just_run_now:
            save_list_to_figs_dir_and_dropbox(result,'best_bb.txt')
        return [latest_date] + result
    else:
        L()
        print('The chosen one is not born yet !')
        L()
        return [latest_date] + ['Empty']
        

# Get day of an year by apple
# with open('Processed_date_list.txt') as f:
#     content = f.read().splitlines()
# for i in list(range(1,len(content))):
#     if Delta_days(content[-1],content[-i]) > 365:
#         All_apple_date = content[-i-22:]
#         break 

if args.just_run_now:
    utopia_bb(0)