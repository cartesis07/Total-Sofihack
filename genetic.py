#IMPORTS

import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import pandas as pd 

#PATHS

input_path = "Hackathon_Data/input_file_csv.csv"
weather_path = "Hackathon_Data/Dataset/weather.csv"
mix_path = "Hackathon_Data/Dataset/mix.csv"
cost_path = "Hackathon_Data/Dataset/cost.csv"

#READ DATA

#input_data = pd.read_csv(input_path) 
#print(input_data.head())

#weather_data = pd.read_csv(weather_path)
#print(weather_data.head())

#mix_data = pd.read_csv(mix_path)
#print(mix_data.head())

#cost_data = pd.read_csv(cost_path)
#print(cost_data.head())
#print(cost_data.describe())

#GENETIC ALGORIGHM FOR ONE VEHICLE



def genetic_vehicle(periods,current_charge,charge_speed,lambda_mix,lambda_cost, mix_list, cost_list):

    def cost_function(X):

        penalty = 0

        charge = 0
        for i in range(periods):
            charge += 30 * X[i] * charge_speed

        if(current_charge + charge < 100):
            penalty = 1

        if(current_charge + charge > 100 + 30 * charge_speed):
            penalty = 1

        score = []
        for i in range(periods):

            mix_der = (mix_list[i] - min(mix_list)) / (max(mix_list) - min(mix_list))
            cost_der = (cost_list[i] - min(cost_list)) / (max(cost_list) - min(cost_list))

            score.append((lambda_mix * mix_der - lambda_cost * cost_der) * X[i])
    
        return  - (sum(score) / len(score)) + penalty

    algorithm_param = {'max_num_iteration': 100,\
                   'population_size':100,\
                   'mutation_probability':0.2,\
                   'elit_ratio': 0.01,\
                   'crossover_probability': 0.5,\
                   'parents_portion': 0.3,\
                   'crossover_type':'uniform',\
                   'max_iteration_without_improv':None}

    model=ga(function=cost_function,dimension=periods,variable_type='bool',algorithm_parameters=algorithm_param)
    model.run()

genetic_vehicle(10,50,0.474316267771597,0.9,0.1,[0.3,0.2,0.5,0.7,0.8,0.9,0.1,0.2,0.3,0.4],[0.6,0.1,0.5,0.5,0.4,0.7,0.3,0.4,0.7,0.2])