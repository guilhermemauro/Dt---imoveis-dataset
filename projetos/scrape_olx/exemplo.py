#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import requests, sys, re, csv
from scrape_olx import Paging, House_apart
from time import sleep

#prepara o arquivo CSV e escreve o cabeçalho
archive = open('apartamentos_JP_0.csv', 'wb')
file_ = csv.writer(archive, quoting=csv.QUOTE_ALL)
file_.writerow(['id', 'quartos', 'condominio', 'tamanho', 'garagem', 'preco', 'cep'])
KEY = 0

#Link do alvo para mineração
LINK_TARGET = "http://es.olx.com.br/norte-do-espirito-santo/vitoria/jardim-da-penha/imoveis/venda/apartamentos"

page = Paging(LINK_TARGET)
print "Abrindo pagina 1"


#o metodo number_pages() retorna o numero de paginas totais de resultados
for n_page in range(2, page.number_pages() + 1):
    print "Salvando dados..."
    #o metodo descr_all() retorna duas listas com a descricao e precos dos anuncios seguindo a ordem dos anuncios no site
    #o conteudo nao vem tratado, cada tipo de anuncio tem uma estrutura de descricao diferente
    descr_all, price_all = page.descr_order_all()
    # o metodo get_links() retorna a lista de links dos anuncios
    for order_descr, order_price, order_link in zip(descr_all, price_all, page.get_links()):
        #a classe House_apart() e criada com base em informacoes de anuncios do tipo VENDA DE IMOVEIS (ainda nao tratados)
        order = House_apart(order_descr, order_price, link=order_link)
        #o metodo clear_character() gera um dicionario com informacoes estruturadas sobre VENDA DE IMOVEIS
        temp_info = order.clear_character()
        # o metodo clear_price() retorna o valor limpo de caracteres especiais em tipo int
        # o metodo get_cep() recupera o cep do imovel limpo em tipo int
        file_.writerow([KEY, temp_info["bedroom"],temp_info["condominium"],temp_info["size"],temp_info["garage"], order.clear_price(), order.get_cep()])
        KEY += 1
    print "Abrindo pagina {}".format(n_page)
    page = Paging(LINK_TARGET+"?o={}".format(n_page))
    print "Pausa para evitar detecao de bot."
    sleep(3)
