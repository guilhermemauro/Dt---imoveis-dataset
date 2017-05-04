#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrape_olx import Paging
from scrape_olx.adtools import House_apart
import csv
from time import sleep

#prepara o arquivo CSV e escreve o cabeçalho
archive = open('apartamentos_JP_0.csv', 'wb')
file_ = csv.writer(archive, quoting=csv.QUOTE_ALL)
file_.writerow(['key','id_anuncio', 'quartos', 'condominio', 'tamanho', 'garagem', 'preco', 'cep', 'nome_contato', 'numero_contato'])
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
    for order_descr, order_price, order_link, id_ad in zip(descr_all, price_all, page.get_links(), page.get_ids()):
        #a classe House_apart() e criada com base em informacoes de anuncios do tipo VENDA DE IMOVEIS (ainda nao tratados)
        order = House_apart(order_descr, order_price, link=order_link)
        #o metodo clear_character() gera um dicionario com informacoes estruturadas sobre VENDA DE IMOVEIS
        temp_info = order.clear_character()
        # o metodo clear_price() retorna o valor limpo de caracteres especiais em tipo int
        # o metodo get_cep() recupera o cep do imovel limpo em tipo int
        seller, phone_seller = order.get_seller()
        file_.writerow([KEY, id_ad, temp_info["bedroom"],temp_info["condominium"],temp_info["size"],temp_info["garage"], order.clear_price(), order.get_cep(), seller, phone_seller])
        KEY += 1
    print "Abrindo pagina {}".format(n_page)
    page = Paging(LINK_TARGET+"?o={}".format(n_page))
    print "Pausa para evitar detecao de bot."
    sleep(3)
