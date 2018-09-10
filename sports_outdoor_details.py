# -*- coding: utf-8 -*-
__author__='wys'
#input是一个详情页的list，获取每个item的详情，返回

from amazon_detailpage import get_detail

import json
import threading
import random
import time


def get_detail_urls(file='sports_outdoor_top100_urllist.txt'):
    result = []
    with open(file,'r',encoding='utf-8') as fin:
        for line in fin:
            detail = eval(line.strip())
            url = detail['url']
            result.append(url)
        result =list(set(result))
        return result

def work_thread():
    global detail_urls
    global lock
    while(detail_urls):
        lock.acquire()
        try:
            url = random.choice(detail_urls)
            #detail_urls.pop(0)
        except Exception:
            pass
        finally:
            # 改完了一定要释放锁:
            lock.release()


        try:
            sleep_time = random.random()*4
            time.sleep(sleep_time)
            detail = get_detail(url)
            detail_output(detail,)
            print(threading.current_thread().name,'get detail done')

            lock.acquire()
            try:
                detail_urls.remove(url)
            except Exception:
                pass
            finally:
                # 改完了一定要释放锁:
                lock.release()

        except Exception as e:
            print(threading.current_thread().name, 'get detail done,error ending')
            print(threading.current_thread().name,e)




def detail_output(detail,file='sports_outdoor_details.txt'):
    with open(file,'a',encoding='utf-8')as fout:
        fout.write(json.dumps(detail,ensure_ascii=False))
        fout.write('\n')


def main():
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

#################全局变量，保存待爬数据列表
detail_urls = []
detail_urls = get_detail_urls()
lock=threading.Lock()   #锁变量，控制detail_urls的互斥访问

########################

if __name__=='__main__':
    main()