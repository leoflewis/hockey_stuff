import mysql.connector, requests, pandas as pd, numpy, math, os
from mysql.connector import Error
from joblib import load

def get_goals(date, home, away, cursor):
    home_awayxG_query = "SELECT count(*) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE EventTeam = {} AND GameDate < '{}' and EventName = 'GOAL';".format(home, date)
    cursor.execute(home_awayxG_query)
    home_xGf = cursor.fetchall()

    away_homexG_query = "SELECT count(*) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE EventTeam = {} AND GameDate < '{}' and EventName = 'GOAL';".format(away, date)
    cursor.execute(away_homexG_query)
    away_xGf = cursor.fetchall()

    home_awayxG_query = "SELECT count(*) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE ConcededTeam = {} AND GameDate < '{}' and EventName = 'GOAL';".format(home, date)
    cursor.execute(home_awayxG_query)
    home_xGa = cursor.fetchall()

    away_homexG_query = "SELECT count(*) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE ConcededTeam = {} AND GameDate < '{}' and EventName = 'GOAL';".format(away, date)
    cursor.execute(away_homexG_query)
    away_xGa = cursor.fetchall()
    hxgf = home_xGf[0][0]
    hxga = home_xGa[0][0]
    axgf = away_xGf[0][0]
    axga = away_xGa[0][0]
    if hxgf == None: hxgf = 0
    if hxga == None: hxga = 0
    if axgf == None: axgf = 0
    if axga == None: axga = 0
    homexGDiffToDate =  hxgf - hxga
    awayxGDiffToDate =  axgf - axga

    return homexGDiffToDate, awayxGDiffToDate

def get_shots(date, home, away, cursor):
    home_awayxG_query = "SELECT count(*) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE EventTeam = {} AND GameDate < '{}' and EventName = 'SHOT';".format(home, date)
    cursor.execute(home_awayxG_query)
    home_xGf = cursor.fetchall()

    away_homexG_query = "SELECT count(*) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE EventTeam = {} AND GameDate < '{}' and EventName = 'SHOT';".format(away, date)
    cursor.execute(away_homexG_query)
    away_xGf = cursor.fetchall()

    home_awayxG_query = "SELECT count(*) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE ConcededTeam = {} AND GameDate < '{}' and EventName = 'SHOT';".format(home, date)
    cursor.execute(home_awayxG_query)
    home_xGa = cursor.fetchall()

    away_homexG_query = "SELECT count(*) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE ConcededTeam = {} AND GameDate < '{}' and EventName = 'SHOT';".format(away, date)
    cursor.execute(away_homexG_query)
    away_xGa = cursor.fetchall()
    hxgf = home_xGf[0][0]
    hxga = home_xGa[0][0]
    axgf = away_xGf[0][0]
    axga = away_xGa[0][0]
    if hxgf == None: hxgf = 0
    if hxga == None: hxga = 0
    if axgf == None: axgf = 0
    if axga == None: axga = 0
    homexGDiffToDate =  hxgf - hxga
    awayxGDiffToDate =  axgf - axga

    return homexGDiffToDate, awayxGDiffToDate

def get_fenwick(date, home, away, cursor):
    home_awayxG_query = "SELECT count(*) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE EventTeam = {} AND GameDate < '{}';".format(home, date)
    cursor.execute(home_awayxG_query)
    home_xGf = cursor.fetchall()

    away_homexG_query = "SELECT count(*) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE EventTeam = {} AND GameDate < '{}';".format(away, date)
    cursor.execute(away_homexG_query)
    away_xGf = cursor.fetchall()

    home_awayxG_query = "SELECT count(*) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE ConcededTeam = {} AND GameDate < '{}';".format(home, date)
    cursor.execute(home_awayxG_query)
    home_xGa = cursor.fetchall()

    away_homexG_query = "SELECT count(*) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE ConcededTeam = {} AND GameDate < '{}';".format(away, date)
    cursor.execute(away_homexG_query)
    away_xGa = cursor.fetchall()
    hxgf = home_xGf[0][0]
    hxga = home_xGa[0][0]
    axgf = away_xGf[0][0]
    axga = away_xGa[0][0]
    if hxgf == None: hxgf = 0
    if hxga == None: hxga = 0
    if axgf == None: axgf = 0
    if axga == None: axga = 0
    homexGDiffToDate =  hxgf - hxga
    awayxGDiffToDate =  axgf - axga

    return homexGDiffToDate, awayxGDiffToDate

def get_xg(date, home, away, cursor):
    home_awayxG_query = "SELECT sum(xG) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE EventTeam = {} AND GameDate < '{}';".format(home, date)
    cursor.execute(home_awayxG_query)
    home_xGf = cursor.fetchall()

    away_homexG_query = "SELECT sum(xG) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE EventTeam = {} AND GameDate < '{}';".format(away, date)
    cursor.execute(away_homexG_query)
    away_xGf = cursor.fetchall()

    home_awayxG_query = "SELECT sum(xG) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE ConcededTeam = {} AND GameDate < '{}';".format(home, date)
    cursor.execute(home_awayxG_query)
    home_xGa = cursor.fetchall()

    away_homexG_query = "SELECT sum(xG) FROM GameEvent e JOIN Game on e.Game = Game.GameId WHERE ConcededTeam = {} AND GameDate < '{}';".format(away, date)
    cursor.execute(away_homexG_query)
    away_xGa = cursor.fetchall()
    hxgf = home_xGf[0][0]
    hxga = home_xGa[0][0]
    axgf = away_xGf[0][0]
    axga = away_xGa[0][0]
    if hxgf == None: hxgf = 0
    if hxga == None: hxga = 0
    if axgf == None: axgf = 0
    if axga == None: axga = 0
    homexGDiffToDate =  hxgf - hxga
    awayxGDiffToDate =  axgf - axga

    return homexGDiffToDate, awayxGDiffToDate


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


df = pd.DataFrame(columns=['homexGDiff','awayxGdiff','homeShotDiff','awayShotDiff', 'homeFenDiff', 'awayFenDiff', 'homeGoalDiff', 'awayGoalDiff', 'homeWin'])

if db.is_connected():
    get_games = "SELECT * FROM Game;"
    cursor = db.cursor()
    
    try:
        cursor.execute(get_games)
        games = cursor.fetchall()
        for game in games:
            homeWin = game[12]
            
            homexGDiffToDate, awayxGDiffToDate = get_xg(game[2], game[7], game[8], cursor)
            
            homeShotDiffToDate, awayShotDiffToDate = get_shots(game[2], game[7], game[8], cursor)
            
            homeGoalDiffToDate, awayGoalDiffToDate = get_goals(game[2], game[7], game[8], cursor)
            
            homefenDiffToDate, awayFenDiffToDate = get_fenwick(game[2], game[7], game[8], cursor)
            
            df.loc[len(df)]= [homexGDiffToDate, awayxGDiffToDate, homeShotDiffToDate, awayShotDiffToDate, homefenDiffToDate, awayFenDiffToDate, homeGoalDiffToDate, awayGoalDiffToDate, homeWin]
            print("added row for game: {}".format(game[0]))
        
        df.to_excel("GameData.xlsx")
            

            


        
    except mysql.connector.errors.IntegrityError:
        print("Id already exists")



