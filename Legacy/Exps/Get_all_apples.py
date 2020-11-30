import urllib.request
import calendar, os
from dateutil import rrule
from datetime import datetime
from argparse import ArgumentParser
from time import sleep

today = datetime.today().strftime("%Y%m%d")

def parse_command_line():
    parser = ArgumentParser(description='Welcome to Utopia')
    parser.add_argument('-m', dest='Massive_mode_end_day', default = today, help='-M <massive download an year from date yyyymmdd >')
    parser.add_argument('-l', dest='length_of_the_date', default = 10000, help='-l <year for 10000, month for 100, day for 1>')
    parser.add_argument('-d', dest='output_dir', default = 'Apples/', help='-d <output directory>')
    return parser.parse_args()

def delete_old_file(Apple_location,day_start):
    #delete all the files that are before day_start
    for filename in os.listdir(Apple_location):
        if filename.endswith(".csv") and (int(filename.split('.')[0]) < int(day_start)):
            os.remove(Apple_location+filename)
            print(filename+' is removed')

def download_apples(day_start,day_end, Apple_location, skip_downloaded):
    if skip_downloaded:
        day_start = max([x.split('.')[0] for x in os.listdir('./Apples')])
    # start downloading new apples
    for dt in rrule.rrule(rrule.DAILY, dtstart=datetime.strptime(day_start, '%Y%m%d'),
            until=datetime.strptime(day_end, '%Y%m%d')):
        day = dt.strftime('%Y%m%d')
        csv_file_name = Apple_location+day+'.csv'
        if os.path.exists(csv_file_name):
            # os.remove(csv_file_name)
            print(day+'.csv already exist')
            continue

        _url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date='+day+'&type=ALLBUT0999'
        try:
            urllib.request.urlretrieve(_url, csv_file_name)
        except urllib.error.URLError:
            print('Network unreachable or twse not responding')
            break

        # need delay to prevent twse block our ip for excessive access
        sleep(10)

        # can not use this to test if apple date exist 
        #      >>>   try: urllib.request.urlopen(_url) except urllib.error.URLError:
        # since twse will give you an empty file and the url is acutally exist
        # so check the file size of the csv file
        if os.stat(csv_file_name).st_size == 0:
            print(day+'.csv is not valid.')
            os.remove(csv_file_name)
            continue

        print(day+'.csv is downloaded.')

def main():

    args = parse_command_line()
    day_start = str(int(args.Massive_mode_end_day) - int(args.length_of_the_date))
    day_end = args.Massive_mode_end_day
    Apple_location = args.output_dir
    
    # skip the data that is already downloaded
    download_apples(day_start,day_end ,Apple_location, True)
    # delete file a year ago
    delete_old_file(Apple_location,day_start)
    
if __name__ == '__main__':
    main()

