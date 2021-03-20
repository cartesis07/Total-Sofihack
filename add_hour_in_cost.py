import numpy as np
import pandas as pd
import os
import datetime

path2 = "Hackathon_Data/Dataset/Prediction1/cost2.csv"

cost_df = pd.read_csv(path2)

print(cost_df.head())

cost_df.dropna()

cost_df['date'] = pd.to_datetime(cost_df['date'],format="%d-%m-%y")

cost_df['new_date'] = pd.Series(
    pd.date_range("01-01-19", periods=7335, freq="30min")
)

print(cost_df.head())

cost_df.to_csv('final_cost1.csv',index = True)
