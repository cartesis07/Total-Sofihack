#IMPORTS

import pandas as pd
import numpy as np
from sklearn import datasets
import tensorflow as tf
import itertools
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from math import sqrt
from tensorflow import keras
from tensorflow.keras import layers
import math

col_list = [' Consommation (MW)', ' Thermique (MW)', ' Nucléaire (MW)', ' Eolien (MW)', ' Solaire (MW)', ' Hydraulique (MW)', ' Pompage (MW)', ' Bioénergies (MW)', ' Ech. physiques (MW)', 'pmer', 'tend', 'cod_tend', 'dd', 'ff', 'td', 'u', 'vv', 'ww', 'w1', 'w2', 'n', 'nbas', 'hbas', 'cl', 'cm', 'ch', 'pres', 'niv_bar', 'geop', 'tend24', 'tn12', 'tn24', 'tx12', 'tx24', 'tminsol', 'sw', 'tw', 'raf10', 'rafper', 'per', 'etat_sol', 'ht_neige', 'ssfrai', 'perssfrai', 'rr1', 'rr3', 'rr6', 'rr12', 'rr24', 'phenspe1', 'phenspe2', 'phenspe3', 'phenspe4', 'nnuage1', 'hnuage1', 'nnuage2', 'hnuage2', 'nnuage3', 'hnuage3', 'nnuage4', 'hnuage4', 'Unnamed: 59', 'Latitude', 'Longitude', 'Altitude']

training_set = pd.read_csv('spread_final/combine/combined.csv',usecols=col_list)

print(np.isnan(training_set.values.sum()))
training_set.fillna(0, inplace=True)
print(np.isnan(training_set.values.sum()))

X = training_set.iloc[:, 10:65].values
y = training_set.iloc[:, 0:10].values

print(X[0])
print(y[0])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

input_layer = keras.Input(shape=(X.shape[1],))
dense_layer_1 = layers.Dense(100, activation='relu')(input_layer)
dense_layer_2 = layers.Dense(50, activation='relu')(dense_layer_1)
dense_layer_3 = layers.Dense(25, activation='relu')(dense_layer_2)
output = layers.Dense(10)(dense_layer_3)

model = keras.Model(inputs=input_layer, outputs=output)
model.compile(loss="mean_squared_error" , optimizer="adam", metrics=["mean_squared_error","accuracy"])

history = model.fit(X_train, y_train, batch_size=2, epochs=1, verbose=1, validation_split=0.2, validation_data=(X_test,y_test))

model.evaluate(X_test, y_test, verbose=1)