from Utopia_tools import *

P_printl()

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
