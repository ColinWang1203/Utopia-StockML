import nltk
import jieba
from nltk.probability import FreqDist

text="""
武漢入境到宜蘭9名失聯者找到了！1自由行遊客不知去向| 我 ...
1 小時前 - 從武漢入境台灣的台商及旅客中有13人填寫要到宜蘭，經縣政府連日追查去向，有4人住在外縣市的親友家，剩下在宜蘭9人原本失聯...
www.bbc.com › zhongwen › trad › chinese-news-51293515
武漢肺炎：隨疫情擴散全球的五大假新聞- BBC News 中文
1 天前 - 從「蝙蝠湯」到「病毒是中國政府製造的生物武器」，雖然這些消息大多沒有可靠來源，但仍在網絡不斷傳播。
news.ltn.com.tw › news › world › breakingnews
武漢肺炎》200萬個口罩還不夠！南韓考慮再捐1.5億給中國 ...
3 小時前 - 〔即時新聞／綜合報導〕中國武漢「新型冠狀病毒」（武漢肺炎）疫情持續延燒，南韓正考慮提供中國500萬美元（約新台幣1.5億元）的援助金，協助中國 ...
"""

words = jieba.lcut(text)
cuted=' '.join(words)
fdist = FreqDist(words)

delarr=[]
for key in fdist:
    if len(key)<2:
        delarr.append(key)
for key in delarr:
    del fdist[key]
    
tops=fdist.most_common(50)
print(tops)
