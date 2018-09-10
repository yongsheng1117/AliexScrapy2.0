# -*- coding: utf-8 -*-
__author__='wys'
#页面爬取程序，在requests的基础上增加异常处理，动态代理ip，回调函数，，，等等功能

import requests
import random
import time
import dynamic_proxy
from dynamic_proxy import dmp

class crawler():
    def __init__(self):

        self.user_agents =[
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
            ]

    def simple_get_by_proxy(self,url,retry=3):
        header = {
            "User-Agent": random.choice(self.user_agents), }
        proxy = dmp.get_proxy()
        try:
            response = requests.get(url, headers=header, proxies={"http": proxy}, timeout=20)
            print(len(response.text))
            return response
        except requests.RequestException as e:  #
            print('requests.get error in class:crawler method:get')
            print(e)
            if(retry > 0):
                return self.simple_get_by_proxy(url,retry -1)
            else:
                return None


    def get(self,url,call_back,retries=3):
        header = {
            "User-Agent": random.choice(self.user_agents),}
        try:
            response = requests.get(url, headers=header, timeout=10)
            res = call_back(response)   #调用回调函数
            if(res):   #成功结束
                pass  #
            else:     #失败
                pass
        except requests.RequestException as e:    #
            print('requests.get error in class:crawler method:get')
            print(e)
            time.sleep(5)
            if(retries > 0):
                return self.get(url,call_back,retries-1)
        except Exception as e2:  #其他模块错误，比如callback错误
            print(e2)

    def get_by_proxy(self,url,call_back):
        #print('enter get_by_proxy')
        header = {
            "User-Agent": random.choice(self.user_agents),}
        proxy = dmp.get_proxy()
        try:
            response = requests.get(url, headers=header, proxies={"http": proxy}, timeout=20)
        except requests.RequestException as e:  #
            print('requests.get error in class:crawler method:get')
            print(e)
            return False
        try:
            msg,res = call_back(response)   #调用回调函数
            if(msg =='success'):   #成功结束
                return True,res   #成功结束，返回上层
            elif(msg =='proxy_unsable'):     #失败
                print('remove unsable proxy ip')
                dmp.remove_ip(proxy)
                return False,res  #失败结束，返回上层
            else:
                return False,res   ####????????????????????
        except ValueError as e2:  #其他模块错误，比如callback错误
            print(e2)
            return False,res

    def __call__(self,url,call_back,):
        self.get_by_proxy(url,call_back,)


if __name__=='__main__':
    cra = crawler()
    url = 'http://www.baidu.com'

    def call_back(response):
        print('call_back method:done')
        print(response.status_code)
        return True  #成功结束，通知上层

    res = cra(url,call_back,retries=2)