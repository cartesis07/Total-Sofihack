import numpy as np
import pandas as pd
import math
import os
import matplotlib.pyplot as plt

folder = "merged_mix_predicted/2019"

dfs = []

for subdir, dirs, files in os.walk(folder):
    for file in files:
        filepath = subdir + os.sep + file
        dfs.append(pd.read_csv(filepath))

total = dfs[0]

for i in range(1,7):
    total['date'] = dfs[i]['date']
    total['# Consommation (MW)'] = total['# Consommation (MW)'] + dfs[i]['# Consommation (MW)']
    total['Bioénergies (MW)'] = total['Bioénergies (MW)'] + dfs[i]['Bioénergies (MW)']
    total['Ech. physiques (MW)'] = total['Ech. physiques (MW)'] + dfs[i]['Ech. physiques (MW)']
    total['Eolien (MW)'] = total['Eolien (MW)'] + dfs[i]['Eolien (MW)']
    total['Hydraulique (MW)'] = total['Hydraulique (MW)'] + dfs[i]['Hydraulique (MW)']
    total['Nucléaire (MW)'] = total['Nucléaire (MW)'] + dfs[i]['Nucléaire (MW)']
    total['Pompage (MW)'] = total['Pompage (MW)'] + dfs[i]['Pompage (MW)']
    total['Solaire (MW)'] = total['Solaire (MW)'] + dfs[i]['Solaire (MW)']
    total['Thermique (MW)'] = total['Thermique (MW)'] + dfs[i]['Thermique (MW)']

total['mix'] = (total['Eolien (MW)'] + total['Solaire (MW)'] + total['Hydraulique (MW)'] - total['Pompage (MW)']) / (total['Thermique (MW)'] + total['Nucléaire (MW)'] + total['Eolien (MW)'] + total['Solaire (MW)'] + total['Hydraulique (MW)'] - total['Pompage (MW)'])

total.to_csv('cost_predicted/total_2019.csv')