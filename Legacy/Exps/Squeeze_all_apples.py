# important : opening the csv file with libreoffice will cause some null columns become not a null one
#             causing the row counting to misbehave, do not open them!!

import pandas, sqlite3, os 
import numpy as np

Database_name = 'Utopia.sqlite'
Database_squeeze_name = 'Avalon.sqlite'

# if os.path.exists(Database_name):
#   os.remove(Database_name)
# if os.path.exists(Database_squeeze_name):
#   os.remove(Database_squeeze_name)

sql_connection_Database_name = sqlite3.connect(Database_name)
sql_cursor_Database_name = sql_connection_Database_name.cursor()
sql_connection_Database_squeeze_name = sqlite3.connect(Database_squeeze_name)
sql_cursor_Database_squeeze_name = sql_connection_Database_squeeze_name.cursor()

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
    sql_create_cmd = 'CREATE TABLE index_'+date+' (num INT, amount INT, high DOUBLE,\
        low DOUBLE, start DOUBLE, end DOUBLE)'
    sql_cursor_Database_name.execute(sql_create_cmd)

    for row in range(db_array.shape[0]):
        sql_write_cmd = 'INSERT INTO index_'+date+' (num, amount, high, low, start, end) values\
        ("'+db_array[row][0]+'", "'+db_array[row][1]+'", "'+db_array[row][2]+'"\
        , "'+db_array[row][3]+'", "'+db_array[row][4]+'", "'+db_array[row][5]+'")'
        sql_cursor_Database_name.execute(sql_write_cmd)
    # remember to commit after you write
    sql_connection_Database_name.commit()
    

# Create Rakuenn
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
        sql_create_cmd = 'CREATE TABLE IF NOT EXISTS apple_'+str(apple[0])+' (date INT, amount INT, high DOUBLE,\
                low DOUBLE, start DOUBLE, end DOUBLE)'
        sql_cursor_Database_squeeze_name.execute(sql_create_cmd)
        sql_write_cmd = 'INSERT INTO apple_'+str(apple[0])+' (date, amount, high, low, start, end) values\
                ( "'+apple_date+'","'+str(apple[1])+'", "'+str(apple[2])+'", "'+str(apple[3])+'"\
                , "'+str(apple[4])+'", "'+str(apple[5])+'")'
        sql_cursor_Database_squeeze_name.execute(sql_write_cmd)
        sql_connection_Database_squeeze_name.commit()

# Record the processed file
for date in sorted(date_all):
    with open('Processed_date_list.txt') as fr:
            with open('Processed_date_list.txt', 'a') as fa:
                if date not in fr.read():
                    fa.write('%s\n' % date)

sql_connection_Database_name.close()
sql_connection_Database_squeeze_name.close()