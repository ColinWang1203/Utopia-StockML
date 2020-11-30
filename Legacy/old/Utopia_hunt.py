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

#user var
# skip_list = [8926, 3557]
skip_list = []

L()
print('Make sure to suspend whether report and change keyboard !!!')
L(-1)

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

with open('Processed_date_list.txt') as f:
    content = f.read().splitlines()

All_22_date = content[-22:]

with open(Fig_dir+'best_alicia.txt') as f:
    content_best_apple = f.read().splitlines()

apple_mid_list = []
for apple in content_best_apple:
    # print(apple.split('apple_')[1].split('\'')[0])
    apple_num = 'apple_'+apple.split('apple_')[1].split('\'')[0]
    # print(apple_num)
    # calculate the mid 22
    sql_cursor_Database_squeeze_name.execute("SELECT * FROM "+apple_num+"")
    sql_apple = sql_cursor_Database_squeeze_name.fetchall()
    mid_sum = 0
    count = 0
    for date in All_22_date:
        for apple_data in sql_apple:
            if compare_string(apple_data[0],date):
                if isinstance(apple_data[5],str):
                    mid_sum += float(apple_data[5].replace(',',''))
                else:
                    mid_sum += apple_data[5]
                count += 1
    if count is not 22:
        print('Warning !!! not 22 date')
    mid = mid_sum/count
    apple_mid_list.append((apple_num, round(mid,2)))

result = apple_mid_list
print('The result is : ')
print(result)
# parse to adb to hunt
hunt_count = 0
hunt_count_loop = 1

if not result:
    print("No result, abort!")
    C()

L()
print("Parsing data to adb now ...")
L()
for i in range(0,min(49,len(result))):
    # skip the one that is hopeless now
    # print(result[i][0])
    for skip_apple in skip_list:
        if compare_string(result[i][0],'apple_'+str(skip_apple)):
            print('skip '+'apple_'+str(skip_apple))
            continue 
            
    # parse the result to droid and track
    # keyevent of 0123456789 in number  pad is adb shell input keyevent 7~16
    # 61 tab (160/68) enter (4/4) back
    # chinese keyboard got a different layout so need to switch to eng keyboard first manually
    # check adb device first
    result_adb = check_output(["adb", "devices"]).decode("utf-8").split(' ')#.find('device') will get sub string cant work
    result_adb = str(result_adb[3].split('\t')).split('\\')
    if 'device' not in result_adb[1]:
        print("Got Error in adb connection, aborting...")
        C()
    # start auto putting data    
    call(["adb", "shell", "input", "tap" , "179" , "264"])
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
    sleep(0.2)
    call(["adb", "shell", "input", "keyevent" , num[num_2]])
    sleep(0.2)
    call(["adb", "shell", "input", "keyevent" , num[num_3]])
    sleep(0.2)
    call(["adb", "shell", "input", "keyevent" , num[num_4]])
    sleep(2)
    call(["adb", "shell", "input", "tap" , "211" , "406"])
    sleep(1)

    hunt_count += 1
    if hunt_count is 20:
        hunt_count_loop += 1
        hunt_count_loop_x = str(125*hunt_count_loop)
        call(["adb", "shell", "input", "keyevent" , "4"])
        sleep(1)    
        call(["adb", "shell", "input", "keyevent" , "4"])
        sleep(2)
        call(["adb", "shell", "input", "tap" , "460" , "112"])
        sleep(1)
        call(["adb", "shell", "input", "tap" , "263" , hunt_count_loop_x])
        sleep(1)
        call(["adb", "shell", "input", "tap" , "936" , "107"])
        sleep(1)
        hunt_count = 0


call(["adb", "shell", "input", "keyevent" , "4"])
sleep(1)
call(["adb", "shell", "input", "keyevent" , "4"])
sleep(1)
call(["adb", "shell", "input", "tap" , "460" , "112"])
sleep(1)
call(["adb", "shell", "input", "tap" , "263" , "125"])
sleep(1)

# now set all the mid 22 for all apples
hunt_count = 0
hunt_count_loop = 1

for i in range(0,min(49,len(result))):
    # print(result[i][0])
    hunt_count += 1
    
    num = ["7","8","9","10","11","12","13","14","15","16"]
    num_str = ""
    for _ in range(hunt_count):
        call(["adb", "shell", "input", "keyevent" , "61"])
        sleep(0.2)
    call(["adb", "shell", "input", "keyevent" , "160"])
    sleep(0.5)
    call(["adb", "shell", "input", "tap" , "439" , "1440"])
    sleep(0.5)
    call(["adb", "shell", "input", "keyevent" , "61"])
    sleep(0.5)
    call(["adb", "shell", "input", "keyevent" , "160"])
    sleep(0.5)
    call(["adb", "shell", "input", "tap" , "443" , "495"])
    sleep(0.5)
    call(["adb", "shell", "input", "keyevent" , "61"])
    sleep(0.5)
    call(["adb", "shell", "input", "keyevent" , "61"])
    sleep(0.5)
    call(["adb", "shell", "input", "keyevent" , "61"])
    sleep(0.5)
    call(["adb", "shell", "input", "keyevent" , "61"])
    sleep(0.5)
    call(["adb", "shell", "input", "keyevent" , "160"])
    sleep(1)

    call(["adb", "shell", "input", "tap" , "687" , "983"]) 
    
    # delete all numbers
    for _ in range(10):
        call(["adb", "shell", "input", "keyevent" , "67"])
        sleep(0.2)
    
    for num_s in str(result[i][1]):
        num_str+=num_s
    for c in num_str:
        if compare_string(c,'.'):
            call(["adb", "shell", "input", "tap" , "674" , "1729"]) # enter dot
            sleep(0.2)
            continue
        call(["adb", "shell", "input", "keyevent" , num[int(c)]])
        sleep(0.2)

    sleep(0.5)
    call(["adb", "shell", "input", "tap" , "909" , "781"]) 
    sleep(0.5)
    # call(["adb", "shell", "input", "tap" , "105" , "1054"]) # check big amount
    # sleep(0.5)
    call(["adb", "shell", "input", "keyevent" , "4"])
    sleep(1)
    call(["adb", "shell", "input", "keyevent" , "4"])
    sleep(1)
    call(["adb", "shell", "input", "swipe", "500" , "700", "500" , "1800"]) # prevent tab from misplacing
    sleep(2)
     
    if hunt_count is 20:
        hunt_count = 0
        hunt_count_loop += 1
        hunt_count_loop_x = str(125*hunt_count_loop)
        call(["adb", "shell", "input", "tap" , "460" , "112"])
        sleep(1)
        call(["adb", "shell", "input", "tap" , "263" , hunt_count_loop_x])
        sleep(10)