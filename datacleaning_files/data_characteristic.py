##read the dataframe from the .csv file
data = pd.read_csv('shotoutcome_genderandplayers.csv')
data

##find out how many total shot event are being used
len(data['gender'])
##find out how many shot event are perform by male
trackm = 0
for i in data['gender']:
    if i == 'male':
        trackm = trackm + 1
##find out how many shot event are perform by female
track = 0
for i in data['gender']:
    if i == 'female':
        track = track + 1




##find out how many teams are female and how many teams are male

#recreate the team_name to gender dictionary as we did in the data_cleaning file
#this portion of the code should be identical the corresponding portion in the data_cleaning file
import ast
empty_dic = {}
for i in data['home_team'].tolist():
    dicti = ast.literal_eval(i)
    team_name = dicti.get('home_team_name')
    gender = dicti.get('home_team_gender')
    empty_dic[team_name] = gender
for i in data['away_team'].tolist():
    dicti = ast.literal_eval(i)
    team_name = dicti.get('away_team_name')
    gender = dicti.get('away_team_gender')
    empty_dic[team_name] = gender
#tack and find out the amount of male and female teams
female_track = 0
male_track = 0
for i in empty_dic:
    if empty_dic.get(i) == 'male':
        male_track+=1
    else:
        female_track+=1
print(male_track)
print(female_track)
