from Utopia_tools import *

#@ try to get all news and paragraph in a month


# ------------ Vars -----------------
top_amount = 30
amount_of_day_past = 20
top_step = 5
# -----------------------------------

final_result_list = []
today = datetime.today().strftime("%Y%m%d")
Database_winds_name = 'DB_Winds.sqlite'
sql_connection_Database_winds_name = sqlite3.connect(Database_winds_name)
sql_cursor_Database_winds_name = sql_connection_Database_winds_name.cursor()

def find(s1, s2, paragraphs, cross_line = True):
    if cross_line:
        result = re.findall(s1+'(.*?)'+s2, paragraphs, re.DOTALL)
    else:
        result = re.findall(s1+'(.*?)'+s2, paragraphs)
    result = list(set(result))# remove duplicate
    return result

# Ignore donwloading if already in processed list
with open('Processed_winds_date_list.txt') as f:
    if today in f.read():
        print('Already process winds today, aborting...')
        C()
        

# Z_write_line(paragraphs,'temp.txt',True)
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
url = 'https://money.udn.com/money/breaknews/1001/0/2'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
paragraphs = P_list2str(soup)
# do the double filter
paragraphs = P_list2str(find('<tr>\n<td>\n<a href="', '</a>', paragraphs, False))
if len(paragraphs) < 1600:
    print('Encounter error in '+url)
    C()
final_result_list += find('">', 'https', paragraphs, False)
# ------------------------------------------------------------------------
url = 'https://money.udn.com/money/breaknews/1001/0/1'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
paragraphs = P_list2str(soup)
# do the double filter
paragraphs = P_list2str(find('<tr>\n<td>\n<a href="', '</a>', paragraphs, False))
if len(paragraphs) < 1600:
    print('Encounter error in '+url)
    C()
final_result_list += find('">', 'https', paragraphs, False)

# ------------------------------------------------------------------------
# normal template
url = 'https://www.chinatimes.com/realtimenews/260410?page=2&chdtv'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
paragraphs = P_list2str(soup)
if len(paragraphs) < 16000:
    print('Encounter error in '+url)
    C()
final_result_list += find('<p class="intro">', '</p>', paragraphs)

# ------------------------------------------------------------------------
url = 'https://www.chinatimes.com/realtimenews/260410?page=1&chdtv'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
paragraphs = P_list2str(soup)
if len(paragraphs) < 16000:
    print('Encounter error in '+url)
    C()
final_result_list += find('<p class="intro">', '</p>', paragraphs)

# ------------------------------------------------------------------------
url = 'https://ec.ltn.com.tw/list/international'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
paragraphs = P_list2str(soup)
if len(paragraphs) < 16000:
    print('Encounter error in '+url)
    C()
final_result_list += find('<p>', '</p>', paragraphs)
final_result_list += find('<small>', '</small>', paragraphs)

# ------------------------------------------------------------------------
url = 'https://www.epochtimes.com/b5/news420.htm'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
paragraphs_list = []
for x in soup:
    paragraphs_list.append(str(x))
paragraphs = ''.join(paragraphs_list)
result = re.findall('<div class="content">(.*?)</div>', paragraphs)
result = list(set(result))# remove duplicate
if len(result) < 10:
    print('Encounter error in '+url)
    C()
final_result_list += result

# ------------------------------------------------------------------------
url = 'https://www.bbc.com/zhongwen/trad/business'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
paragraphs_list = []
for x in soup:
    paragraphs_list.append(str(x))
paragraphs = ''.join(paragraphs_list)
if len(paragraphs) < 1000:
    print('Error occured in '+url)
    C()
result = re.findall('"eagle-item__summary">(.*?)</p>', paragraphs)
result = list(set(result))# remove duplicate
final_result_list += result
result = re.findall('"title-link__title-text">(.*?)</span>', paragraphs)
result = list(set(result))# remove duplicate
if len(result) < 10:
    print('Encounter error in '+url)
    C()
final_result_list += result

# ------------------------------------------------------------------------
url = 'https://www.moneydj.com/KMDJ/News/NewsRealList.aspx?a=MB010000'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
paragraphs_list = []
for x in soup:
    paragraphs_list.append(str(x))
paragraphs = ''.join(paragraphs_list)
if len(paragraphs) < 1000:
    print('Error occured in '+url)
    C()
result = re.findall('title="(.*?)"', paragraphs)
result = list(set(result))# remove duplicate
if len(result) < 10:
    print('Encounter error in '+url)
    C()
final_result_list += result

# --------------- site cnyes <div class="_2bFl theme-list" ---------------
url = 'https://news.cnyes.com/news/cat/headline?exp=a'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
div = soup.find("div", class_="_2bFl theme-list")
paragraphs_list = []
for x in div:
    paragraphs_list.append(str(x))
paragraphs = ''.join(paragraphs_list)
if len(paragraphs) < 1000:
    print('Error occured in '+url)
    C()
result = re.findall('title="(.*?)"', paragraphs)
result = list(set(result))# remove duplicate
if len(result) < 10:
    print('Encounter error in '+url)
    C()

final_result_list += result
# ------------------------------------------------------------------------

# Analyze the result

final_result = ''.join(final_result_list)

words = jieba.lcut(final_result)
cuted=' '.join(words)
fdist = FreqDist(words)

# Add the ignore words here
delarr=['...','\\r\\n','span']

for key in fdist:
    if len(key)<2:
        delarr.append(key)
    elif isint(key):
        delarr.append(key)
for key in delarr:
    del fdist[key]
    
tops=fdist.most_common(50)
print(tops)

# only write once for a day
with open('Processed_winds_date_list.txt') as fr:
        with open('Processed_winds_date_list.txt', 'a') as fa:
            if today not in fr.read():
                for top in tops:
                    sql_create_cmd = 'CREATE TABLE IF NOT EXISTS Word_'+top[0]+' (date INT, amount INT)'
                    sql_cursor_Database_winds_name.execute(sql_create_cmd)
                    sql_write_cmd = 'INSERT INTO Word_'+top[0]+' (date, amount) values ("'+today+'","'+str(top[1])+'")'
                    sql_cursor_Database_winds_name.execute(sql_write_cmd)
                    sql_connection_Database_winds_name.commit()
                fa.write('%s\n' % today)

# get a week, count most 50 words in a week total and plot them

fontP = font_manager.FontProperties(fname='/home/colin/Desktop/utopia/simsun.ttc')

final_result_list = []
today = datetime.today().strftime("%Y%m%d")
Database_winds_name = 'DB_Winds.sqlite'
sql_connection_Database_winds_name = sqlite3.connect(Database_winds_name)
sql_cursor_Database_winds_name = sql_connection_Database_winds_name.cursor()

sql_cursor_Database_winds_name.execute("SELECT name FROM sqlite_master WHERE type='table'")
sql_tables_Database_winds_name = sql_cursor_Database_winds_name.fetchall()

winds_dict = {}

with open('Processed_winds_date_list.txt') as f:
    content = f.read().splitlines()

# first get the total count by winds date
for table in sorted(sql_tables_Database_winds_name):
    table_str = ''.join(table)
    winds_dict[table_str] = 0
    for i in list(range(1, amount_of_day_past + 1)):
        winds_date = content[-i]
        sql_cursor_Database_winds_name.execute("SELECT * FROM "+table_str+"")
        sql_winds = sql_cursor_Database_winds_name.fetchall()
        for sql_wind in sql_winds:
            if compare_string(sql_wind[0], winds_date):
                #update dict
                winds_dict.update({table_str : int(int(winds_dict[table_str]) + int(sql_wind[1]))})

# sort the dict by decending order
winds_dict_sort = {k: v for k, v in sorted(winds_dict.items(), key=lambda item: item[1], reverse=True)}
del_all_fig('Figs/winds')
del_all_fig('/home/colin/Dropbox/Figs/winds')

for top_i in range(0,top_amount,top_step):
    # get the most 20 by getting the first 20 key
    firstpairs = {k: winds_dict_sort[k] for k in list(winds_dict_sort)[top_i:top_i+top_step]}

    # plot all 20 with date
    fig = plt.figure()
    winds_date_list = []
    for i in list(range(1, amount_of_day_past + 1)):
        winds_date_list.append(content[-i])

    winds_date_list.reverse() # x axis of the plot

    for key in firstpairs:
        cloud_list = []
        key_str = ''.join(key)
        for winds_date in winds_date_list:
            sql_cursor_Database_winds_name.execute("SELECT * FROM "+key+"")
            sql_winds = sql_cursor_Database_winds_name.fetchall()
            processed_flag = False
            for sql_wind in sql_winds:
                if compare_string(sql_wind[0], winds_date):
                    cloud_list.append(sql_wind[1])
                    processed_flag = True
            if processed_flag is False:
                cloud_list.append(0)
        label_str = key_str.split('_')[1]
        plt.plot(winds_date_list, cloud_list,label=label_str)

    plt.legend(loc='upper left', prop=fontP)
    figs_file = 'Figs/winds/Winds_'+str(top_i)+'_'+str(top_i+top_step)+'.png'
    fig.savefig(figs_file)
    figs_file = '/home/colin/Dropbox/Figs/winds/Winds_'+str(top_i)+'_'+str(top_i+top_step)+'.png'
    fig.savefig(figs_file)

    # mng = plt.get_current_fig_manager()
    # mng.full_screen_toggle()
    # plt.show(block=False)
    # plt.waitforbuttonpress()

