# -*- coding: utf-8 -*-
__author__='wys'
#定义检查是不是 登录页（robot check页面）的代码

import requests

def is_check_robot(res):
    title = res.title
    if(title =='Robot Check'):
        return True
    else:
        return False

def tpye_of_page(res):
    title = res.title
    if(title =='Robot Check'):
        return 'robot_check_page'
    elif(res.status_code>=500):
        return '500_page'
    elif(400<= res.status_code<500):
        return '400_page'
    else:
        return 'detail_page'
