# -*- coding: utf-8 -*-
__author__='wys'
#input是一个详情页的list，获取每个item的详情，返回
#没有代理支持，所以只能爬取有限的详情页，需要规则过滤掉很多明显没有潜力的商品

from amazon_detailpage import get_detail

import json
import threading
import amazon_detailpage
import random
import re
import time
import dynamic_proxy
from dynamic_proxy import dmp
from crawler import crawler

class details_dataset():
    def __init__(self,file='sports_outdoor_top100_urllist.txt'):
        self.dataset = self.get_detail_urls(file)
        self.lock=threading.Lock()   #锁变量，控制detail_urls的互斥访问

    def get_random_item(self):
        if(not self.dataset):
            return None
        cate = random.choice(list(self.dataset.keys()))
        if(self.dataset[cate]):
            #item = random.choice(self.dataset[cate])
            item = self.dataset[cate][0]
            #print('return random item:')
            #print(item)
            return item
        else:
            self.dataset.pop(cate)
            return self.get_random_item()

    def after_process(self,item,detail): #item:self.dataset[cate]的元素，detail：页面详情
        if(type(item)==str):
            item = eval(item)
        cate = item['category']
        rank = item['rank']
        rank_topcate = re.findall(r'[\d,]+',detail['rank'])[0]
        rank_topcate=''.join([t for t in rank_topcate if t !=','])
        rank_topcate = int(rank_topcate)
        if(rank_topcate>20000):
            print('in after process,rank is lager than 20000')
            print('before remove,lens is',len(self.dataset[cate]))
            self.dataset[cate] = [item for item in self.dataset[cate] if item['rank']<rank ]
            print('after remove,lens is',len(self.dataset[cate]))
        else:
            self.dataset[cate].remove(item)


    def get_detail_urls(self,file):
        result = {}
        with open(file,'r',encoding='utf-8') as fin:
            for line in fin:
                detail = eval(line.strip())
                url = detail['url']
                category = detail['category']
                review = detail['review']
                rank = detail['rank']

                if(category in result):
                    result[category].append(detail)
                else:
                    result[category] = [detail,]
            num = 0
            for cate,details in result.items():
                num += len(details)
            print('dataset init done.')
            print('len of details:',num)
            return result




#################全局变量，保存待爬数据列表
detail_urls = details_dataset()


########################

if __name__=='__main__':


    pass