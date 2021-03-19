#IMPORTS

import os
import datetime

import IPython
import IPython.display
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf

#PATHS

input_path = "Hackathon_Data/input_file_csv.csv"
weather_path = "Hackathon_Data/Dataset/weather.csv"
mix_path = "Hackathon_Data/Dataset/mix.csv"
cost_path = "Hackathon_Data/Dataset/cost.csv"

#READ INPUTS

col_list = ['Code INSEE région', 'Région', 'Date', 'Heure', 'Date - Heure', 'Consommation (MW)', 'Thermique (MW)', 'Nucléaire (MW)', 'Eolien (MW)', 'Solaire (MW)', 'Hydraulique (MW)', 'Pompage (MW)', 'Bioénergies (MW)', 'Ech. physiques (MW)']

mix_data = pd.read_csv(mix_path, usecols=col_list) 
mix_data = mix_data.sort_values(by=['Région'])
print(mix_data.head())
print(list(mix_data))

#deleting useless lines ?
#mix_data = mix_data[mix_data['Thermique (MW)'].notna()]
#print(mix_data.head())

mix_data = mix_data.loc[mix_data['Région'] == 'Ile-de-France']
mix_data = mix_data.dropna()

mix_data = mix_data[~(mix_data['Date'] < '2019-07-04')]

#date_time = pd.to_datetime(mix_data.pop('Date - Heure'), format='%Y-%m-%dT%H:%M:%S')

column_indices = {name: i for i, name in enumerate(mix_data.columns)}

n = len(mix_data)
train_mix = mix_data[0:int(n*0.7)]
val_mix = mix_data[int(n*0.7):int(n*0.9)]
test_mix = mix_data[int(n*0.9):]

num_features = mix_data.shape[1]

#NORMALIZATION
train_mean = train_mix.mean()
train_std = train_mix.std()

train_mix = (train_mix - train_mean) / train_std
val_mix = (val_mix - train_mean) / train_std
test_mix = (test_mix - train_mean) / train_std

#print(mix_data.describe().transpose())

#print(date_time.head())

#df.loc[df[‘Color’]== ‘Green’]

class WindowGenerator():
  def __init__(self, input_width, label_width, shift,
               train_df=train_df, val_df=val_df, test_df=test_df,
               label_columns=None):
    # Store the raw data.
    self.train_df = train_df
    self.val_df = val_df
    self.test_df = test_df

    # Work out the label column indices.
    self.label_columns = label_columns
    if label_columns is not None:
      self.label_columns_indices = {name: i for i, name in
                                    enumerate(label_columns)}
    self.column_indices = {name: i for i, name in
                           enumerate(train_df.columns)}

    # Work out the window parameters.
    self.input_width = input_width
    self.label_width = label_width
    self.shift = shift

    self.total_window_size = input_width + shift

    self.input_slice = slice(0, input_width)
    self.input_indices = np.arange(self.total_window_size)[self.input_slice]

    self.label_start = self.total_window_size - self.label_width
    self.labels_slice = slice(self.label_start, None)
    self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

  def __repr__(self):
    return '\n'.join([
        f'Total window size: {self.total_window_size}',
        f'Input indices: {self.input_indices}',
        f'Label indices: {self.label_indices}',
        f'Label column name(s): {self.label_columns}'])