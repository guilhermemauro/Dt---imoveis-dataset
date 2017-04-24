#!/usr/bin/env python
# -*- coding: utf-8 -*-
from re import findall as fd
from re import sub
from bs4 import BeautifulSoup as bs
from requests import get


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
