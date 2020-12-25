from Utopia_tools import *

#@ show training error

P_enable_logging()
#@ find max paradise apples and analyze
# skip_list = [2548, 2348, 2524, 2505, 2851, 2809,
#              2836, 2889, 5521, 6005, 2884, 2845,
#              2888, 2887, 2890, 5880, 2886, 2812,
#              5876, 2834, 2880, 2801] 
skip_list = []

Database_squeeze_name = 'DB_Avalon.sqlite'
sql_connection_Database_squeeze_name = sqlite3.connect(Database_squeeze_name)
sql_cursor_Database_squeeze_name = sql_connection_Database_squeeze_name.cursor()
Database_juice_name = 'DB_Juice.sqlite'
sql_connection_Database_juice_name = sqlite3.connect(Database_juice_name)
sql_cursor_Database_juice_name = sql_connection_Database_juice_name.cursor()
Database_seeds_name = 'DB_Seeds.sqlite'
sql_connection_Database_seeds_name = sqlite3.connect(Database_seeds_name)
sql_cursor_Database_seeds_name = sql_connection_Database_seeds_name.cursor()

with open('Processed_date_list.txt') as f:
    All_apple_date = f.read().splitlines()
with open('Processed_juice_date_list.txt') as f:
    All_juice_date = f.read().splitlines()
with open('Processed_seeds_date_list.txt') as f:
    All_seeds_date = f.read().splitlines()
with open('Processed_winds_date_list.txt') as f:
    All_winds_date = f.read().splitlines()

# first copy before reverse, 
All_apple_date_reverse = All_apple_date.copy() # this copy is important since list equal will link
All_apple_date_reverse.reverse() # never equal a list to anotehr_list.reverse(), you will get []

# for drawing
color_blue = '#1f77b4'
color_orange = '#ff7f0e'
color_brown = '#A52A2A'
color_green = '#2ca02c'
color_red = '#d62728'
color_purple = '#9467bd'
color_black = '#000000'

def parse_command_line():
    
    parser = ArgumentParser(description='Welcome to Utopia\n',
            formatter_class=RawTextHelpFormatter)
    # parser.add_argument('-J', dest='max_juice', default = False, action='store_true', help='max juice')
    parser.add_argument('-a', dest='para1', type = int, action='store', help='para1')
    parser.add_argument('-b', dest='para2', type = int, action='store', help='para2')
    parser.add_argument('-c', dest='para3', type = int, action='store', help='para3')
    parser.add_argument('-d', dest='para4', type = int, action='store', help='para4')
    parser.add_argument('-e', dest='para5', type = int, action='store', help='para5')
    return parser.parse_args()

# -- algo 1
result_top = 0
result_mid = 0
result_low = 0
result_top_ratio = 0
result_mid_ratio = 0
result_low_ratio = 0
hold_apple_days = 0
All_good_apple_price_bb_dict = {}
paradise_top_result_dict = {}
paradise_mid_result_dict = {}
paradise_low_result_dict = {}
hurricane_result_dict = {}
Last_action = ''
hold_apple_type = 0 # 0 = no apple, 1 = buy top, 2 = buy mid, 3 = buy low
MIN_AMOUNT = 1000*10 # price , 1000
latest_n_date_for_MIN_AMOUT = 20
latest_n_date_for_AVALIABLE = 63
latest_n_date_for_BB = latest_n_date_for_AVALIABLE-21
MIN_LATEST_PRICE = 10
MAX_END_DROP_LOWER_THAN_MID = -0.02
HOLD_APPLE = 'none'
PARADISE = 1
after_touch_apple_day = 0
second_grow = 0 # 0 = not yet, 1 = start second grow
hold_apple_price = 0
harvest_apple_price = 0
apple_price_second_grow = 0
Hurricane_THSH = 50
paradise_dict = {}
TYPE_THSH = 150
TYPE_DAY = 3
Top_mul_days = 5
Low_mul_days = 5
Top_mul_days_n_to_n = 15
Low_mul_days_n_to_n = 20
amount_day_n_to_n = 5
Mid_shift_day = 10
Mid_mul_days = 20
Mid_not_close_mid_day = 5
hold_hurricane = 0
hurricane_count_THSH = 3
hurricane_count = 0
hurricane_out_count_THSH = 5
hurricane_out_count = 0
hold_apple_type_str = 'non'
SECOND_GROW_TOP_HARV_THSH = -0.2
SECOND_GROW_MID_HARV_THSH = -0.2
SECOND_GROW_LOW_HARV_THSH_LOW = -0.05
SECOND_GROW_LOW_HARV_THSH_HIGH = 0.05
SECOND_GROW_TOP_GROW_THSH_3_DAY = -0.15
SECOND_GROW_TOP_GROW_THSH_5_DAY = -0.1
grow_date = ''
TOP_OVER_MID_RATE = -0.02
pick_ratio_in_list = 1
juice_rate_max = 100 # currently only for top and mid
juice_rate_min = -100
MIN_SL_SCORE_FROM_ML_TESTING = 8
juice_pow = 1
replace_mid_to_low = True
LOW_DAY_IGNORE_HARVEST = 1
LOW_POINT_BUMPY_LEN = 20
MIN_RATIO_LOW_LIST_LEN = 0.1
MIN_RATIO_TOP_LIST_LEN = 0.1
LOW_POINT_CLOSE_TO_LOW = 0.01
low_how_close_to_mid_THSH = -0.01
second_low_grow_date = 'non'
Low_second_grow_THSH = -0.05
half_block = {}
OVER_TOP_THSH = -0.05
hold_apple_top_point = 0
hold_apple_top_point_dict = {}
All_holding_apple_dict = {}
grow_date_dict = {}
ALL_APPLE_ML_DATA = []
VA_ALL_APPLE_ML_DATA = []
HOLD_APPLE_LIST = []
HARVEST_APPLE_list = []
HOLD_APPLE_dict = {}
seeds_increase_rate_dict = {}
len_init_hold_apple_dict = 0
final_input_today_list = []
start_day_shift = 0
end_day_shift = 0
model = RandomForestRegressor(n_estimators=5005)
TR_VA_rate = 0.8
VA_Predict_dict = {}
VA_Predict_output = {}
TR_GROW_LOW_THSH = 0.1
paradise_per_grow_list = []

def Algo1(day_shift, Mode) : # next open is defined as strictly 0900 start
# note : in reality, the operation is delayed a day, so follow it at next open
    global result_top
    global result_mid
    global result_low
    global result_top_ratio
    global result_mid_ratio
    global result_low_ratio
    global hold_apple_days
    global All_good_apple_price_bb_dict
    global hold_apple_type
    global second_grow
    global MIN_AMOUNT
    global latest_n_date_for_MIN_AMOUT
    global latest_n_date_for_AVALIABLE
    global latest_n_date_for_BB
    global MIN_LATEST_PRICE
    global MAX_END_DROP_LOWER_THAN_MID
    global HOLD_APPLE
    global PARADISE
    global All_apple_date_reverse
    global after_touch_apple_day
    global harvest_apple_price
    global apple_price_second_grow
    global hold_apple_price
    global TYPE_THSH
    global Top_mul_days
    global hold_hurricane
    global Hurricane_THSH
    global hurricane_count
    global hurricane_count_THSH
    global hurricane_out_count
    global hurricane_out_count_THSH
    global hold_apple_type_str
    global SECOND_GROW_TOP_HARV_THSH
    global SECOND_GROW_MID_HARV_THSH
    global SECOND_GROW_LOW_HARV_THSH_LOW
    global SECOND_GROW_LOW_HARV_THSH_HIGH
    global SECOND_GROW_TOP_GROW_THSH_3_DAY
    global SECOND_GROW_TOP_GROW_THSH_5_DAY
    global paradise_top_result_dict
    global paradise_mid_result_dict
    global paradise_low_result_dict
    global hurricane_result_dict
    global Last_action
    global grow_date
    global Mid_not_close_mid_day
    global Mid_mul_days
    global TOP_OVER_MID_RATE
    global pick_ratio_in_list
    global juice_rate_max
    global juice_rate_min
    global juice_pow
    global second_low_grow_date
    global half_block
    global hold_apple_top_point
    global hold_apple_top_point_dict
    global All_holding_apple_dict
    global grow_date_dict
    global HOLD_APPLE_LIST
    global HARVEST_APPLE_list
    global VA_Predict_dict
    global VA_Predict_output
    global ALL_APPLE_ML_DATA
    global VA_ALL_APPLE_ML_DATA
    global HOLD_APPLE_dict
    global seeds_increase_rate_dict
    global len_init_hold_apple_dict
    global final_input_today_list
    global start_day_shift
    global end_day_shift
    global model
    global MIN_SL_SCORE_FROM_ML_TESTING
    global paradise_per_grow_list

    is_TR_mode = False
    is_VA_mode = False
    is_SL_mode = False # SL the real condition
    is_RL_mode = False # RL should always start at the real grow date, need to overwrte the hold apple

    if Mode == 'TR':
        P_printl('This is in Training mode')
        is_TR_mode = True
    elif Mode == 'VA':
        P_printl('This is in Validation mode')
        is_VA_mode = True
    elif Mode == 'SL':
        P_printl('This is in SimuLation mode')
        is_SL_mode = True
    elif Mode == 'RL':
        P_printl('This is in Real mode')
        is_RL_mode = True
    else :
        P_printl('Unexpected mode input!',4,-1)
        return

    args = parse_command_line()
    # Top_mul_days_n_to_n = args.para1
    # Low_mul_days_n_to_n = args.para2

    if day_shift == 0 or type(day_shift) != int:
        P_printl('Day_shift should be number greater than 0')
        return

    # let next_date be All_apple_date[0] is fine since if day shift = 0 next_date will not be used
    next_date = All_apple_date[-day_shift]
    today = All_apple_date[-(day_shift+1)]
    prev_date = All_apple_date[-(day_shift+2)]
    P_printl('Today is '+today+', shift = '+str(day_shift),1)
    sql_cursor_Database_squeeze_name.execute("SELECT name FROM sqlite_master WHERE type='table'")
    sql_tables_Database_squeeze_name = sql_cursor_Database_squeeze_name.fetchall()
    All_good_apple_list = []

    month_shift = 0
    while True:
        if P_delta_days(All_juice_date[-1-month_shift]+'10',today) <= 0:
            break;
        month_shift += 1
    month_shift += 1
    Year_juice_date = []
    # list of year, max to 2 year
    for i in list(range(0,2)):
        if i == 0 and month_shift == 0:
            Year_juice_date.append(All_juice_date[-12:])
        else:
            Year_juice_date.append(All_juice_date[-(12+(12*i))-month_shift:-(12*i)-month_shift])
    Year_juice_date.reverse()
    P_printl(Year_juice_date)

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

        # filter out any apple not available in latest_n_date_for_AVALIABLE days for latest_n_date_for_BB latest bb
        sql_cursor_Database_squeeze_name.execute("SELECT * FROM "+apple_num+"")
        apple_datas = sql_cursor_Database_squeeze_name.fetchall()
        try :
            iter_dates = All_apple_date[-(latest_n_date_for_AVALIABLE + day_shift) : -day_shift]

            if is_TR_mode or is_VA_mode: # ML mode grow next day open need to check the availability
                iter_dates += [All_apple_date[-day_shift]] # need the outer [] other wise become '2', '0', '2', '0'

            for date in iter_dates:
                found_apple_date = False
                for apple_data in apple_datas:
                    if str(apple_data[0]) == date:
                        found_apple_date = True
                        if str(apple_data[5]) == '--':
                            raise Exception(apple_num+" is a apple with -- data, ignoring...")
                        if isinstance(apple_data[2],str) or isinstance(apple_data[3],str) \
                           or isinstance(apple_data[4],str) or isinstance(apple_data[5],str):  
                            raise Exception(apple_num+" is a apple with str data, ignoring...")
                if not found_apple_date:# date might also be missing, add this
                    raise Exception(apple_num+" is a apple with missing date, ignoring...")

        except Exception as e:
            print(e)
            continue 

        # filter out not enough amount by not reaching MIN_AMOUNT in average in latest_n_date_for_MIN_AMOUT days
        date_count = 0
        apple_amount_total = 0
        apple_price_total = 0
        try:
            if day_shift == 0:
                iter_dates = All_apple_date[-(latest_n_date_for_MIN_AMOUT + day_shift) : ]
            else:
                iter_dates = All_apple_date[-(latest_n_date_for_MIN_AMOUT + day_shift) : -day_shift]
            for date in iter_dates:
                sql_cursor_Database_squeeze_name.execute("SELECT amount FROM "+apple_num+" WHERE date LIKE "+date+"")
                apple_amount_total += int(str(sql_cursor_Database_squeeze_name.fetchall()[0][0]).replace(',',''))
                sql_cursor_Database_squeeze_name.execute("SELECT ends FROM "+apple_num+" WHERE date LIKE "+date+"")
                apple_price_total += sql_cursor_Database_squeeze_name.fetchall()[0][0]
                date_count += 1
            apple_amount_avg = apple_amount_total / date_count
            apple_price_avg = apple_price_total / date_count
            # print(date)
            # print(apple_num)
            # print(apple_amount_avg)
            # print(apple_price_avg)
        except Exception as e:
            print('Error : '+str(e))
            print(apple_num+' is a apple with wrong size, ignoring...')
            continue
        if apple_amount_avg * apple_price_avg < MIN_AMOUNT*1000:
            # if holding apple, do not exclude it becaues of amount not enough
            # All mode should keep the same, except SL mode can slip the holding 1
            if not (is_SL_mode and apple_num == HOLD_APPLE): # ignore the amount when holding apple in SL
                print(apple_num+" not enough amount, abort")
                continue
        
        # filter out any massive change that is bigger than 10% in 22 days
        try:
            for date_prev, date_next in zip(All_apple_date[-(2+day_shift):-(24+day_shift):-1],All_apple_date[-(1+day_shift):-(23+day_shift):-1]):
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
        sql_cursor_Database_squeeze_name.execute("SELECT ends FROM "+apple_num+" WHERE date LIKE "+today+"")
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
        
        # filter out seeds not available in shifted today for a month
        found_14_close_seed_flag = False
        sql_cursor_Database_seeds_name.execute("SELECT * FROM "+apple_num+"")
        sql_seeds = sql_cursor_Database_seeds_name.fetchall()
        All_seeds_date_apple = [i[0] for i in sql_seeds]
        seeds_date_shift = 0
        for date in All_seeds_date_apple[::-1]:
            # print(date)
            if 14 > P_delta_days(today,str(date)) > 0:
                found_14_close_seed_flag = True
                break;
            else:
                seeds_date_shift += 1
        if not found_14_close_seed_flag:
            print('Not enough seeds')
            continue
        # check if shifted all last seeds date matches a month for all 5 dates
        # print(seeds_date_shift)
        seeds_date_month_shift = 0
        seeds_a_month_match_flag = True
        for date in All_seeds_date[::-1][seeds_date_shift:seeds_date_shift+5]:
            # check if the date matches
            # print(str(All_seeds_date_apple[-1-seeds_date_shift-seeds_date_month_shift]))
            # print(date)
            if str(All_seeds_date_apple[-1-seeds_date_shift-seeds_date_month_shift]) != date:
                print('seeds date for a month does not match')
                seeds_a_month_match_flag = False
                break;
            # also check if the sum could be zero
            seeds_data = sql_seeds[-1-seeds_date_shift-seeds_date_month_shift]
            # print(seeds_data)
            sum_data = 0
            for i in range(1,16):
                if type(seeds_data[i]) != float:
                    print('non float seeds, abort')
                    seeds_a_month_match_flag = False
                    break;
                sum_data += seeds_data[i]
            if sum_data == 0:
                print('zero seeds, abort')
                seeds_a_month_match_flag = False
            # print(sum_data)
            seeds_date_month_shift += 1
        if not seeds_a_month_match_flag:
            print('Not match a month seeds')
            continue
        
        #========================================================================================================
        #                               Filter Finish
        #========================================================================================================
        All_good_apple_list.append(apple_num) 
    
    available_apple_amount = len(All_good_apple_list)
    P_printl(today+" available apple amount is : "+str(available_apple_amount),2,3)
    sleep(1)

    top_apple_dict = {}
    mid_apple_dict = {}
    low_apple_dict = {}
    amount_apple_dict = {}
    top_result_list = []
    mid_result_list = []
    low_result_list = []
    juice_increase_rate_dict = {}
    seeds_increase_rate_dict = {}

    for apple_num in All_good_apple_list:
        # calculate 22 bb for latest latest_n_date_for_BB days
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
        while count < latest_n_date_for_BB:
            if day_shift == 0 and count == 0:
                This_22_date = All_apple_date[-22:]
            else:
                This_22_date = All_apple_date[-(22+count+day_shift):-(count+day_shift)]
            This_bb_avg = 0
            This_date = This_22_date[-1]
            This_bb_mid_list = []
            for date in This_22_date:
                sql_cursor_Database_squeeze_name.execute("SELECT * FROM "+apple_num+" WHERE date LIKE "+date+"")
                apple_squeeze = sql_cursor_Database_squeeze_name.fetchall()
                if count == 0:
                    # note that amount 0 can turn into int, so str(apple_squeeze[0][1])
                    amount_apple_dict[date] = int(str(apple_squeeze[0][1]).replace(',','')) # get amount for 22 day
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

        # print('Current day is '+today)
        # print("apple_open is :")
        # print(apple_open_dict)
        # print("apple_high is :")
        # print(apple_high_dict)
        # print("apple_low is :")
        # print(apple_low_dict)
        # print("apple_end is :")
        # print(apple_end_dict)
        # print("bb top is :")
        # print(bb_top_dict)
        # print("bb mid is :")
        # print(bb_mid_dict)
        # print("bb low is :")
        # print(bb_low_dict)

        # collect all of them as a list of dict for this apple
        # note that this based on current shifted day
        All_good_apple_price_bb_dict[apple_num] = { 'open' : apple_open_dict,
                                                    'high' : apple_high_dict,
                                                    'low'  : apple_low_dict,
                                                    'end'  : apple_end_dict,
                                                    'bb_top' : bb_top_dict,
                                                    'bb_mid' : bb_mid_dict,
                                                    'bb_low' : bb_low_dict
                                                  }
        # print(All_good_apple_price_bb_dict) # cost too much time
        
        #calculate the half block by seperate the max bb top and min bb low into 5 blocks 
        #(half block = /10)
        max_bb_top = max(list(bb_top_dict.values()))
        min_bb_low = min(list(bb_low_dict.values()))
        half_block[apple_num] = (max_bb_top - min_bb_low)/10


        #calculate juice just for the grow one
        print('juice '+apple_num)
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
        juice_increase_rate = ((this_year_juice - second_year_juice)/ second_year_juice) * 100
        P_printl("juice_increase_rate ori = "+str(juice_increase_rate))
        # juice_increase_rate = pow(juice_increase_rate, juice_pow)
        juice_increase_rate = round(max(min(juice_increase_rate,juice_rate_max),juice_rate_min),1)
        juice_increase_rate_dict[apple_num] = juice_increase_rate
        P_printl("juice_increase_rate = "+str(juice_increase_rate))

        # calculate seeds growth rate for a month 
        print('seeds '+apple_num)
        sql_cursor_Database_seeds_name.execute("SELECT * FROM "+apple_num+"")
        sql_seeds = sql_cursor_Database_seeds_name.fetchall()
        seeds_month_growth = 1
        for seeds_date_month_shift in range(0,5):
            seeds_first_data = sql_seeds[-1-seeds_date_shift-seeds_date_month_shift]
            seeds_second_data = sql_seeds[-1-seeds_date_shift-4-1]
            # print(seeds_first_data)
            # print(seeds_second_data)
            small_seeds_first = 0
            big_seeds_first = 0
            small_seeds_second = 0
            big_seeds_second = 0
            for i in list(range(1,16)):
                if i < 10:
                    small_seeds_first += seeds_first_data[i]
                    small_seeds_second += seeds_second_data[i]
                else:
                    big_seeds_first += seeds_first_data[i]
                    big_seeds_second += seeds_second_data[i]
            # print(small_seeds_first)
            # print(big_seeds_first)
            # print(small_seeds_second)
            # print(big_seeds_second)
            seeds_ratio_first = big_seeds_first/small_seeds_first
            seeds_ratio_second = big_seeds_second/small_seeds_second
            seeds_first_second_ratio = 1 + ((seeds_ratio_first - seeds_ratio_second) / seeds_ratio_second)
            seeds_month_growth *= seeds_first_second_ratio
            # print(seeds_ratio_first)
            # print(seeds_ratio_second)
            # print(seeds_first_second_ratio)
        seeds_increase_rate_dict[apple_num] = round((seeds_month_growth-1) * 100)

        #========================================================
        #                      Top Algo
        #========================================================
        
        # requirements : once touch high in five days
        # points : 5 days rate mul, if end over top change to minus
        
        count = 0
        try:
            # for date in All_apple_date_reverse[day_shift:day_shift+6]:
            #     if count == 5:
            #         raise Exception(apple_num+" does not touch top in 5 days")
            #     if apple_high_dict[date] > bb_top_dict[date]:
            #         break
            #     count += 1
            if apple_high_dict[today] < bb_top_dict[today] :
                raise Exception(apple_num+" does not touch top")
            P_printl(apple_num+" is an top apple!")

            # days_rise = 1
            # for n in range(1,20+1):
            #     days_rise *= 1 + ((bb_mid_dict[All_apple_date[-n-day_shift]] - bb_mid_dict[All_apple_date[-20-1-day_shift]]) / bb_mid_dict[All_apple_date[-20-1-day_shift]])

            # for n in range(1,5+1):
            #     if apple_low_dict[All_apple_date[-n-day_shift]] > bb_top_dict[All_apple_date[-n-day_shift]]:
            #         days_rise *= 0.5
            #     mid = (apple_high_dict[All_apple_date[-n-day_shift]] - apple_low_dict[All_apple_date[-n-day_shift]])/2 + apple_low_dict[All_apple_date[-n-day_shift]]
            #     days_rise *= 1 - abs((mid - bb_top_dict[All_apple_date[-n-day_shift]])/bb_top_dict[All_apple_date[-n-day_shift]])

            # Top_points = round(days_rise,1)
            Top_points = seeds_increase_rate_dict[apple_num] * -1
            P_printl("Top_points = "+str(Top_points)+'%')
            hold_apple_top_point_dict[apple_num+'_'+today] = Top_points

            top_apple_dict[apple_num] = Top_points
            
        except Exception as e:
            P_printl(e)

        
        #========================================================
        #                      Mid Algo
        #========================================================
        
        try:
            # check that apple should not touch high in five days
            # count = 0
            # for date in All_apple_date_reverse[day_shift:day_shift+6]:
            #     if apple_high_dict[date] > bb_top_dict[date] or apple_low_dict[date] < bb_low_dict[date]:
            #         raise Exception(apple_num+" touched top or low in 5 days")
            #     if count == 5:
            #         break
            #     count += 1
            if apple_high_dict[today] > bb_top_dict[today] or apple_low_dict[today] < bb_low_dict[today]:
                raise Exception(apple_num+" touched top or low")
            P_printl(apple_num+" is an mid apple!")

            mid_apple_dict[apple_num] = 2
        except Exception as e:
            P_printl(e)

        #========================================================
        #                      Low Algo
        #========================================================

        count = 0
        try:
            # for date in All_apple_date_reverse[day_shift:day_shift+6]:
            #     if count == 5:
            #         raise Exception(apple_num+" does not touch low in 5 days")
            #     if apple_low_dict[date] < bb_low_dict[date]:
            #         print("found low condition")
            #         break
            #     count += 1
            if apple_low_dict[today] > bb_low_dict[today]:
                raise Exception(apple_num+" does not touch low")
            P_printl(apple_num+" is an low apple!")
            low_apple_dict[apple_num] = 3
        except Exception as e:
            P_printl(e)


    # Rank the result by their points
    top_result_list = sorted(top_apple_dict.items(), key=lambda x: x[1], reverse=True)
    P_printl(today+" Apple tops are ("+ str(len(top_result_list)) +") :",1)
    P_printl(top_result_list)

    mid_result_list = sorted(mid_apple_dict.items(), key=lambda x: x[1], reverse=True)
    P_printl(today+" Apple mids are ("+ str(len(mid_result_list)) +") :",1)

    low_result_list = sorted(low_apple_dict.items(), key=lambda x: x[1], reverse=True)
    P_printl(today+" Apple lows are ("+ str(len(low_result_list)) +") :",1)

    RESULT_LEN_LIST = [len(top_result_list), len(mid_result_list), len(low_result_list)]
    P_printl('RESULT_LEN_LIST = '+str(RESULT_LEN_LIST))

    # for hold_apple_date in HOLD_APPLE_dict:
    #     print('Currently holding apple : '+str(HOLD_APPLE_dict[hold_apple_date]))
    # gather the dict by date, but not apple_num

    # harvest first to prevent harvest at growing

    # iterate though index in all the hold apples and see if harvest them

    if is_SL_mode:

        # use the prediction here for the SL mode and replace the points
        print('SL start prediction at '+today)
        predict_result_list = []
        for top_result in top_result_list: # iterate again for the prediction
            apple_num = top_result[0]
            print(apple_num)
            input_data = [[len(top_result_list), len(mid_result_list), len(low_result_list),
                          available_apple_amount, juice_increase_rate_dict[apple_num], 
                          seeds_increase_rate_dict[apple_num], top_apple_dict[apple_num]]]
            print(input_data)
            predict_result_sl = round(model.predict(input_data)[0],1)
            predict_result_list.append([apple_num, predict_result_sl])
            P_printl("Predict Top_points = "+str(predict_result_sl))
        # rank again
        predict_result_list.sort(key=lambda x: x[-1], reverse=True)
        P_printl("Predict tops are ("+ str(len(predict_result_list)) +") :",1)
        P_printl(predict_result_list)

        # harvest only when holding
        if len(HOLD_APPLE_LIST) > 0:
            # check condition first
            
            grow_date = HOLD_APPLE_LIST[0]
            HOLD_APPLE = HOLD_APPLE_LIST[1]
            P_printl('Current holding apple is : '+HOLD_APPLE,3)
            hold_apple_price = HOLD_APPLE_LIST[2]
            predict_result = HOLD_APPLE_LIST[3]
            sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
            harvest_apple_price = 0
            try:
                harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            except:
                P_printl('Warning next_date '+HOLD_APPLE+' does not exist, assuming no growing',5)
                HOLD_APPLE_LIST = []
            if harvest_apple_price:
                print(HOLD_APPLE)
                print(today)
                print(All_good_apple_price_bb_dict)
                grow_length = All_apple_date.index(today) - All_apple_date.index(grow_date)
                is_high_over_top_half_block = All_good_apple_price_bb_dict[HOLD_APPLE]['high'][today] - All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today] > half_block[HOLD_APPLE]            
                is_high_over_top_half_block_after_1 = is_high_over_top_half_block and grow_length >= 1
                is_low_higher_than_top_2_p = (All_good_apple_price_bb_dict[HOLD_APPLE]['low'][today] - All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today])/All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today] > 0.02
                is_low_higher_than_top_2_p_after_1 = is_low_higher_than_top_2_p and grow_length >= 1
                is_over_half_block = All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today] - All_good_apple_price_bb_dict[HOLD_APPLE]['high'][today] > half_block[HOLD_APPLE]
                is_over_half_block_after_1 = grow_length >= 1 and is_over_half_block

                # believe the topest now
                price_diff_rate = round((harvest_apple_price - hold_apple_price) / hold_apple_price * 100,1)
                P_printl('price_diff_rate = '+str(price_diff_rate)+', predict_result = '+str(predict_result))
                # is_price_diff_rate_over_predict_result = price_diff_rate > predict_result
                # if is_price_diff_rate_over_predict_result:
                #     P_printl('price_diff_rate reach predict_result',3)

                if is_over_half_block_after_1:
                    P_printl('is_over_half_block_after_1 detected')
                if is_high_over_top_half_block_after_1:
                    P_printl('is_high_over_top_half_block_after_1 detected')
                if is_low_higher_than_top_2_p_after_1:
                    P_printl('is_low_higher_than_top_2_p_after_1 detected')
                if is_over_half_block_after_1 or is_low_higher_than_top_2_p_after_1 :
                    # harvest
                    P_printl('harvest '+HOLD_APPLE+' at '+today,1)
                    P_printl('harvest_apple_price = '+str(harvest_apple_price),1)
                    P_printl('price_diff_rate = '+str(price_diff_rate)+'%',1)
                    PARADISE *= 1+price_diff_rate/100
                    P_printl('now the PARADISE is = '+str(PARADISE),1)
                    HARVEST_APPLE_list.append([HOLD_APPLE, grow_date, today, grow_length, predict_result, price_diff_rate])
                    HOLD_APPLE_LIST = []

        P_printl('SL HARVEST_APPLE_list :',3)
        HARVEST_APPLE_list.sort(key=lambda x: x[-1], reverse=True)
        P_printl(HARVEST_APPLE_list)

        # grow only when no holding        
        if len(HOLD_APPLE_LIST) ==  0:
            # grow apple check
            # first check if exist
            P_printl('Currently holding no apple',3)
            if len(predict_result_list) < 5:
                P_printl('Do nothing when top less than 5 amount',3)
                return
            #@ first check if the middle of the top list > 0 and the highest one > 5
            greater_zero_c = 0
            for tp in predict_result_list:
                if tp[1] > 0:
                    greater_zero_c += 1
            greater_zero_c_rate = round(greater_zero_c/len(predict_result_list),2)
            P_printl('greater_zero_c_rate = '+str(greater_zero_c_rate))
            if greater_zero_c_rate < 0.5:
                P_printl('more than half lesser than 0, grow nothing',3)
                return
            if predict_result_list[0][1] < MIN_SL_SCORE_FROM_ML_TESTING:
                P_printl('highest prediction lower than MIN_SL_SCORE_FROM_ML_TESTING, grow nothing',3)
                return
            # grow apple
            apple_num = predict_result_list[0][0]
            predict_result = predict_result_list[0][1]
            sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+apple_num+" WHERE date LIKE "+next_date+"")
            apple_open = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            # grow value determined by next open, assume never miss
            P_printl(today+' : Grow top apple '+apple_num+' with '+str(apple_open),2)
            HOLD_APPLE_LIST = [today, apple_num, apple_open, predict_result] 

    if is_TR_mode:
        
        pop_apple_num_date = []
        for apple_num_hold_apple_date in HOLD_APPLE_dict:

            HOLD_APPLE = HOLD_APPLE_dict[apple_num_hold_apple_date][1]
            hold_apple_price = HOLD_APPLE_dict[apple_num_hold_apple_date][2]
            after_touch_apple_day = HOLD_APPLE_dict[apple_num_hold_apple_date][3]
            grow_date = apple_num_hold_apple_date.split('_')[2]
            
            if HOLD_APPLE not in All_good_apple_list:
                P_printl(HOLD_APPLE)
                P_printl(All_good_apple_list)
                P_printl('Apple turns into unavailable, pop it and assume this never exist')
                pop_apple_num_date.append(apple_num_hold_apple_date)
                continue

            bb_top_today = All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today]
            bb_mid_today = All_good_apple_price_bb_dict[HOLD_APPLE]['bb_mid'][today]
            sql_cursor_Database_squeeze_name.execute("SELECT highs FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
            hold_apple_price_highs_today = sql_cursor_Database_squeeze_name.fetchall()[0][0]

            if hold_apple_price_highs_today > bb_top_today:
                HOLD_APPLE_dict[apple_num_hold_apple_date][3] = 0
            else:
                HOLD_APPLE_dict[apple_num_hold_apple_date][3] += 1
            
            try:
                sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
                harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                HOLD_APPLE_dict[apple_num_hold_apple_date].append(round((harvest_apple_price - hold_apple_price)/hold_apple_price*100,1))
            except Exception as e:
                P_printl(e)
                print('Caught error in getting harvest_apple_price, pop it')
                pop_apple_num_date.append(apple_num_hold_apple_date)
                continue

            grow_length = All_apple_date.index(today) - All_apple_date.index(grow_date)
            is_high_over_top_half_block = All_good_apple_price_bb_dict[HOLD_APPLE]['high'][today] - All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today] > half_block[HOLD_APPLE]            
            is_high_over_top_half_block_after_1 = is_high_over_top_half_block and grow_length >= 1
            is_low_higher_than_top_2_p = (All_good_apple_price_bb_dict[HOLD_APPLE]['low'][today] - All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today])/All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today] > 0.02
            is_low_higher_than_top_2_p_after_1 = is_low_higher_than_top_2_p and grow_length >= 1
            is_over_half_block = All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today] - All_good_apple_price_bb_dict[HOLD_APPLE]['high'][today] > half_block[HOLD_APPLE]
            is_over_half_block_after_1 = grow_length >= 1 and is_over_half_block

            if is_over_half_block_after_1:
                P_printl('is_over_half_block_after_1 detected')
            if is_high_over_top_half_block_after_1:
                P_printl('is_high_over_top_half_block_after_1 detected')
            if is_low_higher_than_top_2_p_after_1:
                P_printl('is_low_higher_than_top_2_p_after_1 detected')
            if (is_over_half_block_after_1 or is_low_higher_than_top_2_p_after_1):
                # harvest
                P_printl('harvest '+HOLD_APPLE+' at '+today,1)
                P_printl('harvest_apple_price = '+str(harvest_apple_price),1)
                price_diff_rate = round((harvest_apple_price - hold_apple_price) / hold_apple_price * 100,1)
                PARADISE *= 1+price_diff_rate/100
                # price_diff_rate just show the start ends
                #@ calculate the avg diff rate, not just start end
                AVG_diff = round(sum(HOLD_APPLE_dict[apple_num_hold_apple_date][-(len(HOLD_APPLE_dict[apple_num_hold_apple_date])-len_init_hold_apple_dict):])/grow_length,1)
                HARVEST_APPLE_list.append([HOLD_APPLE, grow_date, today, grow_length, price_diff_rate, HOLD_APPLE_dict[apple_num_hold_apple_date][2], HOLD_APPLE_dict[apple_num_hold_apple_date][3],
                                            HOLD_APPLE_dict[apple_num_hold_apple_date][4], HOLD_APPLE_dict[apple_num_hold_apple_date][5],
                                            HOLD_APPLE_dict[apple_num_hold_apple_date][6], HOLD_APPLE_dict[apple_num_hold_apple_date][7],
                                            HOLD_APPLE_dict[apple_num_hold_apple_date][8], HOLD_APPLE_dict[apple_num_hold_apple_date][9], 
                                            HOLD_APPLE_dict[apple_num_hold_apple_date][10], AVG_diff])
                
                # only do this when grow single
                All_price_diff = [a[4] for a in HARVEST_APPLE_list]
                paradise_per_grow = round(sum(All_price_diff)/(len(All_price_diff)),1)
                P_printl('PARADISE rate per grow = '+str(paradise_per_grow)+'%')
                #save date by number to show the real time length
                paradise_per_grow_list.append([int(today),paradise_per_grow])
                
                # print('colin4')
                # print(HOLD_APPLE)
                # print(today)
                # print(grow_length)
                # print(HOLD_APPLE_dict[apple_num_hold_apple_date][-(len(HOLD_APPLE_dict[apple_num_hold_apple_date])-8):])
                # print(sum(HOLD_APPLE_dict[apple_num_hold_apple_date][-(len(HOLD_APPLE_dict[apple_num_hold_apple_date])-8):]))
                ALL_APPLE_ML_DATA.append([HOLD_APPLE_dict[apple_num_hold_apple_date][4], HOLD_APPLE_dict[apple_num_hold_apple_date][5],
                                        HOLD_APPLE_dict[apple_num_hold_apple_date][6], HOLD_APPLE_dict[apple_num_hold_apple_date][7], 
                                        HOLD_APPLE_dict[apple_num_hold_apple_date][8], HOLD_APPLE_dict[apple_num_hold_apple_date][9], 
                                        HOLD_APPLE_dict[apple_num_hold_apple_date][10], AVG_diff])
                # HOLD_APPLE_dict.pop(apple_num_hold_apple_date)
                pop_apple_num_date.append(apple_num_hold_apple_date)
                    
        for apple_num_date in pop_apple_num_date:
            P_printl(str(HOLD_APPLE_dict[apple_num_date])+' is poped')
            HOLD_APPLE_dict.pop(apple_num_date)
            
        #@ grow all top apple not just the highest top point
        #@ SL mode will not grow all but just the top predicted
        if len(top_result_list) == 0 or len(low_result_list)/available_apple_amount > TR_GROW_LOW_THSH:
            P_printl('Do nothing when no top or too much low apple',3)
        else:
            # multi
            # for top_result in top_result_list:
            #     apple_num = top_result[0]
            #     apple_top_point = top_result[1]
            #     sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+apple_num+" WHERE date LIKE "+next_date+"")
            #     apple_open = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            #     # grow value determined by next open, assume never miss
            #     P_printl(today+' : Grow top apple '+apple_num+' with '+str(apple_open),2)
            #     HOLD_APPLE_dict[apple_num+'_'+today] = [int(today), apple_num,
            #                             apple_open, 0, len(top_result_list),
            #                             len(mid_result_list), len(low_result_list),
            #                             available_apple_amount, juice_increase_rate_dict[apple_num], 
            #                             seeds_increase_rate_dict[apple_num], apple_top_point] 
            #     len_init_hold_apple_dict = len(HOLD_APPLE_dict[apple_num+'_'+today])

            # # single
            apple_num = top_result_list[0][0]
            apple_top_point = top_result_list[0][1]
            sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+apple_num+" WHERE date LIKE "+next_date+"")
            apple_open = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            # grow value determined by next open, assume never miss
            P_printl(today+' : Grow top apple '+apple_num+' with '+str(apple_open),2)
            HOLD_APPLE_dict[apple_num+'_'+today] = [int(today), apple_num,
                                    apple_open, 0, len(top_result_list),
                                    len(mid_result_list), len(low_result_list),
                                    available_apple_amount, juice_increase_rate_dict[apple_num], 
                                    seeds_increase_rate_dict[apple_num], apple_top_point] 
            len_init_hold_apple_dict = len(HOLD_APPLE_dict[apple_num+'_'+today])
            

        P_printl('TR HOLD_APPLE_dict :',3)
        HOLD_APPLE_dict = dict(sorted(HOLD_APPLE_dict.items(), key=lambda item: item[1][0], reverse=True))
        P_printl(HOLD_APPLE_dict)
        P_printl('TR HARVEST_APPLE_list :',3)
        HARVEST_APPLE_list.sort(key=lambda x: x[-1], reverse=True)
        P_printl(HARVEST_APPLE_list)
        P_printl('TR ALL_APPLE_ML_DATA :',3)
        ALL_APPLE_ML_DATA.sort(key=lambda x: x[-1], reverse=True)
        P_printl(ALL_APPLE_ML_DATA)

        '''
        P_printl(today+' prepare all the today input for testing',2)
        
        first_line = True
        for top_apple in top_result_list:
            # print('apple is '+top_apple[0])
            # print('top point is '+str(top_apple[1]))
            today_list = [len(top_result_list), len(mid_result_list), len(low_result_list),
                            available_apple_amount, juice_increase_rate_dict[top_apple[0]], 
                            seeds_increase_rate_dict[top_apple[0]],top_apple[1]]
            if day_shift == end_day_shift_TR+1:
                final_input_today_list.append(today_list)
            if first_line:
                print(today_list)
            else:
                print(','+str(today_list))
            first_line = False
        '''

    if is_VA_mode:

        # use the prediction here for the VA mode and replace the points
        print('VA start prediction at '+today)
        predict_result_list = []
        for top_result in top_result_list: # iterate again for the prediction
            apple_num = top_result[0]
            print(apple_num)
            input_data = [[len(top_result_list), len(mid_result_list), len(low_result_list),
                          available_apple_amount, juice_increase_rate_dict[apple_num], 
                          seeds_increase_rate_dict[apple_num], top_apple_dict[apple_num]]]
            print(input_data)
            predict_result_va = round(model.predict(input_data)[0],1)
            predict_result_list.append([apple_num, predict_result_va])
            P_printl("Predict Top_points = "+str(predict_result_va))
            VA_Predict_dict[apple_num+'_'+today] = input_data[0]
            VA_Predict_output[apple_num+'_'+today] = predict_result_va
        # rank again
        predict_result_list.sort(key=lambda x: x[-1], reverse=True)
        P_printl("Predict tops are ("+ str(len(predict_result_list)) +") :",1)
        P_printl(predict_result_list)
        
        pop_apple_num_date = []
        for apple_num_hold_apple_date in HOLD_APPLE_dict:

            HOLD_APPLE = HOLD_APPLE_dict[apple_num_hold_apple_date][1]
            hold_apple_price = HOLD_APPLE_dict[apple_num_hold_apple_date][2]
            after_touch_apple_day = HOLD_APPLE_dict[apple_num_hold_apple_date][3]
            predict_diff = HOLD_APPLE_dict[apple_num_hold_apple_date][4]
            grow_date = apple_num_hold_apple_date.split('_')[2]
            
            if HOLD_APPLE not in All_good_apple_list:
                P_printl(HOLD_APPLE)
                P_printl(All_good_apple_list)
                P_printl('Apple turns into unavailable, pop it and assume this never exist')
                pop_apple_num_date.append(apple_num_hold_apple_date)
                continue

            bb_top_today = All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today]
            bb_mid_today = All_good_apple_price_bb_dict[HOLD_APPLE]['bb_mid'][today]
            sql_cursor_Database_squeeze_name.execute("SELECT highs FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
            hold_apple_price_highs_today = sql_cursor_Database_squeeze_name.fetchall()[0][0]

            if hold_apple_price_highs_today > bb_top_today:
                HOLD_APPLE_dict[apple_num_hold_apple_date][3] = 0
            else:
                HOLD_APPLE_dict[apple_num_hold_apple_date][3] += 1
            
            try:
                sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
                harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                HOLD_APPLE_dict[apple_num_hold_apple_date].append(round((harvest_apple_price - hold_apple_price)/hold_apple_price*100,1))
            except Exception as e:
                P_printl(e)
                print('Caught error in getting harvest_apple_price, pop it')
                pop_apple_num_date.append(apple_num_hold_apple_date)
                continue

            grow_length = All_apple_date.index(today) - All_apple_date.index(grow_date)
            is_high_over_top_half_block = All_good_apple_price_bb_dict[HOLD_APPLE]['high'][today] - All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today] > half_block[HOLD_APPLE]            
            is_high_over_top_half_block_after_1 = is_high_over_top_half_block and grow_length >= 1
            is_low_higher_than_top_2_p = (All_good_apple_price_bb_dict[HOLD_APPLE]['low'][today] - All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today])/All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today] > 0.02
            is_low_higher_than_top_2_p_after_1 = is_low_higher_than_top_2_p and grow_length >= 1
            is_over_half_block = All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today] - All_good_apple_price_bb_dict[HOLD_APPLE]['high'][today] > half_block[HOLD_APPLE]
            is_over_half_block_after_1 = grow_length >= 1 and is_over_half_block

            if is_over_half_block_after_1:
                P_printl('is_over_half_block_after_1 detected')
            if is_high_over_top_half_block_after_1:
                P_printl('is_high_over_top_half_block_after_1 detected')
            if is_low_higher_than_top_2_p_after_1:
                P_printl('is_low_higher_than_top_2_p_after_1 detected')
            if is_over_half_block_after_1 or is_low_higher_than_top_2_p_after_1:
                # harvest
                P_printl('harvest '+HOLD_APPLE+' at '+today,1)
                P_printl('harvest_apple_price = '+str(harvest_apple_price),1)
                price_diff_rate = round((harvest_apple_price - hold_apple_price) / hold_apple_price * 100,1)
                # price_diff_rate just show the start ends
                #@ calculate the avg diff rate, not just start end
                AVG_diff = round(sum(HOLD_APPLE_dict[apple_num_hold_apple_date][-(len(HOLD_APPLE_dict[apple_num_hold_apple_date])-len_init_hold_apple_dict):])/grow_length,1)
                HARVEST_APPLE_list.append([HOLD_APPLE, grow_date, today, predict_diff, AVG_diff])
                VA_ALL_APPLE_ML_DATA.append(VA_Predict_dict[HOLD_APPLE+'_'+grow_date]+[AVG_diff])

                # HOLD_APPLE_dict.pop(apple_num_hold_apple_date)
                pop_apple_num_date.append(apple_num_hold_apple_date)
                    
        for apple_num_date in pop_apple_num_date:
            P_printl(str(HOLD_APPLE_dict[apple_num_date])+' is poped')
            HOLD_APPLE_dict.pop(apple_num_date)
            
        # grow all the apples and check if the avg_diff match the prediction
        if len(top_result_list) == 0:
            P_printl('Do nothing when no top',3)
        else:
            # for predict_result in predict_result_list:
            #     apple_num = predict_result[0]
            #     predict_diff = predict_result[1]
            #     sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+apple_num+" WHERE date LIKE "+next_date+"")
            #     apple_open = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            #     # grow value determined by next open, assume never miss
            #     P_printl(today+' : Grow top apple '+apple_num+' with '+str(apple_open),2)
            #     HOLD_APPLE_dict[apple_num+'_'+today] = [today, apple_num, apple_open, 0, predict_diff] 
            #     len_init_hold_apple_dict = len(HOLD_APPLE_dict[apple_num+'_'+today])
            apple_num = top_result_list[0][0]
            predict_diff = VA_Predict_output[apple_num+'_'+today]
            sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+apple_num+" WHERE date LIKE "+next_date+"")
            apple_open = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            # grow value determined by next open, assume never miss
            P_printl(today+' : Grow top apple '+apple_num+' with '+str(apple_open),2)
            HOLD_APPLE_dict[apple_num+'_'+today] = [today, apple_num, apple_open, 0, predict_diff] 
            len_init_hold_apple_dict = len(HOLD_APPLE_dict[apple_num+'_'+today])
        P_printl('VA HOLD_APPLE_dict :',3)
        HOLD_APPLE_dict = dict(sorted(HOLD_APPLE_dict.items(), key=lambda item: item[1][0], reverse=True))
        P_printl(HOLD_APPLE_dict)
        P_printl('VA HARVEST_APPLE_list :',3)
        HARVEST_APPLE_list.sort(key=lambda x: x[-1], reverse=True)
        P_printl(HARVEST_APPLE_list)
        
        # now use the HARVEST_APPLE_list to calculate the difference of avg_diff and prediction 
        if day_shift == 1:
            Prediction_error = 0
            Prediction_error_report_list = []
            random_guessing_list = []
            P_printl('Reached the last day, calculate how close the prediction is',3)
            for HARVEST_APPLE in HARVEST_APPLE_list:
                Prediction_error += abs(HARVEST_APPLE[3] - HARVEST_APPLE[4])
                Prediction_error_report_list.append(HARVEST_APPLE+[abs(HARVEST_APPLE[3] - HARVEST_APPLE[4])])
                # gather data for random guessing
                random_guessing_list.append(HARVEST_APPLE[4])
            Prediction_error_avg = Prediction_error / len(HARVEST_APPLE_list)
            P_printl('VA Prediction_error_report_list : ',4)
            P_printl(Prediction_error_report_list)

            # guess here by random to compare
            guess_error = 0
            guess_low_range = np.median(random_guessing_list)-np.mean(random_guessing_list)/2
            guess_high_range = np.median(random_guessing_list)+np.mean(random_guessing_list)/2
            for HARVEST_APPLE in HARVEST_APPLE_list:
                guess_result = random.uniform(guess_low_range,guess_high_range)
                guess_error += abs(guess_result - HARVEST_APPLE[4])
            Guess_error_avg = guess_error / len(HARVEST_APPLE_list)
            P_printl('VA Guess_error_avg = '+str(Guess_error_avg),4)

            P_printl('VA Prediction_error_avg = '+str(Prediction_error_avg),4)


def main():
    global start_day_shift
    global end_day_shift
    global model
    global HOLD_APPLE
    global HARVEST_APPLE_list
    global HOLD_APPLE_LIST
    global HOLD_APPLE_dict

    # =======================================================================================================
    # Prepare dates
    args = parse_command_line()
    start_time = time()  
    start_len_shift = 281 # 281 lock at 20200131 for a month seeds
    start_day_shift = len(All_apple_date) - start_len_shift
    end_day_shift = 0
    # overwrite the shift for testing
    # if args.para1:
    #     start_day_shift = args.para1
    
    # end_day_shift_TR = start_day_shift - round((start_day_shift - end_day_shift) * TR_VA_rate)
    
    
    P_printl('start_day_shift = '+str(start_day_shift)+', and end_day_shift = '+str(end_day_shift),0,1)
    
    # =======================================================================================================
    # '''
    # TR, start gathering data

    P_printl('Enter TR mode',5)
    for day_shift in range(start_day_shift,end_day_shift,-1): # train end eariler
        Algo1(day_shift, 'TR')

    elapsed_time_total = str(round(time()-start_time))
    elapsed_time_total_min = str(round((time()-start_time)/60))
    elapsed_time_per_round = str(round((time()-start_time)/(start_day_shift-end_day_shift)))
    # print('Time result')
    P_printl('Execution time : '+elapsed_time_total+' seconds ('+elapsed_time_total_min+' min) total and '+elapsed_time_per_round+' seconds per round')
    P_printl('TR HOLD_APPLE_dict :',3)
    P_printl(HOLD_APPLE_dict)
    P_printl('TR HARVEST_APPLE_list :',3)
    P_printl(HARVEST_APPLE_list)
    P_printl('TR ALL_APPLE_ML_DATA rank:',3)
    P_printl(ALL_APPLE_ML_DATA)


    # only do this when do multi
    # plot the relationship
    ALL=[]
    shutil.rmtree('Figs') 
    os.makedirs('Figs')

    #draw the paradise_per_grow_list
    plt.figure(dpi=200)
    title='paradise_per_grow_list'
    plt.plot([a[0] for a in paradise_per_grow_list], [a[1] for a in paradise_per_grow_list]\
                ,label='Apple',color=color_blue, linestyle='-')
    plt.grid()
    plt.xticks(rotation=30)
    plt.title(title,fontsize=20)
    plt.savefig('Figs/'+title+'.png')

    title_index=['top','mid','low','avail','juice','seeds','point']
    
    for i in range(0,len(ALL_APPLE_ML_DATA[0])-1):
        ALL_APPLE_ML_DATA.sort(key=lambda x: x[i], reverse=True)
        ALL.append([[a[i],a[-1]] for a in ALL_APPLE_ML_DATA])

    for i in range(0,len(ALL_APPLE_ML_DATA[0])-1):
        plt.figure(dpi=200) # change the dpi before plotting to make it bigger, original 100
        # plot apple
        # plt.plot([a[0] for a in ALL[i]], [a[1] for a in ALL[i]]\
        #         ,label='Apple',color=color_blue, linestyle='-')
        plt.bar([a[0] for a in ALL[i]], [a[1] for a in ALL[i]])
        print(title_index[i])
        print([a[0] for a in ALL[i]])
        print('AVG_DIFF')
        print([a[1] for a in ALL[i]])
        plt.grid()
        plt.tick_params(axis='y', which='both', labelleft='on', labelright='on')
        title = '('+str(i)+')_'+title_index[i]+'_paradise'
        plt.title(title,fontsize=20)
        plt.savefig('Figs/'+title+'.png')
        # mngr = plt.get_current_fig_manager()
        # geom = mngr.window.geometry()
        # x,y,dx,dy = geom.getRect()
        # mngr.window.setGeometry(0,0,dx,dy)
        # plt.show(block=False)
        # plt.waitforbuttonpress()
    
    

    '''
    All_data = ALL_APPLE_ML_DATA

    np.random.shuffle(All_data)
    # test_data_amount = round(len(All_data) * 0.2)

    # x = [ a[0:7] for a in All_data[:(len(All_data)-test_data_amount)]]
    # y = [ a[7] for a in All_data[:(len(All_data)-test_data_amount)]]
    x = [ a[0:7] for a in All_data]
    y = [ a[7] for a in All_data]
    x, y = np.array(x), np.array(y)

    model.fit(x, y)
    with open('model_random_forest.pickle', 'wb') as f:
        pickle.dump(model, f)
    
    # with open('model_random_forest.pickle', 'rb') as f:
    #     model = pickle.load(f)
    # All_data = [
    # [130, 225, 13, 368, 3.0, 88, 8.5, 10]
    # ,[130, 225, 13, 368, 32.1, 15, 3.8, 10]
    # ,[130, 225, 13, 368, -0.6, -17, 3.0 ,10]
    # ]
    # x = [ a[0:7] for a in All_data]
    # y = [ a[7] for a in All_data]

    P_printl('Evaluating the training error :',5)

    guess_error = 0
    guess_low_range = np.median(y)-np.mean(y)/2
    guess_high_range = np.median(y)+np.mean(y)/2
    print(guess_low_range)
    print(guess_high_range)
    for dy in y:
        guess_result = random.uniform(guess_low_range,guess_high_range)
        guess_error += abs(guess_result - dy)
        print(guess_result)
        print(guess_error)
    Guess_error_avg = guess_error / len(y)
    P_printl('TR Guess_error_avg = '+str(Guess_error_avg),5)

    # show the training error
    error_sum = 0 
    predict_dx_sum = 0
    for dx,dy in zip(x,y):
        predict_dx_sum += model.predict([dx])[0]
        diff = abs(model.predict([dx])[0] - dy)
        print('diff = '+str(diff))
        error_sum += diff
    MIN_SL_SCORE_FROM_ML_TESTING = np.mean(y)
    P_printl('MIN_SL_SCORE_FROM_ML_TESTING is : '+str(MIN_SL_SCORE_FROM_ML_TESTING))
    TR_error = error_sum/len(x)
    P_printl('Training error is : '+str(TR_error))
    '''
    # =======================================================================================================
    '''
    # VA, start at end_day_shift_TR

    P_printl('Enter VA mode',5)
    with open('model_random_forest.pickle', 'rb') as f:
        model = pickle.load(f)

    HARVEST_APPLE_list = []
    HOLD_APPLE_LIST = []
    HOLD_APPLE_dict = {}
    HOLD_APPLE = 'none'

    for day_shift in range(end_day_shift_TR,0,-1): 
        Algo1(day_shift, 'VA')
    
    P_printl('VA HARVEST_APPLE_list :',3)
    HARVEST_APPLE_list.sort(key=lambda x: x[-1], reverse=True)
    P_printl(HARVEST_APPLE_list)

    P_printl('VA_ALL_APPLE_ML_DATA :',3)
    VA_ALL_APPLE_ML_DATA.sort(key=lambda x: x[-1], reverse=True)
    P_printl(VA_ALL_APPLE_ML_DATA)

    '''
    # =======================================================================================================
    '''
    #SL, date can not cross TR

    P_printl('Enter SL mode',5)
    HARVEST_APPLE_list = []
    HOLD_APPLE_LIST = []
    HOLD_APPLE_dict = {}
    HOLD_APPLE = 'none'

    with open('model_random_forest.pickle', 'rb') as f:
        model = pickle.load(f)
    for day_shift in range(end_day_shift_TR,0,-1):
        Algo1(day_shift, 'SL')

    elapsed_time_total = str(round(time()-start_time))
    elapsed_time_total_min = str(round((time()-start_time)/60))
    elapsed_time_per_round = str(round((time()-start_time)/(start_day_shift-end_day_shift)))
    print('Time result')
    P_printl('Execution time : '+elapsed_time_total+' seconds ('+elapsed_time_total_min+' min) total and '+elapsed_time_per_round+' seconds per round')
    P_printl('PARADISE rate = '+str(round((PARADISE-1)*100))+'%')
    '''

if __name__ == '__main__':
    main()