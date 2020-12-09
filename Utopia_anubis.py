from Utopia_tools import *

#@ do not just pick the rate by harvest day / grow length, need to get every day paradise then avg them
#@ use round to simplify most of the claculations

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
MIN_AMOUNT = 1000*50 # price , 1000
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
juice_rate_max = 1.25 # currently only for top and mid
juice_rate_min = 0.75
juice_pow = 0
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
HOLD_APPLE_LIST = []
HARVEST_APPLE_dict = {}
HOLD_APPLE_dict = {}

def Algo1(day_shift) : # next open is defined as strictly 0900 start
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
    global HARVEST_APPLE_dict
    global ALL_APPLE_ML_DATA
    global HOLD_APPLE_dict

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
            if day_shift == 0:
                iter_dates = All_apple_date[-(latest_n_date_for_AVALIABLE + day_shift) :]
            else:
                iter_dates = All_apple_date[-(latest_n_date_for_AVALIABLE + day_shift) : -day_shift]
            for date in iter_dates:
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
            if apple_num != HOLD_APPLE:
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
        
        #========================================================================================================
        #                               Filter Finish
        #========================================================================================================
        All_good_apple_list.append(apple_num) 
    
    available_apple_amount = len(All_good_apple_list)
    P_printl("Currently available apple amount is : "+str(available_apple_amount),1)
    sleep(1)

    top_apple_dict = {}
    mid_apple_dict = {}
    low_apple_dict = {}
    amount_apple_dict = {}
    top_result_list = []
    mid_result_list = []
    low_result_list = []

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
        
        #calculate the half block by seperate the max bb top and min bb low into 5 blocks 
        #(half block = /10)
        max_bb_top = max(list(bb_top_dict.values()))
        min_bb_low = min(list(bb_low_dict.values()))
        half_block[apple_num] = (max_bb_top - min_bb_low)/10


        #calculate juice
        # juice_dict = {}
        # for dates in Year_juice_date:
        #     dates_str = dates[0]+'~'+dates[-1]
        #     juice_data_accu = 0
        #     for date in dates:
        #         sql_cursor_Database_juice_name.execute("SELECT current FROM "+apple_num+" WHERE date LIKE "+date+"")
        #         juice_data = sql_cursor_Database_juice_name.fetchall()[0][0]
        #         juice_data_accu += juice_data
        #     juice_dict[dates_str] = juice_data_accu
        # this_year_juice = juice_dict[list(juice_dict)[-1]]
        # second_year_juice = juice_dict[list(juice_dict)[-2]]
        # juice_increase_rate = 1+((this_year_juice - second_year_juice)/ second_year_juice)
        # P_printl("juice_increase_rate ori = "+str(juice_increase_rate))
        # juice_increase_rate = pow(juice_increase_rate, juice_pow)
        # juice_increase_rate = max(min(juice_increase_rate,juice_rate_max),juice_rate_min)
        # P_printl("juice_increase_rate = "+str(juice_increase_rate))

        #========================================================
        #                      Top Algo
        #========================================================
        
        # requirements : once touch high in five days
        # points : 5 days rate mul, if end over top change to minus
        
        count = 0
        try:
            for date in All_apple_date_reverse[day_shift:day_shift+6]:
                if count == 5:
                    raise Exception(apple_num+" does not touch top in 5 days")
                if apple_high_dict[date] > bb_top_dict[date]:
                    break
                count += 1
            P_printl(apple_num+" is an top apple!")

            days_rise = 1
            for n in range(1,22+1):
                days_rise *= 1 + ((bb_mid_dict[All_apple_date[-n-day_shift]] - bb_mid_dict[All_apple_date[-n-1-day_shift]]) / bb_mid_dict[All_apple_date[-n-1-day_shift]])
            days_rise *= pow(1 - (bb_top_dict[All_apple_date[-1-day_shift]] - bb_low_dict[All_apple_date[-1-day_shift]])/bb_low_dict[All_apple_date[-1-day_shift]],1)

            Top_points = round(days_rise * 100,1)
            P_printl("Top_points = "+str(Top_points)+'%')
            hold_apple_top_point_dict[apple_num+today] = Top_points

            top_apple_dict[apple_num] = Top_points
        except Exception as e:
            P_printl(e)

        
        #========================================================
        #                      Mid Algo
        #========================================================
        
        try:
            # check that apple should not touch high in five days
            count = 0
            for date in All_apple_date_reverse[day_shift:day_shift+6]:
                if apple_high_dict[date] > bb_top_dict[date] or apple_low_dict[date] < bb_low_dict[date]:
                    raise Exception(apple_num+" touched top or low in 5 days")
                if count == 5:
                    break
                count += 1
                
            P_printl(apple_num+" is an mid apple!")

            mid_apple_dict[apple_num] = 2
        except Exception as e:
            P_printl(e)

        #========================================================
        #                      Low Algo
        #========================================================

        count = 0
        try:
            for date in All_apple_date_reverse[day_shift:day_shift+6]:
                if count == 5:
                    raise Exception(apple_num+" does not touch low in 5 days")
                if apple_low_dict[date] < bb_low_dict[date]:
                    print("found low condition")
                    break
                count += 1
            P_printl(apple_num+" is an low apple!")
            low_apple_dict[apple_num] = 3
        except Exception as e:
            P_printl(e)


    # Rank the result by their points
    top_result_list = sorted(top_apple_dict.items(), key=lambda x: x[1], reverse=True)
    P_printl("Apple tops are ("+ str(len(top_result_list)) +") :",1)
    P_printl(top_result_list)

    mid_result_list = sorted(mid_apple_dict.items(), key=lambda x: x[1], reverse=True)
    P_printl("Apple mids are ("+ str(len(mid_result_list)) +") :",1)

    low_result_list = sorted(low_apple_dict.items(), key=lambda x: x[1], reverse=True)
    P_printl("Apple lows are ("+ str(len(low_result_list)) +") :",1)

    RESULT_LEN_LIST = [len(top_result_list), len(mid_result_list), len(low_result_list)]
    P_printl('RESULT_LEN_LIST = '+str(RESULT_LEN_LIST))

    P_printl('today is'+today,2,1)
    # for hold_apple_date in HOLD_APPLE_dict:
    #     print('Currently holding apple : '+str(HOLD_APPLE_dict[hold_apple_date]))
    # gather the dict by date, but not apple_num

    # harvest first to prevent harvest at growing

    # iterate though index in all the hold apples and see if harvest them

    P_printl('HOLD_APPLE_dict :',3)
    HOLD_APPLE_dict = dict(sorted(HOLD_APPLE_dict.items(), key=lambda item: item[1][-1], reverse=True))
    P_printl(HOLD_APPLE_dict)
    P_printl('HARVEST_APPLE_dict :',3)
    HARVEST_APPLE_dict = dict(sorted(HARVEST_APPLE_dict.items(), key=lambda item: item[1][4], reverse=True))
    P_printl(HARVEST_APPLE_dict)
    P_printl('ALL_APPLE_ML_DATA :',3)
    ALL_APPLE_ML_DATA.sort(key=lambda x: x[5], reverse=True)
    P_printl(ALL_APPLE_ML_DATA)
    

    pop_date = []
    for hold_apple_date in HOLD_APPLE_dict:

        HOLD_APPLE = HOLD_APPLE_dict[hold_apple_date][0]
        hold_apple_price = HOLD_APPLE_dict[hold_apple_date][1]
        after_touch_apple_day = HOLD_APPLE_dict[hold_apple_date][2]
        grow_date = hold_apple_date
        
        if HOLD_APPLE not in All_good_apple_list:
            P_printl(HOLD_APPLE)
            P_printl(All_good_apple_list)
            P_printl('Apple turns into unavailable, pop it')
            # HOLD_APPLE_dict.pop(hold_apple_date)
            pop_date.append(hold_apple_date)
            continue

        bb_top_today = All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today]
        bb_mid_today = All_good_apple_price_bb_dict[HOLD_APPLE]['bb_mid'][today]
        sql_cursor_Database_squeeze_name.execute("SELECT highs FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
        hold_apple_price_highs_today = sql_cursor_Database_squeeze_name.fetchall()[0][0]
        print(HOLD_APPLE_dict[hold_apple_date][2])

        if hold_apple_price_highs_today > bb_top_today:
            HOLD_APPLE_dict[hold_apple_date][2] = 0
        else:
            HOLD_APPLE_dict[hold_apple_date][2] += 1

        sql_cursor_Database_squeeze_name.execute("SELECT ends FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
        apple_price_today = sql_cursor_Database_squeeze_name.fetchall()[0][0]

        #@ accumulate the diff rate for each holding apple
        HOLD_APPLE_dict[hold_apple_date].append(round((apple_price_today - hold_apple_price)/hold_apple_price*100,1))

        grow_length = All_apple_date.index(today) - All_apple_date.index(grow_date)
        is_top_too_crazy = All_good_apple_price_bb_dict[HOLD_APPLE]['high'][today] - All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today] > half_block[HOLD_APPLE]            
        is_top_too_crazy_over_5 = is_top_too_crazy and grow_length >= 5
        print('colin debug')
        print(HOLD_APPLE)
        print(today)
        print(hold_apple_date)
        print(grow_length)
        print('half block of '+HOLD_APPLE+' is '+str(half_block[HOLD_APPLE]))
        print('All_good_apple_price_bb_dict[HOLD_APPLE][high][today] of '+HOLD_APPLE+' is '+str(All_good_apple_price_bb_dict[HOLD_APPLE]['high'][today]))
        print('All_good_apple_price_bb_dict[HOLD_APPLE][bb_top][today] of '+HOLD_APPLE+' is '+str(All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today]))
        print('after_touch_apple_day = '+str(HOLD_APPLE_dict[hold_apple_date][2]))
        if HOLD_APPLE_dict[hold_apple_date][2] >= 5 or is_top_too_crazy_over_5:
            is_over_half_block = All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today] - All_good_apple_price_bb_dict[HOLD_APPLE]['high'][today] > half_block[HOLD_APPLE]
            is_over_top_thsh_in_10_or_over_10 = ((apple_price_today - hold_apple_price)/hold_apple_price < OVER_TOP_THSH and grow_length < 10) or grow_length >= 10
            is_low_higher_than_top_2_p = (All_good_apple_price_bb_dict[HOLD_APPLE]['low'][today] - All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today])/All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today] > 0.02
            print(is_over_half_block)
            print(is_over_top_thsh_in_10_or_over_10)
            print(is_low_higher_than_top_2_p)
            print(is_top_too_crazy_over_5)
            if (is_over_half_block and is_over_top_thsh_in_10_or_over_10) or is_low_higher_than_top_2_p or is_top_too_crazy_over_5:
                # harvest
                P_printl('harvest '+HOLD_APPLE+' at '+today,1)
                sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
                harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                price_diff_rate = round((harvest_apple_price - hold_apple_price) / hold_apple_price * 100,1)
                # price_diff_rate just show the start ends
                HARVEST_APPLE_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, price_diff_rate, HOLD_APPLE_dict[hold_apple_date][3], HOLD_APPLE_dict[hold_apple_date][4], HOLD_APPLE_dict[hold_apple_date][5], HOLD_APPLE_dict[hold_apple_date][6], hold_apple_top_point_dict[HOLD_APPLE+grow_date])
                #@ calculate the avg diff rate, not just start end
                AVG_diff = sum(HOLD_APPLE_dict[hold_apple_date][-(len(HOLD_APPLE_dict[hold_apple_date])-7):])/grow_length
                print('colin4')
                print(HOLD_APPLE)
                print(today)
                print(grow_length)
                print(HOLD_APPLE_dict[hold_apple_date][-(len(HOLD_APPLE_dict[hold_apple_date])-7):])
                print(sum(HOLD_APPLE_dict[hold_apple_date][-(len(HOLD_APPLE_dict[hold_apple_date])-7):]))
                ALL_APPLE_ML_DATA.append([HOLD_APPLE_dict[hold_apple_date][3], HOLD_APPLE_dict[hold_apple_date][4], HOLD_APPLE_dict[hold_apple_date][5], HOLD_APPLE_dict[hold_apple_date][6], hold_apple_top_point_dict[HOLD_APPLE+grow_date], round(AVG_diff,1)])
                # HOLD_APPLE_dict.pop(hold_apple_date)
                pop_date.append(hold_apple_date)
                
    for date in pop_date:
        P_printl(str(HOLD_APPLE_dict[date])+' is poped')
        HOLD_APPLE_dict.pop(date)
        
    # grow
    apple_num = top_result_list[0][0]
    sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+apple_num+" WHERE date LIKE "+next_date+"")
    apple_open = sql_cursor_Database_squeeze_name.fetchall()[0][0]
    # grow value determined by next open, assume never miss
    P_printl(today+' : Grow top apple '+apple_num+' with '+str(apple_open),2)
    HOLD_APPLE_dict[today] = [apple_num, apple_open, 0, len(top_result_list), len(mid_result_list), len(low_result_list), available_apple_amount] # after touch apple

def main():
    start_time = time()  
    start_len_shift = 200
    start_day_shift = len(All_apple_date) - start_len_shift
    end_day_shift = 0
    
    # overwrite the shift for testing
    # start_day_shift = 200
    # end_day_shift = 0
    # P_printl('start_day_shift = '+str(start_day_shift)+', and end_day_shift = '+str(end_day_shift),0,-1)

    for day_shift in range(start_day_shift,end_day_shift,-1):
        Algo1(day_shift)

    elapsed_time_total = str(round(time()-start_time))
    elapsed_time_total_min = str(round((time()-start_time)/60))
    elapsed_time_per_round = str(round((time()-start_time)/(start_day_shift-end_day_shift)))
    print('Time result')
    P_printl('Execution time : '+elapsed_time_total+' seconds ('+elapsed_time_total_min+' min) total and '+elapsed_time_per_round+' seconds per round')
    P_printl(HOLD_APPLE_dict)
    P_printl(HARVEST_APPLE_dict)
    P_printl(ALL_APPLE_ML_DATA)

if __name__ == '__main__':
    main()