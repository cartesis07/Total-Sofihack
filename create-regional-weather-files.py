import numpy as np
import pandas as pd
import math

#PATHS

input_path = "Hackathon_Data/input_file_csv.csv"
weather_path = "Hackathon_Data/Dataset/weather.csv"
mix_path = "Hackathon_Data/Dataset/mix.csv"
cost_path = "Hackathon_Data/Dataset/cost.csv"

new_weather_path = "Hackathon_Data/Dataset/weather+code.csv"

#CREATING CSV FILES

df = pd.read_csv(new_weather_path)

df.sort_values('date', inplace=True)
df.drop_duplicates(subset=["date"], keep = 'last', inplace = True)

print("sorting")
df = df.sort_values('Code INSEE').set_index('Code INSEE')
print("writing")
for key in df.index.unique():
    print(key)
    if(math.isnan(key) != True):
        df.loc[key].sort_values('date').to_csv('%d.csv' % int(key), header=False)