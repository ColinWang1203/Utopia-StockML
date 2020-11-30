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

# Easy rpogram stop
def C():
    sys.exit()

# Create an NaN
def nan():
    return float('nan')

# Create printing a line
def L(sleep_secs=0):
    print('\n==============================================================\n')
    if sleep_secs >0:
        sleep(sleep_secs)
    if sleep_secs == -1:
        input()

# Get avg and ignore nan
def avg(list_data):
    list_data_filt = [ i for i in list_data if i != None]
    if list_data_filt == []:
        return None
    return sum(list_data_filt) / len(list_data_filt)

def Z_delete(path):
    if os.path.exists(path):
        os.remove(path)

def Z_write_line(line_string, filename, remove_old=False):
    if os.path.exists(filename) and remove_old:
        os.remove(filename)
        print('Warning, write file remove_old should not be used in loop.')
        print('Otherwise only the last line will be saved.')
    if not os.path.exists(filename):
        os.mknod(filename)
    with open(filename) as fr:
        with open(filename, 'a') as fa:
            fa.write(line_string+'\n')

def Z_read_line(filename):
    with open(filename) as f:
        return f.read().splitlines()

def Z_new_file(filename):
    with open(filename, 'a') as fa:
        fa.write('')

def YN_Check(check_msg):
    print(check_msg)
    while True:
        key = input()
        if key is not 'Y' and key is not 'N':
            print('Please type Y/N')
        else:
            break
    if key == 'Y':
        return True
    if key == 'N':
        return False
        
def Delta_days(d1,d2):
    return (datetime.strptime(d1, '%Y%m%d') - datetime.strptime(d2, '%Y%m%d')).days

def Delta_months(d1,d2):
    return (int(d1[0:4]) - int(d2[0:4]))*12+(int(d1[4:6]) - int(d2[4:6]))

def compare_string(s1,s2):
	if str(s1) == str(s2):
		return True
	else:
		return False
		
def del_all_fig(Fig_dir):
    filelist = [ f for f in os.listdir(Fig_dir) if f.endswith(".jpg") or f.endswith(".png")  ]
    for f in filelist:
        os.remove(os.path.join(Fig_dir, f))

def Z_list2str(my_list):
    paragraphs_list = []
    for x in my_list:
        paragraphs_list.append(str(x))
    return ''.join(paragraphs_list)

def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def printt(data):
    print(data)
    print(type(data))

def printl(data):
    print('\n==============================================================\n')
    print(data)
    print('\n==============================================================\n')
    
def save_list_to_figs_dir_and_dropbox(data,file_name,concate = False):
    if not concate:
        if os.path.exists('Figs/'+file_name):
            os.remove('Figs/'+file_name)
        if os.path.exists('/home/colin/Dropbox/Figs/'+file_name):
            os.remove('/home/colin/Dropbox/Figs/'+file_name)
    if type(data) is str:
        Z_write_line(data,'Figs/'+file_name)
        Z_write_line(data,'/home/colin/Dropbox/Figs/'+file_name)
    else:
        for line in data:
            Z_write_line(str(line),'Figs/'+file_name)
            Z_write_line(str(line),'/home/colin/Dropbox/Figs/'+file_name)

def skip_apple_by_list(apple_num, skip_list):
    for skip_apple in skip_list:
        if compare_string(apple_num,'apple_'+str(skip_apple)):
            print('skip '+'apple_'+str(skip_apple))
            return True
    return False 

def enable_logging():
    if os.path.exists('utopia.log'):
        os.remove('utopia.log')
    class Logger(object):
        def __init__(self):
            self.terminal = sys.stdout
            self.log = open('utopia.log', 'a')

        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)  

        def flush(self):
            #this flush method is needed for python 3 compatibility.
            #this handles the flush command by doing nothing.
            #you might want to specify some extra behavior here.
            pass    

    sys.stdout = Logger()

def check_adb_connection():
    while True:
        result_adb = check_output(["adb", "devices"]).decode("utf-8").split(' ')#.find('device') will get sub string cant work
        # print(result_adb)
        result_adb = str(result_adb[4].split('\t')).split('\\')
        # print(result_adb)
        try:
            if 'device' in result_adb[1]:
                printl("Found adb device!")
                break
        except:
            print("Got Error in adb connection, retrying...")
            sleep(1)

def parse_three_bamboo(list_result):
    for i in range(0,min(49,len(list_result))):
    
        # parse the list_result to droid and track
        # keyevent of 0123456789 in number  pad is adb shell input keyevent 7~16
        # 61 tab 68 enter 4 back 62 space(can be used to select)
        # chinese keyboard got a different layout so need to switch to eng keyboard first manually
        # check adb device first
        
            
        # start auto putting data    
        call(["adb", "shell", "input", "tap" , "790" , "1739"])
        sleep(2)
        # tab first
        # call(["adb", "shell", "input", "keyevent" , "61"]) # no tab is required anymore
        num = ["7","8","9","10","11","12","13","14","15","16"]
        num_1 = int(list_result[i][0].split('_')[1][0])
        num_2 = int(list_result[i][0].split('_')[1][1])
        num_3 = int(list_result[i][0].split('_')[1][2])
        num_4 = int(list_result[i][0].split('_')[1][3])
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

def swipe_change_three_bamboo_page():
    call(["adb", "shell", "input", "swipe" , "800" , "1000", "200" , "1000"])
    sleep(2)

def remove_former_three_bamboo(delete_len):
    delete_len = int(delete_len)
    if delete_len == 0:
        return
    call(["adb", "shell", "input", "tap" , "1040" , "100"])
    sleep(2)
    for i in range(0,7): # cursor to the first
        call(["adb", "shell", "input", "keyevent" , '61'])
        sleep(0.5)
    while delete_len > 0:
        call(["adb", "shell", "input", "keyevent" , '62']) # space to select
        sleep(1)
        for i in range(0,4):
            call(["adb", "shell", "input", "keyevent" , '61']) # move to the next
            sleep(0.5)
        delete_len -= 1

    call(["adb", "shell", "input", "tap" , "66" , "125"]) # goto previous page
    sleep(2)
        