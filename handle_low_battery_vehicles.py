import numpy as np
import pandas as pd 
import datetime as dt
import pytz

#PATHS

input_path = "Hackathon_Data/input_file_csv.csv"
weather_path = "Hackathon_Data/Dataset/weather.csv"
mix_path = "Hackathon_Data/Dataset/mix.csv"
cost_path = "Hackathon_Data/Dataset/cost.csv"

#READ INPUT DATA

input_data = pd.read_csv(input_path) 

for i in range(input_data.shape[0]):
    current_charge = input_data[' %_charge '].values[i]
    if(current_charge < 20):
        charge_speed = input_data[' vitesse_charge (%/min)'].values[i]
        count = 0
        while(current_charge < 20):
            current_charge += charge_speed
            count += 1
        input_data[' %_charge '].values[i] = current_charge

        # Time conversion
        timezone = pytz.timezone('Europe/Paris')

        start_str = input_data[' dateheure_plug '].values[i]
        start_obj = dt.datetime.strptime(start_str, '%d-%m-%Y _ %H:%M:%S')
        timezone_start_obj = timezone.localize(start_obj)

        timezone_start_obj = timezone_start_obj + dt.timedelta(minutes=count)

        new_string = timezone_start_obj.strftime('%d-%m-%Y _ %H:%M:%S')
        input_data[' dateheure_plug '].values[i] = new_string

        input_data.to_csv('new_input_file_csv',index=False)

