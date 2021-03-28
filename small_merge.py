import numpy as np
import pandas as pd

df = pd.read_csv("Hackathon_Data/Dataset/Prediction1/weather1_selec/selectionnewweather_24.csv")

df = df.fillna(0)

df['time'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S", errors='ignore', utc=True)

#df = df.reset_index(drop=True, inplace=True)
df = df.loc[~df.index.duplicated()]
df = df.set_index("time")

df2 = pd.read_csv("Hackathon_Data/Dataset/Prediction1/mix1/mix_11.csv")

df2 = df2.fillna(0)

df2["time"] = pd.to_datetime(df2['Date - Heure'], format="%Y-%m-%dT%H:%M:%S", errors='ignore', utc=True)

#df2 = df2.reset_index(drop=True, inplace=True)
df2 = df2.loc[~df2.index.duplicated()]
df2 = df2.set_index("time")

result = pd.concat([df2, df], axis=1, join='outer')

result.to_csv('very_test.csv')