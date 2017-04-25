# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 18:27:06 2017

@author: julio
"""

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor



#------------------------------------------------------------------------------
#Nessa parte fica os teste de desempenho
#Vamos começar com um teste simples
#Os inputes são arrays do numpy
def make_acuraccy_continuos(model,x,y):
    erro = 0
    for k in range(len(x)):
        tax = abs(model.predict([float(z) for z in x[k]]) - float(y[k]))
        erro += tax
    acuracy = (1 - erro/sum([float(d) for d in y]))
    return acuracy

#Esta função testa o algoritmo em varias profundidades
#Pode ser usado no CART e RF
def make_depth_test(x_train,y_train,x_test,y_test,max_depth_range=2,model="DTR"):
    if model == "DTR":
        model = DecisionTreeRegressor
    else:
        model = RandomForestRegressor
    
    texts = []
    for x in range(1,max_depth_range+1):
        clf = model(max_depth=x)
        clf.fit(x_train,y_train)
        texts.append(make_acuraccy_continuos(clf,x_test,y_test))
    return texts

#Essa função testa varias amostras para ser uma folha.
#ela ira analisar uma porcentagem de exemplos.
def make_min_samples_test(x_train,y_train,x_test,y_test,test_range=2,model="DTR" ):
     if model == "DTR":
        model = DecisionTreeRegressor
     else:
        model = RandomForestRegressor
     texts = []
     for x in range(2,test_range+1):
        clf = model(n_estimators=24,min_samples_split= float(x)/100)
        clf.fit(x_train,y_train)
        texts.append(make_acuraccy_continuos(clf,x_test,y_test))
     return texts

#Esta função é uzada para achar a melhor profundidade da arvore.
#Ainda em desenvolvimento
#Alerta: exige muito processamento.
def forest_size(x_train,y_train,x_test,y_test,test_range=2):
     texts = []
     for x in range(2,test_range+1):
        clf = RandomForestRegressor(n_estimators=x)
        clf.fit(x_train,y_train)
        texts.append(make_acuraccy_continuos(clf,x_test,y_test))
     return texts

#Essa é usada para acharmos a melhor quantidade de vizinhos.
#Exige bastante processamento.
def neighboars_text(x_train,y_train,x_test,y_test,test_range=2):
    texts = []
    for x in range(2,test_range+1):
        clf = KNeighborsRegressor(n_neighbors=x)
        clf.fit(x_train,y_train)
        texts.append(make_acuraccy_continuos(clf,x_test,y_test))
    return texts


def acharMaisBarato(x_test,y_test,model,tax=0.1):
    x_test,y_test = x_test.values,y_test.values
    pontos = []
    for x in range(len(x_test)):
        if (float(y_test[x]-model.predict(x_test[x])))/y_test[x] <= -tax:
            pontos.append(x_test[x])
    return pontos
        
    
    





