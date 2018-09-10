# -*- coding: utf-8 -*-
__author__='wys'
#
#
import re
import traceback

result_file = 'sports_outdoor_details.txt'

def get_rank(text):   #获取item在sports&outdoor大类里面的排名
    li = text.split('#')
    li = [item for item in li if 'Sports & Outdoors' in item]
    if(li):
        for l in li:
            li_inner = l.split('>')
            if(len(li_inner)>1):
                continue
            else:
                rank_topcate = re.findall(r'[\d,]+', l)[0]
                rank_topcate = ''.join([t for t in rank_topcate if t != ','])
                rank_topcate = int(rank_topcate)
                return rank_topcate
    else:
        return None

def get_review(text):
    try:
        review = re.findall(r'[\d,]+', text)[0]
        review = ''.join([t for t in review if t != ','])
        review = int(review)
        #print(review)
        return review
    except Exception:
        print(traceback.print_exc())
        return None

def get_price(text):
    if(not text):
        return []
    prices = re.findall(r'[\d\.]+',text)
    if(len(prices)>1):
        return [float(item) for item in prices]
    elif(len(prices)==1):
        return [float(prices[0]),]
    else:
        return []


def read_data(file = result_file):
    result = []
    with open(file,'r',encoding='utf-8') as fin:
        for line in fin:
            try:
                line = re.sub('null','None',line)
                item = eval(line.strip())
                rank = item['rank']
                rank_topcate = get_rank(rank)
                #print(rank)
                #print(rank_topcate)

                review = item['review']
                #print(review)
                review = get_review(review)

                price_str = item['price']
                price = get_price(price_str)
                print(price_str)
                print(price)

                if(rank_topcate and rank_topcate < 20000):
                    if(review < 10):
                        if(price and price[0]>20):
                            item['rank_num'] = rank_topcate
                            item['review_num'] = review
                            item['price_num'] = price
                            result.append(item)
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            except:
                print(traceback.print_exc())
        return result

def output(li,file='sports_outdoor_filted.txt'):
    with open(file,'w',encoding='utf-8') as fout:
        for l in li:
            s = '{title}\t{url}\t{rank}\t{review}\t{ship}\t{price}\n'.format(
                title=l['title'],url=l['url'],rank=l['rank_num'],review=l['review_num'],
                ship=l['ship'],price=l['price']
            )
            fout.write(s)

if __name__=='__main__':
    result = read_data()
    print('len of result',len(result))
    result.sort(key=lambda s:s['rank_num'])
    output(result,)
    #result=[item for item in result if item <20000]
    #result.sort()
    #result = list(set(result))
    #print(result)
    #print(len(result))