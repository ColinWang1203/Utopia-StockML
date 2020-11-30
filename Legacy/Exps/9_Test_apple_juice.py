import pandas, os
import requests, sqlite3
from io import StringIO
import time
from datetime import datetime


today = datetime.today().strftime("%Y%m%d")
Database_name = 'Juice.sqlite'
if os.path.exists(Database_name):
  os.remove(Database_name)

sql_connection_Database_name = sqlite3.connect(Database_name)
sql_cursor_Database_name = sql_connection_Database_name.cursor()

# produce date from 99(2010) 100 101 ... today before 10th 
def get_date(date):
    date_y = list(map(str,list(range(2018,int(date[0:4])))))
    date_m = ['%02d'%m for m in list(range(1,13))]
    date_ym = [y+m for y in date_y for m in date_m]

    if date[4:6] == '01':
        return date_ym
    
    if int(date[6:8]) <= 10:
        date_y = date[0:4]
        date_m = ['%02d'%m for m in list(range(1,int(date[4:6])-1))]
        for m in date_m:
            date_ym.append(date_y+m)
    else:
        date_y = date[0:4]
        date_m = ['%02d'%m for m in list(range(1,int(date[4:6])))]
        for m in date_m:
            date_ym.append(date_y+m)
    
    return date_ym

def get_juice(date):
    year = int(date[0:4])-1911
    month = date[4:6]
    if month[0] == '0':
        month = date[5]
    # print(year)
    # print(month)
    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'
    
    # Fake browser
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    r = requests.get(url, headers=headers)
    r.encoding = 'big5'

    dfs = pandas.read_html(StringIO(r.text), encoding='big-5')

    df = pandas.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])
    
    if 'levels' in dir(df.columns):
        df.columns = df.columns.get_level_values(1)
    else:
        df = df[list(range(0,10))]
        column_index = df.index[(df[0] == '公司代號')][0]
        df.columns = df.iloc[column_index]
    
    df['當月營收'] = pandas.to_numeric(df['當月營收'], 'coerce')
    df = df[~df['當月營收'].isnull()]
    df = df[df['公司代號'] != '合計']

    # add delay to prevent ip blocking
    time.sleep(10)
    print(df.values.tolist())
    return df.values.tolist()

def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

# squeeze into db, date is like YYYYMM
def squeeze(date):
    print('Processing date '+date+' ...')
    # ignore date that is alreay processed
    with open('Processed_juice_list.txt') as f:
        if date in f.read():
            print('Skiping '+date)
            return 0

    # get all the apples in the juice date, then init them
    juices_all = get_juice(date)
    # for 99~101 the length is 10
    if len(juices_all[0]) == 10:
        juices = [(i[0],i[2],i[7]) for i in juices_all if isint(i[0])]
    elif len(juices_all[0]) == 11:
        juices = [(i[0],i[7],i[10]) for i in juices_all if isint(i[0])]
    else:
        print('Juice format has changed, stop now ...')
        return -1

    juices.sort(key = lambda x: x[0])

    # print(juices)

    for juice in juices:
        sql_create_cmd = 'CREATE TABLE IF NOT EXISTS apple_'+juice[0]+' (date INT, current INT, accumu INT)'
        sql_cursor_Database_name.execute(sql_create_cmd)
        sql_write_cmd = 'INSERT INTO apple_'+juice[0]+' (date, current, accumu) values\
                ("'+date+'","'+str(juice[1])+'", "'+str(juice[2])+'")'
        sql_cursor_Database_name.execute(sql_write_cmd)
    
    sql_connection_Database_name.commit()

    # Record the processed date
    with open('Processed_juice_list.txt') as fr:
        with open('Processed_juice_list.txt', 'a') as fa:
            if date not in fr.read():
                fa.write('%s\n' % date)

    
def main():
    # date_ym_list = get_date(today)
    # print(date_ym_list)
    # for date_ym in date_ym_list:
    #     squeeze(date_ym)
    squeeze('201001')

if __name__ == '__main__':
    main()