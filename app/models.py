import pymssql
import pandas as pd
from sklearn import preprocessing


def execute_sql(sql):
    connection = pymssql.connect('oracle-database.database.windows.net', 'oracle-database', 'ynov2021-',
                                     'Oracle_SQL_DataBase')
    cur = connection.cursor()
    cur.execute(sql)

    def return_dict_pair(row_item):
        return_dict = {}
        for column_name, row in zip(cur.description, row_item):
            return_dict[column_name[0]] = row
        return return_dict

    return_list = []
    for row in cur:
        row_item = return_dict_pair(row)
        return_list.append(row_item)

    connection.close()

    return return_list


def get_teams(conference):
    sql = "SELECT * FROM dbo.teams WHERE conference = '" + conference + "'"
    print(pd.DataFrame(execute_sql(sql)))
    return execute_sql(sql)


def get_team_statistics(team_id):
    sql = "SELECT * FROM dbo.teams_stats WHERE id = " + team_id
    return execute_sql(sql)


def get_league_statistics():
    sql = "SELECT * FROM dbo.league_stats"
    return execute_sql(sql)


def get_matchs(date_match=None):
    if date_match is not None:
        sql = "SELECT * FROM dbo.matchs_results WHERE start_date_eastern = "+str(date_match)
    else:
        sql = "SELECT * FROM dbo.matchs_results"
    return execute_sql(sql)


def make_prediction(model, scaler, hTeam, vTeam, date_match):
    print(str(hTeam)+" VS "+str(vTeam)+" (date du match : "+str(date_match)+")")

    X_pred = pd.DataFrame([
        generate_kpi_dataframe(
            team1=hTeam,
            team2=vTeam,
            date_match=date_match
        )
    ])

    X_pred = scaler.transform(X_pred)

    prediction = model.predict(X_pred)[0]
    probas_prediction = model.predict_proba(X_pred)

    return prediction, probas_prediction


# Fonction de calcul de la valeur moyenne d'un indicateur d'une équipe sur la saison en cours
def calc_mean(all_matchs, team, date_match, name_kpi_h, name_kpi_v, last_5_matchs=False):
    team_matchs = all_matchs[
        ((all_matchs['h_team'] == team) | (all_matchs['v_team'] == team)) & (all_matchs['start_date_eastern'] < date_match)
        ]

    if (last_5_matchs):
        team_matchs = team_matchs[-5:]

    team_matchs.loc[team_matchs['h_team'] == team, 'kpi'] = team_matchs[name_kpi_h]
    team_matchs.loc[team_matchs['v_team'] == team, 'kpi'] = team_matchs[name_kpi_v]

    return team_matchs.describe()['kpi']['mean']


# Fonction pour générer une ligne contenant les kpis des 2 équipes d'un match, nécessaire pour la prédiction
def generate_kpi_dataframe(team1, team2, date_match):

    all_matchs = pd.DataFrame(get_matchs())

    #
    ### SCORE
    #
    # Moyenne de l'équipe (h & v) sur tous ses matchs précédents (domicile + extérieur confondus)
    h_mean_score_saison = calc_mean(all_matchs, team1, date_match, 'h_team_score', 'v_team_score')
    v_mean_score_saison = calc_mean(all_matchs, team2, date_match, 'h_team_score', 'v_team_score')

    # Moyenne de l'équipe sur ses 5 derniers matchs (domicile + extérieur confondus)
    h_mean_score_last_five = calc_mean(all_matchs, team1, date_match, 'h_team_score', 'v_team_score', True)
    v_mean_score_last_five = calc_mean(all_matchs, team2, date_match, 'h_team_score', 'v_team_score', True)

    #
    ### FGM
    #
    # Moyenne de l'équipe sur tous ses matchs précédents (domicile + extérieur confondus)
    h_mean_fgm_saison = calc_mean(all_matchs, team1, date_match, 'hfgm', 'vfgm')
    v_mean_fgm_saison = calc_mean(all_matchs, team2, date_match, 'hfgm', 'vfgm')

    # Moyenne de l'équipe sur ses 5 derniers matchs (domicile + extérieur confondus)
    h_mean_fgm_last_five = calc_mean(all_matchs, team1, date_match, 'hfgm', 'vfgm', True)
    v_mean_fgm_last_five = calc_mean(all_matchs, team2, date_match, 'hfgm', 'vfgm', True)

    #
    ### FGP
    #
    # Moyenne de l'équipe sur tous ses matchs précédents (domicile + extérieur confondus)
    h_mean_fgp_saison = calc_mean(all_matchs, team1, date_match, 'hfgp', 'vfgp')
    v_mean_fgp_saison = calc_mean(all_matchs, team2, date_match, 'hfgp', 'vfgp')

    # Moyenne de l'équipe sur ses 5 derniers matchs (domicile + extérieur confondus)
    h_mean_fgp_last_five = calc_mean(all_matchs, team1, date_match, 'hfgp', 'vfgp', True)
    v_mean_fgp_last_five = calc_mean(all_matchs, team2, date_match, 'hfgp', 'vfgp', True)

    #
    ### TPP
    #
    # Moyenne de l'équipe sur tous ses matchs précédents (domicile + extérieur confondus)
    h_mean_tpp_saison = calc_mean(all_matchs, team1, date_match, 'htpp', 'vtpp')
    v_mean_tpp_saison = calc_mean(all_matchs, team2, date_match, 'htpp', 'vtpp')

    # Moyenne de l'équipe sur ses 5 derniers matchs (domicile + extérieur confondus)
    h_mean_tpp_last_five = calc_mean(all_matchs, team1, date_match, 'htpp', 'vtpp', True)
    v_mean_tpp_last_five = calc_mean(all_matchs, team2, date_match, 'htpp', 'vtpp', True)

    #
    ### DEF REB
    #
    # Moyenne de l'équipe sur tous ses matchs précédents (domicile + extérieur confondus)
    h_mean_defReb_saison = calc_mean(all_matchs, team1, date_match, 'hdefReb', 'vdefReb')
    v_mean_defReb_saison = calc_mean(all_matchs, team2, date_match, 'hdefReb', 'vdefReb')

    # Moyenne de l'équipe sur ses 5 derniers matchs (domicile + extérieur confondus)
    h_mean_defReb_last_five = calc_mean(all_matchs, team1, date_match, 'hdefReb', 'vdefReb', True)
    v_mean_defReb_last_five = calc_mean(all_matchs, team2, date_match, 'hdefReb', 'vdefReb', True)

    #
    ### TOT REB
    #
    # Moyenne de l'équipe sur tous ses matchs précédents (domicile + extérieur confondus)
    h_mean_totReb_saison = calc_mean(all_matchs, team1, date_match, 'htotReb', 'vtotReb')
    v_mean_totReb_saison = calc_mean(all_matchs, team2, date_match, 'htotReb', 'vtotReb')

    # Moyenne de l'équipe sur ses 5 derniers matchs (domicile + extérieur confondus)
    h_mean_totReb_last_five = calc_mean(all_matchs, team1, date_match, 'htotReb', 'vtotReb', True)
    v_mean_totReb_last_five = calc_mean(all_matchs, team2, date_match, 'htotReb', 'vtotReb', True)

    #
    ### PLUS MINUS
    #
    # Moyenne de l'équipe sur tous ses matchs précédents (domicile + extérieur confondus)
    h_mean_plusMinus_saison = calc_mean(all_matchs, team1, date_match, 'hplusMinus', 'vplusMinus')
    v_mean_plusMinus_saison = calc_mean(all_matchs, team2, date_match, 'hplusMinus', 'vplusMinus')

    # Moyenne de l'équipe sur ses 5 derniers matchs (domicile + extérieur confondus)
    h_mean_plusMinus_last_five = calc_mean(all_matchs, team1, date_match, 'hplusMinus', 'vplusMinus', True)
    v_mean_plusMinus_last_five = calc_mean(all_matchs, team2, date_match, 'hplusMinus', 'vplusMinus', True)

    return {
        'h_mean_score_saison': h_mean_score_saison,
        'v_mean_score_saison': v_mean_score_saison,
        'h_mean_score_last_five': h_mean_score_last_five,
        'v_mean_score_last_five': v_mean_score_last_five,

        'h_mean_fgm_saison': h_mean_fgm_saison,
        'v_mean_fgm_saison': v_mean_fgm_saison,
        'h_mean_fgm_last_five': h_mean_fgm_last_five,
        'v_mean_fgm_last_five': v_mean_fgm_last_five,

        'h_mean_fgp_saison': h_mean_fgp_saison,
        'v_mean_fgp_saison': v_mean_fgp_saison,
        'h_mean_fgp_last_five': h_mean_fgp_last_five,
        'v_mean_fgp_last_five': v_mean_fgp_last_five,

        'h_mean_tpp_saison': h_mean_tpp_saison,
        'v_mean_tpp_saison': v_mean_tpp_saison,
        'h_mean_tpp_last_five': h_mean_tpp_last_five,
        'v_mean_tpp_last_five': v_mean_tpp_last_five,

        'h_mean_defReb_saison': h_mean_defReb_saison,
        'v_mean_defReb_saison': v_mean_defReb_saison,
        'h_mean_defReb_last_five': h_mean_defReb_last_five,
        'v_mean_defReb_last_five': v_mean_defReb_last_five,

        'h_mean_totReb_saison': h_mean_totReb_saison,
        'v_mean_totReb_saison': v_mean_totReb_saison,
        'h_mean_totReb_last_five': h_mean_totReb_last_five,
        'v_mean_totReb_last_five': v_mean_totReb_last_five,

        'h_mean_plusMinus_saison': h_mean_plusMinus_saison,
        'v_mean_plusMinus_saison': v_mean_plusMinus_saison,
        'h_mean_plusMinus_last_five': h_mean_plusMinus_last_five,
        'v_mean_plusMinus_last_five': v_mean_plusMinus_last_five
    }