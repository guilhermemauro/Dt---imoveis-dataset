# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 18:17:28 2017

@author: julio
"""

import pandas as pd

#Aqui iremos trabalhar a abertura dos dados
#Iremos mandar a estrutura pronta para tratamento.
#Irei deixar aqui pois teremos que se comunicar com varias interfaces diferentes

#Uso essa classe para abrir de um file de um doc
#Essa classe ira almentar de acordo com a complexidade dos dados
class Loadfrom_doc(object):
    """Essa classe foi criada para abrir docs de csv.json,exel e etc.
       Favor usar a classe Loadfrom_db para acessar bancos de dados.
       Path: caminho do doc
       features_names: É o nome das colunas que sérão features/Atributos.
       doc= Tipo de documento por hora csv e json
       classes: As classe que serão usadas no treino.
       Esta função prepara para o tratamento
       """
    def __init__(self,path,features_names,doc='csv',classes=-1):
        self.path = path
        self.doc = doc
        self.classes = classes
        self.features_names = features_names
    def loadDataImoveis(self):
        df = pd.read_csv(self.path)
    
        return df[self.features_names],df[self.classes]
    




    
    
    


