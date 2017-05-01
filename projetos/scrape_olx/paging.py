#!/usr/bin/env python
# -*- coding: utf-8 -*-
from re import findall as fd
from re import sub
from bs4 import BeautifulSoup as bs
from requests import get


class Paging(object):
    def __new__(cls, link_target, proxies=None):
        if isinstance(link_target, str):
            return super(Paging, cls).__new__(cls)
        else:
            raise ValueError("link_target must be a string.")

    def __init__(self, link_target, proxies=None):
        self.link_target = link_target
        self.page = get(self.link_target, proxies=proxies)
        self.content = bs(self.page.text, "html.parser")
        self.list = self.content.find("ul", {"id":"main-ad-list"})
        self.current_page = int(self.content.find("li", class_="item number active").text)

    def get_links(self):
        self.list_links = []
        self.list_a_tags = self.list.find_all("a", class_="OLXad-list-link")
        for link in self.list_a_tags:
            self.list_links.append(str(link.get('href')))
        return self.list_links

    def get_ids(self):
        list_ids = []
        list_a_tags = self.list.find_all("a", class_="OLXad-list-link")
        for ids in list_a_tags:
            list_ids.append(int(ids.get('id')))
        return list_ids

    def get_titles(self):
        self.list_title = []
        for title in self.list.find_all("h3", class_="OLXad-list-title mb5px"):
            title = sub("\\t", "", title.text)
            title = sub("\\n", "", title)
            self.list_title.append(title)
        return self.list_title

    def descr_order_all(self):
        self.character = self.list.find_all("p", class_="text detail-specific mt5px")
        self.price = self.list.find_all("p",class_="OLXad-list-price")
        return self.character, self.price

    def number_pages(self):
        self.regex_get_number = "[0-9]+"
        self.a_tag = self.content.find('a', {'title': 'Última página'})
        self.link = self.a_tag.get('href')
        return int(fd(self.regex_get_number, self.link)[0])
