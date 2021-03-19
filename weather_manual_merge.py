#IMPORTS

import numpy as np
import pandas as pd
import os
import datetime

#PATHS

folder_path = "Hackathon_Data/Dataset/Prediction1/weather1_selec"
second_folder_path = "Hackathon_Data/Dataset/Prediction1/mix1"

for subdir, dirs, files in os.walk(folder_path):
    for file in files:

        filepath = subdir + os.sep + file

        print(filepath)

        df = pd.read_csv(filepath)

        df.fillna(0)

        df['time'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S", errors='ignore', utc=True)

        print(file)
        df2 = pd.read_csv(second_folder_path + "/" + "mix_" + file[-6:-4] + ".csv" )

        df2["time"] = pd.to_datetime(df2[' Date - Heure'], format="%Y-%m-%dT%H:%M:%S", errors='ignore', utc=True)

        df3 = df2

        minimal_weather = 0
        for i in range(len(df2)):
            if(df2["time"].values[i] < df["time"].values[i]):
                df3.append(np.concatenate((df.values[i], df2.values[minimal_weather]), axis=None))
            else:
                minimal_weather += 1
                df3.append(pd.concat([df.iloc(i), df2.iloc(minimal_weather)], axis=1))
