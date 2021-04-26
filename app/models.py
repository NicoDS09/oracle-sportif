import pymssql


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
    return execute_sql(sql)


def get_team_statistics(team_id):
    sql = "SELECT * FROM dbo.teams_stats WHERE id = " + team_id
    return execute_sql(sql)


def get_league_statistics():
    sql = "SELECT * FROM dbo.league_stats"
    return execute_sql(sql)
