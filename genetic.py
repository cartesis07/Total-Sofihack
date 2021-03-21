#IMPORTS

import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import pandas as pd 

import datetime as dt
import pytz

import math
import random as rd

from pyproj import Transformer

#PATHS

input_path = "Hackathon_Data/ultra_csv.csv"
to_submit = "Hackathon_Data/to_submit_csv.csv"
predicted_folder = "results_predicted"

#GENETIC ALGORIGHM FOR ONE VEHICLE

def genetic_vehicle(periods,current_charge,charge_speed,lambda_mix,lambda_cost, mix_list, cost_list):

    def cost_function(X):
        penalty = 0
        charge = 0
        count = 0

        objective = current_charge
        difference = 0
        while(objective < 100):
            objective += charge_speed * 30
            difference += 1

        for i in range(periods):
            if(X[i] == 1):
                count += 1
            charge += 30 * X[i] * charge_speed

        
        if(difference != count):
            penalty += abs(difference - count) * 5

        #if(current_charge + charge < 100):
        #    penalty += abs(count - objective)*0.1

        #if(current_charge + charge > 120):
        #    penalty += abs(count - objective)*0.1

        score = []
        for i in range(periods):
            score.append((lambda_mix * mix_list[i] - lambda_cost * cost_list[i]) * X[i])
    
        return - (sum(score) / len(score)) + penalty

    algorithm_param = {'max_num_iteration': 100,\
                   'population_size':150,\
                   'mutation_probability':0.1,\
                   'elit_ratio': 0.01,\
                   'crossover_probability': 0.5,\
                   'parents_portion': 0.3,\
                   'crossover_type':'uniform',\
                   'max_iteration_without_improv':30,
                    }

    model=ga(function=cost_function,dimension=periods,variable_type='bool',algorithm_parameters=algorithm_param,convergence_curve=False)
    model.run()
    solution=model.output_dict
    return solution.get('variable')

#genetic_vehicle(10,50,0.474316267771597,0.1,0.9,[0.3,0.2,0.5,0.7,0.8,0.9,0.1,0.2,0.3,0.4],[60,10,50,50,40,70,30,40,70,20])

#READ INPUT DATA

def ceil_dt(dt, delta):
    return dt + (dt.min - dt) % delta

input_data = pd.read_csv(input_path) 
to_submit = pd.DataFrame(columns=['id_voiture ', 'charge_plan'])
print(input_data.head())
print(list(input_data))

list = []
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

    for j in range(duration):
        window.append(0)

    # 20% battery correction

    corrected_str = input_data[' dateheure_plug '].values[i]
    corrected_obj = dt.datetime.strptime(corrected_str, '%d-%m-%Y _ %H:%M:%S')
    timezone_corrected_obj = timezone.localize(corrected_obj)

    tweak = math.ceil( (timezone_corrected_obj - timezone_start_obj).total_seconds() / 1800 )

    input_len = duration - tweak

    region = input_data['Code INSEE 2'].values[i]

    #handle IDF case
    if(region == 93):
        region = 24

    if(region == 11):
        region = 84

    region_mix = pd.read_csv(predicted_folder + "/" + str(timezone_start_obj.year) + "/" + str(region) + "_" + str(timezone_start_obj.year)  + ".csv",usecols=['date','mix'])
    region_mix.fillna(0.5)
    date_list = region_mix["date"].tolist()
    region_mix_list = region_mix["mix"].tolist()

    cost = pd.read_csv(predicted_folder + "/"  +  "total_" + str(timezone_start_obj.year) + ".csv",usecols=['cost'])
    cost.fillna(50)
    cost_list = cost["cost"].tolist()

    rounded_start = ceil_dt(corrected_obj, dt.timedelta(minutes=30))

    index = date_list.index(rounded_start.strftime("%Y-%m-%d %H:%M:%S"))

    print("index", index)
    cost_list = cost_list[index:(index + input_len+1)]
    region_mix_list = region_mix_list[index:(index + input_len+1)]

    for w in range(len(cost_list)):
        if(cost_list[w] < 0 or cost_list[w] > 200):
            cost_list[w] = 50

    for w in range(len(cost_list)):
        cost_list[w] = cost_list[w] / max(cost_list)

    for k in range(len(region_mix_list)):
        if(region_mix_list[k] < 0 or region_mix_list[k] > 1):
            region_mix_list[k] = 0.5

    print("longueur", input_len)
    print("current_charge", current_charge)
    print(charge_speed)
    print(lambda_mix)
    print(lambda_cost)
    print(cost_list)
    print(region_mix_list)

    result = genetic_vehicle(input_len,current_charge,charge_speed,lambda_mix,lambda_cost,region_mix_list,cost_list)
    result = result.tolist()
    if(tweak != 0):
        for i in range(0,tweak):
            result.insert(0,1)

    if(len(result) != duration):
        print(len(result))
        print(duration)
        print("ALRTLSNDFLSDFHDSFSDJFHKDJSFHDSKFJHDSKFJHDSJKFHDSKJFHKDJSHFKJSDHFDKJSHFJKSDHFKJDSFHKJDSHFKJSDFHJDHSF")
    
    string = ""
    for x in result:
        string += str(int(x))
    print(string)

    df2 = pd.DataFrame({"id_voiture ": [id],
                        "charge_plan": [string]})

    #to_submit.loc[i] = [i+1,string]

    to_submit = to_submit.append(df2, ignore_index = True)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(to_submit)

to_submit.to_csv('to_submit2.csv',index=False)