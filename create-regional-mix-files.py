import numpy as np
import pandas as pd
import math

#PATHS

input_path = "Hackathon_Data/input_file_csv.csv"
weather_path = "Hackathon_Data/Dataset/weather.csv"
mix_path = "Hackathon_Data/Dataset/mix.csv"
cost_path = "Hackathon_Data/Dataset/cost.csv"

#CREATING CSV FILES

col_list = ['Code INSEE région', 'Date', 'Heure', 'Date - Heure', 'Consommation (MW)', 'Thermique (MW)', 'Nucléaire (MW)', 'Eolien (MW)', 'Solaire (MW)', 'Hydraulique (MW)', 'Pompage (MW)', 'Bioénergies (MW)', 'Ech. physiques (MW)']

print("reading")
df = pd.read_csv(mix_path, usecols=col_list)
df.columns = col_list
print("sorting")
df = df.sort_values('Code INSEE région').set_index('Code INSEE région')
print("writing")
for key in df.index.unique():
    print(key)
    if(math.isnan(key) != True):
        df.loc[key].sort_values('Date - Heure').to_csv('%d.csv' % int(key), header=False)