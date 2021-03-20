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

selection = ['Spot',' Consommation (MW)', ' Thermique (MW)', ' Nucléaire (MW)', ' Eolien (MW)', ' Solaire (MW)', ' Hydraulique (MW)', ' Pompage (MW)', ' Bioénergies (MW)', ' Ech. physiques (MW)']

training_set = pd.read_csv('spread_final/combine/merge_cost_mix_train.csv',usecols=selection)

print(np.isnan(training_set.values.sum()))
training_set.fillna(0, inplace=True)
print(np.isnan(training_set.values.sum()))

print(training_set.head())
print(list(training_set))

X = training_set.iloc[:, 1:10].values
y = training_set.iloc[:, 0].values

print(X)
print(y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

input_layer = keras.Input(shape=(X.shape[1],))
dense_layer_1 = layers.Dense(100, activation='relu')(input_layer)
dense_layer_2 = layers.Dense(50, activation='relu')(dense_layer_1)
dense_layer_3 = layers.Dense(25, activation='relu')(dense_layer_2)
output = layers.Dense(1)(dense_layer_3)

model = keras.Model(inputs=input_layer, outputs=output)
model.compile(loss="mean_squared_error" , optimizer="adam", metrics=["mean_squared_error"])

history = model.fit(X_train, y_train, batch_size=2, epochs=30, verbose=1, validation_split=0.2, validation_data=(X_test,y_test))

model.evaluate(X_test, y_test, verbose=1)