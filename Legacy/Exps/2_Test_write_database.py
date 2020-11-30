#use sqlite browser to read the generated file
import sqlite3, os
from datetime import date

Database_name = 'Test_utopia.sqlite'
if os.path.exists(Database_name):
  os.remove(Database_name)

today = date.today().strftime("%Y%m%d")

sql_connection = sqlite3.connect(Database_name)
sql_cursor = sql_connection.cursor()

sql_create_cmd = 'CREATE TABLE index_'+today+' (num INT, high DOUBLE, low DOUBLE, start DOUBLE, end DOUBLE)'
sql_cursor.execute(sql_create_cmd)

sql_write_cmd = 'INSERT INTO index_'+today+' (num, high, low, start, end) values ("2345", "172", "168.5", "169", "171")'
sql_cursor.execute(sql_write_cmd)

sql_connection.commit()

sql_connection.close()
