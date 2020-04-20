'''
@Author: LU Weipeng
@Date: 2020-04-18 09:05:27
@LastEditTime: 2020-04-20 16:58:48
@LastEditors: LU Weipeng
@Description: version for GITHUB
@FilePath: \AMap\getpoi.py
'''

import json
import xlwt
from datetime import datetime
from urllib import request
from urllib.parse import quote
import time
import os
from keyword_type import type, keyword
import shapefile
import re

# 避免在保存json文件时出现非法字符
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


# 获取数据
def get_data(pageindex, url_amap):
    global total_record
    # 暂停500毫秒，防止过快取不到数据
    time.sleep(0.5)
    print('解析页码： ' + str(pageindex) + ' ... ...')
    url = url_amap.replace('pageindex', str(pageindex))
    # 中文编码
    url = quote(url, safe='/:?&=')
    html = ""

    with request.urlopen(url) as f:
        html = f.read()
        rr = json.loads(html)
        if total_record == 0:
            total_record = int(rr['count'])
        return rr['pois']


def getPOIdata(page_size, json_name, url_amap):
    global total_record
    print('获取POI数据开始')
    josn_data = get_data(1, url_amap)
    if (total_record % page_size) != 0:
        page_number = int(total_record / page_size) + 2
    else:
        page_number = int(total_record / page_size) + 1

    with open(json_name, 'w') as f:
        # 去除最后]
        f.write(json.dumps(josn_data).rstrip(']'))
        for each_page in range(2, page_number):
            html = json.dumps(get_data(each_page, url_amap)
                              ).lstrip('[').rstrip(']')
            if html:
                html = "," + html
            f.write(html)
            print('已保存到json文件：' + json_name)
        f.write(']')
    print('获取POI数据结束')

if __name__ == '__main__':

    if not os.path.exists('data_index'):
        os.makedirs('data_index')
    city = ['长沙市']
    keyword = list(set(keyword))

    for i in range(0, len(city)):
        for cnt, j in enumerate(range(0, len(keyword))):
            # 填入你的key
            url_amap = 'http://restapi.amap.com/v3/place/text?key=(your key)&keywords=' + \
                keyword[j] + '&city=' + city[i] + \
                '&citylimit=true&children=1&offset=20&page=pageindex&extensions=all'
            page_size = 25  # 每页记录数据个数
            page_index = r'page=1'  # 显示页码
            global total_record
            total_record = 0
            # 获取数据列
            bkeys = ['id', 'biz_type', 'name', 'type', 'address', 'tel', 'lon', 'lat',
                     'pcode', 'pname', 'citycode', 'cityname', 'adcode', 'adname', 'business_area']
            print('正在获取：%s from %s(%d over %d)' %
                  (keyword[j], city[i], cnt+1, len(keyword)))
            json_name = 'data_amap_%s_from_%s.json' % (
                keyword[j], city[i])
            json_name = 'data_index/'+validateTitle(json_name)
            getPOIdata(page_size, json_name, url_amap)
            # 暂停一下，避免IP地址被屏蔽
            if (i % 10 == 0):
                time.sleep(30)
            elif (i % 10 != 0):
                time.sleep(10)
