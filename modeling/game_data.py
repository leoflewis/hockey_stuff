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

if db.is_connected():
    get_games = "SELECT * FROM Game;"
    cursor = db.cursor()
    
    try:
        cursor.execute(get_games)
        games = cursor.fetchall()
        for game in games:
            print()
            print(game[2])
            print("*** NEW GAME ***")

            home_awayxG_query = "SELECT sum(xG) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE EventTeam = {} AND GameDate < '{}';".format(game[7], game[2])
            cursor.execute(home_awayxG_query)
            home_xGf = cursor.fetchall()
            print("Home team to date xGF: " + str(home_xGf[0][0]))

            away_homexG_query = "SELECT sum(xG) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE EventTeam = {} AND GameDate < '{}';".format(game[8], game[2])
            cursor.execute(away_homexG_query)
            away_xGf = cursor.fetchall()
            print("Away team to date xGF: " + str(away_xGf[0][0]))

            home_awayxG_query = "SELECT sum(xG) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE ConcededTeam = {} AND GameDate < '{}';".format(game[7], game[2])
            cursor.execute(home_awayxG_query)
            home_xGa = cursor.fetchall()
            print("Home team to date xGA: " + str(home_xGa[0][0]))

            away_homexG_query = "SELECT sum(xG) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE ConcededTeam = {} AND GameDate < '{}';".format(game[8], game[2])
            cursor.execute(away_homexG_query)
            away_xGa = cursor.fetchall()
            print("Away team to date xGA: " + str(away_xGa[0][0]))
            


        
    except mysql.connector.errors.IntegrityError:
        print("Id already exists")



