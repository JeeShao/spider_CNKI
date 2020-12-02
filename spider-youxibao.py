# -*- coding: utf-8 -*-
# @FileName: spider-youxibao.py
# @function: #todo
# @Time    : 2020/9/17 22:13
# @Author  : Jee
import os
import csv
import sys
import io
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver  # 导入Selenium的webdriver
from selenium.webdriver.common.keys import Keys  # 导入Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

#判断元素存在
def isElementExist(driver, element):
    flag = True
    driver = driver
    try:
        driver.find_element_by_xpath(element)
        return flag
    except:
        flag = False
        return flag

def func():
    data=[]
    driver = webdriver.Chrome()  # 指定使用的浏览器，初始化webdriver
    driver.implicitly_wait(0.5)  # 隐式等待1seconds页面加载完成 ，为全局设置，设置后所有的元素定位都会等待给定的时间，直到元素出现为止
    URL = "https://android.myapp.com/myapp/category.htm?orgame=2"
    driver.get(URL)
    # time.sleep(1)
    if isElementExist(driver, "//a[@hidefocus='true']"):
        print("点击 “加载更多”")
        loadMoreBtn = driver.find_elements_by_xpath("//div[@class='load-more-btn']//a")[0]
        loadMoreBtn.click()
    # 显示等待
    # try:
    #     element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "app-info-icon")))
    # finally:
    #     time.sleep(10)
    #     driver.quit()
    appList = driver.find_elements_by_xpath("//a[@class='name ofh']")
    for app in appList:
        appName = app.text  #游戏名称
        appUrl = app.get_attribute('href') #游戏url
        print(appName,"  ",appUrl)
        app.click()
        windows = driver.window_handles #获取当前所有窗口句柄 -> list
        driver.switch_to.window(windows[-1])  #切换到最新打开的窗口
        # try:
        #     element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "com-blue-star-num")))
        # finally:
        #     time.sleep(10)
        #     driver.quit()
        #todo  处理打开的最新页面元素
        score = driver.find_elements_by_xpath("//div[@class='com-blue-star-num']")
        info = driver.find_elements_by_xpath("//div[@class='det-ins-num']")
        print("评分:", score[0].text, "下载次数:", info[0].text[:-2], "\n")

        driver.close()  #关闭最新打开的窗口
        driver.switch_to.window(windows[0]) #切换回主窗口 第一次打开的饿窗口
    driver.quit()

if __name__ == '__main__':
    # csv_header = ['Title', 'playCount']
    # f = open('./月榜信息.csv', 'w', newline='')
    # writer = csv.writer(f)
    # writer.writerow(csv_header)
    data = func()
    # writer.writerows(data)
    # f.close()