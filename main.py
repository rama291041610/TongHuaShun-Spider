#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import threading
import random
import time
from config import *
from page import Page
from mysql import Mysql


def is_exist(mysql, kind, title):
    sql = 'SELECT COUNT(*) from news where `type` = "%s" and `title` = "%s"' % (kind, title)
    data = mysql.query(sql)
    if data and data[0] == 0:
        return False
    elif data:
        return True
    else:
        return False


def insert(mysql, info):
    sql = "INSERT INTO  news (type, title, content, time) VALUES ('%s', '%s', '%s', '%s')" % (
        info.get('type'), info.get('title'), info.get('content'), info.get('time'))
    mysql.insert(sql)


def spider(kind):
    mysql = Mysql(config)
    pn = 1

    while True:
        try:
            p = Page(kind, pn)
            articles = p.get_articles()
        except:
            time.sleep(random.uniform(0.24, 1.08))
            continue

        status = False
        for article in articles:
            if article.get_time() < end_time:
                status = True
                break
            elif is_exist(mysql, kind, article.get_title()) == False:
                print(threading.currentThread().getName() + "/" + str(thread_num),
                      datetime.datetime.now(), "Current:" + kind, "Page:", pn, "Title:" + article.get_title())
                insert(mysql, article.get_info_dict())
            else:
                print(threading.currentThread().getName() + "/" + str(thread_num),
                      datetime.datetime.now(), "Current:" + kind, "Page:", pn, "Title:" + article.get_title(),"already exist!")
        if status:
            print(threading.currentThread().getName() + "/" + str(thread_num), datetime.datetime.now(), kind, "Finish!")
            break
        else:
            pn += 1
            time.sleep(random.uniform(1.05, 3.08))


def main():
    global end_time, thread_num
    end_time = "2019-01-01 00:00:00"
    types = ["财经要闻", "宏观经济", "产经新闻", "金融市场", "公司新闻"]
    thread_num = len(types)

    thread_list = []
    for i in range(len(types)):
        thread_list.append(threading.Thread(target=spider, args=(types[i],), name=i))

    for t in thread_list:
        t.start()


if __name__ == '__main__':
    main()
