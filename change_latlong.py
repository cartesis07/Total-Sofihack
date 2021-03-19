import numpy as np
import pandas as pd

from pyproj import Transformer

#PATHS

input_path = "Hackathon_Data/input_file_csv.csv"
weather_path = "Hackathon_Data/Dataset/weather.csv"
mix_path = "Hackathon_Data/Dataset/mix.csv"
cost_path = "Hackathon_Data/Dataset/cost.csv"

new_input_path = "Hackathon_Data/new_input_file_csv.csv"

vehicles = pd.read_csv(new_input_path)

vehicles['Lat'] = ""
vehicles['Long'] = ""

for i in range(vehicles.shape[0]):
    # Geolocalization
    x_wgs_84 = vehicles['x(E) W84-N31'].values[i]
    y_wgs_84 = vehicles['y(N) W84-N31'].values[i]


    transformer = Transformer.from_crs("epsg:32631", "epsg:4326")   
    x2,y2 = transformer.transform(x_wgs_84, y_wgs_84)
    vehicles['Lat'].values[i] = x2
    vehicles['Long'].values[i] = y2

vehicles.to_csv('new_input_file_csv.csv', index=False)