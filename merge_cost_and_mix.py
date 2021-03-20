import numpy as np
import pandas as pd
import os
import datetime

path1 = "spread_final/combine/combined_sum.csv"
path2 = "spread_final/combine/final_cost1.csv"

col_sel = ['Spot','new_date']

df1 = pd.read_csv(path1)
df2 = pd.read_csv(path2,usecols=col_sel)

print(list(df1))
print(list(df2))

print(df1.head())
print(df2.head())

df1['time'] = pd.to_datetime(df1[' Date - Heure'], format="%Y-%m-%dT%H:%M:%S",errors='ignore', utc=True)
df2['time'] = pd.to_datetime(df2['new_date'],format="%Y-%m-%dT%H:%M:%S",errors='ignore', utc=True )

result = df2.merge(df1, how="inner", left_on="time", right_on="time")

print(result.head())

result.to_csv('merge_cost_mix_train.csv',index=False)