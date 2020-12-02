# -*- coding: utf-8 -*-
# @FileName: spider-jiuyou.py
# @function: #todo
# @Time    : 2020/12/2 0:39
# @Author  : Jee
import re
import string
import time
import csv
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


def getData():
    global writer
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
            context = detailDriver.find_elements_by_xpath("//div[@class='text-con']")
            if len(context)==0:
                context = detailDriver.find_elements_by_xpath("//div[@class='post-content']")
                if len(context)==0:
                    print("continue1...")
                    continue
            newsImgsNum = len(context[0].find_elements_by_tag_name("img")) - 1
            try:
                gameName = detailDriver.find_element_by_xpath("//h2[@class='h1-title']/a").text
            except Exception as e:
                print("continue2...")
                continue
            detailDriver.quit()
            print(newsName, " ", newsTime, " ", newsUrl, "", gameName, " ", newsImgsNum)
            data.append({
                "newsName":newsName,
                "gameName":gameName,
                "time": newsTime,
                "url": newsUrl,
                "imgNum": newsImgsNum
                })
            writer.writerow([
                newsName,
                gameName,
                newsTime,
                newsUrl,
                newsImgsNum
                ])
            f.flush()
    #     windows = driver.window_handles  # 获取当前所有窗口句柄 -> list
    #     driver.switch_to.window(windows[-1])  # 切换到最新打开的窗口
    #     driver.close()  # 关闭最新打开的窗口
    #     driver.switch_to.window(windows[0])  # 切换回主窗口 第一次打开的饿窗口
    driver.quit()
    return data


if __name__ == '__main__':
    csv_header = ['新闻名称', '游戏名称','时间','地址','图片数量']
    f = open('./jiuyou_data.csv', 'w', newline='')
    writer = csv.writer(f,dialect='excel')
    writer.writerow([csv_header])
    data = getData()
    print(data)
    f.close()
    # data = [{'time': '2020-12-03', 'newsName': '《第五人格》联动第二弹礼包已开放领取', 'gameName': '第五人格', 'url': 'https://www.9game.cn/dwrg/4848918.html', 'imgNum': 1}]
    # f = open('./jiuyou_data.csv', 'wt', newline='')
    # writer = csv.DictWriter(f, fieldnames=['newsName', 'gameName','time','url','imgNum'])
    # writer.writeheader()  # 将fieldnames写入标题行