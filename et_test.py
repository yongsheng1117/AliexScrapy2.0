# -*- coding: utf-8 -*-
__author__='wys'
#使用isbn好检索孔夫子 网站，得到图书对应的详细信息：书名，定价，图片，描述。。。。

import requests
import re
import os
import json
import time
from ET_IP import ET
from ET_IP import etc
import threading

def sort_url(url):#返回按价格排序的url
    basename = os.path.basename(url)
    dirname = os.path.dirname(url)

    li = basename.split('.')
    li.insert(1,'_0_4_1.')
    newname = ''.join(li)
    newurl = dirname + '/' + newname
    return newurl

def sort_url_quanxin(url):#返回按价格排序的url,只看全新
    basename = os.path.basename(url)
    dirname = os.path.dirname(url)

    li = basename.split('.')
    li.insert(1,'_1_4_1.')
    newname = ''.join(li)
    newurl = dirname + '/' + newname
    return newurl

def read_data(file='booklist_isbn_07071021.txt'):
    print('read data begin')
    with open(file,'r',encoding='utf-8') as fin:
        return fin.readlines()

def output(content,filename='book_info_0708.txt'):
    with open(filename,'a',encoding='utf-8') as fout:
        fout.write(content+'\n')

def isbn2info_kfz(isbn):
    url = 'http://search.kongfz.com/item_result/?status=0&key=' + isbn
    result = {}
    try:
        #print(url)

        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 712 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53',
        }
        #url = 'http://search.kongfz.com/product_result/?status=0&key=9787559413017&order=1'
        html = etc.get(url)  # 超时异常判断 5秒超时
        bookinfo = html.text
        detail_url = re.findall('http://item\.kongfz\.com/book/\d+\.html',bookinfo)
        if(detail_url):
            detail_url = detail_url[0]
            #print(detail_url)

            sorted_url = sort_url(detail_url)
            #print(sorted_url)

            detail_resp = requests.get(sorted_url,headers=headers,timeout=7)
            detail_html = detail_resp.text


            bookname = re.findall(r'<h1 class="detail-title" itemprop="name">(.*?)</h1>',detail_html)
            if(bookname): bookname = bookname[0]
            print(bookname)

            detail_img_url = re.findall(r'<div class="detail-img">[\s\S]*?(http://[^"]*?)"',detail_html)
            if(detail_img_url):detail_img_url = detail_img_url[0]
            #print(detail_img_url)

            author = re.findall(r'<div class="detail-con-right">[\s\S]*?<a.*?>(.*)</a>',detail_html)
            if(author): author = author[0]
            #print(author)
            #seller_list = re.findall(r'<ul class="itemList">[\w\W]*?</ul>',detail_html)
            #print(seller_list)
            price_origin = re.findall(r'定价：(\d+(.\d+)?)',detail_html)
            if(price_origin):price_origin = price_origin[0][0]
            #print(price_origin)

            items = re.findall(r'<li class="gray3 p_l20 fontBlod">(\d+)条</li>',detail_html)[0]
            if(int(items)>60):
                sorted_url = sort_url_quanxin(detail_url)
                detail_resp = requests.get(sorted_url, headers=headers, timeout=7)
                detail_html = detail_resp.text

            li1 = re.findall(r'<div class="list-con-product[^>]*>([^<]*)</div>',detail_html)
            #print(li1)

            li2 = re.findall(r'<div class="list-con-moneys">[\s\S]*?(\d+(.\d+)?)[\s\S]*?</div>',detail_html)
            #print(li2)

            assert len(li1) == len(li2)
            prices = [(li1[i],li2[i][0]) for i in range(len(li1))]
            #print(prices)

            return {'isbn':isbn,'bookname':bookname,'book_face':detail_img_url,
                    'author':author,'price_origin':price_origin,
                    'prices':prices,}

        return result
    except Exception as e:#Exception as e:
        print(e)
        #print(html.text)
        return None

def work_thread():
    global detail_urls
    global lock
    while(detail_urls):

        lock.acquire()
        try:
            line = detail_urls[0]
            isbn = line.split('\t')[0]
            #print(isbn)

            detail_urls.pop(0)
        except Exception:
            pass
        finally:
            # 改完了一定要释放锁:
            lock.release()
        try:
            bookinfo = isbn2info_kfz(isbn)
            if(bookinfo):
                output(json.dumps(bookinfo, ensure_ascii=False), )
                print(threading.current_thread().name,'get %s detail done'%isbn)
            else:
                print(threading.current_thread().name, 'get %s detail done,empty result' % isbn)
        except Exception:
            print(threading.current_thread().name, 'get %s detail done,error ending' % isbn)
            continue

def main():
    t1 = threading.Thread(target=work_thread, name='worker1')
    t2 = threading.Thread(target=work_thread, name='worker2')
    t3 = threading.Thread(target=work_thread, name='worker3')
    t4 = threading.Thread(target=work_thread, name='worker4')
    t5 = threading.Thread(target=work_thread, name='worker5')
    #t6 = threading.Thread(target=work_thread, name='worker6')
    t1.start()
    print('worker1 begin')
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    #t6.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    #t6.join()

#################全局变量，保存待爬数据列表
detail_urls = []
print('before read data')
detail_urls = read_data()[1000:]
lock=threading.Lock()   #锁变量，控制detail_urls的互斥访问

########################


if __name__=='__main__':
    main()

    '''isbn2info_kfz(etc,'9787559413017')

    data = read_data()
    for line in data[19787:]:
        if(line):
            isbn = line.split('\t')[0]
            print(isbn)
            bookinfo = isbn2info_kfz(etc,isbn)

            output(json.dumps(bookinfo,ensure_ascii=False),)

            #time.sleep(3)'''
