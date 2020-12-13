from Utopia_tools import *
with open('Processed_juice_date_list.txt') as f:
    All_juice_date = f.read().splitlines()
with open('Processed_date_list.txt') as f:
    All_apple_date = f.read().splitlines()
with open('Processed_seeds_date_list.txt') as f:
    All_seeds_date = f.read().splitlines()

Database_seeds_name = 'DB_Seeds.sqlite'
sql_connection_Database_seeds_name = sqlite3.connect(Database_seeds_name)
sql_cursor_Database_seeds_name = sql_connection_Database_seeds_name.cursor()
apple_num = 'apple_9958'
sql_cursor_Database_seeds_name.execute("SELECT * FROM "+apple_num+"")
sql_seeds = sql_cursor_Database_seeds_name.fetchall()

today = '20200131'
print(today)

found_14_close_seed_flag = False
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
# check if shifted all last seeds date matches a month for all 5 dates
print(seeds_date_shift)
seeds_date_month_shift = 0
seeds_a_month_match_flag = True
for date in All_seeds_date[::-1][seeds_date_shift:seeds_date_shift+5]:
    # check if the date matches
    print(str(All_seeds_date_apple[-1-seeds_date_shift-seeds_date_month_shift]))
    print(date)
    if str(All_seeds_date_apple[-1-seeds_date_shift-seeds_date_month_shift]) != date:
        print('seeds date for a month does not match')
        seeds_a_month_match_flag = False
        break;
    # also check if the sum could be zero
    seeds_data = sql_seeds[-1-seeds_date_shift-seeds_date_month_shift]
    print(seeds_data)
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
    print(sum_data)
    seeds_date_month_shift += 1
print(seeds_date_month_shift)


# print(sql_seeds)
seeds_month_growth = 1
for seeds_date_month_shift in range(0,5):
    seeds_first_data = sql_seeds[-1-seeds_date_shift-seeds_date_month_shift]
    seeds_second_data = sql_seeds[-1-seeds_date_shift-seeds_date_month_shift-1]
    print(seeds_first_data)
    print(seeds_second_data)
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
    seeds_ratio_first = big_seeds_first/small_seeds_first
    seeds_ratio_second = big_seeds_second/small_seeds_second
    seeds_first_second_ratio = 1 + ((seeds_ratio_first - seeds_ratio_second) / seeds_ratio_second)
    seeds_month_growth *= seeds_first_second_ratio
    print(seeds_ratio_first)
    print(seeds_ratio_second)
    print(seeds_first_second_ratio)
print(round(seeds_month_growth * 1000))
#=========================================================================================================

# def find(s1, s2, paragraphs, cross_line = True):
#     if cross_line:
#         result = re.findall(s1+'(.*?)'+s2, paragraphs, re.DOTALL)
#     else:
#         result = re.findall(s1+'(.*?)'+s2, paragraphs)
#     result = list(set(result))# remove duplicate
#     return result

# url = 'https://www.chinatimes.com/realtimenews/260410?page=2&chdtv'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
# paragraphs = P_list2str(soup)
# P_printt(paragraphs)
# print(find('<p class="intro">', '</p>', paragraphs))

#==========================================================================================================
# Database_squeeze_name = 'DB_Avalon.sqlite'
# sql_connection_Database_squeeze_name = sqlite3.connect(Database_squeeze_name)
# sql_cursor_Database_squeeze_name = sql_connection_Database_squeeze_name.cursor()
# Database_juice_name = 'DB_Juice.sqlite'
# sql_connection_Database_juice_name = sqlite3.connect(Database_juice_name)
# sql_cursor_Database_juice_name = sql_connection_Database_juice_name.cursor()
# Database_seeds_name = 'DB_Seeds.sqlite'
# sql_connection_Database_seeds_name = sqlite3.connect(Database_seeds_name)
# sql_cursor_Database_seeds_name = sql_connection_Database_seeds_name.cursor()

# Fig_dir = 'Figs/' 
# Fig_dir_dropbox = '/home/colin/Dropbox/Figs/'

# with open('Processed_date_list.txt') as f:
#     All_apple_date = f.read().splitlines()
# with open('Processed_juice_date_list.txt') as f:
#     All_juice_date = f.read().splitlines()
# with open('Processed_seeds_date_list.txt') as f:
#     All_seeds_date = f.read().splitlines()
# with open('Processed_winds_date_list.txt') as f:
#     All_winds_date = f.read().splitlines()

# Year_juice_date_list = []
# # list of year, max to 2 year
# for count in range(0,6):
#     Year_juice_date = []
#     if count == 0:
#         for i in list(range(0,2)):
#             if i == 0:
#                 Year_juice_date.append(All_juice_date[-12:])
#             else:
#                 Year_juice_date.append(All_juice_date[-(12+(12*i)):-(12*i)])
#         Year_juice_date.reverse()
#     else :  
#         for i in list(range(0,2)):
#             Year_juice_date.append(All_juice_date[-(12+(12*i)+count):-(12*i)-count])
#         # print(Year_juice_date)
#         # P()
#         Year_juice_date.reverse()
#         # print(Year_juice_date)
#         # P()
#     Year_juice_date_list.append(Year_juice_date)
#     print(Year_juice_date_list)
#     if count ==1:
#         P()

# print(Year_juice_date_list)
# P()

# juice_dict = {}
# for dates in Year_juice_date:
#     dates_str = dates[0]+'~'+dates[-1]
#     juice_data_accu = 0
#     for date in dates:
#         sql_cursor_Database_juice_name.execute("SELECT current FROM "+apple_num+" WHERE date LIKE "+date+"")
#         juice_data = sql_cursor_Database_juice_name.fetchall()[0][0]
#         juice_data_accu += juice_data
#     juice_dict[dates_str] = juice_data_accu
