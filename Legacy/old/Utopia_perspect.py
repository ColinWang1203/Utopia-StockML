# python Utopia_perspect.py -a 4142
# python Utopia_perspect.py -f , Utopia_juice.py required, check if deviate
# python Utopia_perspect.py -d , Utopia_seeds.py required, check if deviate
# python Utopia_perspect.py -c , apple_num_file_alicia

from Utopia_tools import *

import pandas, sqlite3, requests, calendar, os, urllib.request, sys, math
import numpy as np
import matplotlib.pyplot as plt
from dateutil import rrule
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from argparse import ArgumentParser, RawTextHelpFormatter
from time import sleep
from io import StringIO
from random import randint

Database_squeeze_name = 'DB_Avalon.sqlite'
sql_connection_Database_squeeze_name = sqlite3.connect(Database_squeeze_name)
sql_cursor_Database_squeeze_name = sql_connection_Database_squeeze_name.cursor()
Database_juice_name = 'DB_Juice.sqlite'
sql_connection_Database_juice_name = sqlite3.connect(Database_juice_name)
sql_cursor_Database_juice_name = sql_connection_Database_juice_name.cursor()
Database_seeds_name = 'DB_Seeds.sqlite'
sql_connection_Database_seeds_name = sqlite3.connect(Database_seeds_name)
sql_cursor_Database_seeds_name = sql_connection_Database_seeds_name.cursor()

color_blue = '#1f77b4'
color_orange = '#ff7f0e'
color_brown = '#A52A2A'
color_green = '#2ca02c'
color_red = '#d62728'
color_purple = '#9467bd'
color_black = '#000000'

Fig_dir = 'Figs/'
Fig_dir_dropbox = '/home/colin/Dropbox/Figs/'

def parse_command_line():
    
    parser = ArgumentParser(description='Welcome to Utopia\n"Mode" for upper class\n"Index" for lower class\nexample : python Utopia_perspect.py -jsa 2345\n\n',
            formatter_class=RawTextHelpFormatter)
    # Mode
    # parser.add_argument('-J', dest='max_juice', default = False, action='store_true', help='max juice')
    parser.add_argument('-S', dest='save_plot', default = True, action='store_false', help='save plot')
    # index
    parser.add_argument('-j', dest='show_juice', default = True, action='store_false', help='show juice')
    parser.add_argument('-s', dest='show_seeds', default = True, action='store_false', help='show seeds')
    # by given single apple
    parser.add_argument('-a', dest='apple_num', help='by given single apple')
    # by apple in file for juice
    parser.add_argument('-f', dest='apple_num_file_juice', default = False, action='store_true', help='by apple in file juice, get in figs, go to dropbox')
    # by apple in file for seeds
    parser.add_argument('-d', dest='apple_num_file_seeds', default = False, action='store_true', help='by apple in file seeds, get in figs, go to dropbox')
    # by apple in file for alicia
    parser.add_argument('-c', dest='apple_num_file_alicia', default = False, action='store_true', help='by apple in file seeds, get in figs, go to dropbox')
    # by any file in format ('apple_8072', 23.74757124140618)
    parser.add_argument('-A', dest='num_file', type = str, action='store', help='by any formatted file')
    return parser.parse_args()

def main():
    args = parse_command_line()

    # Check if mode is not selected
    # if not args.max_juice:
    #     print('Mode is not selected. Aborting...')
    #     return -1 

    # Get day of an year by apple
    with open('Processed_date_list.txt') as f:
        content = f.read().splitlines()
    for i in list(range(1,len(content))):
        if Delta_days(content[-1],content[-i]) > 365:
            start_date = content[-i]
            All_apple_date = content[-i:]
            break     
    latest_date = content[-1]
    # Generate future data for a month for latter plotting
    # date_All_apple_date = datetime.strptime(All_apple_date[-1],'%Y%m%d')
    # dtstart = date_All_apple_date + relativedelta(days=+1)
    # dtuntil = date_All_apple_date + relativedelta(months=+1)

    # date_All_apple_date_next_month_list = []
    # for dt in rrule.rrule(rrule.DAILY, dtstart=dtstart, until=dtuntil):
    #     date_All_apple_date_next_month_list.append(dt.strftime('%Y%m%d'))

    # Get according apple
    if args.apple_num_file_juice:
        del_all_fig(Fig_dir)
        del_all_fig(Fig_dir_dropbox)
        with open(Fig_dir+'best_juices.txt') as f:
            content_best_apple = f.read().splitlines()
        content_best_apple = [i.replace('apple_','') for i in content_best_apple]
    elif args.apple_num_file_seeds:
        del_all_fig(Fig_dir)
        del_all_fig(Fig_dir_dropbox)
        with open(Fig_dir+'best_seeds.txt') as f:
            content_best_apple = f.read().splitlines()
        content_best_apple = [i.replace('apple_','') for i in content_best_apple]
    elif args.apple_num_file_alicia:
        del_all_fig(Fig_dir)
        del_all_fig(Fig_dir_dropbox)
        with open(Fig_dir+'best_alicia.txt') as f:
            content_best_apple = f.read().splitlines()
        content_best_apple = [i.split('apple_')[1].split('\'')[0] for i in content_best_apple]
    elif args.num_file:
        del_all_fig(Fig_dir+'/top')
        del_all_fig(Fig_dir_dropbox+'/top')
        del_all_fig(Fig_dir+'/mid')
        del_all_fig(Fig_dir_dropbox+'/mid')
        del_all_fig(Fig_dir+'/low')
        del_all_fig(Fig_dir_dropbox+'/low')
        with open(Fig_dir+'Heaven_plot.txt') as f:
            content_best_apple = f.read().splitlines()
        content_best_apple = [i.split('apple_')[1].split('\'')[0] for i in content_best_apple]
    else:
        content_best_apple = [args.apple_num]

    # if args.save_plot:
    #     del_all_fig(Fig_dir)
    #     del_all_fig(Fig_dir_dropbox)

    file_count = 0
        
    for apple_num in content_best_apple:
        file_count+=1
        print('Drawing apple_'+apple_num+' ...')
        try :
            sql_cursor_Database_squeeze_name.execute("SELECT * FROM apple_"+apple_num+"")
            sql_apple = sql_cursor_Database_squeeze_name.fetchall()
            date_apple_dict = {}
            for date in All_apple_date:
                date = str(date)
                # print(date) # 20190726
                # print(datetime.today().strftime('%Y%m%d'))
                for apple_data in sql_apple:
                    if compare_string(apple_data[0],date):
                        # handle missing data
                        if isinstance(apple_data[5],str):
                            if not compare_string(apple_data[5],''):
                                date_apple_dict[date] = float(apple_data[5].replace(',',''))
                            else:
                                date_apple_dict[date] = nan()
                        else: 
                            date_apple_dict[date] = apple_data[5]
            max_apple_value = max(list(date_apple_dict.values()))
            min_apple_value = min(list(date_apple_dict.values()))
            mid_apple_value = sum(list(date_apple_dict.values())) / len(list(date_apple_dict.values()))
            # Plot and save
            # fig = plt.figure()
            plt.figure(dpi=200) # change the dpi before plotting to make it bigger, original 100
            # plot apple
            plt.plot(list(date_apple_dict.keys()), list(date_apple_dict.values())\
                    ,label='Apple',color=color_blue, linestyle='-')
            # Get month avg 22
            date_apple_mavg_dict = {}
            bb_up_dict = {}
            bb_down_dict = {}
            count = 0
            # set y tick to 15 ticks, or at least 1
            list_apple_dict_value = list(date_apple_dict.values())
            list_apple_dict_value = [x for x in list_apple_dict_value if str(x) != 'nan']
            max_apple_value = math.ceil(max(list_apple_dict_value))
            min_apple_value = math.floor(min(list_apple_dict_value))
            if max_apple_value - min_apple_value > 20:
                apple_steps = math.floor((max_apple_value - min_apple_value) / 15)
            else:
                apple_steps = 1
            # print(All_apple_date)
            for date in All_apple_date[::-1]:
                date = str(date)
                date_apple_mavg = 0
                All_22_date = All_apple_date[-(22+count):-(1+count)]
                All_22_date.append(All_apple_date[-(1+count)])
                if len(All_22_date) < 22:
                    # print('reach the end of apple index')
                    break
                apple_len = 0
                bb_list = []
                for day in All_22_date:
                    for apple in sql_apple:
                        # if compare_string(apple_num,"3008"):
                        # print(apple_num)
                        #     printt(apple[0])
                        #     printt(day)
                        # printt(apple[5])
                        #     print(compare_string(apple[0],day))
                        #     print(isinstance(apple[5],str))
                        # avoid if any missing data for specific apple
                        if compare_string(apple[0],day) and not compare_string(apple[5],''):
                            if type(apple[5]) is str:
                                apple_end = float(apple[5].replace(',',''));
                            else:
                                apple_end = apple[5];
                            date_apple_mavg += apple_end
                            bb_list.append(apple_end)
                            apple_len += 1
                            break
                # also need to find the available amount and divide with it
                # print(date_apple_mavg)
                date_apple_mavg_divide = date_apple_mavg / apple_len
                date_apple_mavg_dict[date] = date_apple_mavg_divide
                # print(date_apple_mavg_dict)
                count += 1   
                # create the bb
                bb_std = np.std(bb_list)
                bb_up_dict[date] = date_apple_mavg_divide + (2 * bb_std)
                bb_down_dict[date] = date_apple_mavg_divide - (2 * bb_std)

            # plot apple 22
            plt.plot(list(date_apple_mavg_dict.keys()), list(date_apple_mavg_dict.values())\
                    ,label='Apple 22',color=color_red, linestyle='-')
            # plot bb
            plt.plot(list(bb_up_dict.keys()), list(bb_up_dict.values())\
                    ,label='bb_up',color=color_purple, linestyle='-')
            plt.plot(list(bb_down_dict.keys()), list(bb_down_dict.values())\
                    ,label='bb_down',color=color_purple, linestyle='-')
        except Exception as e:
            print('Error : '+str(e))
            print('Caught error in calculating apple, ignore it...')

        if args.show_juice:
            # Get according juice, assume on 10th
            with open('Processed_juice_date_list.txt') as f:
                content = f.read().splitlines()
            # check juice availability
            if len(content) < 12:
                print('Not enough juice data')
                return -1
            for i in list(range(1,len(content))):
                if Delta_days(content[-1]+'10',content[-i]+'10') > 365 \
                        or Delta_days(content[-i]+'10',start_date) <=0:
                    All_juice_date = content[-i+1:]
                    break    
            try:
                sql_cursor_Database_juice_name.execute("SELECT * FROM apple_"+apple_num+"")
                sql_juice = sql_cursor_Database_juice_name.fetchall()
                
                # print(All_juice_date)
                date_juice_dict = {}
                for date in All_juice_date:
                    date = str(date)
                    for juice_data in sql_juice:
                        if compare_string(juice_data[0],date):
                            # Because we want them all on same plot
                            # Get the date that close to date+'10' the most
                            # date_juice_dict[date+'10'] = int(juice_data[1])
                            modified_date = min(map(int,All_apple_date), key=lambda x:abs(x-int(date+'10')))
                            date_juice_dict[str(modified_date)] = int(juice_data[1]) 

                # Find the mirror ratio
                date_juice_dict_trans = date_juice_dict.copy()
                # first scale, also reflect the var on the chart
                max_juice_value = max(list(date_juice_dict.values()))
                min_juice_value = min(list(date_juice_dict.values()))
                juice_var_ratio = (max_juice_value-min_juice_value) / max_juice_value
                apple_var_ratio = (max_apple_value-min_apple_value) / max_apple_value
                juice_to_apple_var_ratio = juice_var_ratio / apple_var_ratio
                juice_to_apple_ratio = (max_juice_value-min_juice_value) / (max_apple_value-min_apple_value)
                date_juice_dict_trans.update((x, y / juice_to_apple_ratio * juice_to_apple_var_ratio) for x, y in date_juice_dict_trans.items())
                        
                # then shift
                mid_juice_value_scale_to_apple = sum(list(date_juice_dict_trans.values())) / len(list(date_juice_dict_trans.values()))
                shift_juice = mid_juice_value_scale_to_apple - mid_apple_value
                date_juice_dict_trans.update((x, y - shift_juice) for x, y in date_juice_dict_trans.items())

                # plot juice mapping
                # colin comment orange juice
                # plt.plot(list(date_juice_dict_trans.keys()), list(date_juice_dict_trans.values())\
                #         ,label='Juice',color=color_orange, linestyle='-')

                # now get the juice year increase
                try:
                    Year_juice_date_all = []
                    data_juice_curr_prev_dict = {}

                    for juice_shift in range(len(All_juice_date)):
                        Year_juice_date = []
                        # list of year, max to 2 year
                        for i in list(range(0,2)):
                            if i == 0:
                                if juice_shift == 0:
                                    Year_juice_date.append(content[-12:])
                                else:
                                    Year_juice_date.append(content[-12-juice_shift:-juice_shift])
                            else:
                                Year_juice_date.append(content[-(12+(12*i))-juice_shift:-(12*i)-juice_shift])

                        Year_juice_date.reverse()
                        Year_juice_date_all = Year_juice_date + Year_juice_date_all

                    # print(Year_juice_date_all)

                    Year_juice_date_all_curr = []
                    Year_juice_date_all_prev = []
                    
                    for i in range(0,len(Year_juice_date_all),2):
                        # Year_juice_date_all_prev = Year_juice_date_all[i] + Year_juice_date_all_prev
                        # Year_juice_date_all_curr = Year_juice_date_all[i+1] + Year_juice_date_all_curr
                        Year_juice_date_all_prev.append(Year_juice_date_all[i])
                        Year_juice_date_all_curr.append(Year_juice_date_all[i+1])

                    # Year_juice_date_all_curr.reverse()
                    # Year_juice_date_all_prev.reverse()
                    # print(Year_juice_date_all_curr)
                    # print(Year_juice_date_all_prev)

                    #sum the curr and prev and parallel compare
                    for juice_all_curr, juice_all_prev in zip(Year_juice_date_all_curr, Year_juice_date_all_prev):
                        juice_curr_sum = 0
                        for juice_date in juice_all_curr:
                            for juice_data in sql_juice:
                                if compare_string(juice_data[0],juice_date):
                                    juice_curr_sum += juice_data[1]
                        juice_prev_sum = 0
                        for juice_date in juice_all_prev:
                            for juice_data in sql_juice:
                                if compare_string(juice_data[0],juice_date):
                                    juice_prev_sum += juice_data[1]
                        
                        juice_curr_prev_ratio = (juice_curr_sum - juice_prev_sum) / juice_prev_sum
                        current_juice_date = juice_all_curr[-1]
                        modified_date = min(map(int,All_apple_date), key=lambda x:abs(x-int(current_juice_date+'10')))
                        
                        # (optional) define the top of apple is mappped to 50% increase
                        # juice_curr_prev_dict_value = (max_apple_value - mid_apple_value) * 1/0.5 * juice_curr_prev_ratio + mid_apple_value

                        # (optional) define a apple_steps as 10%
                        # juice_curr_prev_dict_value = juice_curr_prev_ratio*100/10*apple_steps + mid_apple_value

                        # (optional) define the rate map by mid value
                        juice_curr_prev_dict_value = juice_curr_prev_ratio * mid_apple_value + mid_apple_value

                        data_juice_curr_prev_dict[str(modified_date)] = juice_curr_prev_dict_value

                    # print(data_juice_curr_prev_dict)
            
                    # plot juice mapping
                    plt.plot(list(data_juice_curr_prev_dict.keys()), list(data_juice_curr_prev_dict.values())\
                            ,label='Juice_curr_prev',color=color_orange, linestyle='-')

                    #plot middle black line
                    middle_dict = {}
                    for i in range(len(All_apple_date)):
                        middle_dict[All_apple_date[i]] = mid_apple_value
                    # print(middle_dict)
                    plt.plot(list(middle_dict.keys()), list(middle_dict.values())\
                            ,label='black_middle',color=color_black, linestyle='-')



                except Exception as e:
                    print('Error : '+str(e))
                    print('Caught error in getting juice with prev, ignore it...')

            except Exception as e:
                print('Error : '+str(e))
                print('Caught error in getting juice, ignore it...')

        if args.show_seeds:
            # Get date in a year for seeds
            sql_cursor_Database_seeds_name.execute("SELECT * FROM apple_"+apple_num+"")
            sql_seeds = sql_cursor_Database_seeds_name.fetchall()
            All_seeds_date = [i[0] for i in sql_seeds if i[0] >= int(start_date)]
            # seeds algo here
            date_seeds_dict = {}
            try :
                for date in All_seeds_date:
                    date = str(date)
                    for seeds_data in sql_seeds:
                        if compare_string(seeds_data[0],date):
                            modified_date = min(map(int,All_apple_date), key=lambda x:abs(x-int(date)))
                            # Get the ratio of big/small seeds
                            # 1~9(100down) 10~15(100up)
                            # big and small depends on apple price 50
                            # price > 50 = 400, price < 50 = 1000
                            apple_latest_price = date_apple_dict[latest_date]
                            #  (deprecated) decide the big and small boundary by best fit
                            small_seeds = 0
                            big_seeds = 0
                            for i in list(range(1,16)):
                                if apple_latest_price > 50:
                                    if i < 15:
                                        small_seeds += seeds_data[i]
                                    else:
                                        big_seeds += seeds_data[i]
                                else:
                                    if i < 15:
                                        small_seeds += seeds_data[i]
                                    else:
                                        big_seeds += seeds_data[i]
                            seeds_ratio = big_seeds/small_seeds
                            date_seeds_dict[str(modified_date)] = seeds_ratio
                
                # Find the mirror ratio
                date_seeds_dict_trans = date_seeds_dict.copy()
                # first scale, also reflect the var on the chart
                max_seeds_value = max(list(date_seeds_dict.values()))
                min_seeds_value = min(list(date_seeds_dict.values()))
                seeds_var_ratio = (max_seeds_value-min_seeds_value) / max_seeds_value
                # apple_var_ratio = (max_apple_value-min_apple_value) / max_apple_value
                seeds_to_apple_var_ratio = seeds_var_ratio / apple_var_ratio
                seeds_to_apple_ratio = (max_seeds_value-min_seeds_value) / (max_apple_value-min_apple_value)
                date_seeds_dict_trans.update((x, y / seeds_to_apple_ratio * seeds_to_apple_var_ratio) for x, y in date_seeds_dict_trans.items())
                # then shift
                # min_seeds_value = min(list(date_seeds_dict_trans.values()))
                mid_seeds_value_scale_to_apple = sum(list(date_seeds_dict_trans.values())) / len(list(date_seeds_dict_trans.values()))
                shift_seeds = mid_seeds_value_scale_to_apple - mid_apple_value
                date_seeds_dict_trans.update((x, y-shift_seeds) for x, y in date_seeds_dict_trans.items())

                # plot seeds mapping
                plt.plot(list(date_seeds_dict_trans.keys()), list(date_seeds_dict_trans.values())\
                        ,label='Seeds',color=color_green, linestyle='-')
            except Exception as e:
                print('Error : '+str(e))
                print('Caught error in getting seed, ignore it...')

        try :
            # print(plt.xticks())
            xticks = plt.xticks()[0]
            xticks_copy = xticks.copy() # careful when copy a list, no copy() will link them together
            # plot the vertical line for month
            cur_mon = 201001
            tick_count = 0
            for day in list(date_apple_dict.keys()):
                if not compare_string(day[0:6],cur_mon):
                    cur_mon = day[0:6]
                    plt.axvline(x=day,color=color_black, linestyle='-', alpha=0.5)
                    xticks[tick_count] = day[4:6]
                else:
                    xticks[tick_count] = None
                tick_count += 1

            # finish the ploting
            title_str = apple_num
            title_str = datetime.now().strftime("%H%M%S-%m%d%Y-") + title_str
            if args.show_juice:
                title_str += '-' + str(round(juice_curr_prev_ratio*100,0)) + '%'
            if args.show_seeds:
                # replace the title with the one in best_seeds_with_juice
                with open(Fig_dir+'best_seeds_with_juice.txt') as f:
                    best_seeds_with_juice = f.read().splitlines()
                for j in best_seeds_with_juice:
                    if compare_string(j.split('_')[1], apple_num):
                        title_str = j.split('e_')[1]
                        break
            
            # fig.suptitle(title_str, fontsize=20)
            plt.title(title_str,fontsize=20)
            # plt.legend(loc='upper left')
            plt.grid()
            # note max need add step to include the highest value axis
            plt.yticks(np.arange(min_apple_value, max_apple_value + apple_steps, apple_steps))

            # plot y axis on both side
            plt.tick_params(axis='y', which='both', labelleft='on', labelright='on')

            # remove the x ticks for clearer plot
            # plt.xticks([])
            # try to add xtick
            plt.xticks(xticks_copy, xticks)

            if args.save_plot:
                plt.savefig(Fig_dir+str(file_count)+'_'+apple_num+'.png')
                plt.savefig(Fig_dir_dropbox+str(file_count)+'_'+apple_num+'.png')
            if not (args.apple_num_file_juice or args.apple_num_file_seeds or args.apple_num_file_alicia):
                mngr = plt.get_current_fig_manager()
                geom = mngr.window.geometry()
                x,y,dx,dy = geom.getRect()
                mngr.window.setGeometry(0,0,dx,dy)
                plt.show(block=False)
                plt.waitforbuttonpress()
        except Exception as e:
            print('Error : '+str(e))
            print('Caught error in ploting, ignore it...')
    
if __name__ == '__main__':
    main()

