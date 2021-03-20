import numpy as np
import pandas as pd
import math
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

inputs_path = "E:\\inputs"
outputs_path = "E:\\outputs"

headers = ['# Consommation (MW)', 'Thermique (MW)', 'Nucléaire (MW)', 'Eolien (MW)', 'Solaire (MW)', 'Hydraulique (MW)', 'Pompage (MW)', 'Bioénergies (MW)', 'Ech. physiques (MW)']
previous = ['date'] + headers

code_region = 52

inputs, outputs = [], []

for subdir, dirs, files in os.walk(inputs_path):
    for file in files:
        filepath = subdir + os.sep + file
        inputs.append(pd.read_csv(filepath, usecols=['CodeINSEE', 'date']))

i_df = pd.concat(inputs)
i_df.reset_index(drop=True, inplace=True)

for subdir, dirs, files in os.walk(outputs_path):
    for file in files:
        filepath = subdir + os.sep + file
        outputs.append(pd.read_csv(filepath))

o_df = pd.concat(outputs)
o_df.reset_index(drop=True, inplace=True)

df = pd.concat([i_df, o_df], axis=1).sort_values(by='date')

df = df[df['CodeINSEE'] == 52]

new_df = pd.DataFrame()
previous_val = dict.fromkeys(previous)
for index, row in df.iterrows():
    for p in previous:
        row['previous_' + p] = previous_val[p]
        if p != 'date' and previous_val[p] is not None:
            delta_time = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S') - datetime.strptime(row['previous_date'], '%Y-%m-%d %H:%M:%S')
            delta_time_sec = 24*3600*delta_time.days + delta_time.seconds
            row['reg_a_' + p] = (row[p] - row['previous_' + p]) / delta_time_sec
            row['reg_b_' + p] = row[p] - row['reg_a_' + p] * datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S').timestamp()
        else:
            row['reg_a_' + p] = 10**99
            row['reg_b_' + p] = 10**99
        previous_val[p] = row[p]
    new_df = new_df.append(row, ignore_index=True)

R = list(new_df.iterrows())

date_debut = datetime.strptime('2020-11-14 00:00:00', '%Y-%m-%d %H:%M:%S')
date_fin = datetime.strptime('2020-11-16 23:30:00', '%Y-%m-%d %H:%M:%S')

date_ar = [date_debut]
while date_ar[-1] != date_fin:
    date_ar.append(date_ar[-1] + timedelta(minutes=30))

result = pd.DataFrame()
current_row = 1
r_date = datetime.strptime(R[current_row][1]['date'], '%Y-%m-%d %H:%M:%S')
for d in date_ar:
    delta_time = d - r_date
    delta_time_sec = 24*3600*delta_time.days + delta_time.seconds
    while delta_time_sec > 0:
        current_row += 1
        r_date = datetime.strptime(R[current_row][1]['date'], '%Y-%m-%d %H:%M:%S')
        delta_time = d - r_date
        delta_time_sec = 24*3600*delta_time.days + delta_time.seconds
    result_line = pd.Series()
    result_line['date'] = d
    result_line['current_row'] = current_row
    for h in headers:
        a = R[current_row][1]['reg_a_' + h]
        b = R[current_row][1]['reg_b_' + h]
        t = d.timestamp()
        r = a*t+b
        result_line['predicted_' + h] = r
    result = result.append(result_line, ignore_index=True)

result.to_csv("E:\\mix_lin_" + str(code_region) + ".csv")
