# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 19:18:57 2017

@author: julio
"""

from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import train_test_split
from recebimento import Loadfrom_doc
import matplotlib.pyplot as plt
from Analise import acharMaisBarato


#A partir daqui iremos preparar os dados para o algoritmo e analise
#Aqui os dados irão sofrer uma transformação por isso uso numpy.
#Essa é a pasta que sofrera maior número de transformações no decorre do processo.

#Essa classe lida com varios tipos de documentos.


data = Loadfrom_doc("C:/Datasets/Apartamentos/apartamentos_JP_0.csv",
features_names=['quartos','condominio','tamanho','garagem','cep'],classes='preco')

x_data,y_data = data.loadDataImoveis()

#Aqui se lida com a quantidade de quartos.
#Substitui pela moda
x_data["quartos"] = x_data["quartos"].fillna(x_data["quartos"].median())

#Aqui lidarei com os valores esquecidos do condominio
#Substituirei pele média
x_data["condominio"] =  x_data["condominio"].fillna(x_data["condominio"].mean())

#Aqui lido com os valores esquicidos do tamanho
#Substituo pela média
x_data["tamanho"] = x_data["tamanho"].fillna(x_data["tamanho"].mean())

#Aqui lido com a garagem.
#Irei substituir por 0 pois presumo que não tenha.
x_data["garagem"] = x_data["garagem"].fillna(0)


x_train,x_test,y_train,y_test = train_test_split(x_data,y_data,test_size=0.25,
                                                 random_state=33)



#-----------------------------------------------------------------------
#----------------------------------------------------------------------


#A partir daqui iremos aplicar os Modelos.
# A ideia é usar uma Decision tree junto com KNN.
# Irei fazer um Ensembler para regressão.
# Se você esta lendo isso Deus tenha piedade de sua Alma.

#Começamos com uma CART trabalhei algumas funções para achar boms paramentros
#Fiz algumas funções para lidar com elas em teste de desempenho.

#      ____Decision trees based methods______

#Treinamos uma DTR basica.
clf = DecisionTreeRegressor(max_depth = 4,criterion="mae",max_features = 4,
                            min_samples_split=40,min_samples_leaf=0.09,
                            splitter="best")
clf.fit(x_train,y_train)

#Cria um Random forest regressor.
#tem funções para lidar em teste de desempenho
forest = RandomForestRegressor(n_estimators=24,criterion="mae",max_depth=6,min_samples_leaf=0.01)
forest.fit(x_train,y_train)


#       _______Neighboars based methods________
#Criar um KNNrefressor.
knn = KNeighborsRegressor(n_neighbors=11,weights='distance')
knn.fit(x_train,y_train)





fig = plt.figure(313)

fig.add_subplot(311)
plt.scatter(range(len(y_test)),y_test)
plt.plot(range(len(x_test)),clf.predict(x_test))
plt.legend(["Regressao da arvore"])

fig.add_subplot(312)
plt.scatter(range(len(y_test)),y_test)
plt.plot(range(len(x_test)),forest.predict(x_test))
plt.legend(["Regressao do Random Forest"])

fig.add_subplot(313)
plt.scatter(range(len(y_test)),y_test)
plt.plot(range(len(x_test)),knn.predict(x_test))
plt.legend(["Regressao do knn"])

a = acharMaisBarato(x_test,y_test,forest,0.1)










