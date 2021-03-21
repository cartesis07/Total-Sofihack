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
from keras import regularizers
import math
import os

col_list = [' Consommation (MW)', ' Thermique (MW)', ' Nucléaire (MW)', ' Eolien (MW)', ' Solaire (MW)', ' Hydraulique (MW)', ' Pompage (MW)', ' Bioénergies (MW)', ' Ech. physiques (MW)', 'pmer', 'tend', 'cod_tend', 'dd', 'ff', 'td', 'u', 'vv', 'ww', 'w1', 'w2', 'n', 'nbas', 'hbas', 'cl', 'cm', 'ch', 'pres', 'niv_bar', 'geop', 'tend24', 'tn12', 'tn24', 'tx12', 'tx24', 'tminsol', 'sw', 'tw', 'raf10', 'rafper', 'per', 'etat_sol', 'ht_neige', 'ssfrai', 'perssfrai', 'rr1', 'rr3', 'rr6', 'rr12', 'rr24', 'phenspe1', 'phenspe2', 'phenspe3', 'phenspe4', 'nnuage1', 'hnuage1', 'nnuage2', 'hnuage2', 'nnuage3', 'hnuage3', 'nnuage4', 'hnuage4', 'Unnamed: 59', 'Latitude', 'Longitude', 'Altitude']

inputs_list = ['pmer', 'tend', 'cod_tend', 'dd', 'ff', 'td', 'u', 'vv', 'ww', 'w1', 'w2', 'n', 'nbas', 'hbas', 'cl', 'cm', 'ch', 'pres', 'niv_bar', 'geop', 'tend24', 'tn12', 'tn24', 'tx12', 'tx24', 'tminsol', 'sw', 'tw', 'raf10', 'rafper', 'per', 'etat_sol', 'ht_neige', 'ssfrai', 'perssfrai', 'rr1', 'rr3', 'rr6', 'rr12', 'rr24', 'phenspe1', 'phenspe2', 'phenspe3', 'phenspe4', 'nnuage1', 'hnuage1', 'nnuage2', 'hnuage2', 'nnuage3', 'hnuage3', 'nnuage4', 'hnuage4', 'Unnamed: 59', 'Latitude', 'Longitude', 'Altitude']

training_set = pd.read_csv('spread_final/combine/combined.csv',usecols=col_list)

print(list(training_set))

sc = StandardScaler()
        
print(np.isnan(training_set.values.sum()))
training_set.fillna(0, inplace=True)
print(np.isnan(training_set.values.sum()))

X = training_set.iloc[:, 10:65].values
y = training_set.iloc[:, 0:9].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

print(X_train.shape)
print(y_train.shape)

X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

input_layer = keras.Input(shape=(X.shape[1],))
dense_layer_1 = layers.Dense(100, activation='relu')(input_layer)
dense_layer_2 = layers.Dense(50, activation='relu')(dense_layer_1)
dense_layer_3 = layers.Dense(25, activation='relu')(dense_layer_2)
output = layers.Dense(9)(dense_layer_3)

# input_layer = keras.Input(shape=(X.shape[1],))
# dense_layer_1 = layers.Dense(200, activation='relu', kernel_regularizer=regularizers.l2(), bias_regularizer=regularizers.l2())(input_layer)
# drop_out_layer_1 = layers.Dropout(0.5)(dense_layer_1)
# dense_layer_2 = layers.Dense(100, activation='relu', kernel_regularizer=regularizers.l2(), bias_regularizer=regularizers.l2())(drop_out_layer_1)
# drop_out_layer_2 = layers.Dropout(0.5)(dense_layer_2)
# dense_layer_3 = layers.Dense(50, activation='relu', kernel_regularizer=regularizers.l2(), bias_regularizer=regularizers.l2())(drop_out_layer_2)
# drop_out_layer_3 = layers.Dropout(0.5)(dense_layer_3)
# output = layers.Dense(9)(drop_out_layer_3)

model = keras.Model(inputs=input_layer, outputs=output)
model.compile(loss="mean_squared_error" , optimizer="adam", metrics=["mean_squared_error"])

history = model.fit(X_train, y_train, batch_size=2, epochs=100, verbose=1, validation_split=0.2, validation_data=(X_test,y_test))

model.evaluate(X_test, y_test, verbose=1)

# folder_2019 = "Hackathon_Data/Dataset/Prediction1/Inputs/2019"

# folder_2020 = "Hackathon_Data/Dataset/Prediction1/Inputs/2020"

# count = 0
# for subdir, dirs, files in os.walk(folder_2019):
#     for file in files:
#         count += 1
#         filepath = subdir + os.sep + file
#         tmp = pd.read_csv(filepath,usecols=inputs_list)
#         tmp_X = tmp.iloc[:, 0:55].values
#         tmp_X = sc.fit_transform(tmp_X)
#         pred = model.predict(tmp_X)
#         np.savetxt("Hackathon_Data/Dataset/Prediction2/Outputs/" + 'output' + file, pred, header="Consommation (MW),Thermique (MW),Nucléaire (MW),Eolien (MW),Solaire (MW),Hydraulique (MW),Pompage (MW),Bioénergies (MW),Ech. physiques (MW)", delimiter=',')

# count = 0
# for subdir, dirs, files in os.walk(folder_2020):
#     for file in files:
#         count += 1
#         filepath = subdir + os.sep + file
#         tmp = pd.read_csv(filepath,usecols=inputs_list)
#         tmp_X = tmp.iloc[:, 0:55].values
#         tmp_X = sc.fit_transform(tmp_X)
#         pred = model.predict(tmp_X)
#         np.savetxt("Hackathon_Data/Dataset/Prediction2/Outputs/" + "output" + file , pred, header="Consommation (MW),Thermique (MW),Nucléaire (MW),Eolien (MW),Solaire (MW),Hydraulique (MW),Pompage (MW),Bioénergies (MW),Ech. physiques (MW)", delimiter=',')
#         #with open("Hackathon_Data/Dataset/Prediction1/Outputs/2020/" + "pred" + str(count) + '.txt', 'w') as filehandle:
#         #    for listitem in pred:
#         #        filehandle.write('%s\n' % listitem)

