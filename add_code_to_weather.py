#IMPORTS

import numpy as np
import pandas as pd

import urllib.request, json

#PATHS

input_path = "Hackathon_Data/input_file_csv.csv"
weather_path = "Hackathon_Data/Dataset/weather.csv"
mix_path = "Hackathon_Data/Dataset/mix.csv"
cost_path = "Hackathon_Data/Dataset/cost.csv"

#DEFAULT API JSON

url = "https://geo.api.gouv.fr/communes"
    
response = urllib.request.urlopen(url)

city_to_region = json.loads(response.read())

#READ INPUTS

weather_df =  pd.read_csv(weather_path)

weather_df['Code INSEE'] = ""

precedent = ""
precedent_code = -1

for i in range(len(weather_df)):
    city = weather_df["Nom"].values[i]
    lat = weather_df["Latitude"].values[i]
    long = weather_df["Longitude"].values[i]

    if(city != precedent):
        string = "https://api-adresse.data.gouv.fr/search/?q=lat=" + str(lat) + "&lon=" + str(long)
        response = urllib.request.urlopen(string)
        data = json.loads(response.read())

        city_code = data.get('features')[0].get('properties').get('citycode')

        for j in range(len(city_to_region)):
            city_j = city_to_region[j].get('code')
            if(city_j == city_code):
                precedent_code = city_to_region[j].get('codeRegion')
                weather_df["Code INSEE"].values[i] = precedent_code
                print(precedent_code)
    else:
        weather_df["Code INSEE"].values[i] = precedent_code
        print(precedent_code)

    precedent = city

print("Writing to csv")
weather_df.to_csv("weather+code.csv", index=False)
print("done")