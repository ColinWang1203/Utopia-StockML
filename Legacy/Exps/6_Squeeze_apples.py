#need to do 4_Test_write_csv_data_to_database.py first
import pandas, sqlite3, os 
import numpy as np

Database_name = 'Test_utopia.sqlite'
Database_squeeze_name = 'Test_utopia_squeeze.sqlite'
if os.path.exists(Database_squeeze_name):
  os.remove(Database_squeeze_name)

# Get all the tables for Database 1 (apple by date)
sql_connection1 = sqlite3.connect(Database_name)
sql_cursor1 = sql_connection1.cursor()
sql_cursor1.execute("SELECT name FROM sqlite_master WHERE type='table'")
sql_tables1 = sql_cursor1.fetchall()

# Get all the tables for Database 2 (apples)
sql_connection2 = sqlite3.connect(Database_squeeze_name)
sql_cursor2 = sql_connection2.cursor()

# loop in tables and arrange the apples
for table in sql_tables1:
    #convert tuple into string
    table_str = ''.join(table)
    print('Loading apples in '+table_str)
    sql_cursor1.execute("SELECT * FROM "+table_str+"")
    sql_apples = sql_cursor1.fetchall()

    for apple in sql_apples:
        sql_create_cmd = 'CREATE TABLE IF NOT EXISTS apple_'+str(apple[0])+' (date INT, amount INT, high DOUBLE,\
                low DOUBLE, start DOUBLE, end DOUBLE)'
        sql_cursor2.execute(sql_create_cmd)
        sql_write_cmd = 'INSERT INTO apple_'+str(apple[0])+' (date, amount, high, low, start, end) values\
                ( "'+str(table_str.split('_')[1])+'","'+str(apple[1])+'", "'+str(apple[2])+'", "'+str(apple[3])+'"\
                , "'+str(apple[4])+'", "'+str(apple[5])+'")'
        sql_cursor2.execute(sql_write_cmd)
        sql_connection2.commit()


sql_cursor1.close()
sql_connection1.close()
sql_cursor2.close()
sql_connection2.close()
