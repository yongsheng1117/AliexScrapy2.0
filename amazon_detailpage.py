# -*- coding: utf-8 -*-
__author__='wys'
#抓取 Amazon 详情页的信息

from bs4 import BeautifulSoup
import requests
from lxml import etree
import re
import json
#from ET_IP import etc
import time
from dynamic_proxy import dmp
import dynamic_proxy

def get_title(html):
    title = html.findAll('span',id='productTitle')
    if(title):
        title= title[0].text
        title=title.strip()
        return title
    else:
        return None


def get_rank(html):
    tr = html.findAll('tr',id='SalesRank')
    #print(tr)
    rank = tr[0].findAll('td',class_='value')
    rank = rank[0].text.strip()
    rank = re.sub('\n','',rank)
    return rank

def get_ship(html):   #imput 就是网页返回文本，不是soup对象
    ship = re.findall(r'Fulfilled by Amazon',html)
    if(ship):
        return 'Fulfilled by Amazon'
    else:
        return 'unknow'

def get_price(html):
    price = html.findAll('span',id='priceblock_ourprice')
    if(price):
        price = price[0].text
        return price
    else:
        return None

def get_review(html):
    review = html.findAll('span',id='acrCustomerReviewText')
    if(review):
        review =review[0].text
    else:
        review = '0 customer reviews(unfund)'
    return review

def get_detail(url):

    try:
        proxy = dmp.get_proxy()
        #print(res.text)
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
        res = requests.get(url,headers=header,proxies={"http": proxy})
        if(res.status_code==200):
            #print(res.status_code)
            #print(res.text)
            html = BeautifulSoup(res.text,'html.parser')
            title = get_title(html)
            ship = get_ship(res.text)
            price = get_price(html)
            rank = get_rank(html)

            asin = re.findall(r'gp/product/([\w\d]{10})/',url)
            asin = asin[0]
            review = get_review(html)
            return {'title':title,'ship':ship,'price':price,'rank':rank,
                    'url':url,'asin':asin,'review':review}
        else:
            #print(res.status_code)
            #print(res.text)
            return {}
    except MemoryError as e:
        print(e)
        return {}

def callback_get_detail(res):
    try:
        html = BeautifulSoup(res.text, 'html.parser')
        title = get_title(html)
        ship = get_ship(res.text)
        price = get_price(html)
        rank = get_rank(html)

        url = res.url
        #asin = re.findall(r'gp/product/([\w\d]{10})/', url)
        #print('asin',asin)
        #asin = asin[0]
        review = get_review(html)
        #print('callback get detail done')
        #print('scrapy result:')
        #print(json.dumps({'title': title, 'ship': ship, 'price': price, 'rank': rank,
        #        'url': url,  'review': review}))
        return 'success',{'title': title, 'ship': ship, 'price': price, 'rank': rank,
                'url': url,  'review': review}
    except Exception as e:
        print('scrapy error.....')
        print(e)
        return 'proxy_unsable',{}

if __name__=='__main__':
    url = 'https://www.amazon.co.uk/gp/product/B07FCM6547/ref=s9_acsd_top_hd_bw_bLcjeV_c_x_1_w?pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=merchandised-search-8&pf_rd_r=BFHJNSVFV216KSS473HF&pf_rd_t=101&pf_rd_p=c67380ec-4d23-58d0-afc4-7b1e477bc63a&pf_rd_i=319535011'

    detail = get_detail(url)
    print(detail)

    detail = get_detail(url)
    print(detail)

    detail = get_detail(url)
    print(detail)