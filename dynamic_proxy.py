# -*- coding: utf-8 -*-
__author__='wys'
#实现动态代理的功能，维护动态代理ip，并且随时跟新

import requests
import random
import time
import threading

class dynamic_proxy():

    def __init__(self):
        print('et init...')
        self.least_num = 5
        self.lock = threading.Lock()  # 锁变量，控制detail_urls的互斥访问
        #self.get_url = 'http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=1000&fa=0&fetch_key=MTczMTc2MDc2OTd8NQ%253D%253D&qty=1&time=1&pro=&city=&port=1&format=txt&ss=4&css=&dt=1&specialTxt=3&specialJson='
        self.get_url = 'http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=1000&fa=0&fetch_key=MTczMTc2MDc2OTd8NQ%253D%253D&qty=1&time=1&pro=&city=&port=1&format=txt&ss=4&css=&dt=1&specialTxt=3&specialJson='
        self.ips = []
        self.get_new_ips()

    def get_new_ips(self):
        try:
            res = requests.get(self.get_url)
            if('msg' in res.text):
                msg = eval(res.text)
                print(msg)
                time.sleep(6)
                self.get_new_ips()
            else:
                result = res.text.split('\t')
                self.ips.extend(result)
                print('get new proxy done,len ips is %d'%len(self.ips))
                print(self.ips)
                if(len(self.ips)<self.least_num):
                    time.sleep(6)
                    self.get_new_ips()
        except Exception:
            pass

    def get_proxy(self):
        #print('in get_proxy',self.ips)
        proxy = random.choice(self.ips)
        return proxy

    def remove_ip(self,ip):
        self.ips.remove(ip)
        if(len(self.ips)< self.least_num):
            self.get_new_ips()
        else:
            pass

    def test_ip_usable(self,ip):
        proxy = ip
        url = "http://www.baidu.com/"
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            }
        try:
            response = requests.get(url, headers=header, proxies={"http": proxy}, timeout=10)
            if response.status_code == 200:
                print('该代理IP可用：',proxy)
                return True
            else:
                print("该代理IP不可用：", proxy)
                return False
        except Exception:
            print("该代理IP无效：", proxy)
            return False

    def test_ip_usable_aliex(self,ip):
        url = 'https://www.aliexpress.com/wholesale?catId=0&SearchText=balloon&page=0'
        proxy = ip
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
        try:
            proxies = {"http": 'http://' + proxy, "https": 'https://' + proxy}
            print(proxies)
            response = requests.get(url, headers=header, proxies=proxies, timeout=40)
            if len(response.text) > 30000:
                print('该代理IP可用：', proxy)
                return True
            else:
                print("该代理IP不可用：", proxy)
                return False
        except Exception:
            print("该代理IP无效：", proxy)
            return False

########################
dmp = dynamic_proxy()   #####模块里面定义的单例对象，导入即可使用

if __name__=='__main__':
    print(dmp)
    for i in range(10):
        proxy = dmp.get_proxy()
        print(proxy)
        dmp.test_ip_usable_aliex(proxy)
