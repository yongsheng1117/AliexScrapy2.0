# -*- coding: utf-8 -*-
__author__='wys'
#input:商品详情页url output：商品详情

import re
import requests
from bs4 import BeautifulSoup

test_detail_url ='https://www.aliexpress.com/item/throw-tent-outdoor-3-4persons-automatic-tents-speed-open-throwing-pop-up-windproof-waterproof-camping-tent/32753911233.html?spm=2114.search0104.3.98.7a404f55InTxDg&ws_ab_test=searchweb0_0,searchweb201602_3_10152_10151_10065_10068_10344_10342_10325_10546_10343_10340_10548_10341_10696_10084_10083_10618_10307_10846_10059_100031_10103_10624_10623_10622_10621_10620,searchweb201603_1,ppcSwitch_5&algo_expid=91fc9efc-1ffa-4d15-bd0f-37ac8bc87bf7-12&algo_pvid=91fc9efc-1ffa-4d15-bd0f-37ac8bc87bf7&priceBeautifyAB=0'

def is_login_page(res):
    length = len(res.text)
    if(length < 30000):
        return True
    else:
        return False

def get_details(url):
    result = {}
    result['url'] = url
    res = requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')

    ######product name
    product_name = soup.findAll('h1',class_='product-name')
    product_name = product_name[0].text
    result['product_name']=product_name
    #print(product_name)

    #####pictures
    pics = []
    pictures = soup.findAll('span',class_='img-thumb-item')
    for pic in pictures:
        img = re.findall(r'src="([^"]*?)"',str(pic))   #匹配src属性里面的url
        img = re.sub(r'_\d+x\d+.jpg','',img[0])    #去除小图片后缀  _50x50.jpg
        pics.append(img)
    result['images'] = pics   #返回商品图片
    #print(pics)


    ###!!!!!!!!!这里是不同类目不一样的地方，帐篷按照颜色来区分，**可能按照尺寸来区分。。。。。
    #####p_property  colors
    dls = soup.findAll('dl',class_='p-property-item')
    try:
        colors = dls[0]
        title = re.findall(r'<dt[^>]*?>(.*)</dt>',str(colors))  #找到dt元素里面包含的文本
        title_subproduct = title[0]

        #print(title_subproduct)

        colors_return = []   #返回的数据
        soup_color =BeautifulSoup(str(colors),'html.parser')  #匹配几个子产品属性
        imgs = soup_color.findAll('img')
        if(imgs):      #####子产品列表放的是图片
            a_li = soup_color.findAll('a')
            ids = {} #暂时存储 skuid
            for a in a_li:
                title = a['title']
                sku_id = a['data-sku-id']
                ids[title] = sku_id
            imgs = soup_color.findAll('img')
            for img in imgs:
                title = img["title"]   #子产品颜色分类
                bigpic =img['bigpic']   #子产品图片
                colors_return.append({'title':title,'img':bigpic,'sku_id':ids[title]})
            #print(colors_return)
        else:  ####子产品列表放的是文字
            a_li = soup_color.findAll('a')
            spans = soup_color.findAll('span')
            for a,span in zip(a_li,spans):
                sku_id = a['data-sku-id']
                title = span.text  # 子产品颜色分类
                colors_return.append({'title': title, 'sku_id': sku_id})
            # print(colors_return)

        ######prices
        skus = re.findall(r'var skuProducts=([\w\W]*?}}\])', res.text)  #包含price的脚本结构
        skus = re.sub('true', 'True', skus[0])  #JavaScript 的true 转化为Python 的True
        skus = re.sub('false','False',skus)
        skus = eval(skus)
        #print(skus)
        for color in colors_return:
            title = color['title']
            sku_id = color['sku_id']
            prices = []
            for sku in skus:
                skuAttr = sku['skuAttr']
                if(title in skuAttr or sku_id in skuAttr):
                    if('actSkuCalPrice' in sku['skuVal']):
                        prices.append(sku['skuVal']['actSkuCalPrice'])   #???,不一定是这个价格
                    elif('skuMultiCurrencyCalPrice' in sku['skuVal']):
                        prices.append(sku['skuVal']['skuMultiCurrencyCalPrice'])  # ???,不一定是这个价格
                    else:
                        prices.append(sku['skuVal']['skuCalPrice'])
                else:
                    pass
            prices = [float(item) for item in prices]
            color['price']= min(prices)

        result['sub_products_title'] = title_subproduct  # 这是子产品的分类属性 比如 颜色，大小
        result['sub_products_list'] = colors_return
        #print(colors_return)
    except KeyError as e:
        print(e)
    finally:
        span_sprice = soup.findAll('span',id='j-sku-discount-price')
        #print(span_sprice)
        if(span_sprice):
            price = span_sprice[0].text
            print('price:',price)
            result['price'] = price
        else:
            span_sprice = soup.findAll('span', id='j-sku-price')
            price = span_sprice[0].text
            print('price:',price)
            result['price'] = price


    #####specifics
    specifics = soup.findAll('li',class_='property-item')
    #print(len(specifics))
    specs = {}
    for sp in specifics:
        soup_in = BeautifulSoup(str(sp),'html.parser')
        title_span = soup_in.findAll('span',class_='propery-title')
        title = title_span[0].text
        desc_span = soup_in.findAll('span',class_='propery-des')
        desc = desc_span[0].text
        specs[title] =desc
    result['specifics']=specs     #这里返回的是product的specifics
    #print(specs)

    '''#############product descriptions
    description_div = soup.findAll('div',class_='description-content')
    descs = []
    if(description_div):
        print(description_div[0])
        soup_desc = BeautifulSoup(str(description_div[0]),'html.parser')
        spans = soup_desc.findAll('span')
        print(spans)
        for span in spans:
            print(span.text)
            descs.append(span.text)
    result['prodict_description'] = descs'''


    return result



if __name__=='__main__':
    url = test_detail_url
    detail = get_details(url)
    print(detail)
