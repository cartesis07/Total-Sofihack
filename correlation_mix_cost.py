import numpy as np
import pandas as pd
import math
import os
import matplotlib.pyplot as plt

#PATHS

input_path = "Hackathon_Data/input_file_csv.csv"
weather_path = "Hackathon_Data/Dataset/weather.csv"
mix_path = "Hackathon_Data/Dataset/mix.csv"
cost_path = "Hackathon_Data/Dataset/cost.csv"

folder_path = "Hackathon_Data/Dataset/Prediction1/mix1"

mixes = []

def computeMix(Thermique,Nucléaire,Eolien,Solaire,Hydraulique,Pompage,Bio):
    ER_sum = Eolien + Solaire + Hydraulique + Pompage + Bio
    ENR_sum = Thermique + Nucléaire
    if(ER_sum + ENR_sum == 0):
        return 0.5
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

        if filepath.endswith(".csv"):
            print (filepath)

avg = []
for i in range(len(mixes[1])):
    sum = 0
    for j in range(1,11):
        sum += mixes[j][i]
    if(sum <= 10 and sum >= 0):
        avg.append(sum/10)
    else:
        avg.append(0.5)

df2 = pd.read_csv("Hackathon_Data/Dataset/Prediction1/mix1/mix_28.csv")
df2["time"] = pd.to_datetime(df2[' Date - Heure'], format="%Y-%m-%dT%H:%M:%S")

mix_abscisse = df2["time"].tolist()

df3 = pd.read_csv("Hackathon_Data/Dataset/Prediction1/cost1.csv")
df3["time"] = pd.to_datetime(df3['date'], format="%d-%m-%y")

cost_abscisse = df3["time"].tolist()
cost_ord = df3["Spot"].tolist()

amin, amax = min(cost_ord), max(cost_ord)
for i, val in enumerate(cost_ord):
    cost_ord[i] = (val-amin) / (amax-amin)

plt.plot(mix_abscisse,avg)
plt.plot(cost_abscisse,cost_ord)
plt.show()
