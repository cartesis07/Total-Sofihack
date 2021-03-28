import pandas as pd
import numpy as np

selection = ['Code INSEE région', 'Date', 'Heure', 'Date - Heure', 'Consommation (MW)', 'Thermique (MW)', 'Nucléaire (MW)', 'Eolien (MW)', 'Solaire (MW)', 'Hydraulique (MW)', 'Pompage (MW)', 'Bioénergies (MW)', 'Ech. physiques (MW)']

df = pd.read_csv('Hackathon_Data/Dataset/Prediction1/mix1/mix_11_work_2.csv',usecols=selection)

df.to_csv('Hackathon_Data/Dataset/Prediction1/mix1/final_work.csv',index=False)