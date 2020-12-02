# -*- coding: utf-8 -*-
# @FileName: spider-jiuyou.py
# @function: #todo
# @Time    : 2020/12/2 0:39
# @Author  : Jee
import re
import string
import time
from selenium import webdriver  # 导入Selenium的webdriver
from selenium.webdriver.common.keys import Keys  # 导入Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


# 判断元素存在
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
    data = []
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)  # 指定使用的浏览器，初始化webdriver
    driver.implicitly_wait(0.5)  # 隐式等待1seconds页面加载完成 ，为全局设置，设置后所有的元素定位都会等待给定的时间，直到元素出现为止
    base = "https://www.9game.cn/news/0_"

    for page in range(1, 1001):
        URL = base + str(page) + "/"
        print("==============url:", URL, "=================")
        driver.get(URL)
        newsList = driver.find_elements_by_xpath("//ul[@class='news-list-con']/li")
        for news in newsList:
            newsName = news.find_element_by_tag_name("a").text
            newsUrl = news.find_element_by_tag_name("a").get_attribute('href')
            newsTime = str.split(news.find_element_by_tag_name("span").text, " ")[0]
            # 进入news详情页面
            detailDriver = webdriver.Chrome(chrome_options=chrome_options)
            detailDriver.get(newsUrl)
            time.sleep(0.5)
            newsImgsNum = len(
                detailDriver.find_elements_by_xpath("//div[@class='text-con']")[0].find_elements_by_tag_name("img")) - 1
            try:
                gameName = detailDriver.find_element_by_xpath("//h2[@class='h1-title']/a").text
            except Exception as e:
                pass
            detailDriver.quit()
            print(newsName, " ", newsTime, " ", newsUrl, "", gameName, " ", newsImgsNum)
        # driver.quit()

    # for news in tieziList:
    #     title = news.text  # 资讯标题
    #     ID = re.findall('\d+', news.get_attribute('href'))[1]  # 资讯ID
    #     tieziUrl = news.get_attribute('href')  # url
    #     game = re.findall('\w+', news.get_attribute('href'))[0]
    #     # time
    #     print("标题:", title, "ID:", ID, "链接:", tieziUrl, "游戏名:", game)
    #     news.click()
    #
    #     windows = driver.window_handles  # 获取当前所有窗口句柄 -> list
    #     driver.switch_to.window(windows[-1])  # 切换到最新打开的窗口
    #     # todo  处理打开的最新页面元素
    #     # score = driver.find_elements_by_xpath("//div[@class='com-blue-star-num']")
    #     # info = driver.find_elements_by_xpath("//div[@class='det-ins-num']")
    #     # print("评分:", score[0].text, "下载次数:", info[0].text[:-2], "\n")
    #
    #     driver.close()  # 关闭最新打开的窗口
    #     driver.switch_to.window(windows[0])  # 切换回主窗口 第一次打开的饿窗口
    driver.quit()


if __name__ == '__main__':
    data = func()
