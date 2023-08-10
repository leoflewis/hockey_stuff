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
            home_homexG_query = "SELECT sum(HomeXG) FROM Game WHERE HomeTeam = {} AND GameDate < '{}';".format(game[7], game[2])
            cursor.execute(home_homexG_query)
            home_homexG = cursor.fetchall()
            print(home_homexG[0][0])
            
            #home_awayxG_query = "SELECT sum(xg) FROM GameEvent WHERE AwayTeam = {} AND GameDate < {}".format(game[7], game[2])
            #away_awayxG_query = "SELECT sum(xg) FROM GameEvent WHERE AwayTeam = {} AND GameDate < {}".format(game[8], game[2])
            #away_homexG_query = "SELECT sum(xg) FROM GameEvent WHERE HomeTeam = {} AND GameDate < {}".format(game[8], game[2])
            print(home_homexG_query)
            #print(home_awayxG_query)
            #print(away_awayxG_query)
            #print(away_homexG_query)
            home_homexG = cursor.fetchall()
            print(home_homexG[0][0])
            


        
    except mysql.connector.errors.IntegrityError:
        print("Id already exists")



