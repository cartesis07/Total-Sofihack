import numpy as np
import pandas as pd
import math
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

headers = ['# Consommation (MW)', 'Thermique (MW)', 'Nucléaire (MW)', 'Eolien (MW)', 'Solaire (MW)', 'Hydraulique (MW)', 'Pompage (MW)', 'Bioénergies (MW)', 'Ech. physiques (MW)']
previous = ['date'] + headers

for subdir, dirs, files in os.walk('mix_predicted/2019'):
    for file in files:
        filepath = subdir + os.sep + file
        result = pd.read_csv(filepath)

        result['mix'] = (result['Eolien (MW)'] + result['Solaire (MW)'] + result['Hydraulique (MW)'] - result['Pompage (MW)']) / (result['Thermique (MW)'] + result['Nucléaire (MW)'] + result['Eolien (MW)'] + result['Solaire (MW)'] + result['Hydraulique (MW)'] - result['Pompage (MW)'])

        #result['date'] = pd.date_range(start='2020-11-14',end='2020-11-17', freq='30min', closed='left')

        result['date'] = pd.date_range(start='2019-07-04',end='2019-07-07', freq='30min', closed='left')

        result.to_csv("merged_mix_predicted/2019/" + file + ".csv")