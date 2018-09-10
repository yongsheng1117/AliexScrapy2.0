# -*- coding: utf-8 -*-
__author__='wys'
#获取et代理动态ip

import requests
from ET_IP import etc
from bs4 import BeautifulSoup

def get_review(html):
    try:
        review = html.findAll('span',id='acrCustomerReviewText')
        review =review[0].text
        return review
    except Exception :
        return None



url = 'https://www.amazon.co.uk/gp/product/B07FCM6547/ref=s9_acsd_top_hd_bw_bLcjeV_c_x_1_w?pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=merchandised-search-8&pf_rd_r=BFHJNSVFV216KSS473HF&pf_rd_t=101&pf_rd_p=c67380ec-4d23-58d0-afc4-7b1e477bc63a&pf_rd_i=319535011'
#url = 'https://www.amazon.co.uk/'
header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            }

response = requests.get(url, headers=header, timeout=7)
html = BeautifulSoup(response.text,'html.parser')
review = get_review(html)
print('local request without proxy')
print(review)

for proxy in etc.ips:
    print(proxy)

    response = requests.get(url, headers=header, proxies={"http": proxy}, timeout=4)
    html = BeautifulSoup(response.text,'html.parser')
    review = get_review(html)
    print(review)
    #print(len(response.text))
