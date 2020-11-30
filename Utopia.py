from Utopia_tools import *

# ===== Global vars =====

today = datetime.today().strftime("%Y%m%d")

# Databases
Database_name = 'DB_Utopia.sqlite'
sql_connection_Database_name = sqlite3.connect(Database_name)
sql_cursor_Database_name = sql_connection_Database_name.cursor()
Database_squeeze_name = 'DB_Avalon.sqlite'
sql_connection_Database_squeeze_name = sqlite3.connect(Database_squeeze_name)
sql_cursor_Database_squeeze_name = sql_connection_Database_squeeze_name.cursor()
Database_juice_name = 'DB_Juice.sqlite'
sql_connection_Database_juice_name = sqlite3.connect(Database_juice_name)
sql_cursor_Database_juice_name = sql_connection_Database_juice_name.cursor()
Database_seeds_name = 'DB_Seeds.sqlite'
sql_connection_Database_seeds_name = sqlite3.connect(Database_seeds_name)
sql_cursor_Database_seeds_name = sql_connection_Database_seeds_name.cursor()

P_enable_logging()

# =======================

def parse_command_line():
    
    parser = ArgumentParser(description='Welcome to Utopia')
    parser.add_argument('-m', dest='Massive_mode_end_day', default = today, help='-M <massive download an year from date yyyymmdd >')
    parser.add_argument('-l', dest='length_of_the_date', default = 10000, help='-l <year for 10000, month for 100, day for 1>')
    parser.add_argument('-d', dest='output_dir', default = 'Apples/', help='-d <output directory>')
    return parser.parse_args()

def delete_old_apples(Apple_location,day_start):

    #delete all the files that are before day_start
    for filename in os.listdir(Apple_location):
        if filename.endswith(".csv") and (int(filename.split('.')[0]) < int(day_start)):
            os.remove(Apple_location+filename)
            print(filename+' is removed')

def download_apples(day_start,day_end, Apple_location, skip_downloaded):
    if P_read_line('Processed_date_list.txt')[-1] == today:
        return 0
    first_start = True
    _url = 'https://www.google.com.tw/?hl=zh-TW'
    try:
        webbrowser.open_new_tab(_url)
        sleep(2)
    except Exception as e:
        P_switch_back_to_utopia_window()
        P_printl(e)
        print('Network unreachable')
        return -1
    P_switch_back_to_utopia_window()

    if skip_downloaded:
        day_start = max([x.split('.')[0] for x in os.listdir('./Apples')])
        # increment by one day
        day_start = (datetime.strptime(day_start, '%Y%m%d')+relativedelta.relativedelta(days=1)).strftime('%Y%m%d')

    # start downloading new apples
    for dt in rrule.rrule(rrule.DAILY, dtstart=datetime.strptime(day_start, '%Y%m%d'),
            until=datetime.strptime(day_end, '%Y%m%d')):
        
        if not first_start:
            print("Delaying for 5 seconds...")
            sleep(5)# prevent excessive access ip blocking

        day = dt.strftime('%Y%m%d')
        csv_file_name = Apple_location+day+'.csv'
        desktop_csv = "/home/colin/Desktop/MI_INDEX_ALLBUT0999_"+day+".csv"
        P_switch_back_to_utopia_window()
        if os.path.exists(csv_file_name):
            print(day+'.csv already exist')
            continue

        _url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date='+day+'&type=ALLBUT0999'
        try:
            # urllib.request.urlretrieve(_url, csv_file_name)
            # twse might block above way, should open a browser
            webbrowser.open_new_tab(_url)
            sleep(2)
        except Exception as e:
            P_switch_back_to_utopia_window()
            P_printl(e)
            print('Network unreachable or twse not responding')
            return -1

        P_switch_back_to_utopia_window()
        # check if exist or we might be blocked
        try:
            downloaded_csv = glob.glob("/home/colin/Desktop/MI_INDEX_ALLBUT0999_*.csv")[0]
        except IndexError:
            print("Download failed, aborting...")
            return -1

        if downloaded_csv == '':
            print('Network unreachable or twse not responding')
            return -1
        # since if you open a browswe and download a wrong day it will auto shift
        # ex : download 0926(sat) and it will download 0928(mon)
        # need to remove the file and continue doing it
        
        if downloaded_csv != desktop_csv:
            print(day+'.csv is not valid.')
            os.remove(downloaded_csv)
            continue

        #rename it for /home/colin/Desktop/MI_INDEX_ALLBUT0999_yyyymmdd.csv to Apples/yyyymmdd.csv
        shutil.move(desktop_csv, "Apples/"+day+".csv")

        # can not use this to test if apple date exist 
        #      >>>   try: urllib.request.urlopen(_url) except urllib.error.URLError:
        # since twse will give you an empty file and the url is acutally exist
        # so check the file size of the csv file
        if os.stat(csv_file_name).st_size == 0:
            print(day+'.csv is not valid.')
            os.remove(csv_file_name)
            continue
        # if it is lower than 80kb, there might be some problem in it
        if os.stat(csv_file_name).st_size < 80000:
            print(day+'.csv is corrupted. Manully check if needed!')
            os.remove(csv_file_name)
            return -1

        print(day+'.csv is downloaded.')
        first_start = False
    
    return 0

def Harvest():

    date_all = [x.split('.')[0] for x in os.listdir('./Apples')]

    # Create Utopia
    for date in sorted(date_all):
        # ignore date that is alreay processed
        with open('Processed_date_list.txt') as f:
            if date in f.read():
                # print('Skiping '+date)
                continue

        filename = './Apples/'+date+'.csv'
        print('Initializing index_'+date)

        # take only the first column and remove the header to truly get all the csv file(first line won't become header)
        db_csv = pandas.read_csv(filename, encoding = 'big5', usecols = [0], header = None)

        # convert pandas.core.frame.DataFrame to numpy.ndarray
        db_array = db_csv.values
        # find where the first one starts, +1 is needed because csv starts from 1
        start_row = int(np.where(db_array == '1101')[0]+1)
        db_csv_filtered = pandas.read_csv(filename, encoding = 'big5', skiprows=start_row,\
            usecols = [0,2,*range(5, 9)], header = None)
        db_array = db_csv_filtered.values

        # note that number can not be the first letter, so add index_
        sql_create_cmd = 'CREATE TABLE index_'+date+' (num INT, amount INT, starts DOUBLE, highs DOUBLE,\
            lows DOUBLE, ends DOUBLE)'
        sql_cursor_Database_name.execute(sql_create_cmd)

        for row in range(db_array.shape[0]):
            sql_write_cmd = 'INSERT INTO index_'+date+' (num, amount, starts, highs, lows, ends) values\
            ("'+db_array[row][0]+'", "'+db_array[row][1]+'", "'+db_array[row][2]+'"\
            , "'+db_array[row][3]+'", "'+db_array[row][4]+'", "'+db_array[row][5]+'")'
            sql_cursor_Database_name.execute(sql_write_cmd)
        # remember to commit after you write
        sql_connection_Database_name.commit()
        

    # Create Avalon
    # get tables in Utopia
    sql_cursor_Database_name.execute("SELECT name FROM sqlite_master WHERE type='table'")
    sql_tables_Database_name = sql_cursor_Database_name.fetchall()

    for table in sorted(sql_tables_Database_name):
        # convert tuple into string
        table_str = ''.join(table)
        apple_date = str(table_str.split('_')[1])
        # skip the processed one
        with open('Processed_date_list.txt') as f:
            if apple_date in f.read():
                # print('Skiping '+apple_date)
                continue
        # start loading
        print('Loading apples in '+table_str)
        sql_cursor_Database_name.execute("SELECT * FROM "+table_str+"")
        sql_apples = sql_cursor_Database_name.fetchall()

        for apple in sql_apples:
            sql_create_cmd = 'CREATE TABLE IF NOT EXISTS apple_'+str(apple[0])+' (date INT, amount INT, starts DOUBLE, highs DOUBLE,\
                    lows DOUBLE, ends DOUBLE)'
            sql_cursor_Database_squeeze_name.execute(sql_create_cmd)
            sql_write_cmd = 'INSERT INTO apple_'+str(apple[0])+' (date, amount, starts, highs, lows, ends) values\
                    ( "'+apple_date+'","'+str(apple[1])+'", "'+str(apple[2])+'", "'+str(apple[3])+'"\
                    , "'+str(apple[4])+'", "'+str(apple[5])+'")'
            sql_cursor_Database_squeeze_name.execute(sql_write_cmd)
            sql_connection_Database_squeeze_name.commit()

    # Record the processed date
    for date in sorted(date_all):
        with open('Processed_date_list.txt') as fr:
                with open('Processed_date_list.txt', 'a') as fa:
                    if date not in fr.read():
                        fa.write('%s\n' % date)

    sql_connection_Database_name.close()
    sql_connection_Database_squeeze_name.close()

# produce date from 99(2010) 100 101 ... today before 10th 
def get_date(date):

    now_datetime = datetime.strptime(date, '%Y%m%d')
    start_date = datetime.strptime('20100110', '%Y%m%d')
    date_ym = []
    while start_date <= now_datetime:
        date_ym.append(start_date.strftime('%Y%m'))
        start_date += relativedelta.relativedelta(months=1)
    # pop out extra month
    date_ym.pop()
    
    return date_ym

def get_juice(date):

    year = int(date[0:4])-1911
    month = date[4:6]
    if month[0] == '0':
        month = date[5]
    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'
    
    # Fake browser
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    r.encoding = 'big5'

    try :
        dfs = pandas.read_html(StringIO(r.text), encoding='big-5')
    except :
        print('Juice '+date+' is not ready.')
        return -1

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

    print(df)

    # add delay to prevent ip blocking
    sleep(10)

    return df.values.tolist()

# squeeze into db, date is like YYYYMM
def squeeze(date):
    
    # ignore date that is alreay processed
    with open('Processed_juice_date_list.txt') as f:
        if date in f.read():
            # print('Juice '+date+' already done, skipping...')
            return 0

    print('Processing juice date '+date+' ...')

    # get all the apples in the juice date, then init them
    juices_all = get_juice(date)
    print(juices_all)
    if juices_all == -1:
        print('Abort squeezing juice '+date+' ...')
        return -1
    # for 99~101 the length is 10
    if len(juices_all[0]) == 10:
        juices = [(i[0],i[2],i[7]) for i in juices_all if type(i[0]) is int]
    # for 102~now the length is 11
    elif len(juices_all[0]) == 11:
        # juices = [(i[0],i[7],i[10]) for i in juices_all if type(i[0]) is int]
        juices = [(i[0],i[7],i[10]) for i in juices_all if len(i[0]) == 4] # now juice first item change to str : '1101'
    else:
        print('Juice format has changed, stop now ...')
        return -1
    juices.sort(key = lambda x: x[0])
    print(juices)

    for juice in juices:
        # use UNIQUE here to prevent duplicates, and for overwrite
        sql_create_cmd = 'CREATE TABLE IF NOT EXISTS apple_'+juice[0]+' (date INT UNIQUE, current INT, accumu INT)'
        sql_cursor_Database_juice_name.execute(sql_create_cmd)
        # use INSERT OR IGNORE to avoid getting errors when inserting duplicate item
        sql_write_cmd = 'INSERT OR IGNORE INTO apple_'+juice[0]+' (date, current, accumu) values\
                ("'+date+'","'+str(juice[1])+'", "'+str(juice[2])+'")'
        sql_cursor_Database_juice_name.execute(sql_write_cmd)
        print('writing juice for apple_'+juice[0])
    
    sql_connection_Database_juice_name.commit()

    # Record the processed date YYYYMM
    with open('Processed_juice_date_list.txt') as fr:
        with open('Processed_juice_date_list.txt', 'a') as fa:
            if date not in fr.read():
                fa.write('%s\n' % date)

def Get_seeds():
    _url = 'https://smart.tdcc.com.tw/opendata/getOD.ashx?id=1-5'

    # currently not knowing the date in csv, give it temp
    csv_file_name_temp = 'Seeds/temp.csv'
    urllib.request.urlretrieve(_url, csv_file_name_temp)

    # get the date in csv
    df = pandas.read_csv(csv_file_name_temp, encoding = 'utf8')
    df_date = str(df.iloc[0][0])
    print('Finish downloading seeds at ' + df_date)

    # example of how to get the pure data
    # print(df.iloc[1].values)
    '''
    [20191227 '0050' 2 46925 87934309 12.55]
    '''
    
    with open('Processed_seeds_date_list.txt') as f:
        lines = f.read().splitlines()
        latest_data_date = lines[-1]

    if df_date == latest_data_date:
        os.remove(csv_file_name_temp)
        print('Seeds '+df_date+' is already done, skipping...')
        return 0

    # check if missing any date info 
    delta_days = (datetime.today() - datetime.strptime(latest_data_date, '%Y%m%d')).days
    if delta_days > 10:
        if not P_user_yn_confirm('More than 10 days not updated, did you check https://www.tdcc.com.tw/smWeb/QryStock.jsp ?'):
            print('aborting')
            return -1

    # Rename the csv
    os.rename(csv_file_name_temp, 'Seeds/'+df_date+'.csv')

    # date is different, start parsing, assuming every data
    # contains perfectly 17 rows
    # while True:

    print('Processing seeeds date '+df_date+' ...')
    
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
    return 0

def Print_latest_result(filename, data_type):
    with open(filename) as f:
        lines = f.read().splitlines()
        latest_data_date = lines[-1]
    print('Latest '+data_type+' is '+latest_data_date+'.') 

def main():

    args = parse_command_line()
    day_start = str(int(args.Massive_mode_end_day) - int(args.length_of_the_date))
    day_end = args.Massive_mode_end_day
    Apple_location = args.output_dir

    # Process apples
    print('===== Apple Start =====')
    if download_apples(day_start,day_end ,Apple_location, True):
        print('Error occured in download_apples()')
        return -1
    # Delete apples a year ago
    delete_old_apples(Apple_location,day_start)
    # Harvest the apples
    Harvest()
    Print_latest_result('Processed_date_list.txt','apple')
    print('===== Apple Done =====')

    # Process juices
    print('===== Juice Start =====')
    date_ym_list = get_date(today)
    for date_ym in date_ym_list:
        squeeze(date_ym)
    Print_latest_result('Processed_juice_date_list.txt','juice')
    print('===== Juice Done =====')

    # Process seeds
    print('===== Seeds Start =====')
    Get_seeds()
    Print_latest_result('Processed_seeds_date_list.txt','seeds')
    print('===== Seeds Done =====')
    
if __name__ == '__main__':
    main()

