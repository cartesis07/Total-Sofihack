import numpy as np
import pandas as pd
import math

#PATHS

col_list = [' Date - Heure', ' Consommation (MW)', ' Thermique (MW)', ' Nucléaire (MW)', ' Eolien (MW)', ' Solaire (MW)', ' Hydraulique (MW)', ' Pompage (MW)', ' Bioénergies (MW)', ' Ech. physiques (MW)']

training_set = pd.read_csv('spread_final/combine/combined.csv',usecols=col_list)


#print(np.isnan(training_set.values.sum()))
#training_set.fillna(0, inplace=True)
#print(np.isnan(training_set.values.sum()))

print(training_set.head())

adjusted_training_set = training_set.groupby(' Date - Heure')[' Consommation (MW)', ' Thermique (MW)', ' Nucléaire (MW)', ' Eolien (MW)', ' Solaire (MW)', ' Hydraulique (MW)', ' Pompage (MW)', ' Bioénergies (MW)', ' Ech. physiques (MW)'].sum().reset_index()

print(adjusted_training_set.head())

adjusted_training_set.to_csv('combined_sum.csv',index=True)