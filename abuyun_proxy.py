# -*- coding: utf-8 -*-
__author__='wys'
#阿布云代理，带出一个ABUYUN_PROXY全局变量
#阿布云代理需要续费，链接：https://center.abuyun.com/#/cloud/http-proxy/tunnel/lists

import requests
import time
import http
import urllib3

class abuyun():
	def __init__(self):
		self.proxyHost = "http-dyn.abuyun.com"
		self.proxyPort = "9020"

		# 代理隧道验证信息
		self.proxyUser = "H9CCZYRXD11T86MD"
		self.proxyPass = "EB58EE4BFFEC2457"

		proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
			"host": self.proxyHost,
			"port": self.proxyPort,
			"user": self.proxyUser,
			"pass": self.proxyPass,
		}

		self.proxies = {
			"http": proxyMeta,
			"https": proxyMeta,   ###！important
		}

########################################定义全局变量ABUYUN,向外部提供代理
aby = abuyun()
ABUYUN_PROXY = aby.proxies

##########################################


###测试代理稳定性
if __name__=='__maain__':
	targetUrl = "https://www.aliexpress.com/wholesale?catId=0&SearchText=balloon&page=0"

	for i in range(100):
		try:
			#time.sleep(1)
			res = requests.get(targetUrl,proxies=ABUYUN_PROXY)
			print(len(res.text))
		except http.client.RemoteDisconnected:
			time.sleep(5)
		except urllib3.exceptions.MaxRetryError:
			time.sleep(5)
		except requests.exceptions.ProxyError:
			time.sleep(5)
		except Exception:
			print('unknow error')
			time.sleep(5)

if __name__=="__main__":
	from aliex_onepage_detail import test_detail_url,get_details
	for i in range(100):
		try:
			res = requests.get(test_detail_url,proxies=ABUYUN_PROXY)
			detail = get_details(res)
			print("{i}:{length}".format(i=i,length = len(res.text)))
			print(detail)
			print('\n')
		except http.client.RemoteDisconnected:
			print('sleep..')
			time.sleep(5)
		except urllib3.exceptions.MaxRetryError:
			print('sleep..')
			time.sleep(5)
		except requests.exceptions.ProxyError:
			print('sleep..')
			time.sleep(5)
		except Exception:
			print('unknow error')
			time.sleep(5)