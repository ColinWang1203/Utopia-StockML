# Sample : python Utopia_slope.py 1101
# find slope apple
import urllib.request, os
import pandas, sqlite3
import numpy as np
import sys, heapq, webbrowser, time, functools
from datetime import datetime
from itertools import chain

today = datetime.today().strftime("%Y%m%d")
Database_name = 'Avalon.sqlite'
sql_connection1 = sqlite3.connect(Database_name)
sql_cursor1 = sql_connection1.cursor()
sql_cursor1.execute("SELECT name FROM sqlite_master WHERE type='table'")
sql_apples = sql_cursor1.fetchall()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_latest_43(today):
    with open('Processed_date_list.txt') as f:
            content = f.read().splitlines()
    return content[-43:]

def examine(date_43, apple):
    sql_cursor1.execute('SELECT * FROM '+''.join(apple[0]))
    sql_apples_data = sql_cursor1.fetchall()

    # convert all INT to STR
    sql_apples_data_date_43 =list(map(str,[i[0] for i in sql_apples_data[-43:]]))

    # check if two date is identical
    if not functools.reduce(lambda i, j : i and j, \
            map(lambda m, k: m == k, date_43, sql_apples_data_date_43), True) :
        print('Some data is missing in '+''.join(apple))
        return False
    # get the apples
    sql_apples_data_range_43 =  sql_apples_data[-43:][:]
    sql_apples_data_range_22 = []
    for m in list(range(0,22)):
        # some apple might contain all the date, but the value in it is not valid
        # so check it
        for i in sql_apples_data_range_43[m:m+22]:
            if not is_number(i[5]):
                print(str(i[5])+' is not a number')
                print('Some data in this date is not valid')
                return False
        range_22_list = [i[5] for i in sql_apples_data_range_43[m:m+22]]
        range_22_list_avg = sum(range_22_list)/len(range_22_list)
        sql_apples_data_range_22.append((str(sql_apples_data[-22+m][0]), range_22_list_avg, sql_apples_data[-22+m][1]))
    # check slope
    if sum([i[1] for i in sql_apples_data_range_22[-20:-15]]) < sum([i[1] for i in sql_apples_data_range_22[-15:-10]]) and \
            sum([i[1] for i in sql_apples_data_range_22[-15:-10]]) < sum([i[1] for i in sql_apples_data_range_22[-10:-5]]) and \
            sum([i[1] for i in sql_apples_data_range_22[-10:-5]]) < sum([i[1] for i in sql_apples_data_range_22[-5:]]):
        # check amount > 1000
        if sum(map(float,[i[2].replace(',','') for i in sql_apples_data_range_22])) / 22 > 1000000:
            return True
        else:
            return False
    else:
        return False

def main():
    # get the latest 43 because the -22 needs -43
    date_43 = get_latest_43(today)
    # get the fitted slope apple for 22 average
    output_list = []
    for apple in sql_apples:
        if examine(date_43, apple):
            output_list.append(apple[0])
    output_list.sort()
    print(output_list)


if __name__ == '__main__':
    main()
