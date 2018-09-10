# -*- coding: utf-8 -*-
__author__='wys'
#从一个大类目开始构造类目树，信息包含每个小类目的100bestseller 链接

from bs4 import BeautifulSoup
import requests
from lxml import etree
import time
from ET_IP import ET
from ET_IP import etc

def find_son_category(cate,cate_url): #cate_url对应100bestsellers 页面；
    #本函数的功能就是提取的子类目的名称和url
    #time.sleep(1)
    #res = requests.get(cate_url)
    res = etc.get(cate_url)

    if(res.status_code ==200):
        soup = BeautifulSoup(res.text,'html.parser')
        top_ul = soup.findAll('ul',id='zg_browseRoot')[0]

        html = etree.HTML(str(top_ul))
        cate_name = html.xpath('//ul/li/span/text()')[0]
        cate_name=cate_name.strip()
        #assert cate_name == cate
        if(not cate_name == cate):
            return None
        cate_current = html.xpath('//ul/li/span/../../ul/li/a/text()')  #/ul/li/span 对应当前category
        cate_urls = html.xpath('//ul/li/span/../../ul/li/a/@href')

        return (cate_name,zip(cate_current,cate_urls))
        #print(zip(cate_current,cate_urls))
        pass
    else:
        return None

def build_category_tree(category_root,category_url):  #从category_root开始构建tree
    category_tree = []
    category_tree.append((category_root,category_root,category_url))    # (cate_tree，cate名,cate_url)
    i = 0
    while(i<len(category_tree)):
        try:
            current = category_tree[i]
            i += 1
            cate_tree,cate_name,cate_url = current
            sons = find_son_category(cate_name,cate_url)
            if(sons):
                for name,url in sons[1]:
                    tree='>'.join([cate_tree,name])   #(父目录，当前目录，子目录）
                    category_tree.append((tree,name,url))
                    #print('append')
                    #print(tree,name,url)
                    print(tree)
            else:
                pass
        except Exception :
            continue
    return category_tree

def get_category_tree(file = 'sports_outdoor_category.txt'):
    result = []
    with open(file,'r',encoding='utf-8') as fin:
        for line in fin:
            tree,name,url = line.strip().split('\t')
            result.append((tree,name,url))
        return result


def category_output(li,file='sports_outdoor_category.txt'):
    with open(file,'a',encoding='utf-8') as fout:
        for item in li:
            fout.write('\t'.join(item))
            fout.write('\n')



if __name__=='__main__':
    cate = 'Sports & Outdoors'
    cate_url = 'https://www.amazon.co.uk/gp/bestsellers/sports/ref=pd_dp_ts_sports_1'

    tree = build_category_tree(cate,cate_url)
    category_output(tree,)
    for item in tree:
        print(item)
