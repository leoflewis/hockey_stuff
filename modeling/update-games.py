import mysql.connector, requests, pandas, numpy, math, os
from mysql.connector import Error
from joblib import load
db = None
try:
    db = mysql.connector.connect(
        host=os.environ.get("AZURE_MYSQL_HOST"),
        user=os.environ.get("AZURE_MYSQL_USER"),
        database=os.environ.get("AZURE_MYSQL_NAME"),
        password=os.environ.get("AZURE_MYSQL_PASSWORD"),
        port=3306
    )
except Error as e:
    print("Error while connecting to MySQL", e) 

if db is not None:
    cursor = db.cursor()
    sql = "SELECT GameID, HomeTeam, AwayTeam FROM Game;"
    vals = ("", "")
    try:
        cursor.execute(sql)
        response = cursor.fetchall()
        for game in response:
            game_id = game[0]
            home_team = game[1]
            away_team = game[2]
            print("Querying game {}".format(game_id))
            print("{} vs {}".format(home_team, away_team))
            sql = "SELECT EventId, EventTeam FROM GameEvent WHERE Game = %s"
            vals= (game_id,)
            cursor.execute(sql, vals)
            results = cursor.fetchall()

            for event in results:
                event_id = event[0]
                event_team = event[1]
                values = (event_id,)
                q = "UPDATE GameEvent SET ConcededTeam = %s WHERE EventId = %s" 
                if event_team == home_team:
                    values = (away_team, event_id)
                else:
                    values = (home_team, event_id)

                print("Updating event {}".format(event_id))
                try:
                    cursor.execute(q, values)
                    db.commit()
                except mysql.connector.errors.Error:
                    print("Error {}".format(e))


    except mysql.connector.errors.DataError as e:
        print("Error {}".format(e))
