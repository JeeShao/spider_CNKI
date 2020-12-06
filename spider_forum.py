# -*- coding: utf-8 -*-
# @FileName: spider_forum.py
# @Time    : 2020/12/4 0:10
# @Author  : Jee

import csv
from selenium import webdriver  # 导入Selenium的webdriver
from selenium.webdriver.chrome.options import Options
import logging

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.WARNING)
# setting of driver
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(0.01)

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

# get all topics` name and url
# return [{"tpName": tpName, "tpUrl": tpUrl},{},{},...]
def getTopics():
    global writer
    data = []
    base = "http://bbs.9game.cn/forum-5981-"

    for page in range(1, 5):
        URL = base + str(page) + ".html"
        print("==========", URL, "==========")
        driver.get(URL)
        topics = driver.find_elements_by_xpath("//a[@class='xst']")
        for tp in topics:
            tpName = tp.text  # topic title
            tpName = str(bytes(tpName, encoding='utf-8').decode('utf-8').encode('gbk', 'ignore').decode('gbk'))
            tpName = tpName.strip()
            tpUrl = tp.get_attribute('href')  # topic url
            data.append({"tpName": tpName, "tpUrl": tpUrl})
            writer.writerow([tpName, tpUrl])
            f.flush()
    return data

# get posts of one topic
def getPosts(topics):
    postOfTopic = {}
    for tp in topics:  # 话题
        tpName = tp['tpName']
        tpUrl = tp['tpUrl']
        pages = getPostsAllPages(tpUrl, "//a[@class='nxt']")
        print("\n【", tpName, "】的评论信息:")
        allPost = [] # 单个话题的所有评论
        for i, p in enumerate(pages):  # 页码
            print(".......第", i + 1, "页.......")
            try:
                driver.get(p)
            except Exception as e:
                logging.warning(e)
                continue
            posts = driver.find_elements_by_xpath("//td[@class='t_f']")
            for p in posts:  # 评论
                post = p.text
                allPost.append(post)
        postOfTopic[tpName] = allPost
    return postOfTopic


# get url of all pages for one topic
def getPostsAllPages(baseUrl, element):
    allPageUrl = [baseUrl]
    url = baseUrl
    while url != "":
        try:
            driver.get(url)
        except Exception as e:
            # traceback.print_exc()
            logging.warning(e)
            break
        nextPage = driver.find_elements_by_xpath(element)
        if len(nextPage) == 0:
            break
        url = nextPage[0].get_attribute('href')
        allPageUrl.append(url)
    return allPageUrl


if __name__ == '__main__':
    csv_header = ['话题名称', '话题地址']
    f = open('./jiuyou_forum_wzry.csv', 'w', newline='')
    writer = csv.writer(f, dialect='excel')
    writer.writerow(csv_header)
    data = getTopics()
    getPosts(data)
    driver.quit()
    f.close()
