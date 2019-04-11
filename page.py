#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"提取页面文章"

import article
import requests
import random
import time
import bs4
import re

headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

types = {"财经要闻": "today_list",
         "宏观经济": "cjzx_list",
         "产经新闻": "cjkx_list",
         "金融市场": "jrsc_list",
         "公司新闻": "fssgsxw_list"}


class Page(object):
    def __init__(self, kind, pn):
        self.__m_url = "http://m.10jqka.com.cn/"
        self.type = kind

        if types.get(kind):
            self.url = "http://news.10jqka.com.cn/" + types[kind] + "/index_" + str(pn) + ".shtml"
            self.__analize_page()
            self.articles = self.__get_all_article()

    def __analize_page(self):
        r = requests.get(self.url, headers=headers)
        if r.status_code == 403:
            time.sleep(1234)
            self.__analize_page()
        else:
            self.__soup = bs4.BeautifulSoup(r.content, "lxml", from_encoding=r.encoding)

    def __get_all_article(self):
        articles = []
        links = map(lambda x: re.sub("http://\\w+\\.10jqka.com\\.cn/", self.__m_url,
                                     x.get('href')), self.__soup.select(".arc-title > a"))
        i = 0
        while i < len(links):
            r = requests.get(links[i], headers=headers, allow_redirects=False)
            if r.status_code == 403:
                time.sleep(1234)
                continue
            try:
                articles.append(article.Article(self.type, r.content, r.encoding))
            except IndexError:
                pass
            finally:
                time.sleep(random.uniform(0.12, 0.36))
                i += 1
        return articles

    def get_articles(self):
        return self.articles
