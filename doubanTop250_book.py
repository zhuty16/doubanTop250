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

def clean_html(html):
    '''清除html文本中的相关转义符号'''
    html = re.sub('&nbsp;', ' ', html)
    html = re.sub('&ensp;', ' ', html)
    html = re.sub('&emsp;', ' ', html)
    html = re.sub('&amp;', '&', html)
    html = re.sub('&lt;', '<', html)
    html = re.sub('&gt;', '>', html)
    html = re.sub('&quot;', '"', html)
    return html    

def doubanTop250_spider(pageNumber):
    '''爬取豆瓣Top250电影'''
    BASE_URL = "http://book.douban.com/top250?start={start}"
    books = []
    for pages in range(pageNumber):
        print "crawling page%d..." % (pages+1)
        startNum = pages * 25
        listurl = BASE_URL.format(start=startNum)
        #print listurl
        soup = BeautifulSoup(urllib2.urlopen(listurl))
        for items in soup.findAll('div',{'class':'pl2'}):
            info = clean_html(str(items))
            url = re.search(r'<a href="(.*?)"', info).group(1)
            try:
                booksoup = BeautifulSoup(urllib2.urlopen(url))
            except Exception,e:
                continue
            
            #book_name = str(booksoup.find('div',{'id':'wrapper'}))
            #print book_name
            #print 'name '
            name = booksoup.find('span',{'property':'v:itemreviewed'}).text
            #print name
            book_info = str(booksoup.find('div',{'id':'info'})).strip('\n')
            #print book_info
            
            author = re.findall(r'<a class="" href=".*?">(.*?)</a>', book_info)[0].decode('utf8')
            press = re.search(r'出版社:</span>(.*?)<br />', book_info).group(1).decode('utf8')
            try:
                original = re.search(r'原作名:</span>(.*?)<br />', book_info).group(1).decode('utf8')
            except Exception,e:
                original = ''
            try:
                translater = re.findall(r'<a class="" href=".*?">(.*?)</a>', book_info)[1].decode('utf8')
            except Exception,e:
                translater = ''
            publishDate = re.search(r'出版年:</span>(.*?)<br />', book_info).group(1).decode('utf8')
            pages = re.search(r'页数:</span>(.*?)<br />', book_info).group(1).decode('utf8')
            price = re.search(r'定价:</span>(.*?)<br />', book_info).group(1).decode('utf8')
            binding = re.search(r'装帧:</span>(.*?)<br />', book_info).group(1).decode('utf8')
            ISBN = re.search(r'ISBN:</span>(.*?)<br />', book_info).group(1).decode('utf8')

            book_interest = booksoup.find('div',{'id':'interest_sectl'})
            score = book_interest.find('strong',{'class':'ll rating_num '}).text
            scoreNum = book_interest.find('span',{'property':'v:votes'}).text

            #related_info = booksoup.find('div',{'class':'related_info'})
            #print related_info
            summary = booksoup.find('div',{'class':'intro'}).text
            #print summary
            item = [name, url, author, press, original, translater, publishDate, pages, price, binding, ISBN, score, scoreNum, summary]
            books.append(item)
    return books

def write_csv(books):
    '''写数据'''
    with open('result_book.csv', 'wb') as f:
        f.write('\xEF\xBB\xBF')
        writer = csv.writer(f)
        writer.writerow(['书名', '链接', '作者', '出版社', '原作名', '译者', '出版时间', '页数', '价格', '装帧', 'ISBN', '评分', '评分人数', '内容简介'])
        for book in books:
            writer.writerow(book)
    f.close()              

if __name__ == '__main__':
    pageNumber = int(raw_input("please enter page number(1-10):"))
    print "doubanTop250 spider is starting..."
    write_csv(doubanTop250_spider(pageNumber))
    print "ending..."
