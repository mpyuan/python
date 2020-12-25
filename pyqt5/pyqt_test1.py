# -*- coding: utf-8 -*-
# @Author: mapyuan
# @Date  :  2020/12/23

from win32com import client
import time
import random
from lxml import etree

print(help(client))
dirver = client.DispatchEx("InternetExplorer.Application")
dirver.Navigate('http://192.168.1.102:8099/backend/site/login')
dirver.Visible = 1
time.sleep(random.randint(2, 8))
dirver.Document.body.getElementsByTagName("p")[3].firstElementChild.click()
dirver.Visible = 1
time.sleep(random.randint(8, 12))
dirver.Document.body.getElementsByTagName("tbody")[1].click()
time.sleep(random.randint(10, 20))
for i in dirver.Document.body.getElementsByTagName("input"):
    if i.name == 'request:hnc':
        i.value = '百度'
# 点击查询
time.sleep(3)
dirver.Visible = 1
for i in dirver.Document.body.getElementsByTagName("input"):
    if i.id == '_searchButton':
        i.click()

time.sleep(20)
form_str=dirver.Document.body.getElementsByTagName("form")[2].innerHTML
print(form_str)
html_str = etree.HTML(form_str)
tr_list = html_str.xpath('//tr[@class="ng-repeat"]')
for tr in tr_list:
    item = {}
    item['注册号'] = tr.xpath('.//td[2]/a/text()')
    item['国际分类'] = tr.xpath('.//td[3]/text()')
    item['申请日期'] = tr.xpath('.//td[4]/text()')
    item['商标名称'] = tr.xpath('.//td[5]/a/text()')
    item['申请人名称'] = tr.xpath('.//td[6]/a/text()')

    print(item)
    with open('item.txt', 'w', encoding='utf-8') as f:
        f.write(str(item))