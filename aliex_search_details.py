# -*- coding: utf-8 -*-
__author__='wys'
#给定检索关键词，返回Aliexpress 检索结果list

import json
import time
import threading
import random
import crawler
from aliex_onepage_detail import get_details
from aliex_onepage_detail import is_login_page
from aliex_search_itemurl_list import get_pages_url
from aliex_search_itemurl_list import searchword2list
from config import SEARCH_WORDS


#################全局变量，保存待爬数据列表
details_urls = []
SEARCH_WORD = ''
########################


def get_pagedetail_callback(res):
    det = get_details(res=res)
    if(det):
        return 'success',det
    else:
        if(is_login_page(res)):
            return 'proxy_unsable',det
        else:
            return 'other_error',det

def after_process(url,res):
    global details_urls
    details_urls.remve(url)

    search_word = '_'.join(SEARCH_WORD.split())
    outputfile_name = 'output/'+ search_word + '.txt'
    detail_output(res,outputfile_name)


def detail_output(detail,file='sports_outdoor_details_2.txt'):
    with open(file,'a',encoding='utf-8')as fout:
        fout.write(json.dumps(detail,ensure_ascii=False))
        fout.write('\n')

def work_thread():
    #print('enter',threading.current_thread().name)
    global detail_urls
    while(detail_urls):
        url = detail_urls.get_random_item()

        try:
            sleep_time = random.random()*6
            time.sleep(sleep_time)

            cra = crawler()
            #print('crawler url:%s'%url)
            flag,res = cra.get_by_proxy(url=url,call_back=get_pagedetail_callback)
            if(flag):
                print(threading.current_thread().name,'get detail done')
                after_process(url,res)
            else:
                print(threading.current_thread().name,'get detail failed')

        except Exception as e:
            print(threading.current_thread().name, 'get detail done,error ending')
            print(threading.current_thread().name,e)

def search_details(searchword):
    global details_urls
    details_urls = searchword2list(searchword)
    global SEARCH_WORD
    SEARCH_WORD = searchword

    if(not details_urls):
        print('urls is none')
        return None

    t1 = threading.Thread(target=work_thread, name='worker1')
    t2 = threading.Thread(target=work_thread, name='worker2')
    #t3 = threading.Thread(target=work_thread, name='worker3')
    #t4 = threading.Thread(target=work_thread, name='worker4')
    #t5 = threading.Thread(target=work_thread, name='worker5')
    #t6 = threading.Thread(target=work_thread, name='worker6')
    t1.start()
    t2.start()
    #t3.start()
    #t4.start()
    #t5.start()
    #t6.start()
    t1.join()
    t2.join()
    #t3.join()
    #t4.join()
    #t5.join()
    #t6.join()



if __name__=='__main__':
    for word in SEARCH_WORDS:
        search_details(word)