# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 18:27:06 2017

@author: julio
"""

import pandas as pd
import numpy as np
import csv
from sklearn.tree import DecisionTreeRegressor
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
#------------------------------------------------------
#Abertura e tratamento de arquivo
with open("C:/Datasets/Apartamentos/apartamentos_JC.csv") as fille:
    data = csv.reader(fille)

    features = data.next()[1:-1]

    x_data,y_data = [],[]
    for x in data:
        x_data.append(x[1:-1])
        y_data.append(x[-1])
    x_data = np.array(x_data)
    y_data = np.array(y_data)

#----------------------------------------------------    
#A partir daqui iremos preparar os dados para o algoritmo e analise

#Aqui se lida com a quantidade de quartos.
#Substitui pela média
x_data[x_data[:,0] == '',0] = np.mean([float(x) for x in x_data[:,0] if x != ''])


#Aqui lido com condominios
#Bolei uma maneira de lidar com falta de tamanho

#Primeiro irei separar o df de acordo com o número de quartos
#A hipotese é simples mais quarto mais area.
um_q = x_data[x_data[:,0] == "1"]
dois_q = x_data[x_data[:,0] == "2"]
tres_q = x_data[x_data[:,0] == "3"]
quatro_q = x_data[x_data[:,0] == "4"]
cinco_q = x_data[x_data[:,0] == "5"]

#Irei criar uma função para essa tarefa.
#É so uma função paliativa
def de_acordo_c_quartos(data):
    data = list(data)
    for x in range(len(data)):
        if data[x][0] == '1':
            data[x][2] = np.mean([float(y[2]) for y in um_q if y[2] != ''])
        if data[x][0] == '2':
            data[x][2] = np.mean([float(y[2]) for y in dois_q if y[2] != ''])
        if data[x][0] == '3':
            data[x][2] = np.mean([float(y[2]) for y in tres_q if y[2] != ''])
        if data[x][0] == '4':
            data[x][2] = np.mean([float(y[2]) for y in quatro_q if y[2] != ''])
        if data[x][0] == '5':
            data[x][2] = np.mean([float(y[2]) for y in cinco_q if y[2] != ''])
    return np.array(data)

#feito isso vamos passar os novos valores        
x_data[x_data[:,2] == ''] = de_acordo_c_quartos(x_data[x_data[:,2] == ''])            

#Aqui lidei com o condominio
#Usei a média para lidar com os valores
x_data[x_data[:,1] == '',1] = np.mean([float(x) for x in x_data[:,1] if x != ''])

#Aqui com o garagem
#substituo pela médiana
x_data[x_data[:,3] == '',3] = np.median([float(x) for x in x_data[:,3] if x != ''])


#Vamos preparar o conjunto de teste e de treino

x_train,x_test,y_train,y_test = train_test_split(x_data,y_data,test_size=0.25,
                                                 random_state=33)

df = pd.DataFrame(x_data,columns=features)

#--------------------------------------------------
#A partir daqui iremos aplicar os Modelos.
# A ideia é usar uma Decision tree junto com KNN.
# Irei fazer um Ensembler para regressão.
# Se você esta lendo isso Deus tenha piedade de sua Alma.

#Começamos com uma CART trabalhei algumas funções para achar boms paramentros
#Fiz algumas funções para lidar com elas em teste de desempenho.
clf = DecisionTreeRegressor(max_depth = 4,criterion="mae",max_features = 4,
                            min_samples_split=40,min_samples_leaf=0.009,
                            splitter="best")
clf.fit(x_train,y_train)

#Cria um Random forest.
#tem funções para lidar em teste de desempenho
forest = RandomForestRegressor(n_estimators=24,criterion="mae",max_depth=4)
forest.fit(x_train,y_train)



#------------------------------------------------------------------------------
#Nessa parte fica os teste de desempenho
#Vamos começar com um teste simples
def make_acuraccy(clf,x,y):
    erro = 0
    for k in range(len(x)):
        tax = abs(clf.predict(x[k])[0] - float(y[k]))
        erro += tax
    acuracy = (1 - erro/sum([float(d) for d in y]))
    return acuracy

#Esta função testa o algoritmo em varias profundidades
#Pode ser usado no CART e RF
def make_depth_test(x_train,y_train,x_test,y_test,max_depth_range=2,model="DTR"):
    if model == "DTR":
        function = DecisionTreeRegressor
    else:
        function = RandomForestRegressor
    
    texts = []
    for x in range(1,max_depth_range+1):
        clf = function(max_depth=x)
        clf.fit(x_train,y_train)
        texts.append(make_acuraccy(clf,x_test,y_test))
    return texts

#Essa função testa varias amostras para ser uma folha.
#ela ira analisar uma porcentagem de exemplos.
def make_min_samples_test(x_train,y_train,x_test,y_test,test_range=2):
    texts = []
    for x in range(2,test_range+1):
        clf = DecisionTreeRegressor(min_samples_split= float(x)/100)
        clf.fit(x_train,y_train)
        texts.append(make_acuraccy(clf,x_test,y_test))
    return texts

#Esta função é uzada para achar a melhor profundidade da arvore.
#Ainda em desenvolvimento
#Alerta: exige muito processamento.
def forest_size(x_train,y_train,x_test,y_test,test_range=2):
     texts = []
     for x in range(2,test_range+1):
        clf = RandomForestRegressor(n_estimators=x)
        clf.fit(x_train,y_train)
        texts.append(make_acuraccy(clf,x_test,y_test))
     return texts
    




#------------------------------------------------------------------------------
#Nessa parte irei trabalhar alguns plotes.

tree_ac = make_acuraccy(clf,x_test,y_test)
#forest_ac = make_acuraccy(forest,x_test,y_test)

forest_deth = make_depth_test(x_train,y_train,x_test,y_test,100,model="RF")



#min_sample_tree = make_min_samples_test(x_train,y_train,x_test,y_test,test_range=100)








