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

        #merge=pd.merge(df2,df, how='inner', left_on="time", right_on="time")

        merge = df2.merge(df, how="outer", left_on="time", right_on="time")

        #df3 = pd.merge_asof(df, df2, left_on="time", right_on="time")

        merge.to_csv('merge' + file,index=True)
        
        if filepath.endswith(".csv"):
            print (filepath)