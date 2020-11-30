import urllib.request
import calendar, os
from dateutil import rrule
from datetime import datetime

day_start = '20191121'
day_end = '20191123'

for dt in rrule.rrule(rrule.DAILY, dtstart=datetime.strptime(day_start, '%Y%m%d'),
        until=datetime.strptime(day_end, '%Y%m%d')):
    day = dt.strftime('%Y%m%d')
    if os.path.exists(day+'.csv'):
        os.remove(day+'.csv')
    _url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date='+day+'&type=ALLBUT0999'
    csv_file_name = day+'.csv'
    urllib.request.urlretrieve(_url, csv_file_name)

    # can not use this to test >>>   try: urllib.request.urlopen(_url) except urllib.error.URLError:
    # since twse will give you an empty file and the url is acutally exist
    # so check the file size of the csv file

    if os.stat(day+'.csv').st_size == 0:
        print(day+'.csv is not valid.')
        os.remove(day+'.csv')
        continue
    print(day+'.csv is downloaded.')
    
        
    



