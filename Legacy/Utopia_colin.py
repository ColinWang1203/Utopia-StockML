from Utopia_tools import *

#====================================================
# TO DOs with #@
#@ use anotehr phone to tack the first result
#@ reconstruct the data that does not missing over three days
#====================================================

##### Initial Notes #####

# test tab_len
# adb shell input keyevent 61
tab_len = 6                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

# block notification (need reboot)
# adb shell settings put global heads_up_notifications_enabled 0
# This is now achieved by "Game mode" app


##### User Variables #####

# There are three types :top mid low
# Basically use the same for all mode, since the fist mode will filter out the next
# set the algo for all three
Algo_mode = 4

# Mininum amount of transaction otherwise discard it
MIN_AMOUNT = 1000

# Mininum latest apple price
MIN_LATEST_PRICE = 10

# Max length parsing
MAX_LEN_PARSE = 5

# user skip list (finance, construction)
skip_list = [2548, 2348, 2524, 2505, 2851, 2809,
             2836, 2889, 5521, 6005, 2884, 2845,
             2888, 2887, 2890, 5880, 2886,
             5876, 2834, 2880, 2801] 
# skip_list = []

#########################
# Logging
P_enable_logging()

#Also collect the code to the log
P_printl(P_read_file('Utopia_colin.py'))
#########################

Database_squeeze_name = 'DB_Avalon.sqlite'
sql_connection_Database_squeeze_name = sqlite3.connect(Database_squeeze_name)
sql_cursor_Database_squeeze_name = sql_connection_Database_squeeze_name.cursor()
Database_juice_name = 'DB_Juice.sqlite'
sql_connection_Database_juice_name = sqlite3.connect(Database_juice_name)
sql_cursor_Database_juice_name = sql_connection_Database_juice_name.cursor()
Database_seeds_name = 'DB_Seeds.sqlite'
sql_connection_Database_seeds_name = sqlite3.connect(Database_seeds_name)
sql_cursor_Database_seeds_name = sql_connection_Database_seeds_name.cursor()

P_printl('Using Algo_mode : '+str(Algo_mode))

Fig_dir = 'Figs/' 
Fig_dir_dropbox = '/home/colin/Dropbox/Figs/'

with open('Processed_date_list.txt') as f:
    All_apple_date = f.read().splitlines()
with open('Processed_juice_date_list.txt') as f:
    All_juice_date = f.read().splitlines()
with open('Processed_seeds_date_list.txt') as f:
    All_seeds_date = f.read().splitlines()
with open('Processed_winds_date_list.txt') as f:
    All_winds_date = f.read().splitlines()

latest_date = All_apple_date[-1]

# last date get from latest heaven_xxx.txt, not from processed date
listd = P_get_list_of_files_in_path('Figs/Heavens')
listd.sort()
prev_date = listd[0].split('_')[2].split('.')[0]

latest_5_date = All_apple_date[-5:]
latest_22_date = All_apple_date[-22:]
latest_42_date = All_apple_date[-42:]
latest_63_date = All_apple_date[-63:] # apple guarantee day

Year_juice_date = []
# list of year, max to 2 year
for i in list(range(0,2)):
    if i == 0:
        Year_juice_date.append(All_juice_date[-12:])
    else:
        Year_juice_date.append(All_juice_date[-(12+(12*i)):-(12*i)])
Year_juice_date.reverse()

# for drawing
color_blue = '#1f77b4'
color_orange = '#ff7f0e'
color_brown = '#A52A2A'
color_green = '#2ca02c'
color_red = '#d62728'
color_purple = '#9467bd'
color_black = '#000000'

for i in list(range(1,len(All_apple_date))):
    if P_delta_days(All_apple_date[-1],All_apple_date[-i]) > 365:
        start_date = All_apple_date[-i]
        latest_365_date = All_apple_date[-i:]
        break    

def parse_command_line():
    parser = ArgumentParser(description='-a : adb_parsing, -f : plot_fig\n',
            formatter_class=RawTextHelpFormatter)
    parser.add_argument('-a', dest='adb_parsing', default = False, action='store_true')
    parser.add_argument('-f', dest='plot_fig', default = False, action='store_true')
    return parser.parse_args()

def draw_apple(apple_num, order, Fig_dir_t, Fig_dir_dropbox_t):
    apple_num = apple_num.split('_')[1]
    print('Drawing apple_'+apple_num+' ...')
    try :
        sql_cursor_Database_squeeze_name.execute("SELECT * FROM apple_"+apple_num+"")
        sql_apple = sql_cursor_Database_squeeze_name.fetchall()
        date_apple_dict = {}
        for date in latest_365_date:
            for apple_data in sql_apple:
                # P_printt(apple_data[0])
                # P_printt(date)
                if str(apple_data[0]) == date:
                    # handle missing data
                    if isinstance(apple_data[5],str):
                        if apple_data[5] != '':
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
        # print(latest_365_date)
        for date in latest_365_date[::-1]:
            date = str(date)
            date_apple_mavg = 0
            All_22_date = latest_365_date[-(22+count):-(1+count)]
            All_22_date.append(latest_365_date[-(1+count)])
            if len(All_22_date) < 22:
                # print('reach the end of apple index')
                break
            apple_len = 0
            bb_list = []
            for day in All_22_date:
                for apple in sql_apple:
                    if str(apple[0]) == day and apple[5] != '':
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

    #========================================================================    
    # Get according juice, assume on 10th
    with open('Processed_juice_date_list.txt') as f:
        content = f.read().splitlines()
    # check juice availability
    if len(content) < 12:
        print('Not enough juice data')
        return -1
    for i in list(range(1,len(content))):
        if P_delta_days(content[-1]+'10',content[-i]+'10') > 365 \
                or P_delta_days(content[-i]+'10',start_date) <=0:
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
                if str(juice_data[0]) == date:
                    # Because we want them all on same plot
                    # Get the date that close to date+'10' the most
                    # date_juice_dict[date+'10'] = int(juice_data[1])
                    modified_date = min(map(int,latest_365_date), key=lambda x:abs(x-int(date+'10')))
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
                        if str(juice_data[0]) == juice_date:
                            juice_curr_sum += juice_data[1]
                juice_prev_sum = 0
                for juice_date in juice_all_prev:
                    for juice_data in sql_juice:
                        if str(juice_data[0]) == juice_date:
                            juice_prev_sum += juice_data[1]
                
                juice_curr_prev_ratio = (juice_curr_sum - juice_prev_sum) / juice_prev_sum
                current_juice_date = juice_all_curr[-1]
                modified_date = min(map(int,latest_365_date), key=lambda x:abs(x-int(current_juice_date+'10')))
                
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
            for i in range(len(latest_365_date)):
                middle_dict[latest_365_date[i]] = mid_apple_value
            # print(middle_dict)
            plt.plot(list(middle_dict.keys()), list(middle_dict.values())\
                    ,label='black_middle',color=color_black, linestyle='-')

        except Exception as e:
            print('Error : '+str(e))
            print('Caught error in getting juice with prev, ignore it...')

    except Exception as e:
        print('Error : '+str(e))
        print('Caught error in getting juice, ignore it...')

    #=============================================================================================================

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
                if str(seeds_data[0]) == date:
                    modified_date = min(map(int,latest_365_date), key=lambda x:abs(x-int(date)))
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
            if str(day[0:6]) == str(cur_mon):
                cur_mon = day[0:6]
                plt.axvline(x=day,color=color_black, linestyle='-', alpha=0.5)
                xticks[tick_count] = day[4:6]
            else:
                xticks[tick_count] = None
            tick_count += 1

        # finish the ploting
        title_str = apple_num
        title_str = datetime.now().strftime("%H%M%S-%m%d%Y-") + title_str
        title_str += ',' + str(round(juice_curr_prev_ratio*100,0)) + '%'
        
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

        plt.savefig(Fig_dir_t+str(order)+'_'+apple_num+'.png')
        plt.savefig(Fig_dir_dropbox_t+str(order)+'_'+apple_num+'.png')
        
    except Exception as e:
        print('Error : '+str(e))
        print('Caught error in ploting, ignore it...')

def main():
    args = parse_command_line()
    P_printl("Please check the 6/7 and language and set page to colin",-1)
    #============================================================================================================
    #                               Filter Start
    #============================================================================================================
    # Get the tables and filter out all the definite unwanted (by name, amount, then 2-y-juice)
    sql_cursor_Database_squeeze_name.execute("SELECT name FROM sqlite_master WHERE type='table'")
    sql_tables_Database_squeeze_name = sql_cursor_Database_squeeze_name.fetchall()
    All_good_apple_list = []
    for apple_num in sql_tables_Database_squeeze_name:
        apple_num = "".join(apple_num)

        # filter out name not in four numbers
        if len(apple_num) > 10:
            print(apple_num+" is not a normal apple, ignoring...")
            continue
        
        # filter out the apple marked as skip (finance, construct ...)
        if int(apple_num.split('_')[1]) in skip_list:
            print(apple_num+" is a skipped apple, ignoring...")
            continue

        # filter out not enough amount by not reaching MIN_AMOUNT in average in 5 days
        date_count = 0
        apple_amount_total = 0
        try:
            for date in latest_5_date:
                sql_cursor_Database_squeeze_name.execute("SELECT amount FROM "+apple_num+" WHERE date LIKE "+date+"")
                # printt(sql_cursor_Database_squeeze_name.fetchall()[0][0])
                apple_amount_total += int(str(sql_cursor_Database_squeeze_name.fetchall()[0][0]).replace(',',''))
                date_count += 1
            apple_amount_avg = apple_amount_total / date_count
        except Exception as e:
            print('Error : '+str(e))
            print(apple_num+' is a apple with wrong size, ignoring...')
            continue
        if apple_amount_avg < MIN_AMOUNT*1000:
            print(apple_num+" not enough amount, abort")
            continue

        # filter out any apple not available in 63 days for 42 latest bb
        sql_cursor_Database_squeeze_name.execute("SELECT * FROM "+apple_num+"")
        apple_datas = sql_cursor_Database_squeeze_name.fetchall()
        try :
            for date in latest_63_date:
                found_apple_date = False
                for apple_data in apple_datas:
                    if str(apple_data[0]) == date:
                        found_apple_date = True
                        if str(apple_data[5]) == '--':
                            raise Exception(apple_num+" is a apple with -- data, ignoring...")
                        if isinstance(apple_data[5],str):  
                            raise Exception(apple_num+" is a apple with str data, ignoring...")
                if not found_apple_date:# date might also be missing, add this
                    raise Exception(apple_num+" is a apple with missing date, ignoring...")

        except Exception as e:
            print(e)
            continue 

        # filter out any massive change that is bigger than 10%
        try:
            for date_prev, date_next in zip(All_apple_date[-2:-24:-1],All_apple_date[-1:-23:-1]):
                sql_cursor_Database_squeeze_name.execute("SELECT ends FROM "+apple_num+" WHERE date LIKE "+date_prev+"")
                apple_squeeze_prev = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                sql_cursor_Database_squeeze_name.execute("SELECT ends FROM "+apple_num+" WHERE date LIKE "+date_next+"")
                apple_squeeze_next = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                # print(apple_num)
                # print(date_prev)
                # print(apple_squeeze_prev)
                # print(date_next)
                # print(apple_squeeze_next)
                # print(abs((apple_squeeze_next - apple_squeeze_prev)/apple_squeeze_prev))
                if abs((apple_squeeze_next - apple_squeeze_prev)/apple_squeeze_prev) > 0.101:
                    raise Exception(apple_num+' might has some abnormal shirnking, ignoring')
        except Exception as e:
            print(e)
            continue

        # filter out apple currently not higher than MIN_LATEST_PRICE
        sql_cursor_Database_squeeze_name.execute("SELECT ends FROM "+apple_num+" WHERE date LIKE "+latest_date+"")
        apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
        if apple_price < MIN_LATEST_PRICE:
            print(apple_num+" is too small, ignoring...")
            continue

        # filter out any apple not available in 2 year juice
        try:
            for dates in Year_juice_date:
                for date in dates:
                    sql_cursor_Database_juice_name.execute("SELECT current FROM "+apple_num+" WHERE date LIKE "+date+"")
                    juice_data = sql_cursor_Database_juice_name.fetchall()[0][0]
        except Exception as e:
            print(e)
            print(apple_num+" is a apple with not enough two year juice, ignoring...")
            continue   
        
        #========================================================================================================
        #                               Filter Finish
        #========================================================================================================
        All_good_apple_list.append(apple_num) 

    available_apple_amount = len(All_good_apple_list)
    P_printl("Currently available apple amount is : "+str(available_apple_amount))
    sleep(1)

    top_apple_dict = {}
    mid_apple_dict = {}
    low_apple_dict = {}
    amount_apple_dict = {}
    top_result_list = []
    mid_result_list = []
    low_result_list = []

    for apple_num in All_good_apple_list:
        # calculate 22 bb for latest 42 days
        P_printl("Now is "+apple_num)
        # if apple_num == 'apple_1305':
        #     C()
        count = 0
        bb_top_dict = {}
        bb_mid_dict = {}
        bb_low_dict = {}
        apple_open_dict = {}
        apple_high_dict = {}
        apple_end_dict = {}
        apple_low_dict = {}
        while count < 42:
            This_22_date = All_apple_date[-(22+count):-(1+count)]
            This_22_date.append(All_apple_date[-(1+count)])
            This_bb_avg = 0
            This_date = This_22_date[-1]
            This_bb_mid_list = []
            for date in This_22_date:
                sql_cursor_Database_squeeze_name.execute("SELECT * FROM "+apple_num+" WHERE date LIKE "+date+"")
                apple_squeeze = sql_cursor_Database_squeeze_name.fetchall()
                if count == 0:
                    amount_apple_dict[date] = int(apple_squeeze[0][1].replace(',','')) # get amount for 22 day
                apple_open_dict[date] = apple_squeeze[0][2] # take int out of list(tuple)
                apple_high_dict[date] = apple_squeeze[0][3] 
                apple_low_dict[date] = apple_squeeze[0][4] 
                apple_end_dict[date] = apple_squeeze[0][5] 
                This_bb_mid_list.append(apple_end_dict[date])
            This_bb_avg = sum(This_bb_mid_list) / 22
            bb_std = np.std(This_bb_mid_list)
            bb_top = This_bb_avg + (2 * bb_std)
            bb_low = This_bb_avg - (2 * bb_std)
            bb_mid_dict[This_date] = This_bb_avg
            bb_top_dict[This_date] = bb_top
            bb_low_dict[This_date] = bb_low
            count += 1

        print("apple_open is :")
        print(apple_open_dict)
        print("apple_high is :")
        print(apple_high_dict)
        print("apple_low is :")
        print(apple_low_dict)
        print("apple_end is :")
        print(apple_end_dict)
        print("bb top is :")
        print(bb_top_dict)
        print("bb mid is :")
        print(bb_mid_dict)
        print("bb low is :")
        print(bb_low_dict)

        #calculate juice
        juice_dict = {}
        for dates in Year_juice_date:
            dates_str = dates[0]+'~'+dates[-1]
            juice_data_accu = 0
            for date in dates:
                sql_cursor_Database_juice_name.execute("SELECT current FROM "+apple_num+" WHERE date LIKE "+date+"")
                juice_data = sql_cursor_Database_juice_name.fetchall()[0][0]
                juice_data_accu += juice_data
            juice_dict[dates_str] = juice_data_accu
        this_year_juice = juice_dict[list(juice_dict)[-1]]
        second_year_juice = juice_dict[list(juice_dict)[-2]]
        juice_increase_rate = 1+((this_year_juice - second_year_juice)/ second_year_juice)
        P_printl("juice_increase_rate = "+str(juice_increase_rate))

        P_printl('Using Algo mode '+str(Algo_mode))
        #========================================================
        #                      Top Algo
        #========================================================
        if Algo_mode == 1:
            TOP_TOUCH_COUNT = 3 # how many apple_high should reach the bb_top
            # Mode 1 : touch high by TOP_TOUCH_COUNT days
            # points : round(three_day_rise * a_month_rise) * 100 - 100

            #calculate Top_points = round(three_day_rise * a_month_rise) * 100 - 100
            #note that for multipling the factors we have to shift it to 0.xx~1.xx, not signed numbers
            three_day_rise = 1 + (apple_end_dict[All_apple_date[-1]] - apple_end_dict[All_apple_date[-3]]) / apple_end_dict[All_apple_date[-3]]
            month_rise = 1 + (apple_end_dict[All_apple_date[-1]] - apple_end_dict[All_apple_date[-22]]) / apple_end_dict[All_apple_date[-22]]
            Top_points = round(three_day_rise * month_rise * 100) - 100
            P_printl("Top_points = "+str(Top_points)+'%')

            count = 0
            try:
                for date in All_apple_date[::-1]:
                    if count == TOP_TOUCH_COUNT:
                        break 
                    if apple_high_dict[date] < bb_top_dict[date]:
                        raise Exception(apple_num+" does not high enough!") 
                    count += 1
                P_printl(apple_num+" is an top apple!")
                top_apple_dict[apple_num] = Top_points
                continue # once found the apple type, ignore the other type calculation
            except Exception as e:
                P_printl(e)
        
        # Mode 2 : find those want to soar 
        # requirements : once touch high in five days, and amount also reach a month high in 5 days
        # Points : 22..*5*4*3*2_day_rise (end-end) * 6*5*4*3*2 juice rate
        if Algo_mode == 2:
            days_rise = 1 # mode 2
            for n in range(2,23):# mode 2
                days_rise *= 1+((apple_end_dict[All_apple_date[-n+1]] - apple_end_dict[All_apple_date[-n]]) / apple_end_dict[All_apple_date[-n]])# mode 2

            Top_points = round(days_rise * 100) - 100 # mode 2
            P_printl("Top_points = "+str(Top_points)+'%')

            count = 0
            high_touch = 0
            try:
                for date in All_apple_date[::-1]:
                    if high_touch:
                        break
                    if count == 5:
                        raise Exception(apple_num+" does not touch top in 5 days")
                    if apple_high_dict[date] > bb_top_dict[date]:
                        high_touch = 1 
                    count += 1
                P_printl(apple_num+" is an top apple!")
                top_apple_dict[apple_num] = Top_points
            
            except Exception as e:
                P_printl(e)
        
        # Mode 3 : low variance touch the high
        # requirements : once touch high in five days, and amount also reach a month high in 5 days
        # points : decreased by variance from 100
        # note : top 5 result should assistnat judgement by drawings
        if Algo_mode == 3:
            count = 0
            high_touch = 0
            try:
                for date in All_apple_date[::-1]:
                    if high_touch:
                        steady_ratio = 1
                        for n in range(5,22):
                            steady_ratio *= 1-(abs((apple_end_dict[All_apple_date[-n+1]] - apple_end_dict[All_apple_date[-n]]) / apple_end_dict[All_apple_date[-n]]))
                        amount_ratio = math.pow(0.8, (amount_apple_dict[latest_date] / (sum(amount_apple_dict.values()) / len(amount_apple_dict.values()))) / 10)
                        Top_points = round(steady_ratio * amount_ratio * 100) 
                        P_printl("Top_points = "+str(Top_points)+'%')
                        break
                    if count == 5:
                        raise Exception(apple_num+" does not touch top in 5 days")
                    if apple_high_dict[date] > bb_top_dict[date]:
                        high_touch = 1 
                    count += 1
                P_printl(apple_num+" is an top apple!")
                top_apple_dict[apple_num] = Top_points
            except Exception as e:
                P_printl(e)
        
        # Mode 4
        # requirements : once touch high in five days
        # points : 5 days rate mul, if low over top change to minus
        # action in : first one, 40% in at any, if yesterday high does not touch top, next day 40% in at any 
        # action out: 4 days high not touch top, next day sell at any
        if Algo_mode == 4:
            count = 0
            try:
                for date in All_apple_date[::-1]:
                    if count == 5:
                        raise Exception(apple_num+" does not touch top in 5 days")
                    if apple_high_dict[date] > bb_top_dict[date]:
                        break
                    count += 1
                P_printl(apple_num+" is an top apple!")

                days_rise = 1 
                for n in range(2,7):
                    diff = apple_end_dict[All_apple_date[-n+1]] - apple_end_dict[All_apple_date[-n]]
                    if apple_low_dict[All_apple_date[-n+1]] > bb_top_dict[All_apple_date[-n+1]] and diff > 0:
                        diff = diff * -1
                    days_rise *= 1+(diff / apple_end_dict[All_apple_date[-n]])

                Top_points = round(days_rise * 100 - 100,2)
                P_printl("Top_points = "+str(Top_points)+'%')

                top_apple_dict[apple_num] = Top_points
            except Exception as e:
                P_printl(e)
            

        #========================================================
        #                      Mid Algo
        #========================================================
        if Algo_mode == 1:
            DAYS_TO_STAY_HIGHER_MID = 8 # days in 22 to stay above mid by MAX_END_DROP_HIGHER_THAN_MID
            MAX_END_DROP_HIGHER_THAN_MID = 0.05 
            MAX_END_DROP_LOWER_THAN_MID = -0.02 # all 22 not drop over this
            MID_CONSEC_RISE = 3 # how many weeks mid should always be higher than previous
            # Mode 1:
            # chceck if : 1. more than DAYS_TO_STAY_HIGHER_MID days to stay on top MAX_END_DROP_HIGHER_THAN_MID
            #             2. 22 not drop over mid by MAX_END_DROP_LOWER_THAN_MID
            #             3. check if mid is rising
            Mid_points = juice_increase_rate
            count = 0
            try:
                for date in latest_22_date[::-1]:
                    ratio = (apple_end_dict[date] - bb_mid_dict[date]) / bb_mid_dict[date]
                    if ratio > MAX_END_DROP_HIGHER_THAN_MID:
                        count += 1
                    if ratio < MAX_END_DROP_LOWER_THAN_MID:
                        raise Exception(apple_num+" is a apple that drop over mid more than MAX_END_DROP_LOWER_THAN_MID, ignoring...") 
                if count < DAYS_TO_STAY_HIGHER_MID:
                    raise Exception(apple_num+" is a apple that does not pass more than DAYS_TO_STAY_HIGHER_MID days to stay on top MAX_END_DROP_HIGHER_THAN_MID, ignoring...") 
                # check if mid is rising
                for i in range(0,MID_CONSEC_RISE):
                    if apple_end_dict[All_apple_date[-(i+1)*5]] > apple_end_dict[All_apple_date[-(i*5+1)]]:
                        raise Exception(apple_num+" does not meet consec mid high!")
                # if currently touch mid then add it
                if apple_low_dict[latest_date] < bb_mid_dict[latest_date]:
                    P_printl(apple_num+" is an mid apple!")
                    mid_apple_dict[apple_num] = Mid_points
            except Exception as e:
                P_printl(e)  
        # Mode 2 : try alicia and colin
        # requirements : does not touch high in 5 days but above mid in 22 days
        # points : month_rise * juice_increase_rate
        if Algo_mode == 2:
            MAX_END_DROP_LOWER_THAN_MID = -0.02 # all 22 not drop over this
            # month_rise = 1
            # for n in range(9,23): # this way we want a flat out better than a fast drop, starts from 8 days ago
            #     month_rise *= 1 + (apple_end_dict[All_apple_date[-8]] - apple_end_dict[All_apple_date[-n]]) / apple_end_dict[All_apple_date[-n]]
            # Mid_points = round(month_rise * juice_increase_rate * 100) - 100
            days_rise = 1 
            for n in range(11,32): # find highest one 10 days ago in a month
                days_rise *= 1+((apple_end_dict[All_apple_date[-n+1]] - apple_end_dict[All_apple_date[-n]]) / apple_end_dict[All_apple_date[-n]])# mode 2
            Mid_points = round(days_rise * 100) - 100
            P_printl("Mid_points = "+str(Mid_points))
            try:
                # check that apple should not touch high in five days
                count = 0
                for date in All_apple_date[::-1]:
                    if high_touch:
                        raise Exception(apple_num+" touched top in 5 days")
                    if count == 5:
                        break
                    if apple_high_dict[date] > bb_top_dict[date]:
                        high_touch = 1 
                    count += 1
                # check if drop over mid, also take average with a before/after days
                # for date in latest_22_date[::-1]:
                #     ratio = (apple_end_dict[date] - bb_mid_dict[date]) / bb_mid_dict[date]
                for n in range(2,23):
                    ratio = ((apple_end_dict[All_apple_date[-n]] + apple_end_dict[All_apple_date[-(n-1)]] + apple_end_dict[All_apple_date[-(n+1)]])/3 - bb_mid_dict[All_apple_date[-n]]) / bb_mid_dict[All_apple_date[-n]]
                    if ratio < MAX_END_DROP_LOWER_THAN_MID:
                        raise Exception(apple_num+" is a apple that mean 3 drop over mid more than MAX_END_DROP_LOWER_THAN_MID, ignoring...") 
                P_printl(apple_num+" is an mid apple!")
                mid_apple_dict[apple_num] = Mid_points
            except Exception as e:
                P_printl(e)
        # Mode 3 has no mid
        if Algo_mode == 3:
            #do nothing
            P_printl("ignore mid")

        # Mode 4
        # requirements : high does not touch top or low in 5 days
        # points : 10~32 days mul 
        # action in : first one, 40% in at any price, if yesterday touch low, next day 40% in at any price
        # action out: over 22 days after either in, over 10%(25%) after double in
        if Algo_mode == 4:
            MAX_END_DROP_LOWER_THAN_MID = -0.02 # all 22 not drop over this
            try:
                # check that apple should not touch high in five days
                count = 0
                for date in All_apple_date[::-1]:
                    if apple_high_dict[date] > bb_top_dict[date] or apple_low_dict[date] < bb_low_dict[date]:
                        raise Exception(apple_num+" touched top or low in 5 days")
                    if count == 5:
                        break
                    count += 1
                 
                P_printl(apple_num+" is an mid apple!")

                days_rise = 1 
                for n in range(11,32): 
                    penalty = (apple_end_dict[All_apple_date[-n+1]] - apple_end_dict[All_apple_date[-n]])
                     # if over mid double the penalty
                    if apple_end_dict[All_apple_date[-n]] < bb_mid_dict[All_apple_date[-n]] and penalty < 0:
                        penalty = penalty * 2
                    days_rise *= 1+(penalty / apple_end_dict[All_apple_date[-n]])
               
                Mid_points = round(days_rise * 100 - 100, 2)
                P_printl("Mid_points = "+str(Mid_points))

                mid_apple_dict[apple_num] = Mid_points
            except Exception as e:
                P_printl(e)

        #========================================================
        #                      Low Algo
        #========================================================
        if Algo_mode == 1:
            LOW_TOUCH_COUNT = 1 # how many apple_low should reach the bb_low
            # Mode 1 : check if apple_low touch the bb_low
            #calculate Low_points = (1+((bblow - apple_low) / apple_low)) * (1+((bb_low - apple_open) / apple_open)) * 100 - 100
            Low_points = (1+((bb_low_dict[latest_date] - apple_low_dict[latest_date]) / apple_low_dict[latest_date])) \
                            *(1+((bb_low_dict[latest_date] - apple_open_dict[latest_date]) / apple_open_dict[latest_date])) \
                            * 100 - 100
            P_printl("Low_points = "+str(Low_points)+'%')

            count = 0
            try:
                for date in All_apple_date[::-1]:
                    if count == LOW_TOUCH_COUNT:
                        break
                    if apple_low_dict[date] > bb_low_dict[date]:
                        raise Exception(apple_num+" does not low enough!") 
                    count += 1
                P_printl(apple_num+" is an low apple!")
                low_apple_dict[apple_num] = Low_points
                continue # once found the apple type, ignore the other type calculation
            except Exception as e:
                P_printl(e)

        # Mode 2 : Catch the bumpy ones
        # requirements : once touch low in five days
        # Points : mainly compare how many times it goes near at high/low in turn within 42 days, if equal then compare the bump range
        if Algo_mode == 2:
            Low_points = 0
            direction = 'up'
            last_day = latest_date
            for date in latest_42_date[::-1]:
                # print(date)
                if (bb_top_dict[date] - apple_high_dict[date])/apple_high_dict[date] < 0.02 and \
                        direction == 'up' and (apple_end_dict[date] - apple_end_dict[last_day])/apple_end_dict[last_day] > 0.05:
                    Low_points += 1+ ((apple_end_dict[date] - apple_end_dict[last_day])/apple_end_dict[last_day]) / 100
                    direction = 'low'
                    last_day = date
                    # print(bb_top_dict[date])
                    # print(apple_high_dict[date])
                    # print((bb_top_dict[date] - apple_high_dict[date])/apple_high_dict[date])
                    # print(str(apple_num)+'low')
                if (apple_low_dict[date] - bb_low_dict[date])/bb_low_dict[date] < 0.02 and \
                            direction == 'low' and (apple_end_dict[last_day] - apple_end_dict[date])/apple_end_dict[date] > 0.05:
                    Low_points += 1 + ((apple_end_dict[last_day] - apple_end_dict[date])/apple_end_dict[date]) / 100
                    direction = 'up' 
                    last_day = date
                    # print((apple_low_dict[date] - bb_low_dict[date])/bb_low_dict[date])
                    # print(str(apple_num)+'up')

            # for n in range(2,6):
            #     Low_points *= 1+((apple_high_dict[latest_date] - apple_low_dict[All_apple_date[-n]]) / apple_low_dict[All_apple_date[-n]])
            
            # Low_points = Low_points * 100 - 100 
            # Low_points = Low_points * juice_increase_rate
            P_printl("Low_points = "+str(Low_points))

            count = 0
            try:
                for date in All_apple_date[::-1]:
                    if count == 5:
                        raise Exception(apple_num+" does not touch low in 5 days")
                    if apple_low_dict[date] < bb_low_dict[date]:
                        break
                    count += 1
                P_printl(apple_num+" is an low apple!")
                low_apple_dict[apple_num] = Low_points
            except Exception as e:
                P_printl(e)

        # Mode 3 : top variance touch the low , sell when reach top
        # requirements : once touch low in five days, and amount also reach a month high in 5 days
        # points : increased by variance from 100 X (max_amount / acg_amount)
        # note : top 5 result should assistnat judgement by drawings
        if Algo_mode == 3:
            count = 0
            low_touch = 0
            try:
                for date in All_apple_date[::-1]:
                    if low_touch:
                        steady_ratio = 1
                        for n in range(5,22):
                            steady_ratio *= 1+(abs((apple_end_dict[All_apple_date[-n+1]] - apple_end_dict[All_apple_date[-n]]) / apple_end_dict[All_apple_date[-n]]))
                        amount_ratio = math.pow(0.8, (amount_apple_dict[latest_date] / (sum(amount_apple_dict.values()) / len(amount_apple_dict.values()))) / 10)
                        Low_points = round(steady_ratio * amount_ratio * 100) 
                        P_printl("Low_points = "+str(Low_points)+'%')
                        break
                    if count == 5:
                        raise Exception(apple_num+" does not touch low and reach max amount in 5 days")
                    if apple_low_dict[date] < bb_low_dict[date]:
                        print("found low condition")
                        low_touch = 1 
                    count += 1
                P_printl(apple_num+" is an low apple!")
                low_apple_dict[apple_num] = Low_points
            except Exception as e:
                P_printl(e)
        
        # Mode 4
        # requirements : low touch low in 5 days
        # points : touch high low count + bumpy rate * amount rate
        # action in : first one, 40% in at any, if yesterday drop over 10%, next day in at any
        # action out: 22 days after in, or touch mid, or 10 after double in
        if Algo_mode == 4:
            count = 0
            try:
                for date in All_apple_date[::-1]:
                    if count == 5:
                        raise Exception(apple_num+" does not touch low in 5 days")
                    if apple_low_dict[date] < bb_low_dict[date]:
                        print("found low condition")
                        break
                    count += 1
                P_printl(apple_num+" is an low apple!")

                Low_points = 0
                direction = 'up'
                last_day = All_apple_date[-1]
                average_amount_3_days = (amount_apple_dict[All_apple_date[-1]] + amount_apple_dict[All_apple_date[-2]] + amount_apple_dict[All_apple_date[-3]])/3
                # higher the amount, lower the point
                amount_ratio = math.pow(0.8, (average_amount_3_days / (sum(amount_apple_dict.values()) / len(amount_apple_dict.values()))) / 10)
                for date in latest_42_date[::-1]:
                    date = str(date)
                    
                    if ((bb_top_dict[date] - apple_high_dict[date])/apple_high_dict[date]) < 0.02 and \
                                direction == 'up' and (apple_end_dict[date] - apple_end_dict[last_day])/apple_end_dict[last_day] > 0.05:
                        Low_points = Low_points + 1+ ((apple_end_dict[date] - apple_end_dict[last_day])/apple_end_dict[last_day]) * amount_ratio / 100
                        direction = 'low'
                        last_day = date

                    if ((apple_low_dict[date] - bb_low_dict[date])/bb_low_dict[date]) < 0.02 and \
                                direction == 'low' and (apple_end_dict[last_day] - apple_end_dict[date])/apple_end_dict[date] > 0.05:
                        Low_points = Low_points + 1 + ((apple_end_dict[last_day] - apple_end_dict[date])/apple_end_dict[date]) * amount_ratio / 100
                        direction = 'up' 
                        last_day = date
                P_printl("Low_points = "+str(Low_points))

                low_apple_dict[apple_num] = Low_points
            except Exception as e:
                P_printl(e)

        #========================================================
        #                      VIX Algo
        #========================================================
        # if over 75% stock all reach low in 5 days, prompt the vix warning
        if Algo_mode == 2 or 3 or 4:
            if len(low_result_list) / available_apple_amount > 0.5:
                P_printl('Warning !!!!!')
                P_printl(' $$$$$ V.I.X $$$$$ Coming !!!!!')
                P_printl('Warning !!!!!')


    # Rank the result by their points
    top_result_list = sorted(top_apple_dict.items(), key=lambda x: x[1], reverse=True)
    print("Apple tops are ("+ str(len(top_result_list)) +") :")
    P_printl(top_result_list)

    mid_result_list = sorted(mid_apple_dict.items(), key=lambda x: x[1], reverse=True)
    print("Apple mids are ("+ str(len(mid_result_list)) +") :")
    P_printl(mid_result_list)

    low_result_list = sorted(low_apple_dict.items(), key=lambda x: x[1], reverse=True)
    print("Apple lows are ("+ str(len(low_result_list)) +") :")
    P_printl(low_result_list)

    
    TML = [latest_date+"_top_", latest_date+"_mid_", latest_date+"_low_"]
    RESULT_LEN_LIST = [len(top_result_list), len(mid_result_list), len(low_result_list)]
    MAX_INDEX = RESULT_LEN_LIST.index(max(RESULT_LEN_LIST))
    # check if the last date is the same and remove it before adding a new one
    # note that this "can only" prevent running this script multiple times in a same day from duplicate results
    with open(Fig_dir+'TML_Records.txt') as f:
        TML_records = f.read().splitlines()
    if TML_records[-1].split('_')[0] == latest_date: # delete the duplicate if run multiple times on a same day
        P_delete_file('Figs/TML_Records.txt')
        P_write(TML_records[:-1],'Figs/TML_Records.txt')
    Latest_TML = TML[MAX_INDEX]+str(round(max(RESULT_LEN_LIST)/available_apple_amount*100))+'%'
    P_write(Latest_TML,'Figs/TML_Records.txt')
    P_printl("TML Latest 5 Records :")
    with open(Fig_dir+'TML_Records.txt') as f:
        TML_records = f.read().splitlines()
    for i in range(0,5):
        print(TML_records[len(TML_records)-5+i])

    #========================================================
    #               Write files and adb parsing
    #========================================================

    # Save Figures
    if args.plot_fig:
        for _dir in [Fig_dir+'1_top/',Fig_dir_dropbox+'1_top/',
                     Fig_dir+'2_mid/',Fig_dir_dropbox+'2_mid/',
                     Fig_dir+'3_low/',Fig_dir_dropbox+'3_low/']:
            P_del_file_type_in_dir(_dir,"png")

        count = 1
        for apple_num, juice_increase in top_result_list:
            draw_apple(apple_num, count, Fig_dir+'1_top/', Fig_dir_dropbox+'1_top/')
            count += 1

        count = 1
        for apple_num, juice_increase in mid_result_list:
            draw_apple(apple_num, count, Fig_dir+'2_mid/', Fig_dir_dropbox+'2_mid/')
            count += 1

        count = 1
        for apple_num, juice_increase in low_result_list:
            draw_apple(apple_num, count, Fig_dir+'3_low/', Fig_dir_dropbox+'3_low/')
            count += 1

    #@ create a file to indicate the drawings are finished and use it above to avoid drawing again
    #@ this also need a re-draw input parameter

    # change sort order to backward
    heavens_list = P_get_list_of_files_in_path('Figs/Heavens')
    heavens_list.sort()
    file_index = 999999 - len(heavens_list)
    file_index_PREV = file_index+1
    # if run this multiple times, overwrite the existing one by comparing the date
    if heavens_list[0].split('.txt')[0].split('_')[2] == All_apple_date[-1]:
        file_index += 1
        file_index_PREV += 1
    HEAVEN_DIR = 'Figs/Heavens/Heaven_'+str(file_index)+'_'+latest_date+'.txt'
    HEAVEN_DIR_PREV = 'Figs/Heavens/Heaven_'+str(file_index_PREV)+'_'+prev_date+'.txt'

    # Read the len of each now before rewriting
    if not os.path.exists(HEAVEN_DIR_PREV):
        P_printl('Error : prev data Heaven.txt not found in '+HEAVEN_DIR_PREV)
        return -1

    # Parse result to three bamboo
    if args.adb_parsing:
        with open(HEAVEN_DIR_PREV) as f:
            Heaven_data = f.read()
        LEN_OF_LAST_TOP = int(Heaven_data.split("tops are (")[1].split(')')[0])
        LEN_OF_LAST_MID = int(Heaven_data.split("mids are (")[1].split(')')[0])
        LEN_OF_LAST_LOW = int(Heaven_data.split("lows are (")[1].split(')')[0])

        P_check_adb_connection()

        P_remove_former_three_bamboo(LEN_OF_LAST_TOP, tab_len, MAX_LEN_PARSE)
        P_parse_three_bamboo(top_result_list)
        P_swipe_change_three_bamboo_page()

        P_remove_former_three_bamboo(LEN_OF_LAST_MID, tab_len, MAX_LEN_PARSE)
        P_parse_three_bamboo(mid_result_list)
        P_swipe_change_three_bamboo_page()

        P_remove_former_three_bamboo(LEN_OF_LAST_LOW, tab_len, MAX_LEN_PARSE)
        P_parse_three_bamboo(low_result_list)

    # Save the result 
    P_delete_file(HEAVEN_DIR)
    P_write("==============================================",HEAVEN_DIR)
    P_write("Apple tops are ("+ str(len(top_result_list)) +"):",HEAVEN_DIR)
    P_write(top_result_list,HEAVEN_DIR)
    P_write("==============================================",HEAVEN_DIR)
    P_write("Apple mids are ("+ str(len(mid_result_list)) +"):",HEAVEN_DIR)
    P_write(mid_result_list,HEAVEN_DIR)
    P_write("==============================================",HEAVEN_DIR)
    P_write("Apple lows are ("+ str(len(low_result_list)) +"):",HEAVEN_DIR)
    P_write(low_result_list,HEAVEN_DIR)
    P_write("==============================================",HEAVEN_DIR)

    # also collect the TML latest 5 records into Heaven
    with open(Fig_dir+'TML_Records.txt') as f:
        TML_records = f.read().splitlines()
    P_write("==============================================",HEAVEN_DIR)
    P_write("TML Latest 5 Records :",HEAVEN_DIR)
    P_write(TML_records[-5:],HEAVEN_DIR)
    P_write("==============================================",HEAVEN_DIR)

    #@ also collect the input command and current Utopia_colin.py code?

    #@ parse the result to adb only and do not calculate      

    P_copy_file('utopia.log','Figs/utopia.log')
    logs_list = P_get_list_of_files_in_path('Figs/Logs')
    logs_list.sort()
    file_index_log = 999999 - len(logs_list)
    if logs_list[0].split('.log')[0].split('_')[2] == All_apple_date[-1]:
        file_index_log += 1
    P_copy_file('utopia.log','Figs/Logs/Log_'+str(file_index_log)+'_'+latest_date+'.log')
    # Backup the figs folder to cloud 
    if args.adb_parsing or args.plot_fig:
        P_figs_cloud_backup()  
    # Done            
    P_printl("Finised!")


if __name__ == '__main__':
    main()