#!/usr/bin/env python
# -*- coding: utf-8 -*-
from re import findall as fd
from re import sub
from bs4 import BeautifulSoup as bs
from requests import get


class Paging(object):
    def __new__(cls, link_target):
        if isinstance(link_target, str):
            return super(Paging, cls).__new__(cls)
        else:
            raise ValueError("link_target must be a string.")

    def __init__(self, link_target):
        self.link_target = link_target
        self.page = get(self.link_target)
        self.content = bs(self.page.text, "html.parser")
        self.list = self.content.find("ul", {"id":"main-ad-list"})

    def get_links(self):
        self.list_links = []
        self.list_a_tags = self.list.find_all("a", class_="OLXad-list-link")
        for link in self.list_a_tags:
            self.list_links.append(str(link.get('href')))
        return self.list_links

    def descr_order_all(self):
        self.character = self.list.find_all("p", class_="text detail-specific mt5px")
        self.price = self.list.find_all("p",class_="OLXad-list-price")
        return self.character, self.price

    def number_pages(self):
        self.regex_get_number = "[0-9]+"
        self.a_tag = self.content.find('a', {'title': 'Última página'})
        self.link = self.a_tag.get('href')
        return int(fd(self.regex_get_number, self.link)[0])


class House_apart(object):
    def __init__(self, text, price, link=None):
        self.text = text.text
        self.price = price.text
        self.link = link
        self.regex_list = {"bedroom":"[0-9]+ q", "size":"[0-9]+ m", "condominium":"\$ [0-9]+", "garage":"[0-9]+ v"}
        self.regex_sub_list = {"bedroom": " q", "size":" m", "condominium":"\$ ", "garage":" v"}
        self.regex_price = ["R\$ ", "\."]

    def clear_character(self):
        self.list_to_return = {}
        for regex in self.regex_list:
            temp_value = fd(self.regex_list[regex], self.text)
            if temp_value != []:
                temp_value = sub(self.regex_sub_list[regex], "", temp_value[0])
                self.list_to_return[regex] = int(temp_value)
            else:
                self.list_to_return[regex] = None
        return self.list_to_return

    def clear_price(self):
        for regex in self.regex_price:
            self.price = sub(regex, "", self.price)
        return int(self.price)

    def get_cep(self):
        if self.link:
            page = get(self.link)
            content = bs(page.text, "html.parser")
            self.cep = fd("[0-9]{5}-[0-9]{3}", content.text)
            self.cep = sub("-", "", self.cep[0])
            return int(self.cep)
        else:
            return None
