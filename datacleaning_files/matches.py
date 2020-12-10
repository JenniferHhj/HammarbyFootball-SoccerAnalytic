##this file should create a dataframe that contain all information of each matches
##data scratching from the "Matches" folder in the soccerdata



import pandas as pd
import numpy as np

##Mount the drive in google colab
from google.colab import drive
drive.mount('/content/drive')

##upload and read all the .json file in the drive
##also drop all the broken json file
directory_path = '/content/drive/My Drive/soccerdata/data/matchess/'
#path to the files

import os
import json
json_name = os.listdir(directory_path)
holder = []
for i in json_name:
    if i.endswith('.json'):
        try:
            data = json.load(open(directory_path + i))
            each =  pd.DataFrame(data)
            holder.append(each)
        except ValueError as ve:
            print(i)


##merge all the .json file into one dataframe and print out the shape of the dataframe
merged = pd.concat(holder)
print(merged.shape)

##Save the dataframe to a .csv file into the local environment
merged.head(10)
merged.to_csv('/content/drive/My Drive/soccerdata/data/matches/matches_each.csv', index = False)
