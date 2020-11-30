# important : opening the csv file with libreoffice will cause some null columns become not a null one
#             causing the row counting to misbehave, do not open them!!

import pandas, sqlite3, os 
import numpy as np

Database_name = 'Test_utopia.sqlite'
# delete if exist
if os.path.exists(Database_name):
  os.remove(Database_name)

date_all = ['20190604', '20191125']

for date in date_all :

  # take only the first column and remove the header to truly get all the csv file(first line won't become header)
  db_csv = pandas.read_csv(date+'.csv', encoding = 'big5', usecols = [0], header = None)

  # convert pandas.core.frame.DataFrame to numpy.ndarray
  db_array = db_csv.values
  #find where the first one starts, +1 is needed because csv starts from 1
  start_row = int(np.where(db_array == '1101')[0]+1)
  # print(start_row)

  db_csv_filtered = pandas.read_csv(date+'.csv', encoding = 'big5', skiprows=start_row,\
    usecols = [0,2,*range(5, 9)], header = None)
  # print(type(db_csv_filtered))

  db_array = db_csv_filtered.values

  # print(type(db_array))
  # print(db_array.shape)

  sql_connection = sqlite3.connect(Database_name)
  sql_cursor = sql_connection.cursor()

  #note that number can not be the first letter, so add index_
  sql_create_cmd = 'CREATE TABLE index_'+date+' (num INT, amount INT, high DOUBLE,\
    low DOUBLE, start DOUBLE, end DOUBLE)'
  sql_cursor.execute(sql_create_cmd)

  for row in range(db_array.shape[0]):
    sql_write_cmd = 'INSERT INTO index_'+date+' (num, amount, high, low, start, end) values\
      ("'+db_array[row][0]+'", "'+db_array[row][1]+'", "'+db_array[row][2]+'"\
      , "'+db_array[row][3]+'", "'+db_array[row][4]+'", "'+db_array[row][5]+'")'
    sql_cursor.execute(sql_write_cmd)
  # remember to commit after you write
  sql_connection.commit()

sql_connection.close()
