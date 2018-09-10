# -*- coding: utf-8 -*-
__author__='wys'
#input是一个详情页的list，获取每个item的详情，返回
#没有代理支持，所以只能爬取有限的详情页，需要规则过滤掉很多明显没有潜力的商品

from amazon_detailpage import get_detail

import json
import threading
import amazon_detailpage
import random
import time
import dynamic_proxy
from dynamic_proxy import dmp
from crawler import crawler
from details_dataset import details_dataset




def get_call_back(res):
    #print('enter get_call_back ')
    msg,result = amazon_detailpage.callback_get_detail(res)
    if(msg =='proxy_unsable'):
        return msg,result
    elif(msg=='success'):
        detail_output(result,)
        return msg,result
    else:
        return msg,result

def detail_output(detail,file='sports_outdoor_details_2.txt'):
    with open(file,'a',encoding='utf-8')as fout:
        fout.write(json.dumps(detail,ensure_ascii=False))
        fout.write('\n')

def work_thread():
    #print('enter',threading.current_thread().name)
    global detail_urls
    while(detail_urls):
        item = detail_urls.get_random_item()
        url = item['url']

        try:
            sleep_time = random.random()*6
            time.sleep(sleep_time)

            cra = crawler()
            #print('crawler url:%s'%url)
            flag,res = cra.get_by_proxy(url=url,call_back=get_call_back)
            if(flag):
                print(threading.current_thread().name,'get detail done')
                detail_urls.after_process(item,res)
            else:
                print(threading.current_thread().name,'get detail failed')

        except Exception as e:
            print(threading.current_thread().name, 'get detail done,error ending')
            print(threading.current_thread().name,e)

def main():
    t1 = threading.Thread(target=work_thread, name='worker1')
    t2 = threading.Thread(target=work_thread, name='worker2')
    t3 = threading.Thread(target=work_thread, name='worker3')
    #t4 = threading.Thread(target=work_thread, name='worker4')
    #t5 = threading.Thread(target=work_thread, name='worker5')
    #t6 = threading.Thread(target=work_thread, name='worker6')
    t1.start()
    t2.start()
    t3.start()
    #t4.start()
    #t5.start()
    #t6.start()
    t1.join()
    t2.join()
    t3.join()
    #t4.join()
    #t5.join()
    #t6.join()

#################全局变量，保存待爬数据列表
detail_urls = details_dataset()

########################

if __name__=='__main__':
    main()