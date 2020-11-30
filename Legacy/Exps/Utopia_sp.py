# Sample : python Utopia_sp.py 1101
# remaining problem : should use processed_date_list.txt to get date in apple
import urllib.request, os
import pandas, sqlite3
import numpy as np
import sys, heapq
import webbrowser, time
import numpy.core.defchararray as np_f
from datetime import datetime
from itertools import chain

today = datetime.today().strftime("%Y%m%d")
sp_data_length = 20
filename = 'currentsp.csv'
Database_name = 'Avalon.sqlite'
sql_connection1 = sqlite3.connect(Database_name)
sql_cursor1 = sql_connection1.cursor()
# get apple from cmd argv
if not sys.argv[1:]:
    print('Did not specify the apple, Exit now ...')
    sys.exit()
sql_cursor1.execute('SELECT * FROM apple_'+''.join(sys.argv[1:]))
sql_apples = sql_cursor1.fetchall()


def download_sp():
    if os.path.exists(filename):
        os.remove(filename)

    _url = 'http://www.digitallook.com/cgi-bin/dlmedia/price_download.cgi/'+\
            'download.csv?action=download&csi=50095'+\
            '&start_day='+today[6:8]+'&start_month='+today[4:6]+'&start_year='+str(int(today[0:4])-1)+\
            '&end_day='+today[6:8]+'&end_month='+today[4:6]+'&end_year='+today[0:4]+'&type=csv'

    try:
        urllib.request.urlretrieve(_url, filename)
    except urllib.error.URLError:
        print('Network unreachable or sp not responding')
        return -1

    # if it is lower than 10kb, there might be some problem in it
    if os.stat(filename).st_size < 10000:
        print(filename+' is corrupted.')
        os.remove(filename)
        return -1
    return 0

def extract_sp_data(shift_day):
    db_csv = pandas.read_csv(filename, encoding = 'big5', usecols = [0], header = None)
    # convert pandas.core.frame.DataFrame to numpy.ndarray
    db_array = db_csv.values
    # print(db_array.shape[0])
    max_row = db_array.shape[0] - 1
    skips = max_row - sp_data_length + 1
    print('Extracting data from '+db_array[skips-shift_day]+' to '+db_array[max_row-shift_day])
    # print(list(range(0,skips - shift_day)))
    # print(list(range(max_row - shift_day + 1, max_row + 1)))
    db_csv_filtered = pandas.read_csv(filename, encoding = 'big5', \
            skiprows = list(range(0, skips - shift_day)) + \
                    list(range(max_row - shift_day + 1, max_row + 1)),\
            usecols = range(0,5), header = None)
    # print(db_csv_filtered.values)

    # transform Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec to 1~12
    db_csv_filtered_value = np.ndarray(shape=(20,5))
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for month in month_list:
        for m in list(range(0,20)):
            day = np.array2string(np_f.replace(db_csv_filtered.values[m][0], month, str("{:02d}".format(month_list.index(month)+1))))
            if db_csv_filtered.values[m][0].split('-')[1] == month:
                db_csv_filtered_value[m][0] = int(day.split('-')[2][0:4]+ day.split('-')[1]+ day.split('-')[0][1:3])
                db_csv_filtered_value[m][1:5] = db_csv_filtered.values[m][1:5]
    # print(db_csv_filtered_value)
    return db_csv_filtered_value

# get the apple in date list
def get_apple_by_date(date):
    count = 0
    apple_tuple_list = [(date_t,) for date_t in date]
    # print(apple_tuple_list)
    for day in date:
        apple_found = False
        for apple in sql_apples:
            the_apple = [index for index in apple if apple[0] == day]
            if the_apple:
                apple_tuple_list[count] += (the_apple[5],)
                apple_found = True
        # if the date is not available, give a '' for dictionary to work properly, cuz dict need 2 (,)
        if not apple_found:
            apple_tuple_list[count] += ('',)     
        count += 1
    return apple_tuple_list

def get_abs_diff_sp_apple_normalized(apple_tuple_list,sp_tuple_list):
    # print(apple_tuple_list)
    # print(vix_tuple_list)
    # Normalize vix to apple==
    # ==Get the ratio==
    apple_w_list = [a[1] for a in apple_tuple_list]
    sp_w_list = [v[1] for v in sp_tuple_list]
    #   change '' into nan then we can use np.nan function to ignore nan
    apple_w_list_np = [np.nan if a == '' else a for a in apple_w_list]
    max_sp = max(sp_w_list)
    min_sp = min(sp_w_list)
    max_apple = np.nanmax(apple_w_list_np)
    min_apple = np.nanmin(apple_w_list_np)
    shift_sp_to_apple = min_sp- min_apple
    ratio_sp_to_apple = (max_sp - min_sp) / (max_apple - min_apple)
    # ==Get the ratio==
    # Count the amount of coresspondind apple cuz it might not exist
    cursor = 0
    abs_diff_list = []
    for v in sp_w_list:
        # print(apple_w_list[cursor])
        # print(v)
        if apple_w_list[cursor]: 
            # first shift to the same min value then compress by first shifting the min_vix then shift back
            v -= shift_sp_to_apple
            v -= min_apple
            v /= ratio_sp_to_apple
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
    if download_sp():
        print('Error occurred in download_sp()')
        return -1
    
    # get latest apple according to latest vix and freeze it
    apple_tuple_list_filtered = []
    day_shift = 0
    while len(apple_tuple_list_filtered) < 20:
        sp_extract_date_0 = extract_sp_data(day_shift)
        date_in_sp_extract_date_0 = [day[0] for day in sp_extract_date_0]
        # print(date_in_sp_extract_date_0)
        apple_tuple_list = get_apple_by_date(date_in_sp_extract_date_0)
        # print(apple_tuple_list)
        # make sure apple is up to date
        apple_tuple_list_filtered = list(filter(lambda x:all(i is not '' for i in x),apple_tuple_list))
        if len(apple_tuple_list_filtered) < 20:
            print('Apple is not up to date '+'('+str(len(apple_tuple_list_filtered))+'/20)')
            print('Shift by one day earlier')
        day_shift += 1
    # print(apple_tuple_list_filtered)
    
    day_shift = 0
    relation_ratio_list = []
    while True:    
        if day_shift == 0:
            sp_extract_date = sp_extract_date_0
        else :
            sp_extract_date = extract_sp_data(day_shift)
        
        day_pointer = sp_extract_date[0][0]
        if day_pointer < int(sql_apples[10][0]):
            print('Not valid date, Stop')
            break

        # compare shifted vix with latest apple
        sp_tuple_list = [(sp_t[0],sp_t[2]) for sp_t in sp_extract_date]
        relation_ratio = get_abs_diff_sp_apple_normalized(apple_tuple_list,sp_tuple_list)
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
    print('Top 3 period is : ')
    max_relation_ratio_day_shift_list = heapq.nlargest(3, range(len(relation_ratio_list)), relation_ratio_list.__getitem__)
    for max_relation_ratio_day_shift in max_relation_ratio_day_shift_list:
        extract_sp_data(max_relation_ratio_day_shift)
        print('with '+str(relation_ratio_list[max_relation_ratio_day_shift])+' relation ratio')

    # open browser for sp
    input("Press Enter to continue...")
    url = 'https://www.google.com/search?ei=bFzoXf-nJYmZr7wP65-K4AM&q=s%26p+500&oq=s%26p+500&gs_l=psy-ab.3..0i67j0i131i67j0i131j0j0i67j0j0i67l2j0l2.11933291.11933655..11933797...0.0..0.104.441.4j1......0....1..gws-wiz.......0i7i30j0i7i10i30j0i8i30j0i203j0i5i30j0i5i10i30.xJbkBHHPLUw&ved=0ahUKEwj_jaHirJ3mAhWJzIsBHeuPAjwQ4dUDCAs&uact=5'
    webbrowser.get('/usr/bin/google-chrome').open(url)
        
    
    

if __name__ == '__main__':
    main()
