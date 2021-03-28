import numpy as np
import pandas as pd
import math
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

inputs_path = "Hackathon_Data/Dataset/Prediction2/Inputs"

headers = ['pmer', 'tend', 'cod_tend', 'dd', 'ff', 'td', 'u', 'vv', 'ww', 'w1', 'w2', 'n', 'nbas', 'hbas', 'cl', 'cm', 'ch', 'pres', 'niv_bar', 'geop', 'tend24', 'tn12', 'tn24', 'tx12', 'tx24', 'tminsol', 'sw', 'tw', 'raf10', 'rafper', 'per', 'etat_sol', 'ht_neige', 'ssfrai', 'perssfrai', 'rr1', 'rr3', 'rr6', 'rr12', 'rr24', 'phenspe1', 'phenspe2', 'phenspe3', 'phenspe4', 'nnuage1', 'hnuage1', 'nnuage2', 'hnuage2', 'nnuage3', 'hnuage3', 'nnuage4', 'hnuage4', 'Unnamed: 59']
previous = ['date'] + headers

code_region = 84

inputs, outputs = [], []

for subdir, dirs, files in os.walk(inputs_path):
    for file in files:
        filepath = subdir + os.sep + file
        inputs.append(pd.read_csv(filepath, usecols=['CodeINSEE', 'date']))

        new_file_path = "Hackathon_Data/Dataset/Prediction4/Inputs/" + file[0:14] + "_input.csv"
        outputs.append(pd.read_csv(new_file_path,usecols=headers))

#pd.concat([df1, df2], axis=1)

i_df = pd.concat(inputs)
i_df.reset_index(drop=True, inplace=True)

o_df = pd.concat(outputs)
o_df.reset_index(drop=True, inplace=True)

df = pd.concat([i_df, o_df], axis=1).sort_values(by='date')

print(df.head())

df = df[df['CodeINSEE'] == code_region]

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

date_debut = datetime.strptime('2019-07-04 00:00:00', '%Y-%m-%d %H:%M:%S')
date_fin = datetime.strptime('2019-07-06 23:30:00', '%Y-%m-%d %H:%M:%S')
# date_debut = datetime.strptime('2020-11-14 00:00:00', '%Y-%m-%d %H:%M:%S')
# date_fin = datetime.strptime('2020-11-16 23:30:00', '%Y-%m-%d %H:%M:%S')

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
    for h in headers:
        a = R[current_row][1]['reg_a_' + h]
        b = R[current_row][1]['reg_b_' + h]
        t = d.timestamp()
        r = a*t+b
        result_line['predicted_' + h] = r
    result = result.append(result_line, ignore_index=True)

#result['mix'] = (result['predicted_Eolien (MW)'] + result['predicted_Solaire (MW)'] + result['predicted_Hydraulique (MW)'] - result['predicted_Pompage (MW)']) / (result['predicted_Thermique (MW)'] + result['predicted_Nucléaire (MW)'] + result['predicted_Eolien (MW)'] + result['predicted_Solaire (MW)'] + result['predicted_Hydraulique (MW)'] - result['predicted_Pompage (MW)'])

result = result[['date','predicted_pmer', 'predicted_tend', 'predicted_cod_tend', 'predicted_dd', 'predicted_ff', 'predicted_td', 'predicted_u', 'predicted_vv', 'predicted_ww', 'predicted_w1', 'predicted_w2', 'predicted_n', 'predicted_nbas', 'predicted_hbas', 'predicted_cl', 'predicted_cm', 'predicted_ch', 'predicted_pres', 'predicted_niv_bar', 'predicted_geop', 'predicted_tend24', 'predicted_tn12', 'predicted_tn24', 'predicted_tx12', 'predicted_tx24', 'predicted_tminsol', 'predicted_sw', 'predicted_tw', 'predicted_raf10', 'predicted_rafper', 'predicted_per', 'predicted_etat_sol', 'predicted_ht_neige', 'predicted_ssfrai', 'predicted_perssfrai', 'predicted_rr1', 'predicted_rr3', 'predicted_rr6', 'predicted_rr12', 'predicted_rr24', 'predicted_phenspe1', 'predicted_phenspe2', 'predicted_phenspe3', 'predicted_phenspe4', 'predicted_nnuage1', 'predicted_hnuage1', 'predicted_nnuage2', 'predicted_hnuage2', 'predicted_nnuage3', 'predicted_hnuage3', 'predicted_nnuage4', 'predicted_hnuage4', 'predicted_Unnamed: 59']]

result.fillna(0)

result.to_csv("weather_predicted/2019/" + str(code_region) + "_2019" + ".csv")