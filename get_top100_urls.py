# -*- coding: utf-8 -*-
__author__='wys'
#首先构造category-tree 然后找到各个子目录的top100 urls ,输出备用

from category_tree import get_category_tree
from bestseller100_list import get_bestseller_list
from ET_IP import ET
from ET_IP import etc
import json

def top100_urls_output(li,file='sports_outdoor_top100_urllist.txt'):
    with open(file,'a',encoding='utf-8') as fout:
        for item in li:
            fout.write(json.dumps(item,ensure_ascii=False))
            fout.write('\n')


def get_top100(cate_tree,url):
    top100 = get_bestseller_list(url)
    for i in range(len(top100)):
        top100[i]['category'] = cate_tree
        top100[i]['rank'] = i

    top100_urls_output(top100, )


if __name__=='__main__':
    cate = 'Sports & Outdoors'
    cate_url = 'https://www.amazon.co.uk/gp/bestsellers/sports/ref=pd_dp_ts_sports_1'

    tree =get_category_tree()
    for item in tree:
        #print(item)
        try:
            cate_tree,cate,url = item
            print(item)

            top100 = get_bestseller_list(url)
            #print(top100)
            for i in range(len(top100)):
                top100[i]['category'] = cate_tree
                top100[i]['rank'] = i
            #print(top100)
            top100_urls_output(top100, )
            print('done')
        except Exception:
            continue