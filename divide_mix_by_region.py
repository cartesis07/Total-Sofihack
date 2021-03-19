import numpy as np
import pandas as pd

#PATHS

input_path = "Hackathon_Data/input_file_csv.csv"
weather_path = "Hackathon_Data/Dataset/weather.csv"
mix_path = "Hackathon_Data/Dataset/mix.csv"
cost_path = "Hackathon_Data/Dataset/cost.csv"

#READ INPUTS

mix_data = pd.read_csv(mix_path)
mix_data = mix_data.sort_values(by=['Code INSEE région'])

mix_data.to_csv("mix_sorted.csv", index=False)