#IMPORTS

import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import pandas as pd 

import datetime as dt
import pytz

import math
import random as rd

from pyproj import Transformer

input_path = "Hackathon_Data/ultra_csv.csv"
to_submit = "Hackathon_Data/to_submit_csv.csv"
predicted_folder = "results_predicted/ULTIMATE_COST"

def ceil_dt(dt, delta):
    return dt + (dt.min - dt) % delta

input_data = pd.read_csv(input_path) 
to_submit = pd.DataFrame(columns=['id_voiture ', 'charge_plan'])
print(input_data.head())
print(list(input_data))

for i in range(30):
    window = []

    id = input_data['id_voiture '].values[i]
    current_charge = input_data[' %_charge '].values[i]
    charge_speed = input_data[' vitesse_charge (%/min)'].values[i]
    lambda_mix = input_data[' %_mix_energetique '].values[i]
    lambda_cost = input_data[' %_cout_elec '].values[i]

    # Time conversion
    timezone = pytz.timezone('Europe/Paris')

    start_str = input_data['Past_date'].values[i]
    start_obj = dt.datetime.strptime(start_str, '%d-%m-%Y _ %H:%M:%S')
    timezone_start_obj = timezone.localize(start_obj)

    stop_str = input_data[' dateheure_Previs_stop '].values[i]
    stop_obj = dt.datetime.strptime(stop_str, '%d-%m-%Y _ %H:%M:%S')
    timezone_stop_obj = timezone.localize(stop_obj)

    duration = math.ceil( (timezone_stop_obj - timezone_start_obj).total_seconds() / 1800 )

    corrected_str = input_data[' dateheure_plug '].values[i]
    corrected_obj = dt.datetime.strptime(corrected_str, '%d-%m-%Y _ %H:%M:%S')
    timezone_corrected_obj = timezone.localize(corrected_obj)

    tweak = math.ceil( (timezone_corrected_obj - timezone_start_obj).total_seconds() / 3600 )

    current_charge += ((timezone_corrected_obj - timezone_start_obj).total_seconds() / 3600) * charge_speed

    input_len = duration - tweak

    region = input_data['Code INSEE 2'].values[i]

    #handle IDF case
    if(region == 24 or region == 11 or region == 75):
        mix_path = "group_predicted/" + str(timezone_start_obj.year)  + "/24_" + str(timezone_start_obj.year) + ".csv"
        region_mix = pd.read_csv(mix_path,usecols=['date','mix'])

    if(region == 84 or region == 76 or region == 93):
        mix_path = "group_predicted/" + str(timezone_start_obj.year)  + "/84_" + str(timezone_start_obj.year) + ".csv"
        region_mix = pd.read_csv(mix_path,usecols=['date','mix'])

    if(region == 52 or region == 53 or region == 28):
        mix_path = "group_predicted/" + str(timezone_start_obj.year)  + "/52_" + str(timezone_start_obj.year) + ".csv"
        region_mix = pd.read_csv(mix_path,usecols=['date','mix'])

    if(region != 11 and region != 93):
        adjustement_mix = pd.read_csv("results_predicted/total_" + str(timezone_start_obj.year)  + ".csv",usecols=['date','mix'])
        region_mix = pd.read_csv(mix_path,usecols=['date','mix'])

    #region_mix.fillna(0.5)
    date_list = region_mix["date"].tolist()
    region_mix_list = region_mix["mix"].tolist()
    if(region != 11 and region != 93):
        adjustement_mix_list = adjustement_mix["mix"].tolist()

    cost = pd.read_csv(predicted_folder + "/"  +  "total_" + str(timezone_start_obj.year) + "_cost.csv",usecols=['cost'])
    #cost.fillna(50)
    cost_list = cost["cost"].tolist()

    rounded_start = ceil_dt(corrected_obj, dt.timedelta(minutes=30))

    index = date_list.index(rounded_start.strftime("%Y-%m-%d %H:%M:%S"))

    print("index", index)
    cost_list = cost_list[index:(index + input_len)]
    region_mix_list = region_mix_list[index:(index + input_len)]
    if(region != 11 and region != 93):
        adjustement_mix_list = adjustement_mix_list[index:(index + input_len)]
        for l in range(len(region_mix_list)):
            region_mix_list[l] = (region_mix_list[l] + adjustement_mix_list[l])/2

    # for w in range(len(cost_list)):
    #    if(cost_list[w] < 0 or cost_list[w] > 200):
    #        cost_list[w] = 50

    for w in range(len(cost_list)):
        cost_list[w] = (cost_list[w] - min(cost_list)) / (max(cost_list) - min(cost_list))

    for m in range(len(region_mix_list)):
        region_mix_list[m] = (region_mix_list[m] - min(region_mix_list)) / (max(region_mix_list) - min(region_mix_list))

    # for k in range(len(region_mix_list)):
    #     if(region_mix_list[k] < 0 or region_mix_list[k] > 1):
    #         region_mix_list[k] = 0.5

    combination = []

    for m in range(len(region_mix_list)):
        combination.append(region_mix_list[m] * lambda_mix - cost_list[m] * lambda_cost)

    for j in range(len(combination)):
        window.append(0)

    estimate = 0
    charge = current_charge
    while(charge < 100):
        charge += 30 * charge_speed
        estimate += 1

    print(combination)

    indexes = sorted(range(len(combination)), key=lambda i: combination[i])[-2*estimate:]

    # previous = 0
    # index = 0
    # while(estimate > 0):
    #     if(abs(indexes[index]-previous) >= 3 or previous == 0):
    #         window[indexes[index]] = 1
    #         previous = indexes[index]
    #         estimate -= 1
    #     index += 1

    #for i in range(len(indexes)):
        
    indexes = sorted(indexes)

    if(len(indexes) % 2 == 1):
        window[indexes[0]] = 1
        indexes.pop(0)

    for w in range(len(indexes)):
            if(w % 2 == 1):
                window[indexes[w]] = 1
        
    if(tweak != 0):
        for m in range(tweak):
            window.insert(0,1)

    string = ""
    for x in window:
        string += str(int(x))
        print(string)

    df2 = pd.DataFrame({"id_voiture ": [id],
                        "charge_plan": [string]})

    to_submit = to_submit.append(df2, ignore_index = True)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(to_submit)

to_submit.to_csv('combine_regions3.csv',index=False,sep = ';')