from flask import Flask, render_template, request
import pandas as pd
from math import *
from google.cloud import datastore
import numpy as np
import joblib

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

class MatchData():
    seriesName = ""
    seasonName = ""
    matchDate = ""
    matchId = ""
    competitionId = 0

    homeTeamName = ""
    homeTeamXG = 0
    homeTeamGoals = 0
    homeTeamNumShots = 0
    homeTeamShotEvents = pd.DataFrame()

    awayTeamName = ""
    awayTeamXG = 0
    awayTeamGoals = 0
    awayTeamNumShots = 0
    awayTeamShotEvents = pd.DataFrame()

class MatchInfo():
    competition_id = 0
    match_id = 0
    name = ""
    season = ""
    gender = ""
    country = ""
    date = ""
    hometeam = ""
    awayteam = ""

class Competitions():
    all_competitions = pd.DataFrame()

class Competition():
    id = 0
    name = ""
    season = ""
    gender = ""
    country = ""
    all_matches = pd.DataFrame()

#HTTPS REQUEST ENDPOINTS
@app.route('/', methods=['GET'])
def xGoals():
    return render_template('start.html')

@app.route('/select-competitions', methods=['GET'])
def competitions():
    data = get_competitions_data() #gets all existing competitions
    return render_template('competitions.html', competitions = data)

@app.route('/competition-information', methods=['POST', 'GET'])
def competition_information():
    if request.method == 'POST':
        competitionId = request.form['competition']
        data = get_series_data(competitionId) #Gets competition info and all matches for this competition
        return render_template('competition-information.html', competition = data)

@app.route('/create-competition', methods=['POST', 'GET'])
def create_competition():
    competition = Competition()
    if request.method == 'POST':
        competition.name = request.form['compname']
        competition.country = request.form['country']
        competition.season = request.form['season']
        competition.gender = request.form['gender']

        data = store_competition_data(competition) #stores and returns competition info and all matches for this competition
        return render_template('competition-information.html', competition = data)

@app.route('/create-match', methods=['POST'])
def create_match():
    matchInfo = MatchInfo()
    if request.method == 'POST':
        matchInfo.competition_id = int(request.form['competitionid'])
        matchInfo.name = request.form['name']
        matchInfo.season = request.form['season']
        matchInfo.gender = request.form['gender']
        matchInfo.country = request.form['country']
        matchInfo.date = request.form['date']
        matchInfo.hometeam = request.form['hometeam']
        matchInfo.awayteam = request.form['awayteam']
        data = store_match_data(matchInfo) #stores and returns match to/from database
    return render_template('index.html', matchData = data)

@app.route('/view-match', methods=['POST', 'GET'])
def view_match():
    if request.method == 'POST':
        matchId = request.form['match']
        data = get_match_data(matchId) #gets match data from database
        return render_template('view-statistics.html', matchData = data)

@app.route('/edit-match', methods=['POST', 'GET'])
def edit_match():
    if request.method == 'POST':
        matchId = request.form['match']
        data = get_match_data(matchId) #gets match data from database
        return render_template('index.html', matchData = data)

@app.route('/add-shot', methods=['POST', 'GET'])
def add_shot():
    #stores shot to database

    if request.method == 'POST':

        datastore_client = datastore.Client.from_service_account_json("xg-test-project-734003e4e35c.json")

        #converts shot result into right format
        shot_result = 0
        shot_result_string = request.form['shotoutcome']
        if shot_result_string == 'goal':
            shot_result = 1

        #stores the shot
        match_key = datastore_client.key("shotData")
        matchObject = datastore.Entity(key=match_key)
        matchObject.update(
           {
               "match_id": int(request.form['matchid']),
               "pos_x": float(request.form['posx']),
               "pos_y": float(request.form['posy']),
               "shot_result": shot_result,
               "shot_team": request.form['team'],
               "xg": np.around(float(request.form['xg']),2),
               }
            )
        datastore_client.put(matchObject)

        #gets all shots from same match
        matchData = get_match_data(int(request.form['matchid']))

        #Sends match data to template
        return render_template('index.html', matchData = matchData)

@app.route('/get-xg', methods=['POST', 'GET'])
def get_xg():
    if request.method == 'POST':
        #gets feature values from form
        pos_x = float(request.form['posx'])
        pos_y = float(request.form['posy'])
        num_players = int(request.form['playerpos'])
        first_time = request.form['ftime']
        shot_type = request.form['shottype']
        #TODO: get more features

        #alculates distance to goal and distance to center
        center_value = abs(pos_y-(80/2))
        distance_value = np.sqrt(pos_x**2 + center_value**2)

        #calculates angle using law of cosine
        p = pos_x
        s = np.abs(pos_y - 44)
        q = np.abs(pos_y - 36)
        a = np.sqrt(q**2 + p**2)
        b = np.sqrt(s**2 + p**2)
        c = 8
        angle_value = np.arccos((a**2 + b**2 - c**2)/(2*a*b))

        #converts features into right format
        head, foot = 0, 0
        if shot_type == 'foot':
            foot = 1
        if shot_type == 'header':
            head = 1

        firstTime = 0
        if first_time == 't_ftime':
            firstTime = 1

        #gets xgModel
        fileName = 'soccer_analytics.pkl'
        xg_model = joblib.load(fileName)

        #Inputs values into model
        xg_columns = ["angle", "obstructing_players", 'distance', 'Foot', 'Head', 'first_time', 'dist_to_center']
        data = []
        data.append([angle_value, num_players, distance_value, foot, head, firstTime, center_value])
        input_values = pd.DataFrame(data, columns = xg_columns)

        results = xg_model.predict_proba(input_values) #predicts the probability of a shot

        #returns xG value
        return str(results[0][1])



#HEPLER FUNCTIONS AND DATASTORE COMMUNICATION FUNCTIONS
def store_match_data(matchInfo):
    #Stores a new match to the database. Returns match data.

    datastore_client = datastore.Client.from_service_account_json("xg-test-project-734003e4e35c.json")

    #looks for match with same information as in matchInfo
    query = datastore_client.query(kind='matchData')
    query.add_filter('match_date', '=', matchInfo.date)
    query.add_filter('home_team', '=', matchInfo.hometeam)
    query.add_filter('away_team', '=', matchInfo.awayteam)
    query.add_filter('competition_id', '=', matchInfo.competition_id)

    #Checks if match already exists. If it does, it returns data from that match.
    for match in query.fetch():
       matchdata = get_match_data(match.key.id)
       return matchdata

    #Stores the match
    match_key = datastore_client.key("matchData")
    matchObject = datastore.Entity(key=match_key)
    matchObject.update(
       {
           "match_date": matchInfo.date,
           "home_team": matchInfo.hometeam,
           "away_team": matchInfo.awayteam,
           "competition_id": matchInfo.competition_id,
           "series": matchInfo.name,
       }
    )
    datastore_client.put(matchObject)

    #Gets matchdata from stored match
    for match in query.fetch():
       matchdata = get_match_data(match.key.id)

    return matchdata


def store_competition_data(competition):
    #Stores a new competition to the database. Returns competition data.

    datastore_client = datastore.Client.from_service_account_json("xg-test-project-734003e4e35c.json")

    query = datastore_client.query(kind='competitionData')
    query.add_filter('country', '=', competition.country)
    query.add_filter('name', '=', competition.name)
    query.add_filter('season', '=', competition.season)
    query.add_filter('gender', '=', competition.gender)

    #Checks if competition already exists. If it does, it returns data from that competition
    for comp in query.fetch():
       competition = get_series_data(comp.key.id)
       return competition

    #Stores the competition
    competition_key = datastore_client.key("competitionData")
    competitionObject = datastore.Entity(key=competition_key)
    competitionObject.update(
       {
           "country": competition.country,
           "name": competition.name,
           "season": competition.season,
           "gender": competition.gender,
       }
    )
    datastore_client.put(competitionObject)

    #gets and returns competition (=series) data
    for comp in query.fetch():
       competition = get_series_data(comp.key.id)

    return competition

def get_competitions_data():
    #gets all existing competitions from the database

    datastore_client = datastore.Client.from_service_account_json("xg-test-project-734003e4e35c.json")
    query = datastore_client.query(kind='competitionData')

    competitions = Competitions()
    data = []

    for competition in query.fetch():
        data.append([competition.key.id, competition['name'], competition['season'], competition['gender'], competition['country']])

    #puts the retrieved competitions data into Competitions object
    columns = ['seriesid', 'seriesname', 'season', 'gender', 'country']
    competitions.all_competitions = pd.DataFrame(data, columns=columns)

    return competitions


def get_series_data(competitionId):
    #gets all data from a specific competition from database. This includes information about the competition itself, as well as all its matches.

    datastore_client = datastore.Client.from_service_account_json("xg-test-project-734003e4e35c.json")
    query = datastore_client.query(kind='competitionData')

    comp_id = int(competitionId)
    key = datastore_client.key("competitionData", comp_id)
    competition_obj = datastore_client.get(key) #returns all information in the row with this competition id

    #stores competition data into Competition object
    competition = Competition()
    competition.id = competitionId
    competition.name = competition_obj['name']
    competition.season = competition_obj['season']
    competition.country = competition_obj['country']
    competition.gender = competition_obj['gender']


    match_query = datastore_client.query(kind='matchData')
    match_query.add_filter("competition_id", "=", comp_id) #filters to only look at matches with correct competition id

    data = []
    for match in match_query.fetch(): #will only get matches from the specified competition
        data.append([match.key.id, match['match_date'], match['home_team'], match['away_team'], match['competition_id']])

    columns = ['matchid', 'date', 'home_team', 'away_team', 'competition_id']
    competition.all_matches = pd.DataFrame(data, columns=columns)

    return competition


def get_match_data(matchId):
    #gets all data from a specific match from database

    datastore_client = datastore.Client.from_service_account_json("xg-test-project-734003e4e35c.json")

    match_Id = int(matchId)
    key = datastore_client.key("matchData", match_Id)
    match_obj = datastore_client.get(key) #returns all information in the row with this match id

    #stores match data into matchData object
    matchData = MatchData()
    matchData.seriesName = match_obj['series']
    matchData.matchDate = match_obj['match_date']
    matchData.matchId = matchId
    matchData.homeTeamName = match_obj['home_team']
    matchData.awayTeamName = match_obj['away_team']
    matchData.competitionId = match_obj['competition_id']

    eventData = get_all_stored_events(matchId) #gets all shot events from the specified match

    homeShotEvents = []
    awayShotEvents = []

    #stores shot event data into matchData object
    for i, shotEvent in eventData.iterrows():
        if shotEvent.loc['shot_team'] == matchData.homeTeamName:
            matchData.homeTeamXG += shotEvent.loc['xg']
            matchData.homeTeamGoals += shotEvent.loc['shot_result']
            matchData.homeTeamNumShots += 1
            homeShotEvents.append(list(shotEvent.iloc[:]))
        else:
            matchData.awayTeamXG += shotEvent.loc['xg']
            matchData.awayTeamGoals += shotEvent.loc['shot_result']
            matchData.awayTeamNumShots += 1
            awayShotEvents.append(list(shotEvent.iloc[:]))

    shotsColumns = ["match_id","shot_team", "pos_x", "pos_y", "shot_result", "xg"]
    matchData.homeTeamShotEvents = pd.DataFrame(homeShotEvents, columns=shotsColumns)
    matchData.awayTeamShotEvents = pd.DataFrame(awayShotEvents, columns=shotsColumns)

    return matchData

def get_all_stored_events(matchId):
    #gets all shot events from a specific match

    datastore_client = datastore.Client.from_service_account_json("xg-test-project-734003e4e35c.json")

    match_Id = int(matchId)
    query = datastore_client.query(kind='shotData')
    query.add_filter("match_id", "=", match_Id) #filters to only look in rows with correct match id

    eventColumns = ["match_id", "shot_team", "pos_x", "pos_y", "shot_result", "xg"]
    shotEvents = []

    for shot in query.fetch(): #will only get events from the specified match
        shotEvents.append([shot.key.id, shot['shot_team'], shot['pos_x'], shot['pos_y'], shot['shot_result'], shot['xg']])

    eventData = pd.DataFrame(shotEvents, columns=eventColumns)

    return eventData

if __name__ == '__main__':
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='localhost', port=8080, debug=True)
