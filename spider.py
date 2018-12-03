#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
# import cookielib
# import urllib2
import os
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver  #导入Selenium的webdriver
from selenium.webdriver.common.keys import Keys  #导入Keys
import re

def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print (path+' 创建成功')
        return True
    else:
        print (path+' 目录已存在')
        return False

#保存摘要 name.txt
def save_abstract(file,str):
	with open(file,'w') as f:
		f.write(str)

path = '摘要文件'
zh_pattern = re.compile(u'[\u4e00-\u9fa5]+') #判断中文

mkdir(path)
driver = webdriver.Chrome()  #指定使用的浏览器，初始化webdriver
driver.get("http://yuanjian.cnki.net/cjfd/Home/Detail/WYXY201804")  #请求网页地址
# headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
# url = 'http://www.cnki.com.cn/Article/CJFDTOTAL-WYXY201805005.htm'
# r = requests.get(url,headers=headers) #像目标url地址发送get请求，返回一个response对象
# soup = BeautifulSoup(r.text, 'lxml')
csv_header=['题目','URL']
f = open('paper_urls.csv','w',newline='')
writer = csv.writer(f) 
writer.writerow([csv_header])
			        
soup = BeautifulSoup(driver.page_source, 'lxml')
all_div = soup.find('div',id='divCJFDCatalog').find_all('div',class_='l-box')#获取栏目
for div in all_div:
	column = div.find('div').string.strip() #栏目名
	if column:
		# print('\n',column)
		tab_lefts = div.find_all('div',class_='tab-left')
		titles=[i.find('a') for i in tab_lefts]
		for title in titles:
			title_name=(title.string).strip()
			url=title['href']
			

			driver.get(url)
			soup = BeautifulSoup(driver.page_source, 'lxml')
			abstract = soup.find('div', style="text-align:left;word-break:break-all").get_text()
			content = abstract.split('：',1)[1]
			if content[0]!='正' and zh_pattern.search(title_name):
				print(title_name)
				writer.writerow([title_name,url])#存入paper_urls.csv

				file = os.path.join(path,title_name.replace('/','')+'.txt')
				save_abstract(file,content)
f.close()
driver.close()
# title = soup.find('h1',{'class':'xx_title'}).string
# abstract = soup.find_all('div', style="text-align:left;word-break:break-all")
# for i in abstract:
# 	print(i.string)
