#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"提取页面文章"

import article
import requests
import bs4
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}

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
        self.__soup = bs4.BeautifulSoup(r.text, "lxml")

    def __get_all_article(self):
        articles = []
        links = map(lambda x: re.sub("http://\\w+\\.10jqka.com\\.cn/", self.__m_url,
                                     x.get('href')), self.__soup.select(".arc-title > a"))
        for link in links:
            r = requests.get(link, headers=headers, allow_redirects=False)
            try:
                articles.append(article.Article(self.type, r.text))
            except IndexError:
                pass
        return articles

    def get_articles(self):
        return self.articles
