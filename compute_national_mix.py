import numpy as np
import pandas as pd
import math
import os
import matplotlib.pyplot as plt

folder = "results_predicted/2019"

dfs = []

for subdir, dirs, files in os.walk(folder):
    for file in files:
        filepath = subdir + os.sep + file

        dfs.append(pd.read_csv(filepath))

total = dfs[0]

for i in range(1,7):
    total['predicted_# Consommation (MW)'] = total['predicted_# Consommation (MW)'] + dfs[i]['predicted_# Consommation (MW)']
    total['predicted_Bioénergies (MW)'] = total['predicted_Bioénergies (MW)'] + dfs[i]['predicted_Bioénergies (MW)']
    total['predicted_Ech. physiques (MW)'] = total['predicted_Ech. physiques (MW)'] + dfs[i]['predicted_Ech. physiques (MW)']
    total['predicted_Eolien (MW)'] = total['predicted_Eolien (MW)'] + dfs[i]['predicted_Eolien (MW)']
    total['predicted_Hydraulique (MW)'] = total['predicted_Hydraulique (MW)'] + dfs[i]['predicted_Hydraulique (MW)']
    total['predicted_Nucléaire (MW)'] = total['predicted_Nucléaire (MW)'] + dfs[i]['predicted_Nucléaire (MW)']
    total['predicted_Pompage (MW)'] = total['predicted_Pompage (MW)'] + dfs[i]['predicted_Pompage (MW)']
    total['predicted_Solaire (MW)'] = total['predicted_Solaire (MW)'] + dfs[i]['predicted_Solaire (MW)']
    total['predicted_Thermique (MW)'] = total['predicted_Thermique (MW)'] + dfs[i]['predicted_Thermique (MW)']

total.to_csv('results_predicted/2019/total_2019.csv')