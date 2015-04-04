#-*- coding: utf-8 -*-
"""douban_Top250"""
import urllib2
import string
import re
import csv
from BeautifulSoup import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')

startNum = 0
pageNumber = 4
BASE_URL = "http://movie.douban.com/top250?start={start}"
films = []


def clean_html(html):
    '''清除html文本中的相关转义符号'''
    html = re.sub(u'&nbsp;', ' ', html)
    html = re.sub(u'&ensp;', ' ', html)
    html = re.sub(u'&emsp;', ' ', html)
    html = re.sub(u'&amp;', '&', html)
    html = re.sub(u'&lt;', '<', html)
    html = re.sub(u'&gt;', '>', html)
    html = re.sub(u'&quot;', '"', html)
    return html    

print "spider is starting..."

for pages in range(pageNumber):
    print "crawling page%d..." % (pages+1)
    startNum = pages * 25
    listurl = BASE_URL.format(start=startNum)
    #print listurl
    soup = BeautifulSoup(urllib2.urlopen(listurl))
    
    for items in soup.findAll('div',{'class':'info'}):
        info = clean_html(str(items))
        name = items.find('span',{'class':'title'}).text
        url = re.search(r'<a href="(.*?)"', str(info)).group(1)

        filmsoup = BeautifulSoup(urllib2.urlopen(url))
        
        film_info = str(filmsoup.find('div',{'id':'info'}))
        #print film_info
        director = re.search(r'导演</span>: <span class="attrs"><a href=".*?">(.*?)</a>', film_info).group(1).decode('utf8')
        screenwriter = re.search(r'编剧</span>: <span class="attrs"><a href=".*?">(.*?)</a>', film_info).group(1).decode('utf8')
        actor = re.search(r'主演</span>: <span class="attrs"><a href=".*?">(.*?)</a>', film_info).group(1).decode('utf8')
        nation = re.search(r'制片国家/地区:</span>(.*?)<br />', film_info).group(1).strip().decode('utf8')
        language = re.search(r'语言:</span>(.*?)<br />', film_info).group(1).strip().decode('utf8')
        releaseDate = re.search(r'上映日期:.*?">(.*?)</span>', film_info).group(1).decode('utf8')
        length = re.search(r'片长:.*?">(.*?)</span>', film_info).group(1).decode('utf8')

        film_interest = filmsoup.find('div',{'id':'interest_sectl'})
        score = film_interest.find('strong',{'class':'ll rating_num'}).text
        scoreNum = film_interest.find('span',{'property':'v:votes'}).text

        related_info = filmsoup.find('div',{'class':'related-info'})
        summary = related_info.find('span',{'property':'v:summary'}).text
        
        item = [name, url, director, screenwriter, actor, nation, language, releaseDate, length, score, scoreNum, summary]
        films.append(item)
        
        #print name, url, director, screenwriter, actor, nation, language, releaseDate, length, score, scoreNum, summary
        #print '\n'

with open('result.csv', 'wb') as f:
    f.write('\xEF\xBB\xBF')
    writer = csv.writer(f)
    writer.writerow(['电影名称', '链接', '导演', '编剧', '主演', '国家和地区', '语言', '上映日期', '片长', '评分', '评分人数', '剧情简介'])
    for film in films:
        writer.writerow(film)
f.close()              

print "spider is ending..."
