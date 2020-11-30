
# make sure do this every day

import urllib.request, pandas, os, sqlite3
from datetime import date, datetime
from Utopia_tools import *

# if os.path.exists('DB_Seeds.sqlite'):
#     os.remove('DB_Seeds.sqlite')

Database_seeds_name = 'DB_Seeds.sqlite'
sql_connection_Database_seeds_name = sqlite3.connect(Database_seeds_name)
sql_cursor_Database_seeds_name = sql_connection_Database_seeds_name.cursor()

# today = date.today().strftime("%Y%m%d")

def Get_seeds():
    _url = 'https://smart.tdcc.com.tw/opendata/getOD.ashx?id=1-5'

    # currently not knowing the date in csv, give it temp
    csv_file_name_temp = 'Seeds/temp.csv'
    urllib.request.urlretrieve(_url, csv_file_name_temp)

    # get the date in csv
    df = pandas.read_csv(csv_file_name_temp, encoding = 'utf8')
    df_date = str(df['資料日期'][0])
    
    # example of how to get the pure data
    # print(df.iloc[1].values)
    '''
    [20191227 '0050' 2 46925 87934309 12.55]
    '''
    
    # get the lastest date in processed date and check until today
    with open('Processed_seeds_date_list.txt') as f:
        lines = f.read().splitlines()
        latest_data_date = lines[-1]

    if df_date == latest_data_date:
        os.remove(csv_file_name_temp)
        print('No new seeds found')
        return 0

    # check if missing any date info https://www.tdcc.com.tw/smWeb/QryStock.jsp
    delta_days = (datetime.today() - datetime.strptime(latest_data_date, '%Y%m%d')).days
    if delta_days > 8:
        if not YN_Check('More than 8 days not updated, did you check https://www.tdcc.com.tw/smWeb/QryStock.jsp ?'):
            print('aborting')
            C()

    # Rename the csv
    os.rename(csv_file_name_temp, 'Seeds/'+df_date+'.csv')

    # date is different, start parsing, assuming every data
    # contains perfectly 17 rows
    # while True:
    
    j=0
    while True:
        df_row_list = []
        try:
            df_row_list.append(df.iloc[j][0])
            apple_num = df.iloc[j][1]
            sql_create_cmd = 'CREATE TABLE IF NOT EXISTS apple_'+apple_num+' (date INT UNIQUE,\
                    n1 FLOAT, n2 FLOAT, n3 FLOAT, n4 FLOAT, n5 FLOAT, \
                    n6 FLOAT, n7 FLOAT, n8 FLOAT, n9 FLOAT, n10 FLOAT, \
                    n11 FLOAT, n12 FLOAT, n13 FLOAT, n14 FLOAT, n15 FLOAT)'
            sql_cursor_Database_seeds_name.execute(sql_create_cmd)
        except IndexError:
            print('Reach the end of seeds')
            print('===== Seeds Done =====')
            break
        for i in list(range(15)):
            df_row_list.append(df.iloc[j+i][5])
        
        # use INSERT OR IGNORE to avoid getting errors when inserting duplcate item
        sql_write_cmd = 'INSERT OR IGNORE INTO apple_'+apple_num+' (date\
                , n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15) values\
                ("'+str(df_row_list[0])+'","'+str(df_row_list[1])+'",\
                 "'+str(df_row_list[2])+'","'+str(df_row_list[3])+'",\
                 "'+str(df_row_list[4])+'","'+str(df_row_list[5])+'",\
                 "'+str(df_row_list[6])+'","'+str(df_row_list[7])+'",\
                 "'+str(df_row_list[8])+'","'+str(df_row_list[9])+'",\
                 "'+str(df_row_list[10])+'","'+str(df_row_list[11])+'",\
                 "'+str(df_row_list[12])+'","'+str(df_row_list[13])+'",\
                 "'+str(df_row_list[14])+'","'+str(df_row_list[15])+'")'
        sql_cursor_Database_seeds_name.execute(sql_write_cmd)
        sql_connection_Database_seeds_name.commit()

        j += 17

    with open('Processed_seeds_date_list.txt') as fr:
        with open('Processed_seeds_date_list.txt', 'a') as fa:
            if df_date not in fr.read():
                fa.write('%s\n' % df_date)
    return 1


Get_seeds()


