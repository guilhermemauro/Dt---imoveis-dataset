#!/usr/bin/env python
# -*- coding: utf-8 -*-
from re import findall as fd
from re import sub
from bs4 import BeautifulSoup as bs
from requests import get
from PIL import Image
from StringIO import StringIO as sio
from pytesseract import image_to_string

class House_apart(object):
    def __init__(self, text, price, link=None, proxies=None):
        #self.text = text.text
        #self.price = price.text
        self.link = link
        self.proxies = proxies
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
        if self.link != None:
            page = get(self.link, proxies=self.proxies)
            content = bs(page.text, "html.parser")
            self.cep = fd("[0-9]{5}-[0-9]{3}", content.text)
            self.cep = sub("-", "", self.cep[0])
            return int(self.cep)
        else:
            return None
    def get_seller(self):
        if self.link != None:
            page= get(self.link, proxies=self.proxies)
            content = bs(page.text, "html.parser")
            self.seller_name = content.find("li", class_="item owner mb10px ")
            self.seller_contact = str(content.find("span", {"id":"visible_phone"}).img['src'])
            page = get("http:{}".format(self.seller_contact), proxies=self.proxies)
            self.seller_name = sub("\\n", "", self.seller_name.text)
            if page.status_code == 200:
                self.seller_contact = image_to_string(Image.open(sio(page.content)))
            else:
                self.seller_contact = None

            return str(self.seller_name), self.seller_contact
        else:
            return None
