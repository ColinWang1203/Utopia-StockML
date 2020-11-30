# Sample : python Utopia_juice.py
# next month juice predict
import pandas, sqlite3, requests, calendar, os, urllib.request, functools#, logging
import numpy as np
import matplotlib.pyplot as plt
from dateutil import rrule
from datetime import datetime
from argparse import ArgumentParser
from time import sleep
from io import StringIO
from fbprophet import Prophet

# ===== Global vars =====

today = datetime.today().strftime("%Y%m%d")

# Databases
Database_squeeze_name = 'DB_Avalon.sqlite'
sql_connection_Database_squeeze_name = sqlite3.connect(Database_squeeze_name)
sql_cursor_Database_squeeze_name = sql_connection_Database_squeeze_name.cursor()
Database_juice_name = 'DB_Juice.sqlite'
sql_connection_Database_juice_name = sqlite3.connect(Database_juice_name)
sql_cursor_Database_juice_name = sql_connection_Database_juice_name.cursor()

# Suppress fbprophet logging
# logging.getLogger('fbprophet').setLevel(logging.WARNING)

Fig_dir = 'Figs'

# Delete all former figures
filelist = [ f for f in os.listdir(Fig_dir) if f.endswith(".jpg") ]
for f in filelist:
    os.remove(os.path.join(Fig_dir, f))

# =======================

def get_date(start_date,end_date):

    start_date = str(start_date)
    end_date = str(end_date)

    date_y1 = start_date[0:4]
    date_m1 = ['%02d'%m for m in list(range(int(start_date[4:6]),13))]
    date_ym = [date_y1+m for m in date_m1]
    date_y = list(map(str,list(range(int(start_date[0:4])+1,int(end_date[0:4])))))
    date_m = ['%02d'%m for m in list(range(1,13))]
    date_ym = date_ym + ([y+m for y in date_y for m in date_m])

    if end_date[4:6] == '01':
        return date_ym
    
    if int(end_date[6:8]) <= 10:
        date_y = end_date[0:4]
        date_m = ['%02d'%m for m in list(range(1,int(end_date[4:6])-1))]
        for m in date_m:
            date_ym.append(date_y+m)
    else:
        date_y = end_date[0:4]
        date_m = ['%02d'%m for m in list(range(1,int(end_date[4:6])))]
        for m in date_m:
            date_ym.append(date_y+m)
    
    return date_ym

def check_date_available(date_1,date_2,apple):

    if not functools.reduce(lambda i, j : i and j, \
            map(lambda m, k: m == k, date_1, date_2), True) :
        # print('Some data is missing in '+''.join(apple))
        return False
    return True

def get_max_juice(check_date):
    # best_juice = []
    best_juice_prophet = []
    # Get the tables
    sql_cursor_Database_juice_name.execute("SELECT name FROM sqlite_master WHERE type='table'")
    sql_tables_Database_juice_name = sql_cursor_Database_juice_name.fetchall()
    
    for apple in sql_tables_Database_juice_name:
        # First check length more than a year
        # Get all stuff in apple
        apple_str = ''.join(apple)
        sql_cursor_Database_juice_name.execute("SELECT * FROM "+apple_str+"")
        juice = sql_cursor_Database_juice_name.fetchall()
        juice_date = list(map(str,[i[0] for i in juice]))
        if not check_date_available(juice_date[-len(check_date):],check_date,apple_str):
            print(apple_str+' date not enough for '+check_date[0])
            continue
        juice_curr = [i[1] for i in juice]
        juice_accu = [i[2] for i in juice]
        juice_curr_same = [i[1] for i in juice if str(i[0])[4:6] == check_date[-1][4:6]]
        juice_accu_same = [i[2] for i in juice if str(i[0])[4:6] == check_date[-1][4:6]]

        # compare to the same month
        if juice_curr[-1] == max(juice_curr_same) and juice_accu[-1] == max(juice_accu_same):
            # best_juice.append(apple_str)
            # Before prophet, check if the data is intact
            date_all = get_date(juice_date[0],today)
            if not functools.reduce(lambda i, j : i and j, \
                map(lambda m, k: m == k, date_all, juice_date), True) :
                print("Date in "+apple_str+" is not intact, ignore it")
                print('date_all is :')
                print(date_all)
                print('juice_date is :')
                print(juice_date)
                continue                

            # Before prophet, check paper > 1000
            sql_cursor_Database_squeeze_name.execute("SELECT * FROM "+apple_str+"")
            apple_juice = sql_cursor_Database_squeeze_name.fetchall()
            # note that some ZERO in the amount will turn into int, which can not apply to replace, check it
            amount = [i[1].replace(',','') for i in apple_juice if isinstance(i[1], str)]
            amount = list(map(int,amount))
            amount_avg = sum(amount)/len(amount)
            if amount_avg < 1000000: # 1000
                print(apple_str+" amount not enough with : "+str(amount_avg))
                continue

            # Reform data into [('YYYY-MM',value), ...] for prophet
            juice_date_p = [i[0:4]+'-'+i[4:6] for i in juice_date]
            juice_arrange = list(zip(juice_date_p,juice_curr))
            df = pandas.DataFrame(data=juice_arrange, columns=['ds','y'])
            # tune the changepoint_prior_scale, higher more fit, but could overfit
            m = Prophet(changepoint_prior_scale = 25)#.add_seasonality(name='yearly',period=12,fourier_order=10)
            m.fit(df)
            future = m.make_future_dataframe(periods=1, freq = "MS")
            forecast = m.predict(future)

            # Plot and save
            fig = plt.figure()
            plt.plot(juice_date_p, juice_curr)
            juice_date_p2 = juice_date_p
            juice_date_p2.append('next')
            plt.plot(juice_date_p2, forecast[['yhat']])
            plt.plot(juice_date_p2, forecast[['trend']])
            fig.suptitle(apple_str, fontsize=20)
            fig.savefig(Fig_dir+'/'+apple_str+'.jpg')
            # mngr = plt.get_current_fig_manager()
            # geom = mngr.window.geometry()
            # x,y,dx,dy = geom.getRect()
            # mngr.window.setGeometry(0,0,dx,dy)
            # plt.show(block=False)
            # plt.pause(3)
            # plt.close('all')
            
            forecast_juice = int(forecast['yhat'].iloc[-1])
            # here we use the preditced one to compare, not the actual one i.e : juice_curr[-1]
            forecast_curr_best_juice = int(forecast['yhat'].iloc[-2])
            rate_up_down = int((forecast_juice / forecast_curr_best_juice - 1) * 100)
            best_juice_prophet.append((apple_str,forecast_curr_best_juice,forecast_juice,str(rate_up_down)+'%'))

    return best_juice_prophet

def main():
    
    # check the availablity from 201801
    check_date = get_date('201801',today)
    
    best_juice_prophet = get_max_juice(check_date)
    best_juice_prophet.sort(key=lambda tup: int(tup[3].split('%')[0]))
    for p in best_juice_prophet:
        print(p)
    
    
if __name__ == '__main__':
    main()
