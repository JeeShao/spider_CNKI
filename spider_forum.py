# -*- coding: utf-8 -*-
# @FileName: spider_forum.py
# @Time    : 2020/12/4 0:10
# @Author  : Jee

import csv
from selenium import webdriver  # 导入Selenium的webdriver
from selenium.webdriver.chrome.options import Options
import logging

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.WARNING)
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
    # data = []
    base = "http://bbs.9game.cn/forum-12607-"

    for page in range(1, 500):
        data = []  # 用于存放返回话题结果数据 list
        URL = base + str(page) + ".html"
        print("==========", URL, "==========")
        driver.get(URL)  # 访问网页
        topics = driver.find_elements_by_xpath("//a[@class='xst']")  # 过滤该页所有话题信息
        for tp in topics:  # 遍历该页所有话题list
            tpName = tp.text  # topic title
            tpName = str(bytes(tpName, encoding='utf-8').decode('utf-8').encode('gbk', 'ignore').decode('gbk'))  # 转换编码
            tpName = tpName.strip()  # 去除话题标题前后空格
            tpUrl = tp.get_attribute('href')  # topic url
            data.append({"tpName": tpName, "tpUrl": tpUrl})  # 标题和地址数据添加至data中
            writer.writerow([tpName, tpUrl])  # 将话题和地址信息写入csv文件
            f.flush()  # 将内存数据刷入磁盘文件
        getPosts(data)  # 获取话题评论并写入文件


# get posts of one topic
def getPosts(topics):
    postOfTopic = {}
    for tp in topics:  # 话题
        tpName = tp['tpName']
        tpUrl = tp['tpUrl']
        pages = getPostsAllPages(tpUrl, "//a[@class='nxt']")  # 获取某个话题存在所有的评论页url
        print("\n【", tpName, "】的评论信息:")
        allPost = []  # 单个话题的所有评论
        for i, p in enumerate(pages):  # 页码
            print(".......第", i + 1, "页.......")
            try:
                driver.get(p)
            except Exception as e:
                logging.warning(e)
                continue
            posts = driver.find_elements_by_xpath("//td[@class='t_f']")  # 获取该页评论信息
            for p in posts:  # 遍历评论
                post = p.text
                post = str(bytes(post, encoding='utf-8').decode('utf-8').encode('gbk', 'ignore').decode('gbk')).strip()
                if post != '':
                    allPost.append([post])
        postOfTopic[tpName] = allPost
        print(allPost)
        writer_post.writerows(allPost)
        f_post.flush()
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
    csv_header = ['话题名称', '话题地址']  # 表格标题栏
    f = open('./jiuyou_forum_hyld_topic.csv', 'w', newline='')  # 打开文件
    writer = csv.writer(f, dialect='excel')  # csv写文件实例
    writer.writerow(csv_header)  # 写入表格标题

    csv_header_post = ['话题回复']
    f_post = open('./jiuyou_forum_hyld_post.csv', 'w', newline='')
    writer_post = csv.writer(f_post, dialect='excel')
    writer_post.writerow(csv_header_post)

    data = getTopics()  # 获取所有话题信息(话题名称-话题地址)
    f.close()  # 关闭文件
    f_post.close()
    driver.quit()  # 推出浏览器
