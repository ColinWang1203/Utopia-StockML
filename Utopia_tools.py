import pandas, sqlite3, requests, calendar, os, urllib.request, sys, math, shutil, webbrowser, glob
import re, nltk, jieba, random
import numpy as np
import matplotlib.pyplot as plt
from dateutil import *
from datetime import date, datetime
# from dateutil.relativedelta import relativedelta # this will cause error, so just import * on top
from argparse import ArgumentParser, RawTextHelpFormatter
from time import sleep, time
from io import StringIO
from random import randint
from subprocess import call,check_output
from distutils import *
from nltk.probability import FreqDist
from bs4 import BeautifulSoup, SoupStrainer
from matplotlib import font_manager
from sklearn.ensemble import RandomForestRegressor

# All of my function starts with 'P_'


# ===============================================================
#                Logging and Debuging
# ===============================================================

def P():
    P_switch_back_to_utopia_window()
    sys.exit()

def P_user_yn_confirm(_check_msg):
    print(_check_msg)
    while True:
        key = input()
        if key not in ['Y','N','y','n']:
            print('Please type Y/N or y/n')
        else:
            break
    if key == 'Y' or 'y':
        return True
    if key == 'N' or 'n':
        return False

def P_printt(data):
    print(data)
    print(type(data))

def P_printl(string = None, level = 0, sleep_secs = 0):
    if type(string) == str:
        print('\n==============================================================\n')
        if level > 0:
            print('Colin'+str(level)+' : '+string)
            print('\n==============================================================\n')
        else:
            print(string)
            print('\n==============================================================\n')
    if type(string) == list:
        print('\n==============================================================\n')
        for l in string:
            print(l)
        print('\n==============================================================\n')
    if type(string) == dict:
        print('\n==============================================================\n')
        for l in string:
            print(string[l])
        print('\n==============================================================\n')
    if isinstance(string, np.ndarray):
        print('\n==============================================================\n')
        for l in string:
            print(l)
        print('\n==============================================================\n')
    if sleep_secs > 0:
        sleep(sleep_secs)
    if sleep_secs == -1:
        input()

def P_enable_logging():
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d%H%M%S")
    file_name = '/media/colin/Ubuntu-D/Utopia_Logs/utopia_'+dt_string+'.log'
    if os.path.exists(file_name):
        os.remove(file_name)
    class Logger(object):
        def __init__(self):
            self.terminal = sys.stdout
            self.log = open(file_name, 'a')

        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)  

        def flush(self):
            #this flush method is needed for python 3 compatibility.
            #this handles the flush command by doing nothing.
            #you might want to specify some extra behavior here.
            pass    

    sys.stdout = Logger()

# ===============================================================
#                Dates Calculation
# ===============================================================

def P_delta_days(_d1,_d2):
    return (datetime.strptime(_d1, '%Y%m%d') - datetime.strptime(_d2, '%Y%m%d')).days

def P_delta_months(_d1,_d2):
    return (int(_d1[0:4]) - int(_d2[0:4]))*12+(int(_d1[4:6]) - int(_d2[4:6]))

# ===============================================================
#                Structure Converting
# ===============================================================    

def P_list2str(my_list):
    paragraphs_list = []
    for x in my_list:
        paragraphs_list.append(str(x))
    return ''.join(paragraphs_list)

# ===============================================================
#                File Ops
# ===============================================================

def P_delete_file(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        P_printl("Note : File does not exist!")

def P_del_file_type_in_dir(_path, _type):
    list_file = [ f for f in os.listdir(_path) if f.endswith("."+_type)]
    for _file in list_file:
        os.remove(os.path.join(_path, _file))

def P_write_line(string, path):
    if type(string) is not str:
        print("data is not a str!")
        return -1
    if not os.path.exists(path):
        os.mknod(path)
    with open(path) as fr:
        with open(path, 'a') as fa:
            fa.write(string+'\n')

def P_read_line(_path):
    with open(_path) as f:
        return f.read().splitlines()

def P_read_file(_path):
    with open(_path) as f:
        return f.read()

def P_write_list(list_data, path):
    if type(list_data) is not list:
        print("data is not a list!")
        return -1
    if not os.path.exists(path):
        os.mknod(path)
    for data in list_data:
        P_write_line(str(data), path)

def P_write(data, path): #support list and string now
    if type(data) is str:
        P_write_line(data, path)
    if type(data) is list:
        P_write_list(data, path)

def P_figs_cloud_backup():
    shutil.rmtree('/home/colin/Dropbox/Figs')
    shutil.copytree('Figs','/home/colin/Dropbox/Figs')

def P_get_list_of_files_in_path(path):
    return [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]

def P_copy_file(from_path, to_path):
    shutil.copyfile(from_path, to_path)

# ===============================================================
#                ADB Parsing
# ===============================================================
def P_check_adb_connection():
    while True:
        result_adb = check_output(["adb", "devices"]).decode("utf-8").split(' ')#.find('device') will get sub string cant work
        # print(result_adb)
        result_adb = str(result_adb[4].split('\t')).split('\\')
        # print(result_adb)
        try:
            if 'device' in result_adb[1]:
                P_printl("Found adb device!")
                break
        except:
            print("Got Error in adb connection, retrying...")
            sleep(1)
    sleep(2)

def P_parse_three_bamboo(list_result):
    for i in range(0,min(5,len(list_result))):
        # print("Parsing "+list_result[i][0]+' ...')
        # parse the list_result to droid and track
        # keyevent of 0123456789 in number  pad is adb shell input keyevent 7~16
        # 61 tab 68 enter 4 back 62 space(can be used to select)
        # chinese keyboard got a different layout so need to switch to eng keyboard first manually
        # check adb device first
        
            
        # start auto putting data    
        # call(["adb", "shell", "input", "tap" , "790" , "1739"])
        call(["adb", "shell", "input", "tap" , "753" , "2207"])
        sleep(2)
        # tab first
        # call(["adb", "shell", "input", "keyevent" , "61"]) # no tab is required anymore
        num = ["7","8","9","10","11","12","13","14","15","16"]
        num_1 = int(list_result[i][0].split('_')[1][0])
        num_2 = int(list_result[i][0].split('_')[1][1])
        num_3 = int(list_result[i][0].split('_')[1][2])
        num_4 = int(list_result[i][0].split('_')[1][3])
        call(["adb", "shell", "input", "keyevent" , num[num_1]])
        sleep(0.5)
        call(["adb", "shell", "input", "keyevent" , num[num_2]])
        sleep(0.5)
        call(["adb", "shell", "input", "keyevent" , num[num_3]])
        sleep(0.5)
        call(["adb", "shell", "input", "keyevent" , num[num_4]])
        sleep(0.5)

        # call(["adb", "shell", "input", "tap" , "367" , "710"])
        call(["adb", "shell", "input", "tap" , "361" , "984"])
        sleep(2)
        # call(["adb", "shell", "input", "tap" , "81" , "365"])
        call(["adb", "shell", "input", "tap" , "72" , "463"])
        sleep(1.5)#1.5
        # call(["adb", "shell", "input", "tap" , "962" , "87"])
        call(["adb", "shell", "input", "tap" , "970" , "206"])
        sleep(3.5)#3.5

def P_swipe_change_three_bamboo_page():
    # call(["adb", "shell", "input", "swipe" , "800" , "1000", "200" , "1000"])
    call(["adb", "shell", "input", "swipe" , "800" , "1000", "200" , "1000"])
    sleep(3)

def P_remove_former_three_bamboo(delete_len, tab_len, MAX_LEN_PARSE):
    if delete_len == 0:
        return
    if delete_len > MAX_LEN_PARSE:
        delete_len = MAX_LEN_PARSE
    # call(["adb", "shell", "input", "tap" , "1040" , "100"])
    call(["adb", "shell", "input", "tap" , "1040" , "200"])
    sleep(2)
    for i in range(0,tab_len): # cursor to the first
        call(["adb", "shell", "input", "keyevent" , '61'])
        sleep(0.5)
    while delete_len:
        call(["adb", "shell", "input", "keyevent" , '62']) # space to select
        sleep(0.5)
        for i in range(0,4):
            call(["adb", "shell", "input", "keyevent" , '61']) # move to the next
            sleep(0.5)
        delete_len -= 1

    sleep(1)
    call(["adb", "shell", "input", "keyevent" , '4']) # goto previous page
    sleep(3)

# ===============================================================
#                Window managers
# ===============================================================
def P_switch_back_to_utopia_window():
    #switch the window back, make sure you open Utopia_colin.py or Utopia.py
    os.system("wmctrl -R Utopia_colin.py - Visual Studio Code")
    os.system("wmctrl -R Utopia_anubis.py - Visual Studio Code")
    os.system("wmctrl -R Utopia.py - Visual Studio Code")
    os.system("wmctrl -R Utopia_tools.py - Visual Studio Code")
