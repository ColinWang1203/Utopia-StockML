from Utopia_tools import *

#@ pick low for top?
#@ find a way to discribe the shifting of the seeds and cap it, because a single line to sepearete is poor

P_enable_logging()
#@ find max paradise apples and analyze
skip_list = [2548, 2348, 2524, 2505, 2851, 2809,
             2836, 2889, 5521, 6005, 2884, 2845,
             2888, 2887, 2890, 5880, 2886, 2812,
             5876, 2834, 2880, 2801] 

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
TYPE_THSH = 250
TYPE_DAY = 5
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
SECOND_GROW_LOW_HARV_THSH_LOW = -0.1
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
low_how_close_to_mid_THSH = -0.02
second_low_grow_date = 'non'
Low_second_grow_THSH = -0.1
half_block = {}
OVER_TOP_THSH = -0.05

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
    P_printl('Paradise rate is '+str(round((PARADISE-1)*100))+'%',1)
    paradise_dict[today] = round((PARADISE-1)*100)
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
        P_printl("juice_increase_rate ori = "+str(juice_increase_rate))
        juice_increase_rate = pow(juice_increase_rate, juice_pow)
        juice_increase_rate = max(min(juice_increase_rate,juice_rate_max),juice_rate_min)
        P_printl("juice_increase_rate = "+str(juice_increase_rate))

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
            # days_rise = 1 
            # try Top_mul_days days end top abs diff
            # for n in range(1,Top_mul_days+1):
            #     end_top_abs_diff = 1 - abs((apple_end_dict[All_apple_date[-n-day_shift]] - bb_top_dict[All_apple_date[-n-day_shift]]) / bb_top_dict[All_apple_date[-n-day_shift]])
            #     days_rise *= end_top_abs_diff

            # bb mid mul
            # days_rise = 1
            # for n in range(2,Top_mul_days+2):
            #     diff = 1 + ((bb_mid_dict[All_apple_date[-n+1-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]]) / bb_mid_dict[All_apple_date[-n-day_shift]])
            #     days_rise *= diff

            # bb mid mul n to n
            # top_mul_first = 1
            # top_mul_second = 1
            # for n in range(2,Top_mul_days_n_to_n+2):
            #     diff = 1 + ((bb_mid_dict[All_apple_date[-n+1-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]]) / bb_mid_dict[All_apple_date[-n-day_shift]])
            #     top_mul_first *= diff
            # for n in range(Top_mul_days_n_to_n+2, Top_mul_days_n_to_n+2+Top_mul_days_n_to_n):
            #     diff = 1 + ((bb_mid_dict[All_apple_date[-n+1-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]]) / bb_mid_dict[All_apple_date[-n-day_shift]])
            #     top_mul_second *= diff
            # days_rise *= (top_mul_first / top_mul_second)



            # reverse
            # amount_total_first = 0
            # amount_total_second = 0
            # for n in range(1,amount_day_n_to_n+1):
            #     amount_total_first += amount_apple_dict[All_apple_date[-n-day_shift]]
            # for n in range(amount_day_n_to_n+1, amount_day_n_to_n+1+amount_day_n_to_n):
            #     amount_total_second += amount_apple_dict[All_apple_date[-n-day_shift]]
            # amount_rate_first_second = amount_total_second / amount_total_first

            # top_mul_first = 1
            # top_mul_second = 1
            # for n in range(2,Low_mul_days_n_to_n+2):
            #     diff = 1 + ((bb_mid_dict[All_apple_date[-n+1-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]]) / bb_mid_dict[All_apple_date[-n-day_shift]])
            #     top_mul_first *= diff
            # for n in range(Low_mul_days_n_to_n+2, Low_mul_days_n_to_n+2+Low_mul_days_n_to_n):
            #     diff = 1 + ((bb_mid_dict[All_apple_date[-n+1-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]]) / bb_mid_dict[All_apple_date[-n-day_shift]])
            #     top_mul_second *= diff
            # top_mul_first_second_rate = top_mul_first/ top_mul_second

            # if top_mul_first_second_rate > 1:
            #     amount_rate_first_second = max(1/top_mul_first_second_rate,min(amount_rate_first_second,top_mul_first_second_rate))
            # else:
            #     amount_rate_first_second = min(amount_rate_first_second,top_mul_first_second_rate)

            # P_printl('colin apple '+apple_num+' amount_rate_first_second '+str(amount_rate_first_second)+' top_mul_first_second_rate '+str(top_mul_first_second_rate)+' today '+today)
            
            # days_rise = amount_rate_first_second * top_mul_first_second_rate



            # days_rise = 1
            # for n in range(2,Top_mul_days+2): 
            #     diff = apple_end_dict[All_apple_date[-n+1-day_shift]] - apple_end_dict[All_apple_date[-n-day_shift]]
            #     if apple_end_dict[All_apple_date[-n+1-day_shift]] > bb_top_dict[All_apple_date[-n+1-day_shift]] and diff > 0:
            #         diff *= -1
            #     days_rise *= 1+(diff / apple_end_dict[All_apple_date[-n-day_shift]])
            
            # days_ago_rate = 1 + (apple_end_dict[-1-day_shift-20] - apple_end_dict[today]) / apple_end_dict[today]
            # days_rise *= days_ago_rate


            # days_rise = 1
            # for n in range(1,Top_mul_days+1):
            #     mid_in_top_mid =  (bb_top_dict[All_apple_date[-n-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]]) * 0.75 + bb_mid_dict[All_apple_date[-n-day_shift]]
            #     days_rise *= 1 - abs((apple_end_dict[All_apple_date[-n-day_shift]] - mid_in_top_mid)/mid_in_top_mid)
            # # decrease the point by each day's highs low var mul
            # for n in range(1,Top_mul_days+1):
            #     days_rise *= 1-abs((apple_high_dict[All_apple_date[-n-day_shift]] - apple_low_dict[All_apple_date[-n-day_shift]]) / apple_low_dict[All_apple_date[-n-day_shift]])
            # # bb mid mul close to 1
            # for n in range(2,Top_mul_days+2):
            #     days_rise *= 1 - abs(((bb_mid_dict[All_apple_date[-n+1-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]]) / bb_mid_dict[All_apple_date[-n-day_shift]]))


            days_rise = 1
            # for n in range(2,5+2):
            #     days_rise *= 1 - (((bb_mid_dict[All_apple_date[-n+1-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]]) / bb_mid_dict[All_apple_date[-n-day_shift]]))
            for n in range(2,3+2):
                days_rise *= 1 + ((apple_end_dict[All_apple_date[-n+1-day_shift]] - apple_end_dict[All_apple_date[-n-day_shift]]) / apple_end_dict[All_apple_date[-n-day_shift]])

            Top_points = round(days_rise * 100,5)
            P_printl("Top_points = "+str(Top_points)+'%')

            top_apple_dict[apple_num] = Top_points
        except Exception as e:
            P_printl(e)

        
        #========================================================
        #                      Mid Algo
        #========================================================
    
        # requirements : high/low does not touch top/low in 5 days
        # points : how_many_days_stay_above_mid * days_mul * how_close_to_mid
        
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
 
            how_many_days_stay_above_mid = 0
            for mid_day_above_shift in range(1,40): # len should not exceed latest_n_date_for_BB(42), set to 40 here
                date = All_apple_date[-day_shift-mid_day_above_shift]
                if (apple_end_dict[date] - bb_mid_dict[date])/bb_mid_dict[date] < MAX_END_DROP_LOWER_THAN_MID:
                    break
                else:
                    how_many_days_stay_above_mid += 1
            P_printl(apple_num+' , how_many_days_stay_above_mid = '+str(how_many_days_stay_above_mid)+' date = '+today)
            
            days_rise = 1
            # shift by Mid_shift_day for previously rise but now slow
            for n in range(Mid_shift_day,Mid_mul_days+Mid_shift_day):
                diff = 1 + ((bb_mid_dict[All_apple_date[-n+1-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]]) / bb_mid_dict[All_apple_date[-n-day_shift]])
                days_rise *= diff
            # for n in range(11,32): 
            #     ratio = 1 + ((apple_end_dict[All_apple_date[-n+1-day_shift]] - apple_end_dict[All_apple_date[-n-day_shift]]) / apple_end_dict[All_apple_date[-n-day_shift]])
            #     # if over mid just kill this apple by 10 times penalty
            #     if ((apple_end_dict[All_apple_date[-n-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]])/bb_mid_dict[All_apple_date[-n-day_shift]] < MAX_END_DROP_LOWER_THAN_MID):
            #         ratio = ratio * 0.1
            #     days_rise *= ratio
            
            # currently in Days_not_close_mid days how far from the mid, setup the penalty
            for n in range(1,Mid_not_close_mid_day+1):
                days_rise *= 1 - abs((apple_end_dict[All_apple_date[-n-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]])/bb_mid_dict[All_apple_date[-n-day_shift]])

            Mid_points = round(how_many_days_stay_above_mid * days_rise * juice_increase_rate * 100 - 100, 2)
            P_printl("Mid_points = "+str(Mid_points))

            mid_apple_dict[apple_num] = Mid_points
        except Exception as e:
            P_printl(e)

        #========================================================
        #                      Low Algo
        #========================================================

        # requirements : low touch low in 5 days
        # points : touch high low count * end diff with last touch(bumpy rate) * average_amount_3_days rate
        # action in : 1. 50% grow at next open
        #             2. if yesterday over 10%, next day 50% grow at open
        # action out: 1. all harvest at touch mid
        #             2. 22 days after either in harvest all at open
        #             3. 10 after double harvest all at open
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

            # Low_points = 0
            # direction = 'up'
            # last_day = All_apple_date[-1-day_shift]
            # average_amount_3_days = (amount_apple_dict[All_apple_date[-1-day_shift]] + amount_apple_dict[All_apple_date[-2-day_shift]] + amount_apple_dict[All_apple_date[-3-day_shift]])/3
            # # higher the amount, lower the point
            # amount_ratio = math.pow(0.8, (average_amount_3_days / (sum(amount_apple_dict.values()) / len(amount_apple_dict.values()))) / 10)
            # for date in All_apple_date_reverse[day_shift:day_shift+LOW_POINT_BUMPY_LEN]:
            #     date = str(date)
                
            #     if ((bb_top_dict[date] - apple_high_dict[date])/apple_high_dict[date]) < 0.02 and \
            #                 direction == 'up' and (apple_end_dict[date] - apple_end_dict[last_day])/apple_end_dict[last_day] > 0.05:
            #         Low_points = Low_points + 1+ ((apple_end_dict[date] - apple_end_dict[last_day])/apple_end_dict[last_day]) * amount_ratio / 100
            #         direction = 'low'
            #         last_day = date

            #     if ((apple_low_dict[date] - bb_low_dict[date])/bb_low_dict[date]) < 0.02 and \
            #                 direction == 'low' and (apple_end_dict[last_day] - apple_end_dict[date])/apple_end_dict[date] > 0.05:
            #         Low_points = Low_points + 1 + ((apple_end_dict[last_day] - apple_end_dict[date])/apple_end_dict[date]) * amount_ratio / 100
            #         direction = 'up' 
            #         last_day = date
            

            # # if tpday does not touch LOW_POINT_CLOSE_TO_LOW low, then minimize the point
            # if (apple_low_dict[today] - bb_low_dict[today]) / bb_low_dict[today] > LOW_POINT_CLOSE_TO_LOW:
            #     Low_points *= 0.1




            # amount_total_first = 0
            # amount_total_second = 0
            # for n in range(1,amount_day_n_to_n+1):
            #     amount_total_first += amount_apple_dict[All_apple_date[-n-day_shift]]
            # for n in range(amount_day_n_to_n+1, amount_day_n_to_n+1+amount_day_n_to_n):
            #     amount_total_second += amount_apple_dict[All_apple_date[-n-day_shift]]
            # amount_rate_first_second = amount_total_second / amount_total_first

            # low_mul_first = 1
            # low_mul_second = 1
            # for n in range(2,Low_mul_days_n_to_n+2):
            #     diff = 1 + ((bb_mid_dict[All_apple_date[-n+1-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]]) / bb_mid_dict[All_apple_date[-n-day_shift]])
            #     low_mul_first *= diff
            # for n in range(Low_mul_days_n_to_n+2, Low_mul_days_n_to_n+2+Low_mul_days_n_to_n):
            #     diff = 1 + ((bb_mid_dict[All_apple_date[-n+1-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]]) / bb_mid_dict[All_apple_date[-n-day_shift]])
            #     low_mul_second *= diff
            
            # low_mul_first_second_rate = low_mul_second / low_mul_first
            # if low_mul_first_second_rate > 1:
            #     amount_rate_first_second = max(1/low_mul_first_second_rate,min(amount_rate_first_second,low_mul_first_second_rate))
            # else:
            #     amount_rate_first_second = min(amount_rate_first_second,low_mul_first_second_rate)
            # P_printl('colin apple '+apple_num+' amount_rate_first_second '+str(amount_rate_first_second)+' low_mul_first_second_rate '+str(low_mul_first_second_rate)+' today '+today)

            # # how close to low
            # close_low_rate = (bb_low_dict[today]- apple_end_dict[today]) / apple_end_dict[today]
            
            # Low_points = amount_rate_first_second * low_mul_first_second_rate * close_low_rate



            # days_rise = 1
            # for n in range(2,Low_mul_days+2):
            #     diff = 1 + ((bb_mid_dict[All_apple_date[-n+1-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]]) / bb_mid_dict[All_apple_date[-n-day_shift]])
            #     days_rise *= diff
            # close_low_rate = 1 + (bb_low_dict[today]- apple_end_dict[today]) / apple_end_dict[today]
            # days_rise *= close_low_rate


            # days_rise = 1
            # for n in range(1,Low_mul_days+1):
            #     mid_in_mid_low =  (bb_mid_dict[All_apple_date[-n-day_shift]] - bb_low_dict[All_apple_date[-n-day_shift]]) * 0.25 + bb_low_dict[All_apple_date[-n-day_shift]]
            #     days_rise *= 1 - abs((apple_end_dict[All_apple_date[-n-day_shift]] - mid_in_mid_low)/mid_in_mid_low)
            # # decrease the point by each day's highs low var mul
            # for n in range(1,Low_mul_days+1):
            #     days_rise *= 1 - abs((apple_high_dict[All_apple_date[-n-day_shift]] - apple_low_dict[All_apple_date[-n-day_shift]]) / apple_low_dict[All_apple_date[-n-day_shift]])
            # # bb mid mul close to 1
            # for n in range(2,Low_mul_days+2):
            #     days_rise *= 1 - abs(((bb_mid_dict[All_apple_date[-n+1-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]]) / bb_mid_dict[All_apple_date[-n-day_shift]]))


            days_rise = 1
            for n in range(2+5,5+2+5+10):
                days_rise *= 1 + (((bb_mid_dict[All_apple_date[-n+1-day_shift]] - bb_mid_dict[All_apple_date[-n-day_shift]]) / bb_mid_dict[All_apple_date[-n-day_shift]]))
            for n in range(2,Low_mul_days+2):
                days_rise *= 1 - ((apple_end_dict[All_apple_date[-n+1-day_shift]] - apple_end_dict[All_apple_date[-n-day_shift]]) / apple_end_dict[All_apple_date[-n-day_shift]])

            Low_points = round(days_rise * 100,5)

            P_printl("Low_points = "+str(Low_points))
            low_apple_dict[apple_num] = Low_points
        except Exception as e:
            P_printl(e)


    # Rank the result by their points
    top_result_list = sorted(top_apple_dict.items(), key=lambda x: x[1], reverse=True)
    P_printl("Apple tops are ("+ str(len(top_result_list)) +") :",1)
    P_printl(top_result_list)

    mid_result_list = sorted(mid_apple_dict.items(), key=lambda x: x[1], reverse=True)
    P_printl("Apple mids are ("+ str(len(mid_result_list)) +") :",1)
    P_printl(mid_result_list)

    low_result_list = sorted(low_apple_dict.items(), key=lambda x: x[1], reverse=True)
    P_printl("Apple lows are ("+ str(len(low_result_list)) +") :",1)
    P_printl(low_result_list)

    RESULT_LEN_LIST = [len(top_result_list), len(mid_result_list), len(low_result_list)]
    P_printl(RESULT_LEN_LIST)
    MAX_INDEX = RESULT_LEN_LIST.index(max(RESULT_LEN_LIST))

# Also need to calcualte the ratio and if 100% is reached, then change mode can be earlyer than 5 days

    P_printl('Currently holding apple : '+HOLD_APPLE+', today = '+today,1)

    if MAX_INDEX == 0:
        result_top += 1
        result_top_ratio += (len(top_result_list) / available_apple_amount * 100)
        result_mid = result_low = 0
        result_mid_ratio = result_low_ratio = 0
    if MAX_INDEX == 1:
        # replace_mid_to_low
        # result_mid += 1
        # result_mid_ratio += (len(mid_result_list) / available_apple_amount * 100)
        # result_top = result_low = 0
        # result_top_ratio = result_low_ratio = 0
        if len(low_result_list)/available_apple_amount > MIN_RATIO_LOW_LIST_LEN :
            result_low += 1
            result_low_ratio += (len(low_result_list) / available_apple_amount * 100)
            result_mid = result_top = 0
            result_mid_ratio = result_top_ratio = 0
        else:
            if len(top_result_list)/available_apple_amount > MIN_RATIO_TOP_LIST_LEN:
                result_top += 1
                result_top_ratio += (len(top_result_list) / available_apple_amount * 100)
                result_mid = result_low = 0
                result_mid_ratio = result_low_ratio = 0

    if MAX_INDEX == 2:
        # low max grow nothing
        # result_low += 1
        # result_low_ratio += (len(low_result_list) / available_apple_amount * 100)
        # result_mid = result_top = 0
        # result_mid_ratio = result_top_ratio = 0
        result_low = result_mid = result_top = 0
        result_low_ratio = result_mid_ratio = result_top_ratio = 0
    P_printl('result_top = '+str(result_top)+', result_mid = '+str(result_mid)+', result_low = '+str(result_low),1)
    P_printl('result_top_ratio = '+str(result_top_ratio)+', result_mid_ratio = '+str(result_mid_ratio)+', result_low_ratio = '+str(result_low_ratio),1)
    
    # setup the str for changing type log
    if hold_apple_type == 0:
        hold_apple_type_str = 'non'
    if hold_apple_type == 1:
        hold_apple_type_str = 'top'
    if hold_apple_type == 2:
        hold_apple_type_str = 'mid'
    if hold_apple_type == 3:
        hold_apple_type_str = 'low'

    #========================================================
    #                      Hurr algo
    #========================================================
    # when hurricane comes clear all the countings for TYPE_DAY and TYPE_THSH
    # hurricane_count need to be consecutive
    Hurricane_level = round(len(low_result_list) / available_apple_amount * 100)
    P_printl('Hurricane level is '+str(Hurricane_level))
    if Hurricane_level > Hurricane_THSH:
        hurricane_count += 1
        hurricane_out_count = 0
    else:
        hurricane_count = 0 # so hurricane_count need to be consecutive to hurricane_count_THSH
        hurricane_out_count += 1
    if hurricane_count >= hurricane_count_THSH:
        # clean the counting even if no apple is holding
        result_top = result_mid = result_low = 0
        result_top_ratio = result_mid_ratio = result_low_ratio = 0
        if not hold_hurricane:
            P_printl('Hurricane in now : '+today,2)
            hurricane_result_dict[today] = Hurricane_level
        else:
            P_printl('Hurricane keep holding at : '+today,2)
            hurricane_result_dict[today] = Hurricane_level
        hold_hurricane = 1
        if hold_apple_type > 0:
            #harvest
            sql_cursor_Database_squeeze_name.execute("SELECT ends FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
            harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            price_diff_rate = (harvest_apple_price - hold_apple_price) / hold_apple_price
            if not second_grow:
                price_diff_rate = price_diff_rate / 2 # if not second grow, only half
            grow_length = All_apple_date.index(today) - All_apple_date.index(grow_date)
            if hold_apple_type == 1:
                paradise_top_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
            if hold_apple_type == 2:
                paradise_mid_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
            if hold_apple_type == 3:
                paradise_low_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
            PARADISE = PARADISE * (1 + price_diff_rate)
            P_printl(today+' : harvest '+hold_apple_type_str+' apple by hurricane '+HOLD_APPLE+' with '+str(harvest_apple_price)+ ' : '+str(price_diff_rate*100)+'%',2)
            hold_apple_price = 0
            hold_apple_type = 0
            after_touch_apple_day = 0
            HOLD_APPLE = 'none'
            return
    if hold_hurricane and (result_top >= TYPE_DAY or result_top_ratio > TYPE_THSH or
            result_mid >= TYPE_DAY or result_mid_ratio > TYPE_THSH or result_low >= TYPE_DAY or
            result_low_ratio > TYPE_THSH or hurricane_out_count >= hurricane_out_count_THSH):
        P_printl(today+' : Hurricane out',2)
        hold_hurricane = 0
        hurricane_count = 0
        hurricane_out_count = 0

    # divide into two situations: no prev apple and with prev apple
    # grow top when no holding, or change type
    if result_top >= TYPE_DAY or result_top_ratio > TYPE_THSH:
        if hold_apple_type == 0:
            # grow
            index = round(len(top_result_list) * (1-pick_ratio_in_list))
            apple_num = top_result_list[index][0]
            sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+apple_num+" WHERE date LIKE "+next_date+"")
            apple_open = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            # grow value determined by next open, assume never miss
            P_printl(today+' : Grow top apple '+apple_num+' with '+str(apple_open),2)
            HOLD_APPLE = apple_num
            hold_apple_price = apple_open
            hold_apple_type = 1
            result_top = result_mid = result_low = 0
            result_top_ratio = result_mid_ratio = result_low_ratio = 0
            second_grow = 1 # top apple goes full
            grow_date = today
        else:
            # if type is the same, wait for the apple condition, 
            # but if the type has changed, harvest at next open and grow with new one
            # this could happne in between the first grow and second grow
            if hold_apple_type != 1 : 
                # if during second grow do not change the type
                if second_grow:
                    P_printl('During second grow, ignore changing type to top',2)
                else:
                    # harvest
                    sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
                    harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                    price_diff_rate = (harvest_apple_price - hold_apple_price) / hold_apple_price
                    if not second_grow:
                        price_diff_rate = price_diff_rate / 2 # if not second grow, only half
                    grow_length = All_apple_date.index(today) - All_apple_date.index(grow_date)
                    if hold_apple_type == 1:
                        paradise_top_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                    if hold_apple_type == 2:
                        paradise_mid_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                    if hold_apple_type == 3:
                        paradise_low_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                    PARADISE = PARADISE * (1 + price_diff_rate)
                    P_printl(today+' : harvest '+HOLD_APPLE+' from '+hold_apple_type_str+' to top at '+str(harvest_apple_price)+ ', earning = '+str(price_diff_rate*100)+'%',2)
                    # grow
                    apple_num = top_result_list[0][0]
                    sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+apple_num+" WHERE date LIKE "+next_date+"")
                    apple_open = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                    # grow value determined by next open, assume never miss
                    P_printl(today+' : Grow top apple '+apple_num+' with '+str(apple_open),2)
                    HOLD_APPLE = apple_num
                    hold_apple_price = apple_open
                    hold_apple_type = 1
                    result_top = result_mid = result_low = 0
                    result_top_ratio = result_mid_ratio = result_low_ratio = 0
                    second_grow = 1 # top apple goes full
                    grow_date = today
        # return should not return, you might be holding an apple that needs the condition count below

     # grow mid when no holding, or change type
    if result_mid >= TYPE_DAY or result_mid_ratio > TYPE_THSH:
        if hold_apple_type == 0:
            #grow
            index = round(len(mid_result_list) * (1-pick_ratio_in_list))
            apple_num = mid_result_list[index][0]
            sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+apple_num+" WHERE date LIKE "+next_date+"")
            apple_open = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            # grow value determined by next open, assume never miss
            P_printl(today+' : Grow mid apple '+apple_num+' with '+str(apple_open),2)
            HOLD_APPLE = apple_num
            hold_apple_price = apple_open
            hold_apple_type = 2
            result_top = result_mid = result_low = 0
            result_top_ratio = result_mid_ratio = result_low_ratio = 0
            second_grow = 0
            grow_date = today
        else:
            # if type is the same, wait for the apple condition, 
            # but if the type has changed, harvest at next open and grow with new one
            if hold_apple_type != 2: 
                # if during second grow do not change the type
                if second_grow:
                    P_printl('During second grow, ignore changing type to mid',2)
                else:
                    # harvest
                    sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
                    harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                    price_diff_rate = (harvest_apple_price - hold_apple_price) / hold_apple_price
                    if not second_grow:
                        price_diff_rate = price_diff_rate / 2 # if not second grow, only half in
                    grow_length = All_apple_date.index(today) - All_apple_date.index(grow_date)
                    if hold_apple_type == 1:
                        paradise_top_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                    if hold_apple_type == 2:
                        paradise_mid_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                    if hold_apple_type == 3:
                        paradise_low_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                    PARADISE = PARADISE * (1 + price_diff_rate)
                    P_printl(today+' : harvest '+HOLD_APPLE+' from '+hold_apple_type_str+' to mid at '+str(harvest_apple_price)+ ', earning = '+str(price_diff_rate*100)+'%',2)
                    # grow
                    apple_num = mid_result_list[0][0]
                    sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+apple_num+" WHERE date LIKE "+next_date+"")
                    apple_open = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                    # grow value determined by next open, assume never miss
                    P_printl(today+' : Grow mid apple '+apple_num+' with '+str(apple_open),2)
                    HOLD_APPLE = apple_num
                    hold_apple_price = apple_open
                    hold_apple_type = 2
                    result_top = result_mid = result_low = 0
                    result_top_ratio = result_mid_ratio = result_low_ratio = 0
                    second_grow = 0
                    grow_date = today
        # return should not return, you might be holding an apple that needs the condition count below
    
    # grow low when no holding, or change type
    if result_low >= TYPE_DAY or result_low_ratio > TYPE_THSH:
        if hold_apple_type == 0:
            #grow
            index = round(len(low_result_list) * (1-pick_ratio_in_list))
            apple_num = low_result_list[index][0]
            sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+apple_num+" WHERE date LIKE "+next_date+"")
            apple_open = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            # grow value determined by next open, assume never miss
            P_printl(today+' : Grow low apple '+apple_num+' with '+str(apple_open),2)
            HOLD_APPLE = apple_num
            hold_apple_price = apple_open
            hold_apple_type = 3
            result_top = result_mid = result_low = 0
            result_top_ratio = result_mid_ratio = result_low_ratio = 0
            second_grow = 0
            grow_date = today
        else:
            # if type is the same, wait for the apple condition, 
            # but if the type has changed, harvest at next open and grow with new one
            if hold_apple_type != 3: 
                # if during second grow do not change the type, (now top apple accept change type)
                if second_grow :
                    P_printl('During second grow, ignore changing type to low',2)
                else:
                    # harvest
                    sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
                    harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                    price_diff_rate = (harvest_apple_price - hold_apple_price) / hold_apple_price
                    if not second_grow:
                        price_diff_rate = price_diff_rate / 2 # if not second grow, only half in
                    grow_length = All_apple_date.index(today) - All_apple_date.index(grow_date)
                    if hold_apple_type == 1:
                        paradise_top_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                    if hold_apple_type == 2:
                        paradise_mid_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                    if hold_apple_type == 3:
                        paradise_low_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                    PARADISE = PARADISE * (1 + price_diff_rate)
                    P_printl(today+' : harvest '+HOLD_APPLE+' from '+hold_apple_type_str+' to low at '+str(harvest_apple_price)+ ', earning = '+str(price_diff_rate*100)+'%',2)
                    # grow
                    apple_num = low_result_list[0][0]
                    sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+apple_num+" WHERE date LIKE "+next_date+"")
                    apple_open = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                    # grow value determined by next open, assume never miss
                    P_printl(today+' : Grow low apple '+apple_num+' with '+str(apple_open),2)
                    HOLD_APPLE = apple_num
                    hold_apple_price = apple_open
                    hold_apple_type = 3
                    result_top = result_mid = result_low = 0
                    result_top_ratio = result_mid_ratio = result_low_ratio = 0
                    second_grow = 0
                    grow_date = today
        # return should not return, you might be holding an apple that needs the condition count below

    # Harvest Condition Not_avail:
    # Apple turns into an unavailable apple, harvest at next open
    if hold_apple_type > 0 and (HOLD_APPLE not in All_good_apple_list):
        # harvest
        sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
        harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
        price_diff_rate = (harvest_apple_price - hold_apple_price) / hold_apple_price
        if not second_grow:
            price_diff_rate = price_diff_rate / 2 # if not second grow, only half in
        grow_length = All_apple_date.index(today) - All_apple_date.index(grow_date)
        if hold_apple_type == 1:
            paradise_top_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
        if hold_apple_type == 2:
            paradise_mid_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
        if hold_apple_type == 3:
            paradise_low_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
        PARADISE = PARADISE * (1 + price_diff_rate)
        P_printl(today+' : harvest '+hold_apple_type_str+' apple by not avail '+HOLD_APPLE+' at '+str(harvest_apple_price)+ ', earning = '+str(price_diff_rate*100)+'%',2)
        hold_apple_price = 0
        hold_apple_type = 0
        after_touch_apple_day = 0
        HOLD_APPLE = 'none'
        result_top = result_mid = result_low = 0
        result_top_ratio = result_mid_ratio = result_low_ratio = 0
        second_grow = 0
        return 
    
    # Note : second grow equals average the two hold_apple_price, and paradise diff do not need /2

    # Harvest Conditions Top :
    # use the same condition for the first grow and second grow
    # First grow :
    #   1. 3 days end 20% lower top
    #   2. 5 days end 10% lower top
    #   action : 
    #   first : second grow and reset the after_touch_apple_day
    #   second: next day harvest at open
    if hold_apple_type == 1:
        P_printl('after_touch_apple_day = '+str(after_touch_apple_day))
        bb_top_today = All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today]
        bb_mid_today = All_good_apple_price_bb_dict[HOLD_APPLE]['bb_mid'][today]
        sql_cursor_Database_squeeze_name.execute("SELECT highs FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
        hold_apple_price_highs_today = sql_cursor_Database_squeeze_name.fetchall()[0][0]
        if hold_apple_price_highs_today > bb_top_today:
            after_touch_apple_day = 0
        else:
            after_touch_apple_day += 1

        sql_cursor_Database_squeeze_name.execute("SELECT ends FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
        apple_price_today = sql_cursor_Database_squeeze_name.fetchall()[0][0]
        # if after_touch_apple_day == 3:
        #     if (apple_price_today - hold_apple_price)/hold_apple_price < SECOND_GROW_TOP_GROW_THSH_3_DAY:
        #         if not second_grow:
        #             # second grow
        #             P_printl(' 3 days end SECOND_GROW_TOP_GROW_THSH lower top, second grow it',1)
        #             sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
        #             hold_apple_price_next_day = sql_cursor_Database_squeeze_name.fetchall()[0][0]
        #             hold_apple_price = (hold_apple_price + hold_apple_price_next_day)/2 # take the average of two grows
        #             P_printl(today+' : second grow '+hold_apple_type_str+' '+HOLD_APPLE+' at '+str(hold_apple_price_next_day)+' with new hold '+str(hold_apple_price),2)
        #             after_touch_apple_day = 0
        #             second_grow = 1
        #             return
        #         else:
        #             # harvest
        #             P_printl(' 3 days end SECOND_GROW_TOP_GROW_THSH lower top, harvest it',1)
        #             sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
        #             harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
        #             price_diff_rate = (harvest_apple_price - hold_apple_price) / hold_apple_price
        #             PARADISE = PARADISE * (1 + price_diff_rate)
        #             P_printl(today+' : harvest '+hold_apple_type_str+' apple after second grow '+HOLD_APPLE+' at '+str(harvest_apple_price))
        #             P_printl('hold apple average is '+str(hold_apple_price)+', earning = '+str(price_diff_rate*100)+'%',2)
        #             hold_apple_price = 0
        #             hold_apple_type = 0
        #             after_touch_apple_day = 0
        #             HOLD_APPLE = 'none'
        #             result_top = result_mid = result_low = 0
        #             result_top_ratio = result_mid_ratio = result_low_ratio = 0
        #             second_grow = 0
        #             return

        if after_touch_apple_day >= 5:
            # over_mid_rate = (apple_price_today - bb_mid_today) / bb_mid_today
            # if ((apple_price_today - bb_top_today)/bb_top_today < SECOND_GROW_TOP_GROW_THSH_5_DAY) or (over_mid_rate < TOP_OVER_MID_RATE):
            # print('colin3')
            # print(today)
            # print(All_good_apple_price_bb_dict[HOLD_APPLE]['high'][today])
            # print(half_block[HOLD_APPLE])
            # P()
            is_over_half_block = All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today] - All_good_apple_price_bb_dict[HOLD_APPLE]['high'][today] > half_block[HOLD_APPLE]
            grow_length = All_apple_date.index(today) - All_apple_date.index(grow_date)
            is_over_top_thsh_in_22_or_over_22 = ((apple_price_today - hold_apple_price)/hold_apple_price < OVER_TOP_THSH and grow_length < 22) or grow_length >= 22
            if is_over_half_block and is_over_top_thsh_in_22_or_over_22:
                # if not second_grow:
                #     # second grow
                #     P_printl('5 days end SECOND_GROW_TOP_GROW_THSH_5_DAY lower top or over mid, second grow it',1)
                #     sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
                #     hold_apple_price_next_day = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                #     hold_apple_price = (hold_apple_price + hold_apple_price_next_day)/2 # take the average of two grows
                #     after_touch_apple_day = 0 # reset after_touch_apple_day after second grow
                #     P_printl(today+' : second grow '+hold_apple_type_str+' '+HOLD_APPLE+' at '+str(hold_apple_price_next_day)+' with new hold '+str(hold_apple_price),2)
                #     second_grow = 1
                #     return
                # else:
                # harvest
                P_printl('5 days end SECOND_GROW_TOP_GROW_THSH_5_DAY lower top or over mid',1)
                sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
                harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                price_diff_rate = (harvest_apple_price - hold_apple_price) / hold_apple_price

                if hold_apple_type == 1:
                    paradise_top_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                if hold_apple_type == 2:
                    paradise_mid_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                if hold_apple_type == 3:
                    paradise_low_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                PARADISE = PARADISE * (1 + price_diff_rate)
                P_printl(today+' : harvest '+hold_apple_type_str+' apple after second grow '+HOLD_APPLE+' at '+str(harvest_apple_price))
                P_printl('hold apple average is '+str(hold_apple_price)+', earning = '+str(price_diff_rate*100)+'%, day = '+str(grow_length),2)
                hold_apple_price = 0
                hold_apple_type = 0
                after_touch_apple_day = 0
                HOLD_APPLE = 'none'
                result_top = result_mid = result_low = 0
                result_top_ratio = result_mid_ratio = result_low_ratio = 0
                second_grow = 0
                return

    # Harvest Conditions Mid :
    #   harvest condition at next open: 
    #     1. After both grow: touch top
    #     2. After first grow : over 22 days
    #     3. After second grow : over 10% with new avg apple price or touch mid
    #   second grow condition at next open:
    #     1. After first grow : touch low
    if hold_apple_type == 2:
        # count the date first for 22 days and check for the touch top
        sql_cursor_Database_squeeze_name.execute("SELECT highs FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
        hold_apple_price_highs_today = sql_cursor_Database_squeeze_name.fetchall()[0][0]
        if (hold_apple_price_highs_today > All_good_apple_price_bb_dict[HOLD_APPLE]['bb_top'][today]) or after_touch_apple_day >= 22 :
            # harvest
            sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
            harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            price_diff_rate = (harvest_apple_price - hold_apple_price) / hold_apple_price
            if not second_grow:
                price_diff_rate = price_diff_rate / 2 # if not second grow, only half in
            grow_length = All_apple_date.index(today) - All_apple_date.index(grow_date)
            if hold_apple_type == 1:
                paradise_top_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
            if hold_apple_type == 2:
                paradise_mid_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
            if hold_apple_type == 3:
                paradise_low_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
            PARADISE = PARADISE * (1 + price_diff_rate)
            P_printl(today+' : harvest '+hold_apple_type_str+' apple by reach top or 22 days '+HOLD_APPLE+' at '+str(harvest_apple_price)+ ', earning = '+str(price_diff_rate*100)+'%',2)
            hold_apple_price = 0
            hold_apple_type = 0
            after_touch_apple_day = 0
            HOLD_APPLE = 'none'
            result_top = result_mid = result_low = 0
            result_top_ratio = result_mid_ratio = result_low_ratio = 0
            second_grow = 0
            return
        else:
            after_touch_apple_day += 1

        # check if second grow 
        if second_grow == 0:
            sql_cursor_Database_squeeze_name.execute("SELECT lows FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
            hold_apple_price_lows_today = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            if hold_apple_price_lows_today < All_good_apple_price_bb_dict[HOLD_APPLE]['bb_low'][today]:
                sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
                hold_apple_price_next_day = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                hold_apple_price = (hold_apple_price + hold_apple_price_next_day) / 2
                P_printl(today+' : second grow '+hold_apple_type_str+' '+HOLD_APPLE+' at '+str(hold_apple_price_next_day)+' with new hold '+str(hold_apple_price),2)
                # second grow here do not reset the after_touch_apple_day
                second_grow = 1
                return
        # second grow over SECOND_GROW_MID_HARV_THSH or touch mid
        if second_grow == 1:
            sql_cursor_Database_squeeze_name.execute("SELECT ends FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
            hold_apple_price_ends_today = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            rate_drop = (hold_apple_price_ends_today - hold_apple_price) / hold_apple_price
            sql_cursor_Database_squeeze_name.execute("SELECT highs FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
            hold_apple_price_highs_today = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            if rate_drop < SECOND_GROW_MID_HARV_THSH or hold_apple_price_highs_today > All_good_apple_price_bb_dict[HOLD_APPLE]['bb_mid'][today]:
                #harvest
                sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
                harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                price_diff_rate = (harvest_apple_price - hold_apple_price) / hold_apple_price
                grow_length = All_apple_date.index(today) - All_apple_date.index(grow_date)
                if hold_apple_type == 1:
                    paradise_top_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                if hold_apple_type == 2:
                    paradise_mid_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                if hold_apple_type == 3:
                    paradise_low_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                PARADISE = PARADISE * (1 + price_diff_rate)
                P_printl(today+' : harvest '+hold_apple_type_str+' apple after second grow '+HOLD_APPLE+' at '+str(harvest_apple_price))
                P_printl('hold apple average is '+str(hold_apple_price)+', earning = '+str(price_diff_rate*100)+'%, day = '+str(grow_length),2)
                hold_apple_price = 0
                hold_apple_type = 0
                after_touch_apple_day = 0
                HOLD_APPLE = 'none'
                result_top = result_mid = result_low = 0
                result_top_ratio = result_mid_ratio = result_low_ratio = 0
                second_grow = 0
                return
    # Harvest Conditions Low :
    #   harvest condition at next open: 
    #     1. After both grow: touch mid
    #     2. After first grow : over 22 days
    #     3. After second grow : over 10% or earn 5%
    #   second grow condition at next open:
    #     1. After first grow : over 10%
    if hold_apple_type == 3:
        # count the date first for 22 days and check for the touch mid
        sql_cursor_Database_squeeze_name.execute("SELECT highs FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
        hold_apple_price_highs_today = sql_cursor_Database_squeeze_name.fetchall()[0][0]
        # calculate the hold days and ignore harvest if lower than LOW_DAY_IGNORE_HARVEST
        grow_length = All_apple_date.index(today) - All_apple_date.index(grow_date)
        low_how_close_to_mid = (hold_apple_price_highs_today - All_good_apple_price_bb_dict[HOLD_APPLE]['bb_mid'][today])/All_good_apple_price_bb_dict[HOLD_APPLE]['bb_mid'][today]
        
        sql_cursor_Database_squeeze_name.execute("SELECT ends FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
        hold_apple_price_ends_today = sql_cursor_Database_squeeze_name.fetchall()[0][0]
        sql_cursor_Database_squeeze_name.execute("SELECT ends FROM "+HOLD_APPLE+" WHERE date LIKE "+All_apple_date[-(day_shift+2)]+"")
        hold_apple_price_ends_yesterday = sql_cursor_Database_squeeze_name.fetchall()[0][0]
        is_today_lower_than_yesterday = hold_apple_price_ends_today < hold_apple_price_ends_yesterday
        # if (low_how_close_to_mid > low_how_close_to_mid_THSH and grow_length > LOW_DAY_IGNORE_HARVEST and is_today_lower_than_yesterday) or after_touch_apple_day >= 22 :
        if (All_good_apple_price_bb_dict[HOLD_APPLE]['end'][today] > All_good_apple_price_bb_dict[HOLD_APPLE]['bb_mid'][today] and grow_length > LOW_DAY_IGNORE_HARVEST and is_today_lower_than_yesterday) or after_touch_apple_day >= 22 :
            # harvest
            sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
            harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            price_diff_rate = (harvest_apple_price - hold_apple_price) / hold_apple_price
            if not second_grow:
                price_diff_rate = price_diff_rate / 2 # if not second grow, only half in
            if hold_apple_type == 1:
                paradise_top_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
            if hold_apple_type == 2:
                paradise_mid_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
            if hold_apple_type == 3:
                paradise_low_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
            PARADISE = PARADISE * (1 + price_diff_rate)
            P_printl(today+' : harvest '+hold_apple_type_str+' apple by reach mid or 22 days '+HOLD_APPLE+' at '+str(harvest_apple_price)+ ', earning = '+str(price_diff_rate*100)+'%',2)
            hold_apple_price = 0
            hold_apple_type = 0
            after_touch_apple_day = 0
            HOLD_APPLE = 'none'
            result_top = result_mid = result_low = 0
            result_top_ratio = result_mid_ratio = result_low_ratio = 0
            second_grow = 0
            return
        else:
            after_touch_apple_day += 1

        # check if second grow 
        if second_grow == 0:
            sql_cursor_Database_squeeze_name.execute("SELECT ends FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
            hold_apple_price_ends_today = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            rate_drop = (hold_apple_price_ends_today - hold_apple_price) / hold_apple_price
            if rate_drop < Low_second_grow_THSH: 
                sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
                hold_apple_price_next_day = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                hold_apple_price = (hold_apple_price + hold_apple_price_next_day) / 2
                P_printl(today+' : second grow '+hold_apple_type_str+' '+HOLD_APPLE+' at '+str(hold_apple_price_next_day)+' with new hold '+str(hold_apple_price),2)
                # second grow here do not reset the after_touch_apple_day
                second_grow = 1
                second_low_grow_date = today
                return
        # second grow over SECOND_GROW_LOW_HARV_THSH_LOW or SECOND_GROW_LOW_HARV_THSH_HIGH
        if second_grow == 1:
            sql_cursor_Database_squeeze_name.execute("SELECT ends FROM "+HOLD_APPLE+" WHERE date LIKE "+today+"")
            hold_apple_price_ends_today = sql_cursor_Database_squeeze_name.fetchall()[0][0]
            diff_rate = (hold_apple_price_ends_today - hold_apple_price) / hold_apple_price
            second_low_grow_date_len = All_apple_date.index(today) - All_apple_date.index(second_low_grow_date)
            if diff_rate < SECOND_GROW_LOW_HARV_THSH_LOW or diff_rate > SECOND_GROW_LOW_HARV_THSH_HIGH or second_low_grow_date_len > 22:
                #harvest
                sql_cursor_Database_squeeze_name.execute("SELECT starts FROM "+HOLD_APPLE+" WHERE date LIKE "+next_date+"")
                harvest_apple_price = sql_cursor_Database_squeeze_name.fetchall()[0][0]
                price_diff_rate = (harvest_apple_price - hold_apple_price) / hold_apple_price
                grow_length = All_apple_date.index(today) - All_apple_date.index(grow_date)
                if hold_apple_type == 1:
                    paradise_top_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                if hold_apple_type == 2:
                    paradise_mid_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                if hold_apple_type == 3:
                    paradise_low_result_dict[today] = (HOLD_APPLE, grow_date, today, grow_length, round(price_diff_rate*100))
                PARADISE = PARADISE * (1 + price_diff_rate)
                P_printl(today+' : harvest '+hold_apple_type_str+' apple after second grow '+HOLD_APPLE+' at '+str(harvest_apple_price))
                P_printl('hold apple average is '+str(hold_apple_price)+', earning = '+str(price_diff_rate*100)+'%, day = '+str(grow_length),2)
                hold_apple_price = 0
                hold_apple_type = 0
                after_touch_apple_day = 0
                HOLD_APPLE = 'none'
                result_top = result_mid = result_low = 0
                result_top_ratio = result_mid_ratio = result_low_ratio = 0
                second_grow = 0
                return

def main():
    start_time = time()  
    start_len_shift = 200
    start_day_shift = len(All_apple_date) - start_len_shift
    end_day_shift = 0
    
    # overwrite the shift for testing
    # start_day_shift = 100
    # end_day_shift = 0
    # P_printl('start_day_shift = '+str(start_day_shift)+', and end_day_shift = '+str(end_day_shift))
    # P_printl('',0,-1)

    for day_shift in range(start_day_shift,end_day_shift,-1):
        Algo1(day_shift)

    elapsed_time_total = str(round(time()-start_time))
    elapsed_time_total_min = str(round((time()-start_time)/60))
    elapsed_time_per_round = str(round((time()-start_time)/(start_day_shift-end_day_shift)))
    print('Time result')
    P_printl('Execution time : '+elapsed_time_total+' seconds ('+elapsed_time_total_min+' min) total and '+elapsed_time_per_round+' seconds per round')

    print('Hurricane result')
    P_printl(hurricane_result_dict)
    print('Paradise result')
    P_printl(paradise_dict)
    print('Paradise top result')
    P_printl(paradise_top_result_dict)
    print('Paradise mid result')
    P_printl(paradise_mid_result_dict)
    print('Paradise low result')
    P_printl(paradise_low_result_dict)

if __name__ == '__main__':
    main()