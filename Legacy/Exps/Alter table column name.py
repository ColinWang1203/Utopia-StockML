from Utopia_tools import *

import pandas, sqlite3, requests, calendar, os, urllib.request, sys
import numpy as np
from dateutil import rrule, relativedelta
from datetime import date, datetime
from argparse import ArgumentParser, RawTextHelpFormatter
from time import sleep
from io import StringIO

# ===== Global vars =====

today = datetime.today().strftime("%Y%m%d")

# Databases
Database_name = 'DB_Utopia.sqlite'
sql_connection_Database_name = sqlite3.connect(Database_name)
sql_cursor_Database_name = sql_connection_Database_name.cursor()
Database_squeeze_name = 'DB_Avalon.sqlite'
sql_connection_Database_squeeze_name = sqlite3.connect(Database_squeeze_name)
sql_cursor_Database_squeeze_name = sql_connection_Database_squeeze_name.cursor()

# =======================
        

# Create Avalon
# get tables in Utopia
sql_cursor_Database_name.execute("SELECT name FROM sqlite_master WHERE type='table'")
sql_tables_Database_name = sql_cursor_Database_name.fetchall()

for table in sorted(sql_tables_Database_name):
    # convert tuple into string
    table_str = ''.join(table)
    # sql_create_cmd = 'ALTER TABLE apple_'+str(apple[0])+' CHANGE (date INT, amount INT, start DOUBLE, high DOUBLE,\
    #         low DOUBLE, end DOUBLE)'
    sql_create_cmd = 'ALTER TABLE '+table_str+' RENAME COLUMN high TO starts'
    sql_cursor_Database_name.execute(sql_create_cmd)
    sql_create_cmd = 'ALTER TABLE '+table_str+' RENAME COLUMN low TO highs'
    sql_cursor_Database_name.execute(sql_create_cmd)
    sql_create_cmd = 'ALTER TABLE '+table_str+' RENAME COLUMN start TO lows'
    sql_cursor_Database_name.execute(sql_create_cmd)
    sql_create_cmd = 'ALTER TABLE '+table_str+' RENAME COLUMN end TO ends'
    sql_cursor_Database_name.execute(sql_create_cmd)

sql_connection_Database_name.close()

