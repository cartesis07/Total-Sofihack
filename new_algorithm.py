#IMPORTS

import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import pandas as pd 

import datetime as dt
import pytz

import math
import random as rd

from pyproj import Transformer

from scipy.interpolate import lagrange

input_path = "Hackathon_Data/ultra_csv.csv"
to_submit = "Hackathon_Data/to_submit_csv.csv"
mix_predicted_folder = "merged_mix_predicted"
predicted_folder = "results_predicted"


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
    if(region == 93 or region == 11):
        mix_path = "results_predicted/total_" + str(timezone_start_obj.year)  + ".csv"
        region_mix = pd.read_csv(mix_path,usecols=['date','mix'])

    else:
        mix_path = mix_predicted_folder + "/" + str(timezone_start_obj.year) + "/output" + str(region) + "_" + str(timezone_start_obj.year)  + ".csv"
        region_mix = pd.read_csv(mix_path,usecols=['date','mix'])
        average_mix = pd.read_csv("results_predicted/total_" + str(timezone_start_obj.year)  + ".csv",usecols=['date','mix'])

    #region_mix.fillna(0.5)
    date_list = region_mix["date"].tolist()
    region_mix_list = region_mix["mix"].tolist()

    if(region != 93 and region != 11):
       average_list = average_mix["mix"].tolist()

    cost = pd.read_csv(predicted_folder + "/"  +  "total_" + str(timezone_start_obj.year) + "_cost.csv",usecols=['cost'])
    #cost.fillna(50)
    cost_list = cost["cost"].tolist()

    rounded_start = ceil_dt(corrected_obj, dt.timedelta(minutes=30))

    index = date_list.index(rounded_start.strftime("%Y-%m-%d %H:%M:%S"))

    print("index", index)
    cost_list = cost_list[index:(index + input_len)]
    region_mix_list = region_mix_list[index:(index + input_len)]
    if(region != 93 and region != 11):
        average_list = average_list[index:(index + input_len)]

    # for w in range(len(cost_list)):
    #    if(cost_list[w] < 0 or cost_list[w] > 200):
    #        cost_list[w] = 50
    if(region != 93 and region != 11):
         for l in range(len(region_mix_list)):
             region_mix_list[l] = (region_mix_list[l] + average_list[l]) / 2

    N = len(cost_list)

    x = np.array([0, N/4, N/2, 3*N/4, N])
    y = np.array([-1, 1, -1, 1, -1])

    poly = lagrange(x, y)

    for w in range(len(cost_list)):
        cost_list[w] = (cost_list[w] - min(cost_list)) / (max(cost_list) - min(cost_list))
        cost_list[w] += ((w - len(cost_list)/2)*0.1)**2

        #cost_list[w] -= ((w - len(cost_list)/2)*0.1)**2

        #cost_list[w] += 1

        #cost_list[w] += poly[w]*0.1

    for m in range(len(region_mix_list)):
        region_mix_list[m] = (region_mix_list[m] - min(region_mix_list)) / (max(region_mix_list) - min(region_mix_list))
        region_mix_list[w] -= ((w - len(region_mix_list)/2)*0.1)**2

        #region_mix_list[m] += ((m - len(region_mix_list)/2)*0.1)**2

        #region_mix_list[m] += poly[m]*0.1

    # if(lambda_mix > lambda_cost):
    #     for w in range(len(cost_list)):
    #         region_mix_list[w] -= ((w - len(region_mix_list)/2)*0.1)**2
    #         #if(w > math.floor(len(region_mix_list)/2) - 2 or w < math.floor(len(region_mix_list)/2) + 2):
    #         #    region_mix_list[w] = 0
    #         #region_mix_list[w] += poly[w]
    # else:
    #     for w in range(len(cost_list)):
    #         cost_list[w] += ((w - len(cost_list)/2)*0.1)**2
            #if(w == math.floor(len(cost_list)/2)):
            #    cost_list[w] = 100
            #cost_list[w] -= poly[w]

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

    indexes = sorted(range(len(combination)), key=lambda i: combination[i])[-estimate:]

    for w in range(len(indexes)):
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

to_submit.to_csv('new2.csv',index=False,sep = ';')