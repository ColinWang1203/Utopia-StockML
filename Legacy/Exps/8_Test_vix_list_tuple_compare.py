# Sample : python 8_Test_vix_list_tuple_compare.py 1101
# 
import urllib.request, os
import pandas, sqlite3
import numpy as np
import sys
from datetime import datetime
from itertools import chain

today = datetime.today().strftime("%Y%m%d")
vix_data_length = 20
filename = 'vixcurrent.csv'
if os.path.exists(filename):
  os.remove(filename)
Database_name = 'Avalon.sqlite'
sql_connection1 = sqlite3.connect(Database_name)
sql_cursor1 = sql_connection1.cursor()
# get apple from cmd argv
sql_cursor1.execute('SELECT * FROM apple_'+''.join(sys.argv[1:]))
sql_apples = sql_cursor1.fetchall()

# def parse_command_line():
#     parser = ArgumentParser(description='Welcome to vix Utopia')
#     parser.add_argument('-m', dest='Massive_mode_end_day', default = today, help='-M <massive download an year from date yyyymmdd >')
#     parser.add_argument('-l', dest='length_of_the_date', default = 10000, help='-l <year for 10000, month for 100, day for 1>')
#     parser.add_argument('-d', dest='output_dir', default = 'Apples/', help='-d <output directory>')
#     return parser.parse_args()

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

def extract_vix_data(shift_day):
    db_csv = pandas.read_csv(filename, encoding = 'big5', usecols = [0], header = None)
    # convert pandas.core.frame.DataFrame to numpy.ndarray
    db_array = db_csv.values
    # print(db_array.shape[0])
    max_row = db_array.shape[0] - 1
    skips = max_row - vix_data_length + 1
    print('Extracting data from '+db_array[skips-shift_day]+' to '+db_array[max_row-shift_day])
    # print(list(range(0,skips - shift_day)))
    # print(list(range(max_row - shift_day + 1, max_row + 1)))
    db_csv_filtered = pandas.read_csv(filename, encoding = 'big5', \
            skiprows = list(range(0, skips - shift_day)) + \
                    list(range(max_row - shift_day + 1, max_row + 1)),\
            usecols = range(0,5), header = None)
    # print(db_csv_filtered.values)
    return db_csv_filtered.values

# get the apple in date list
def get_apple_by_date(date):
    count = 0
    apple_tuple_list = [(date_t,) for date_t in date]
    # print(apple_tuple_list)
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

def get_abs_diff_vix_apple_normalized(apple_tuple_list,vix_tuple_list):
    # print(apple_tuple_list)
    # print(vix_tuple_list)
    # Normalize vix to apple==
    # ==Get the ratio==
    apple_w_list = [a[1] for a in apple_tuple_list]
    vix_w_list = [v[1] for v in vix_tuple_list]
    #   change '' into nan then we can use np.nan function to ignore nan
    apple_w_list_np = [np.nan if a == '' else a for a in apple_w_list]
    # no need to handle '' in vix since the vixcurrent.csv will not contain null data
    # vix_w_list = [0 if v == '' else v for v in vix_w_list]
    max_vix = max(vix_w_list)
    min_vix = min(vix_w_list)
    max_apple = np.nanmax(apple_w_list_np)
    min_apple = np.nanmin(apple_w_list_np)
    shift_vix_to_apple = min_vix- min_apple
    ratio_vix_to_apple = (max_vix - min_vix) / (max_apple - min_apple)
    # ==Get the ratio==
    # Count the amount of coresspondind apple cuz it might not exist
    cursor = 0
    abs_diff_list = []
    for v in vix_w_list:
        # print(apple_w_list[cursor])
        # print(v)
        if apple_w_list[cursor]: 
            # first shift to the same min value then compress by first shifting the min_vix then shift back
            v -= shift_vix_to_apple
            v -= min_apple
            v /= ratio_vix_to_apple
            v += min_apple
            # print(v)
            # get diff
            abs_diff_list.append(abs(apple_w_list[cursor] - v))
            # print(abs_diff_list)
        cursor += 1
    # while diff, shift the vix data and "fix" the apple date at newest to compare
    # following is the example of searching the same day as vix, currently do not use it
    # abs_diff_dict = {key: abs(apple_tuple_list_dict[key] - vix_tuple_list_dict.get(key, 0)) \
    #     for key in vix_tuple_list_dict.keys() if apple_tuple_list_dict[key]!=''}
    
    # abs_diff_dict_average = sum(abs_diff_dict.values()) / apple_tuple_list_dict_count
    abs_diff_average = sum(abs_diff_list) / len(abs_diff_list)
    relation_ratio = 1- (abs_diff_average / (max_apple - min_apple))
    # return (relation_ratio,'('+str(len(vix_tuple_list))+'/'+str(len(abs_diff_list))+')')
    return relation_ratio

def main():
    if download_vix():
        print('Error occurred in get_vix()')
        return -1
    day_shift = 0
    day_pointer = ''
    # get latest apple according to latest vix and freeze it
    vix_extract_date_0 = extract_vix_data(0)
    date_in_vix_extract_date_0 = [day[0] for day in vix_extract_date_0]
    apple_tuple_list = get_apple_by_date(date_in_vix_extract_date_0)
    # make sure apple is up to date
    apple_tuple_list_filtered = list(filter(lambda x:all(i is not '' for i in x),apple_tuple_list))
    if len(apple_tuple_list_filtered) < 20:
        print('Apple is not up to date '+'('+str(len(apple_tuple_list_filtered))+'/20)')
        return -1

    relation_ratio_list = []
    while True:    
        if day_shift == 0:
            vix_extract_date = vix_extract_date_0
        else :
            vix_extract_date = extract_vix_data(day_shift)
        day_pointer = vix_extract_date[0][0].split('/')[2] + \
                vix_extract_date[0][0].split('/')[0] + vix_extract_date[0][0].split('/')[1]
        if int(day_pointer) < int(sql_apples[0][0]):
        # if int(day_pointer) < int('20191104'):
            print('Not valid date, Stop')
            break
        # do not shift the date in apple accroding to vix, fix it to latest
        # date_in_vix_extract_date = [day[0] for day in vix_extract_date]
        # apple_tuple_list = get_apple_by_date(date_in_vix_extract_date)

        # need to calcualte the mappings and give it to apple_tuple_list

        vix_tuple_list = [(vix_t[0],vix_t[4]) for vix_t in vix_extract_date]
        relation_ratio = get_abs_diff_vix_apple_normalized(apple_tuple_list,vix_tuple_list)
        print(relation_ratio)
        relation_ratio_list.append(relation_ratio)
        day_shift += 1
        
    # find the max relation_ratio, the index will be the same as day shift
    max_relation_ratio_day_shift = relation_ratio_list.index(max(relation_ratio_list))
    print('Max period is : ')
    extract_vix_data(max_relation_ratio_day_shift)
    print('with '+str(max(relation_ratio_list))+' relation ratio')
    

if __name__ == '__main__':
    main()
