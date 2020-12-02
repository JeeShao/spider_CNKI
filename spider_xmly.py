#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import csv
import sys
import io
import requests
from bs4 import BeautifulSoup
from selenium import webdriver  # 导入Selenium的webdriver
from selenium.webdriver.common.keys import Keys  # 导入Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def func():
    data=[]
    driver = webdriver.Chrome()  # 指定使用的浏览器，初始化webdriver
    driver.implicitly_wait(10)  # seconds
    for pageNo in range(1,6):
        URL = "http://www.lrts.me/rank/down/month/%s/20" % pageNo
        driver.get(URL)  # 请求网页
        soup = BeautifulSoup(driver.page_source, 'lxml')
        titlTag = soup.find_all('a', class_="book-item-name")
        titleHrefList = ['http://www.lrts.me'+i['href'] for i in titlTag]
        titleNameList = [i.string.strip() for i in titlTag]
        resList = list(zip(titleNameList,titleHrefList))
        print(titleNameList)
        print(titleHrefList)
        print(resList)

        for name ,url in resList:
            driver.get(url)  # 请求网页
            soup = BeautifulSoup(driver.page_source, 'lxml')
            playCount = soup.find('div',class_='d-o d-book-o').find('a').find('span').find('em').get_text().strip()
            print(name,' 的播放量是 ',playCount)
            data.append([name,playCount])
    print(data)
    driver.close()
    return data


if __name__ == '__main__':
    csv_header = ['Title', 'playCount']
    f = open('./月榜信息.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(csv_header)
    data = func()
    writer.writerows(data)
    f.close()
