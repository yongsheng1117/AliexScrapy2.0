# -*- coding: utf-8 -*-
__author__='wys'
#按关键词检索aliexpress首页，得到item的list
import re
import time
import requests
from bs4 import BeautifulSoup
from abuyun_proxy import ABUYUN_PROXY
from header import HEADER

SEARCH_URL_NO_PARAM ='https://www.aliexpress.com/wholesale?catId=0'

def get_retry(url,retry= 3):
    try:
        res = requests.get(url=url,header=HEADER.get_header(),proxies=ABUYUN_PROXY)
        if(len(res.text) >30000):
            return res
        else:
            if(retry >0):
                time.sleep(5)
                return get_retry(url,retry-1)
            else:
                print('try to get url:{url} ,but get None'.format(url=url))
                return None
    except Exception:
        if (retry > 0):
            time.sleep(5)
            return get_retry(url, retry - 1)
        else:
            print('try to get url:{url} ,but get None'.format(url=url))
            return None

def get_items_from_one_page(page_url):
    result = []

    res = get_retry(page_url,retry=3)

    if(res):
        soup = BeautifulSoup(res.text,'html.parser')
        a_li = soup.findAll('a',class_='picRind history-item ') #可能有遗漏，

        for a in a_li:
            href = a['href']
            href = re.sub(r'^//','',href)  #删掉herf开头的两个//符号
            result.append('http://'+href)
            print(href,'\n')
        return result
    else:
        return None


def get_pages_url(search_word,pages=60):  #input：检索词 output:检索前pages页的urls
    search_word = re.sub('\s+', '+', search_word)
    start_url = SEARCH_URL_NO_PARAM
    url_page_0 =start_url + '&SearchText=' + search_word +'&page=0'
    #print(url_page_0)
    res = get_retry(url_page_0)     #访问第一页的内容得到搜索结果数，计算一共有多少pages
    if(res):
        html = res.text
        soup = BeautifulSoup(html,'html.parser')
        result_count_p = soup.findAll('strong',class_='search-count')   #返回结果数在一个strong内
        #print(result_count_p)
        result_num = result_count_p[0].text
        result_num = re.sub(r'\D','',result_num)  #替换掉数字显示里面的逗号
        result_num = int(result_num)

        page_real = result_num/48   #检索到的内容页数
        if(page_real<pages):
            pages = int(page_real)

        result = []
        for i in range(pages):
            url_page_i = start_url + '&SearchText=' + search_word + '&page=' + str(i)
            result.append(url_page_i)
        return result
    else:
        return None



def searchword2list(search_word,pages=60):  ## 以searchword为检索词，检索aliexpress获取详情页url返回
    result = []
    pages = get_pages_url(search_word, pages)
    print(pages)
    if(pages):
        for page in pages:
            try:
                item_urls = get_items_from_one_page(page)
                result.extend(item_urls)
            except ValueError as e:
                print(e)
        return result
    else:
        return None

if __name__=='__main__':
    '''urls = get_pages_url('tent outdoor',10)
    for ul in urls:
        print(ul)

    url = urls[0]
    details = get_items_from_one_page(url)
    for d in details:
        print(d)'''

    sw = "balloon"
    li = searchword2list(sw,2)
    for l in li :
        print(l)
    print(len(li))