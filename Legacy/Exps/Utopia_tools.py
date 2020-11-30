import pandas, sqlite3, requests, calendar, os, urllib.request, sys
import numpy as np
from dateutil import rrule
from datetime import date, datetime
from argparse import ArgumentParser
from time import sleep
from io import StringIO

# Easy rpogram stop
def C():
    sys.exit()

# Create an NaN
def nan():
    return float('nan')

# Create printing a line
def L(sleep_secs=0):
    print('========================================')
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
    if remove_old:
        os.remove(filename)
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
    
def compare_string(s1,s2):
	if str(s1) == str(s2):
		return True
	else:
		return False
		
def del_all_fig(Fig_dir):
    filelist = [ f for f in os.listdir(Fig_dir) if f.endswith(".jpg") ]
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
    