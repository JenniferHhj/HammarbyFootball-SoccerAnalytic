##This file should do the initial cleaning for the DataFrame
##Merge and Extract some specific value for further training purpose


##import all the necessary packages
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

##read the dataframe
data = pd.read_csv('merged.csv')
data

##datacleaning

##drop all the rows in the "shot" column that contain Nan value
shot = data.dropna(subset=['shot'])
##obatin the team name and position of each event(action)
position_index = list(shot.index)
position_df = shot.loc[position_index,:]
position_list = list(position_df['location'])
name_list = list(shot['team'])

##convert the string to dictionary dataframe in columns
import ast
dict1df = pd.DataFrame.from_dict(dict1,orient = 'index')
dict1df.transpose()
##add all those values in the dictionary to columns to the original dataframe
dataframeholder = []
start = 0
##match the action of every event to it's accordinate team
for i in shot['shot'].tolist():
    dicti = ast.literal_eval(i)
    idf = pd.DataFrame.from_dict(dicti,orient = 'index')
    finali = idf.transpose()
    finali['player_position'] = position_list[start]
    name_dict = ast.literal_eval(name_list[start])
    finali['name'] = name_dict.get('name')
    start = start+1
    #finali.reset_index(drop = True)
    dataframeholder.append(finali)
len(dataframeholder)
merged = pd.concat(dataframeholder)

##find out each rows's value in the outcome column
outcome = merged['outcome']
outcomeholder = []
for t in outcome.tolist():
    #print(type(t))
    try:
        value = t.get('name')
        outcomeholder.append(value)
    except AttributeError:
        outcomeholder.append(np.nan)
##add the outcome value to the original dataframe with an addiitonal columns
merged['shot_outcome'] = outcomeholder
merged.head()



###convert the string in the Freezefemae column to a dictionary
data = merged.copy()
tech = data['freeze_frame'].tolist()
listholder = []
#import string
for po in tech:
    try:
        d = eval(po)
        #print('success')
        listholder.append(d)
    except (TypeError, NameError):
        d = []
        listholder.append(d)

##Here in each element in the each_freeframe list holds t2o dataframe.
##The first dataframe hold all the information of the players on the fireld that's from the same team.
##The second dataframe hold all the information of the players on the fielld that's from the opponent team.
##It should be fairly easy to access those data when train the algorithm.
##Further modify/add in more attribute if needed.
for i in listholder:
    locationt = []
    playert = []
    positiont = []
    locationp = []
    playerp = []
    positionp = []
    for a in i:
        try:
            location_i = a.get('location')
            position_i = a.get('position')
            player_i = a.get('player')
            if a.get('teammate'):
                locationt.append(location_i)
                positiont.append(position_i)
                playert.append(player_i)
            else:
                locationp.append(location_i)
                positionp.append(position_i)
                playerp.append(player_i)
        except (TypeError, AttributeError):
            d = {}
            false_d.append(d)
    freezeframe_t = pd.DataFrame({'position': positiont,'location':locationt,'player':playert})
    freezeframe_p = pd.DataFrame({'position': positionp,'location':locationp,'player':playerp})
    combine = [freezeframe_t,freezeframe_p]
    each_freeframe = each_freeframe + [combine]
##information about teammate
teammate_info = [i[0] for i in each_freeframe]
##information about opponent
oppnent_info = [i[1] for i in each_freeframe]
##save those values and add two columns to the original dataframe
data['teammate_info'] = teammate_info
data['oppnent_info'] = oppnent_info




##matching each event with it's accordingnate gender of female/male
##load the merge .csv file that contain all information about a match
ty1 = pd.read_csv('matches_each.csv')
##using the information in the matches_each.csv
##creat a dictionary that match each each with its corresponding gender
import ast
empty_dic = {}
#update the dictionary of all home teams
for i in ty1['home_team'].tolist():
    dicti = ast.literal_eval(i)
    team_name = dicti.get('home_team_name')
    gender = dicti.get('home_team_gender')
    empty_dic[team_name] = gender
#update the dictionary of all away_team
for i in ty1['away_team'].tolist():
    dicti = ast.literal_eval(i)
    team_name = dicti.get('away_team_name')
    gender = dicti.get('away_team_gender')
    empty_dic[team_name] = gender
##now use the dictionary to matches each team with it's corresponding gender in the same order as the original dataframe
gender_holder = []
for i in data['name']:
    gender = empty_dic.get(i)
    gender_holder.append(gender)
data['gender'] = gender_holder

##save the dataframe into a .csv file to local environment
data.to_csv("/Users/haojuanhe/Downloads/shotoutcome_genderandplayers.csv")
