import numpy as np
import pandas as pd
import math
import os
import matplotlib.pyplot as plt

#PATHS

folder_path = "Hackathon_Data/Dataset/Prediction1/mix1_régional"

mixes = []
names = []

def computeMix(Thermique,Nucléaire,Eolien,Solaire,Hydraulique,Pompage,Bio):
    ER_sum = Eolien + Solaire + Hydraulique + Pompage + Bio
    ENR_sum = Thermique + Nucléaire
    if(ER_sum + ENR_sum == 0):
        return 0
    if(ER_sum/(ER_sum + ENR_sum) <= 0 or ER_sum/(ER_sum + ENR_sum) >= 1):
        return 0
    else:
        return ER_sum/(ER_sum + ENR_sum)
    
for subdir, dirs, files in os.walk(folder_path):
    for file in files:
        filepath = subdir + os.sep + file

        df = pd.read_csv(filepath)
        df = df.replace(np.nan, 0)
        list = []
        for i in range(len(df)):
            mix = computeMix(df[' Thermique (MW)'].values[i],df[' Nucléaire (MW)'].values[i],df[' Eolien (MW)'].values[i],df[' Solaire (MW)'].values[i],df[' Hydraulique (MW)'].values[i],df[' Pompage (MW)'].values[i],df[' Bioénergies (MW)'].values[i])
            list.append(mix)
        
        mixes.append(list)
        names.append(filepath)

        if filepath.endswith(".csv"):
            print (filepath)

df2 = pd.read_csv("Hackathon_Data/Dataset/Prediction1/mix1/mix_28.csv")
df2["time"] = pd.to_datetime(df2[' Date - Heure'], format="%Y-%m-%dT%H:%M:%S")

mix_abscisse = df2["time"].tolist()

figure, axes = plt.subplots(nrows=2, ncols=2)

print(names)

#plt.plot(mix_abscisse,avg)
for i in range(0,4):
    if(i < 2):
        axes[0,i].plot(mix_abscisse,mixes[i])
    else:
        axes[1,i-2].plot(mix_abscisse,mixes[i])

figure.tight_layout()
figure.show()
plt.show()