import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Make numpy printouts easier to read.
np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

print(tf.__version__)

col_list = [' Consommation (MW)', ' Thermique (MW)', ' Nucléaire (MW)', ' Eolien (MW)', ' Solaire (MW)', ' Hydraulique (MW)', ' Pompage (MW)', ' Bioénergies (MW)', ' Ech. physiques (MW)', 'pmer', 'tend', 'cod_tend', 'dd', 'ff', 'td', 'u', 'vv', 'ww', 'w1', 'w2', 'n', 'nbas', 'hbas', 'cl', 'cm', 'ch', 'pres', 'niv_bar', 'geop', 'tend24', 'tn12', 'tn24', 'tx12', 'tx24', 'tminsol', 'sw', 'tw', 'raf10', 'rafper', 'per', 'etat_sol', 'ht_neige', 'ssfrai', 'perssfrai', 'rr1', 'rr3', 'rr6', 'rr12', 'rr24', 'phenspe1', 'phenspe2', 'phenspe3', 'phenspe4', 'nnuage1', 'hnuage1', 'nnuage2', 'hnuage2', 'nnuage3', 'hnuage3', 'nnuage4', 'hnuage4', 'Unnamed: 59', 'Latitude', 'Longitude', 'Altitude']

dataset = pd.read_csv('spread_final/combine/combined.csv',usecols=col_list)

dataset.fillna(0)

print(dataset.head())

train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

print(list(dataset))

print(list(dataset.dtypes))

#sns.pairplot(train_dataset[['Altitude', 'td', 'dd', 'pmer']], diag_kind='kde')
#plt.show()

train_features = train_dataset.copy()
test_features = test_dataset.copy()

train_labels = train_features.pop(' Thermique (MW)')
test_labels = test_features.pop(' Thermique (MW)')

train_dataset.describe().transpose()[['mean', 'std']]

influence = np.array(train_features[' Nucléaire (MW)'])
print(np.shape(influence))

influence_normalizer = preprocessing.Normalization(input_shape=[1,])
influence_normalizer.adapt(influence)

influence_model = tf.keras.Sequential([
    influence_normalizer,
    layers.Dense(units=1)
])

influence_model.summary()

print(influence_model.predict(influence[:10]))

influence_model.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.1),
    loss='mean_absolute_error')

history = influence_model.fit(
    train_features[' Nucléaire (MW)'], train_labels,
    epochs=100,
    # suppress logging
    verbose=0,
    # Calculate validation results on 20% of the training data
    validation_split = 0.2)