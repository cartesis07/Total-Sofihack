#IMPORTS

import numpy as np
import pandas as pd
import os
import datetime

#PATHS

folder_path = "Hackathon_Data/Dataset/Prediction1/final_merge"

for subdir, dirs, files in os.walk(folder_path):
    for file in files:
        filepath = subdir + os.sep + file

        print(filepath)

        df = pd.read_csv(filepath)

        list = ['Unnamed: 0', 'Code INSEE région', ' Date', ' Heure', ' Date - Heure', ' Consommation (MW)', ' Thermique (MW)', ' Nucléaire (MW)', ' Eolien (MW)', ' Solaire (MW)', ' Hydraulique (MW)', ' Pompage (MW)', ' Bioénergies (MW)', ' Ech. physiques (MW)', 'time', 'Unnamed: 0.1', 'date', 'pmer', 'tend', 'cod_tend', 'dd', 'ff', 't', 'td', 'u', 'vv', 'ww', 'w1', 'w2', 'n', 'nbas', 'hbas', 'cl', 'cm', 'ch', 'pres', 'niv_bar', 'geop', 'tend24', 'tn12', 'tn24', 'tx12', 'tx24', 'tminsol', 'sw', 'tw', 'raf10', 'rafper', 'per', 'etat_sol', 'ht_neige', 'ssfrai', 'perssfrai', 'rr1', 'rr3', 'rr6', 'rr12', 'rr24', 'phenspe1', 'phenspe2', 'phenspe3', 'phenspe4', 'nnuage1', 'hnuage1', 'nnuage2', 'hnuage2', 'nnuage3', 'hnuage3', 'nnuage4', 'hnuage4', 'Unnamed: 59', 'Latitude', 'Longitude', 'Altitude']

        df = df[df['Altitude'].astype(bool)]

        df.to_csv('spread' + file)

        #SPREAD WEATHER

        last_row = 0
        for i in range(len(df)):
            if(last_row != 0 and np.isnan(df['Altitude'].values[i])):
                for j in range(17,len(list)):
                    df[list[j]].values[i] = df[list[j]].values[last_row]
            else :
                if(not np.isnan(df['Altitude'].values[i])):
                    last_row = i


        if filepath.endswith(".csv"):
            print (filepath)