#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"提取文章信息"

import bs4
import re


class Article():
    def __init__(self, kind, text, encoding):
        self.__soup = bs4.BeautifulSoup(text, "lxml", from_encoding=encoding)
        self.type = kind
        self.title = self.get_title()
        self.content = self.get_content()
        self.time = self.get_time()

    def get_time(self):
        return re.sub(r'[^\d\-:\s]+', "", self.__soup.select(".date")[0].text.replace("\xa0", "")).strip()

    def get_title(self):
        return self.__soup.select("#articleTitle")[0].text

    def get_content(self):
        return self.__soup.select(".page_content")[0].text.replace("\u3000", "").strip()

    def get_info_dict(self):
        return {'type': self.type, 'title': self.title, 'content': self.content, 'time': self.time}
