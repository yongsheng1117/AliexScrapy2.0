# -*- coding: utf-8 -*-
__author__='wys'
#获取et代理动态ip

import requests
import random
import time

class ET():
    def __init__(self):
        #self.get_url = 'http://47.106.180.108:8081/Index-generate_api_url.html?packid=2&fa=0&qty=10&port=1&format=txt&ss=4&css=&ipport=1&et=1&pro=&city='
        print('et init...')
        self.get_url = 'http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=2&fa=0&fetch_key=&qty=15&time=1&pro=&city=&port=1&format=txt&ss=4&css=&dt=1&specialTxt=3&specialJson='
        self.ips = {}    #key:ip  value:failed time list
        self.ips = self.get_new_ips()

    def get_new_ips(self):
        res = requests.get(self.get_url)
        if('msg' in res.text):
            msg = eval(res.text)
            print(msg)
            time.sleep(5)
            self.get_new_ips()
        else:
            result = res.text.split('\t')
            result = {item:[] for item in result}
            for key,value in result.items():
                self.ips[key] = value
            print('get new proxy done,len ips is %d'%len(self.ips))
            print(self.ips)
            return result

    def get(self,url):
        sleep_time = random.random()*7
        time.sleep(sleep_time)
        proxy,_ = random.choice(list(self.ips.items()))
        #print('proxy:',proxy)

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
        try:
            response = requests.get(url, headers=header, proxies={"http": proxy}, timeout=5)
            if response.status_code == 200:
                return response
            else:
                self.proxy_fail(proxy)
                return response
        except Exception:
            for i in range(3):
                try:
                    proxy, _ = random.choice(list(self.ips.items()))
                    response = requests.get(url, headers=header, proxies={"http": proxy}, timeout=5)
                    if response.status_code == 200:
                        return response
                    else:
                        continue
                except Exception:
                    continue
            return None

    def proxy_fail(self,ip):
        self.ips[ip].append(time.time())
        for ft in self.ips[ip]:
            now = time.time()
            if(now -ft >300):
                self.ips[ip].remove(ft)
        if(len(self.ips[ip])> 5):
            print('ip',ip,'failed more 5 in 5 minute,erased')
            self.ips.pop(ip)
            self.refresh_ips()

    def refresh_ips(self):
        if(len(self.ips)<20):
            print('usabel ips is less than 10,get new')
            self.get_new_ips()
            print('usable ips is',len(self.ips))

    def renew_all_ip(self):
        self.ips ={}
        self.get_new_ips()
        print('renew all ips')
        print('len of ips is:%d now'%len(self.ips))

    def test_ip_usable(self,ip):
        proxy = ip
        url = "http://www.baidu.com/"
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            }
        try:
            response = requests.get(url, headers=header, proxies={"http": proxy}, timeout=1)
            if response.status_code == 200:
                #print('该代理IP可用：',proxy)
                return True
            else:
                #print("该代理IP不可用：", proxy)
                return False
        except Exception:
            #print("该代理IP无效：", proxy)
            return False

########################
etc = ET()   #####模块里面定义的单例对象，导入即可使用

if __name__=='__main__':
    #et = ET()

    url = 'http://search.kongfz.com/product_result/?key=9787550256606&status=0'

    for i in range(10000):
        res = etc.get(url)
        print(i)
        print(res.status_code)