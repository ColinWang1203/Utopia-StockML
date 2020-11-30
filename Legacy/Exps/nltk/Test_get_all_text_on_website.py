# extract all the titles on https://news.cnyes.com/news/cat/headline?exp=a

# example for getting the title in cnyes
# <div class="_2bFl theme-list"

import requests, re
from bs4 import BeautifulSoup

response = requests.get('https://news.cnyes.com/news/cat/headline?exp=a')
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)
text = {}
div = soup.find("div", class_="_2bFl theme-list")
paragraphs_list = []
for x in div:
    paragraphs_list.append(str(div))
paragraphs = ''.join(paragraphs_list)
result_list = re.findall('title="(.*?)"', paragraphs)
result = ''.join(result_list)
print(result)
