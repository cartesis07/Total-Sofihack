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

input_path = "Hackathon_Data/input_file_csv.csv"
weather_path = "Hackathon_Data/Dataset/weather.csv"
mix_path = "Hackathon_Data/Dataset/mix.csv"
cost_path = "Hackathon_Data/Dataset/cost.csv"

#GENETIC ALGORIGHM FOR ONE VEHICLE

def genetic_vehicle(periods,current_charge,charge_speed,lambda_mix,lambda_cost, mix_list, cost_list):

    def cost_function(X):
        penalty = 0

        charge = 0
        for i in range(periods):
            charge += 30 * X[i] * charge_speed

        if(current_charge + charge < 100):
            penalty = 1000

        if(current_charge + charge > 100 + 30 * charge_speed):
            penalty = 1000

        score = []
        for i in range(periods):

            mix_der = (mix_list[i] - min(mix_list)) / (max(mix_list) - min(mix_list))
            cost_der = (cost_list[i] - min(cost_list)) / (max(cost_list) - min(cost_list))

            score.append((lambda_mix * mix_der - lambda_cost * cost_der) * X[i])
    
        return  - (sum(score) / len(score)) + penalty

    algorithm_param = {'max_num_iteration': 100,\
                   'population_size':100,\
                   'mutation_probability':0.1,\
                   'elit_ratio': 0.01,\
                   'crossover_probability': 0.5,\
                   'parents_portion': 0.3,\
                   'crossover_type':'uniform',\
                   'max_iteration_without_improv':None,
                    }

    model=ga(function=cost_function,dimension=periods,variable_type='bool',algorithm_parameters=algorithm_param,convergence_curve=False)
    model.run()

#genetic_vehicle(10,50,0.474316267771597,0.1,0.9,[0.3,0.2,0.5,0.7,0.8,0.9,0.1,0.2,0.3,0.4],[60,10,50,50,40,70,30,40,70,20])

#READ INPUT DATA

input_data = pd.read_csv(input_path) 
print(input_data.head())
print(list(input_data))

results = []
score = []

tmp_mix = []
tmp_cost = []

for i in range(50):
    tmp_mix.append(rd.random())
    tmp_cost.append(rd.uniform(0,100))

count = 0
for i in range(input_data.shape[0]):
    current_charge = input_data[' %_charge '].values[i]
    charge_speed = input_data[' vitesse_charge (%/min)'].values[i]
    lambda_mix = input_data[' %_mix_energetique '].values[i]
    lambda_cost = input_data[' %_cout_elec '].values[i]

    # Time conversion
    timezone = pytz.timezone('Europe/Paris')

    start_str = input_data[' dateheure_plug '].values[i]
    start_obj = dt.datetime.strptime(start_str, '%d-%m-%Y _ %H:%M:%S')
    timezone_start_obj = timezone.localize(start_obj)

    stop_str = input_data[' dateheure_Previs_stop '].values[i]
    stop_obj = dt.datetime.strptime(stop_str, '%d-%m-%Y _ %H:%M:%S')
    timezone_stop_obj = timezone.localize(stop_obj)

    difference = math.floor( (timezone_stop_obj - timezone_start_obj).total_seconds() / 3600 )

    #genetic_vehicle(difference,current_charge,charge_speed,lambda_mix,lambda_cost,tmp_mix,tmp_cost)