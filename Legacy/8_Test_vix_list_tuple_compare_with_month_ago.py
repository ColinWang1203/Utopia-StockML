import urllib.request, os
import pandas, sqlite3
import numpy as np
from datetime import datetime

today = datetime.today().strftime("%Y%m%d")
#take a month
day_start = str(int(today)-100)
filename = 'vixcurrent.csv'
if os.path.exists(filename):
  os.remove(filename)

def download_vix():
    _url = 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv'

    try:
        urllib.request.urlretrieve(_url, filename)
    except urllib.error.URLError:
        print('Network unreachable or vix not responding')

    # if it is lower than 100kb, there might be some problem in it
    if os.stat(filename).st_size < 100000:
        print(filename+' is corrupted.')
        os.remove(filename)
        return -1
    return 0

def extract_vix_data():
    db_csv = pandas.read_csv(filename, encoding = 'big5', usecols = [0], header = None)
    # convert pandas.core.frame.DataFrame to numpy.ndarray
    db_array = db_csv.values
    date_rearrange = day_start[4]+day_start[5]+'/'+day_start[6]+day_start[7]+'/'\
            +day_start[0]+day_start[1]+day_start[2]+day_start[3]
    #find month ago starts
    date_index = 0
    for i,date_in_vix in enumerate(db_array):
        if date_in_vix == [date_rearrange]:
            date_index = i
    # if month ago happens to be not available, fall back and find data before it
    if date_index == 0:
        day_start_before = day_start
        while date_index == 0:
            day_start_before = str(int(day_start_before)-1)
            date_rearrange = day_start_before[4]+day_start_before[5]+'/'+day_start_before[6]+day_start_before[7]+'/'\
                +day_start_before[0]+day_start_before[1]+day_start_before[2]+day_start_before[3]
            for i,date_in_vix in enumerate(db_array):
                if date_in_vix == [date_rearrange]:
                    date_index = i

    db_csv_filtered = pandas.read_csv(filename, encoding = 'big5', skiprows=date_index-1,\
        usecols = range(0,4), header = None)
    db_array_filtered = db_csv_filtered.values
    print(db_array_filtered.shape)

def main():
    if download_vix():
        print('Error occurred in get_vix()')
        return -1
    extract_vix_data()

if __name__ == '__main__':
    main()
