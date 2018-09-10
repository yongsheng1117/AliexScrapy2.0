# -*- coding: utf-8 -*-
__author__='wys'
#input:bestseller100的url,返回100个商品的list

from bs4 import BeautifulSoup
import requests
from lxml import etree
import time
from ET_IP import etc

def get_bestseller_list_onepage(url):
    result = []
    site_name = 'https://www.amazon.co.uk'

    #res = requests.get(url)
    res = etc.get(url)
    if (res.status_code == 200):
        soup = BeautifulSoup(res.text, 'html.parser')
        # items = soup.findAll('li',class_='zg-item-immersion')
        items = soup.findAll('span', class_='aok-inline-block zg-item')
        for item in items:
            item_detail_url = site_name + item.a['href']

            xp = etree.HTML(str(item))
            review = xp.xpath('//span/div/a[2]/text()')
            if (review):
                review=review[0].replace(',','')
                review = int(review)
            else:
                review = 0
            result.append({'url': item_detail_url, 'review': review})
        return result
    else:
        return []

def get_next_page(url):
    #res = requests.get(url)
    res = etc.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    ul = soup.findAll('ul',class_='a-pagination')
    xp = etree.HTML(str(ul))
    next_page = xp.xpath('//li/a[text()=2]/@href')
    return next_page[0]

def get_bestseller_list(url):
    result = []
    first_page = url
    next_page = get_next_page(url)


    onelist = get_bestseller_list_onepage(first_page)
    twolist = get_bestseller_list_onepage(next_page)
    result.extend(onelist)
    result.extend(twolist)
    return result


if __name__=='__main__':
    url = 'https://www.amazon.co.uk/Best-Sellers-Sports-Outdoors-American-Football/zgbs/sports/671783011'

    li = get_bestseller_list(url)
    for l in li:
        print(l)

