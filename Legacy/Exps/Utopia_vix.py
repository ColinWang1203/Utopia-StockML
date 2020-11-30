# Sample : python Utopia_vix.py 1101
# start date get from latest vix, if it's more than a week delay, stop
# freeze apple find vix, show the most related period of vix
import urllib.request, os
import pandas, sqlite3
import numpy as np
import matplotlib.pyplot as plt
import sys, heapq, webbrowser, time
from Utopia_tools import *
from datetime import datetime
from itertools import chain

today = datetime.today()#.strftime("%Y%m%d")
vix_data_length = 20
filename = 'currentvix.csv'
if os.path.exists(filename):
  os.remove(filename)
Database_name = 'DB_Avalon.sqlite'
sql_connection1 = sqlite3.connect(Database_name)
sql_cursor1 = sql_connection1.cursor()
# get apple from cmd argv
if not sys.argv[1:]:
    print('Did not specify the apple, Exit now ...')
    sys.exit()
sql_cursor1.execute('SELECT * FROM apple_'+''.join(sys.argv[1:]))
sql_apples = sql_cursor1.fetchall()


def download_vix():
    _url = 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv'

    try:
        urllib.request.urlretrieve(_url, filename)
    except urllib.error.URLError:
        print('Network unreachable or vix not responding')
        return -1

    # if it is lower than 100kb, there might be some problem in it
    if os.stat(filename).st_size < 100000:
        print(filename+' is corrupted.')
        os.remove(filename)
        return -1
    return 0

def print_date(shift_day):
    db_csv = pandas.read_csv(filename, encoding = 'big5', usecols = [0], header = None)
    db_array = db_csv.values
    max_row = db_array.shape[0] - 1
    skips = max_row - vix_data_length + 1
    return (db_array[skips-shift_day]+' to '+db_array[max_row-shift_day])

def extract_vix_data(shift_day):
    db_csv = pandas.read_csv(filename, encoding = 'big5', usecols = [0], header = None)
    # convert pandas.core.frame.DataFrame to numpy.ndarray
    db_array = db_csv.values
    max_row = db_array.shape[0] - 1
    skips = max_row - vix_data_length + 1
    # print('Extracting data from '+db_array[skips-shift_day]+' to '+db_array[max_row-shift_day])
    db_csv_filtered = pandas.read_csv(filename, encoding = 'big5', \
            skiprows = list(range(0, skips - shift_day)) + \
                    list(range(max_row - shift_day + 1, max_row + 1)),\
            usecols = range(0,5), header = None)
    # if the shift_day = 0, check the latest date in vix if it's not delaying more than a week
    if shift_day == 0:
        d1 = datetime.strptime(db_csv_filtered.values[-1][0], "%m/%d/%Y")#.strftime("%Y-%m-%d")
        TimeDiff = today - d1
        if TimeDiff.days > 7:
            print("Might be some error in vix data, aborting...")
            C()
    
    ''' db_csv_filtered.values : 
    [['11/21/2019' 13.35 13.86 12.49 13.13]
    ['11/22/2019' 12.82 13.25 12.33 12.34]
    ['11/25/2019' 12.51 12.59 11.73 11.87]
    ['11/26/2019' 11.88 12.04 11.42 11.54]
    ['11/27/2019' 11.55 11.79 11.44 11.75]
    ['11/29/2019' 12.5 12.83 12.12 12.62]
    ['12/02/2019' 12.69 15.27 12.55 14.91]
    ['12/03/2019' 14.68 17.99 14.61 15.96]
    ['12/04/2019' 16.38 16.4 14.12 14.8]
    ['12/05/2019' 14.46 15.37 14.17 14.52]
    ['12/06/2019' 14.37 14.47 13.19 13.62]
    ['12/09/2019' 14.25 16.07 12.25 15.86]
    ['12/10/2019' 15.8 16.9 14.93 15.68]
    ['12/11/2019' 15.57 15.97 14.98 14.99]
    ['12/12/2019' 14.94 15.55 13.6 13.94]
    ['12/13/2019' 13.18 14.35 12.54 12.63]
    ['12/16/2019' 12.47 12.53 11.71 12.14]
    ['12/17/2019' 12.23 12.47 11.9 12.29]
    ['12/18/2019' 12.24 12.7 11.93 12.58]
    ['12/19/2019' 12.55 12.78 12.43 12.5]]
    '''
    return db_csv_filtered.values

# get the apple in date list
def get_apple_by_date(date):
    count = 0
    apple_tuple_list = [(date_t,) for date_t in date]
    ''' date
    ['11/21/2019', '11/22/2019', '11/25/2019', '11/26/2019', '11/27/2019',
     '11/29/2019', '12/02/2019', '12/03/2019', '12/04/2019', '12/05/2019',
     '12/06/2019', '12/09/2019', '12/10/2019', '12/11/2019', '12/12/2019',
     '12/13/2019', '12/16/2019', '12/17/2019', '12/18/2019', '12/19/2019']
    '''
    for day in date:
        apple_found = False
        for apple in sql_apples:
            date_arrange = day.split('/')[2]+ day.split('/')[0]+ day.split('/')[1]
            the_apple = [index for index in apple if str(apple[0]) == date_arrange]
            if the_apple:
                apple_tuple_list[count] += (the_apple[5],)
                apple_found = True
        # if the date is not available, give a '' for dictionary to work properly, cuz dict need 2 (,)
        if not apple_found:
            apple_tuple_list[count] += ('',)     
        count += 1
    return apple_tuple_list

def plot_vix_apple(apple_tuple_list,vix_tuple_list):
    apple_w_list = [a[1] for a in apple_tuple_list]
    vix_w_list = [v[1] for v in vix_tuple_list]
    apple_w_list_np = [np.nan if a == '' else a for a in apple_w_list]
    max_vix = max(vix_w_list)
    min_vix = min(vix_w_list)
    max_apple = np.nanmax(apple_w_list_np)
    min_apple = np.nanmin(apple_w_list_np)
    shift_vix_to_apple = min_vix- min_apple
    ratio_vix_to_apple = (max_vix - min_vix) / (max_apple - min_apple)

    vix_w_list_map = []
    for m in vix_w_list:
        vix_w_list_map.append((m - shift_vix_to_apple - min_apple)/ratio_vix_to_apple + min_apple)

    date = [a[0] for a in apple_tuple_list]
    plt.plot(date, apple_w_list)
    plt.plot(date, vix_w_list_map)
    mngr = plt.get_current_fig_manager()
    geom = mngr.window.geometry()
    x,y,dx,dy = geom.getRect()
    mngr.window.setGeometry(0,0,dx,dy)
    plt.show(block=False)
    plt.pause(3)
    plt.close('all')


def get_dot_product_vix_norm_apple(apple_tuple_list,vix_tuple_list):
    # Normalize vix to apple==
    # ==Get the ratio==
    apple_w_list = [a[1] for a in apple_tuple_list]
    vix_w_list = [v[1] for v in vix_tuple_list]
    # change '' into nan then we can use np.nan function to ignore nan for gettinh max and min
    apple_w_list_np = [np.nan if a == '' else a for a in apple_w_list]
    # no need to handle '' in vix since the vixcurrent.csv will not contain null data
    # vix_w_list = [0 if v == '' else v for v in vix_w_list]
    # normalize the vix to fit in apple
    max_vix = max(vix_w_list)
    min_vix = min(vix_w_list)
    max_apple = np.nanmax(apple_w_list_np)
    min_apple = np.nanmin(apple_w_list_np)
    shift_vix_to_apple = min_vix- min_apple
    ratio_vix_to_apple = (max_vix - min_vix) / (max_apple - min_apple)
    # ==Get the ratio==
    # Count the amount of coresspondind apple cuz it might not exist
    cursor = 0
    np_dot_list = []

    # iterate by two elements 
    # ex:
    # l = [1,2,3,4,5,6]
    # for i,j in list(zip(l,l[1:])):
    #   print(str(i)+','+str(j))
    #
    # output :
    # 1,2
    # 2,3
    # 3,4
    # 4,5
    # 5,6

    for v1,v2 in list(zip(vix_w_list,vix_w_list[1:])):
        # print(apple_w_list)
        if apple_w_list[cursor+1]: 
            # first shift to the same min value then compress by first shifting the min_vix then shift back
            v1 -= shift_vix_to_apple
            v1 -= min_apple
            v1 /= ratio_vix_to_apple
            v1 += min_apple
            v2 -= shift_vix_to_apple
            v2 -= min_apple
            v2 /= ratio_vix_to_apple
            v2 += min_apple
            # get diff >> This is a bad idea, we should use the dot product instead
            # abs_diff_list.append(abs(apple_w_list[cursor] - v))
            
            # get the dot product here, assume the x axis is 10% of max_apple
            # print(apple_w_list[cursor+1])
            
            vix_vector = [max_apple/10 , v2-v1]
            # make the '' data becomes a zero vector to calculate
            if apple_w_list[cursor+1] == '' or apple_w_list[cursor] == '':
                apple_vector = [0, 0]
            else:
                apple_vector = [max_apple/10 , apple_w_list[cursor+1]-apple_w_list[cursor]]
            np_dot_list.append(np.dot(apple_vector, vix_vector))
            # print(apple_vector)
            # print(vix_vector)
            # print(np.dot(apple_vector, vix_vector))

        cursor += 1
    # while diff, shift the vix data and "fix" the apple date at newest to compare
    # following is the example of searching the same day as vix, currently do not use it
    # abs_diff_dict = {key: abs(apple_tuple_list_dict[key] - vix_tuple_list_dict.get(key, 0)) \
    #     for key in vix_tuple_list_dict.keys() if apple_tuple_list_dict[key]!=''}

    relation_ratio = sum(np_dot_list)

    return relation_ratio


def get_avg_in_20(vix_data):
    all_close = [i[4] for i in vix_data]
    return avg(all_close)

def main():
    if download_vix():
        print('Error occurred in get_vix()')
        return -1
    
    # get latest apple according to latest vix and freeze it
    apple_tuple_list_filtered = []
    day_shift = 0
    while len(apple_tuple_list_filtered) < vix_data_length:
        vix_extract_date_0 = extract_vix_data(day_shift)
        date_in_vix_extract_date_0 = [day[0] for day in vix_extract_date_0]
        apple_tuple_list = get_apple_by_date(date_in_vix_extract_date_0)
        # make sure apple is up to date
        apple_tuple_list_filtered = list(filter(lambda x:all(i is not '' for i in x),apple_tuple_list))
        ''' apple_tuple_list_filtered
        [('11/21/2019', 77.6), ('11/22/2019', 77.8), ('11/25/2019', 77.4), ('11/26/2019', 79.0), 
        ('11/27/2019', 78.5), ('11/29/2019', 77.5), ('12/02/2019', 78.0), ('12/03/2019', 77.6), 
        ('12/04/2019', 77.2), ('12/05/2019', 77.9), ('12/06/2019', 77.4), ('12/09/2019', 77.3), 
        ('12/10/2019', 78.5), ('12/11/2019', 78.8), ('12/12/2019', 78.0), ('12/13/2019', 77.4), ('12/16/2019', 77.7)]
        '''
        if len(apple_tuple_list_filtered) < vix_data_length:
            print('Apple is not up to date '+'('+str(len(apple_tuple_list_filtered))+'/20)')
            print('Shift by one day earlier')
        day_shift += 1
    
    day_shift = vix_data_length
    day_pointer = ''
    relation_ratio_list = []
    # shifting algo is here
    while True:    
        vix_extract_date = extract_vix_data(day_shift)
        day_pointer = vix_extract_date[0][0].split('/')[2] + \
                vix_extract_date[0][0].split('/')[0] + vix_extract_date[0][0].split('/')[1]
        if int(day_pointer) < int(sql_apples[0][0]):
            print('Not valid date, Stop')
            break

        # compare shifted vix with latest apple
        vix_tuple_list = [(vix_t[0],vix_t[4]) for vix_t in vix_extract_date]
        relation_ratio = get_dot_product_vix_norm_apple(apple_tuple_list,vix_tuple_list)
        # print(relation_ratio)
        relation_ratio_list.append(relation_ratio)
        day_shift += 1
        
    # find the max relation_ratio, the index will be the same as day shift
    print('Apple is :')
    print(apple_tuple_list_filtered)
    # print('Best period is : ')
    # max_relation_ratio_day_shift = relation_ratio_list.index(max(relation_ratio_list))
    # extract_vix_data(max_relation_ratio_day_shift)
    # print('with '+str(max(relation_ratio_list))+' relation ratio')
    avg_diff_list = []
    # get the prediction here, without uncertainty boundary
    print('Top 3 period is : ')
    max_relation_ratio_day_shift_list = heapq.nlargest(3, range(len(relation_ratio_list)), relation_ratio_list.__getitem__)
    max_relation_ratio_day_shift_list = [i+vix_data_length for i in max_relation_ratio_day_shift_list]
    for max_relation_ratio_day_shift in max_relation_ratio_day_shift_list:
        v = extract_vix_data(max_relation_ratio_day_shift)
        print(print_date(max_relation_ratio_day_shift)+' with '+str(relation_ratio_list[max_relation_ratio_day_shift])+' relation ratio')
        # Get the average of 20 and compare to next 20
        avg_20 = get_avg_in_20(v)
        avg_next_20 = get_avg_in_20(extract_vix_data(max_relation_ratio_day_shift-vix_data_length))
        # Get the percentage of increase or decrease in avg
        avg_diff = (avg_next_20 - avg_20) / avg_20 * 100 # in %
        avg_diff_list.append(avg_diff)

        # plot_vix_apple(apple_tuple_list,v)

    avg_diff_list_avg = avg(avg_diff_list)
    
    # Find the confidence of relationship between vix and apple
    # Get the average next month vix and apple and normalize diff them
    # Start from shifting the day by 20 and do an year
    # Do an average for the top 3 for next month and compare to average of 20 vix

    # Start by shifting vix 20 day
    day_shift_outer = vix_data_length
    day_pointer = ''
    vix_apple_diff_abs_list = []
    while True:
        print('Current day shift = '+str(day_shift_outer)+' : '+print_date(day_shift_outer))
        day_shift_inner = vix_data_length
        relation_ratio_list = []

        vix_extract_date = extract_vix_data(day_shift_outer)
        day_pointer = vix_extract_date[0][0].split('/')[2] + \
                vix_extract_date[0][0].split('/')[0] + vix_extract_date[0][0].split('/')[1]
        if int(day_pointer) < int(sql_apples[0][0]):
            print('Not valid date, Stop')
            break
        date_in_vix_extract_date = [day[0] for day in vix_extract_date]
        apple_tuple_list = get_apple_by_date(date_in_vix_extract_date)
    
        while True:    
            vix_extract_date_inner = extract_vix_data(day_shift_inner)
            day_pointer = vix_extract_date_inner[0][0].split('/')[2] + \
                    vix_extract_date_inner[0][0].split('/')[0] + vix_extract_date_inner[0][0].split('/')[1]
            if int(day_pointer) < int(sql_apples[0][0]):
                # print('Not valid date, Stop')
                break

            # compare shifted vix with latest apple
            vix_tuple_list = [(vix_t[0],vix_t[4]) for vix_t in vix_extract_date_inner]
            relation_ratio = get_dot_product_vix_norm_apple(apple_tuple_list,vix_tuple_list)
            # print(relation_ratio)
            relation_ratio_list.append(relation_ratio)
            day_shift_inner += 1

        max_relation_ratio_day_shift_list = heapq.nlargest(3, range(len(relation_ratio_list)), relation_ratio_list.__getitem__)
        # need to also shift the max_relation_ratio_day_shift_list with the initial day_shift_inner
        max_relation_ratio_day_shift_list = [i+vix_data_length for i in max_relation_ratio_day_shift_list]

        for max_relation_ratio_day_shift in max_relation_ratio_day_shift_list:
            vix_extract_date = extract_vix_data(max_relation_ratio_day_shift)
            date_in_vix_extract_date = [day[0] for day in vix_extract_date]
            apple_tuple_list = get_apple_by_date(date_in_vix_extract_date)
            apple_tuple_list_filtered = list(filter(lambda x:all(i is not '' for i in x),apple_tuple_list))

            vix_extract_date_next20 = extract_vix_data(max_relation_ratio_day_shift-vix_data_length)
            date_in_vix_extract_date_next20 = [day[0] for day in vix_extract_date_next20]
            apple_tuple_list_next20 = get_apple_by_date(date_in_vix_extract_date_next20)
            apple_tuple_list_filtered_next20 = list(filter(lambda x:all(i is not '' for i in x),apple_tuple_list_next20))

            vix_avg = avg([i[4] for i in vix_extract_date])
            apple_avg = avg([i[1] for i in apple_tuple_list_filtered])
            vix_avg_next20 = avg([i[4] for i in vix_extract_date_next20])
            apple_avg_next20 = avg([i[1] for i in apple_tuple_list_filtered_next20])

            vix_avg_diff = (vix_avg_next20 - vix_avg) / vix_avg * 100
            apple_avg_diff = (apple_avg_next20 - apple_avg) / apple_avg * 100

            vix_apple_diff_abs = abs(vix_avg_diff - apple_avg_diff)
            vix_apple_diff_abs_list.append(vix_apple_diff_abs)
        day_shift_outer += 1

    vix_apple_diff_abs_list_avg = avg(vix_apple_diff_abs_list)

    # Show the Result
    L()
    print('Prediction : '+str(int(avg_diff_list_avg)-int(vix_apple_diff_abs_list_avg))+'%'\
            +'~'+str(int(avg_diff_list_avg)+int(vix_apple_diff_abs_list_avg))+'% for next month')
    L()



    # open browser for vix
    # input("Press Enter to continue...")
    # url = 'https://www.macromicro.me/charts/47/vix'
    # webbrowser.get('/usr/bin/google-chrome').open(url)
    
    

if __name__ == '__main__':
    main()

