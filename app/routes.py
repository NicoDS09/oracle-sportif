from flask import render_template, request, redirect, url_for
from app import app
from app.models import *


### Page d'accueil ###
@app.route('/')
@app.route('/index')
def hello_world():
    return render_template('base_two_choice_pages.html', title='Accueil', menu_1="ANALYSE", redirect_1="/conferences", menu_2="PREDICTION", redirect_2="/predictions")


### Prédictions résultats d'une équipes ###

@app.route('/predictions')
def predictions():
    return render_template('predictions.html')

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
    return render_template('base_team_statistics.html', title='Team Statistics', teams_statistics=teams_statistics)

@app.route('/players')
def show_players():
    players = get_players()
    app.logger.debug(players)

    return render_template('players.html', title='Liste des joueurs', players=players)
