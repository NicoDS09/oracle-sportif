from flask import render_template, request, redirect, url_for
from app import app
from app.models import *
import os
import joblib

app.config['MODEL_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'model_logreg.joblib')
app.config['SCALER_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'standard_scaler.joblib')

### Page d'accueil ###
@app.route('/')
@app.route('/index')
def hello_world():
    return render_template('base_two_choice_pages.html', title='Accueil', menu_1="ANALYSE", redirect_1="/conferences", menu_2="PREDICTION", redirect_2="/predictions")


### Prédictions résultats d'une équipes ###

@app.route('/predictions')
def predictions():

    date_match = 20200814
    # date_match = 20210427

    date_match_str = "14/08/2020"
    # date_match_str = "27/04/2021"

    # Load du model de RL + du Scaler
    model = joblib.load(open(app.config['MODEL_PATH'], 'rb'))
    scaler = joblib.load(open(app.config['SCALER_PATH'], 'rb'))

    matchs = get_matchs(date_match)
    for match in matchs:
        is_h_team_win_predicted, probas_prediction = make_prediction(model, scaler, match['h_team'], match['v_team'], date_match)

        match['is_h_team_win_predicted'] = is_h_team_win_predicted
        match['probas_h_team_win'] = round(probas_prediction[1], 2)
        match['probas_v_team_win'] = round(probas_prediction[0], 2)
        match['h_team_name'] = get_team_name_by_id(match['h_team'])
        match['v_team_name'] = get_team_name_by_id(match['v_team'])

    print(len(matchs))
    return render_template('predictions.html', matchs=matchs, date_match=date_match, date_match_str=date_match_str)

### Page choix conférences pour équipes ###

@app.route('/conferences')
def teams():
    return render_template('base_two_choice_pages.html', title='Conferences', menu_1="EAST", redirect_1="/teams_east", menu_2="WEST", redirect_2="/teams_west")

### Page équipes conférence est ###

@app.route('/teams_east')
def teams_east():
    teams = get_teams("East")

    return render_template('base_conferences_team.html', title='East Conference', teams=teams)

### Page équipes conférence ouest ###

@app.route('/teams_west')
def teams_west():
    teams = get_teams("West")
    return render_template('base_conferences_team.html', title='West Conference', teams=teams)

### Page statitiques d'une équipe ###
@app.route('/team_statistics/<team_id>')
def team_statistics(team_id) :
    teams_statistics = get_team_statistics(team_id)
    league_statistics = get_league_statistics()
    return render_template('base_team_statistics.html', title='Team Statistics', teams_statistics=teams_statistics, league_statistics=league_statistics)

