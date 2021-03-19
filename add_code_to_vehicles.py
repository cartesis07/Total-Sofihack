#IMPORTS

import numpy as np
import pandas as pd

import urllib.request, json

#PATHS

input_path = "Hackathon_Data/input_file_csv.csv"
weather_path = "Hackathon_Data/Dataset/weather.csv"
mix_path = "Hackathon_Data/Dataset/mix.csv"
cost_path = "Hackathon_Data/Dataset/cost.csv"

new_input_path = "Hackathon_Data/new_input_file_csv.csv"

#DEFAULT API JSON

url = "https://geo.api.gouv.fr/communes"
    
response = urllib.request.urlopen(url)

city_to_region = json.loads(response.read())

#READ INPUTS

vehicles =  pd.read_csv(new_input_path)

vehicles['Code INSEE'] = ""

for i in range(len(vehicles)):
    lat = vehicles["Lat"].values[i]
    long = vehicles["Long"].values[i]

    string = "https://api-adresse.data.gouv.fr/search/?q=lat=" + str(lat) + "&lon=" + str(long)
    response = urllib.request.urlopen(string)
    data = json.loads(response.read())

    city_code = data.get('features')[0].get('properties').get('citycode')

    for j in range(len(city_to_region)):
        city_j = city_to_region[j].get('code')
        if(city_j == city_code):
            vehicles["Code INSEE"].values[i] = city_to_region[j].get('codeRegion')

print("Writing to csv")
vehicles.to_csv("vehicles+code+new.csv", index=False)
print("done")