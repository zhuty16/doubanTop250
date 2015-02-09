#-*- coding: utf-8 -*-
"""film_spider"""
import urllib2
import string
import re
from BeautifulSoup import BeautifulSoup

startNum = 0
pageNumber = 3
BASE_URL = "http://movie.douban.com/top250?start={start}"


def clean_html(html):
    '''清除html文本中的相关转义符号
    '''
    html = re.sub('&nbsp;', ' ', html)
    html = re.sub('&ensp;', ' ', html)
    html = re.sub('&emsp;', ' ', html)
    html = re.sub('&amp;', '&', html)
    html = re.sub('&lt;', '<', html)
    html = re.sub('&gt;', '>', html)
    html = re.sub('&quot;', '"', html)
    return html


for j in range(1, pageNumber+1):
    startNum = (j-1)*25

    listurl = BASE_URL.format(start=startNum)
    #print listurl
    soup = BeautifulSoup(urllib2.urlopen(BASE_URL.format(start=startNum)))

    

    for i in soup.findAll('div',{'class':'info'}):
        info = clean_html(str(i))
        name = i.find('span',{'class':'title'}).text
        url = re.search(r'<a href="(.*?)"', str(info)).group(1)

        filmsoup = BeautifulSoup(urllib2.urlopen(url))
        
        film_info = filmsoup.find('div',{'id':'info'})
        #print film_info
        director = re.search(r'导演</span>: <span class="attrs"><a href=".*?">(.*?)</a>', str(film_info)).group(1).decode('utf8')
        screenwriter = re.search(r'编剧</span>: <span class="attrs"><a href=".*?">(.*?)</a>', str(film_info)).group(1).decode('utf8')
        actor = re.search(r'主演</span>: <span class="attrs"><a href=".*?">(.*?)</a>', str(film_info)).group(1).decode('utf8')
        nation = re.search(r'制片国家/地区:</span>(.*?)<br />', str(film_info)).group(1).decode('utf8')
        language = re.search(r'语言:</span>(.*?)<br />', str(film_info)).group(1).decode('utf8')
        releaseDate = re.search(r'上映日期:.*?">(.*?)</span>', str(film_info)).group(1).decode('utf8')
        length = re.search(r'片长:.*?">(.*?)</span>', str(film_info)).group(1).decode('utf8')
        
        filminterest = filmsoup.find('div',{'id':'interest_sectl'})
        score = filminterest.find('strong',{'class':'ll rating_num'}).text
        scoreNum = filminterest.find('span',{'property':'v:votes'}).text

        
        print name, url, director, screenwriter, actor, nation, language, releaseDate, length, score, scoreNum
        print '\n'
