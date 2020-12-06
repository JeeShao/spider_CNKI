# -*- coding: utf-8 -*-
# @FileName: spider_forum.py
# @function: #
# @Time    : 2020/12/4 0:10
# @Author  : Jee

import csv
from selenium import webdriver  # 导入Selenium的webdriver
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


# get topic name and url
# return [{"tpName": tpName, "tpUrl": tpUrl},{},{},...]
def getTopics():
    global writer
    data = []
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)  # 指定使用的浏览器，初始化webdriver
    driver.implicitly_wait(0.5)  # 隐式等待1seconds页面加载完成 ，为全局设置，设置后所有的元素定位都会等待给定的时间，直到元素出现为止
    base = "http://bbs.9game.cn/forum-5981-"

    for page in range(1, 2):
        URL = base + str(page) + ".html"
        print("\n==============url:", URL, "=================")
        driver.get(URL)
        topics = driver.find_elements_by_xpath("//a[@class='xst']")
        print(len(topics))
        for tp in topics:
            tpName = tp.text  # topic title
            tpName = str(bytes(tpName, encoding='utf-8').decode('utf-8').encode('gbk', 'ignore').decode('gbk'))
            tpUrl = tp.get_attribute('href')  # topic url
            print(tpName, " ", tpUrl)
            data.append({"tpName": tpName, "tpUrl": tpUrl})
            writer.writerow([tpName, tpUrl])
            f.flush()
    driver.quit()
    return data

# get topics` posts
def getPosts(topics):
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(0.5)
    for tp in topics:
        tpName = tp['tpName']
        tpUrl = tp['tpUrl']
        driver.get(tpUrl)
        posts = driver.find_elements_by_xpath("//td[@class='t_f']")
        print("\n=====",tpName,"的评论信息:")
        for p in posts:
            post = p.text
            print(post)





if __name__ == '__main__':
    csv_header = ['话题名称','话题地址']
    f = open('./jiuyou_forum_wzry.csv', 'w', newline='')
    writer = csv.writer(f, dialect='excel')
    writer.writerow(csv_header)
    data = getTopics()
    getPosts(data)
    f.close()

