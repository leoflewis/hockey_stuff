import mysql.connector, requests, pandas, numpy, math, os, csv
from mysql.connector import Error


def parse_data(db):
    cursor = db.cursor()
    sql = "SELECT * FROM Player;"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            id = row[0]
            response = requests.get("https://statsapi.web.nhl.com/api/v1/people/{}?expand=person.stats&expand=stats.team&stats=yearByYear&season=20222023&site=en_nhl".format(id)).json()
            if response['people'][0]['primaryPosition']['code'] != 'G':
                for stat in response['people'][0]['stats'][0]['splits']:
                    if stat['season'] == '20222023' and stat['league']['name'] == 'National Hockey League':
                        season = stat['season']
                        teamId = stat['team']['id']
                        toi = float(stat['stat']['timeOnIce'].replace(":", "."))
                        assists = stat['stat']['assists']
                        goals = stat['stat']['goals']
                        pim = stat['stat']['pim']
                        shots = stat['stat']['shots']
                        games = stat['stat']['games']
                        hits = stat['stat']['hits']
                        ppg = stat['stat']['powerPlayGoals']
                        ppp = stat['stat']['powerPlayPoints']
                        pptoi = float(stat['stat']['powerPlayTimeOnIce'].replace(":", "."))
                        evtoi = float(stat['stat']['evenTimeOnIce'].replace(":", "."))
                        fopct = stat['stat']['faceOffPct']
                        shotpct = stat['stat']['shotPct']
                        gwg = stat['stat']['gameWinningGoals']
                        otg = stat['stat']['overTimeGoals']
                        shg = stat['stat']['shortHandedGoals']
                        shp = stat['stat']['shortHandedPoints']
                        shtoi = float(stat['stat']['shortHandedTimeOnIce'].replace(":", "."))
                        blocks = stat['stat']['blocked']
                        pm = stat['stat']['plusMinus']
                        points = stat['stat']['points']
                        shifts = stat['stat']['shifts']
                        #print(str(id) + " " + str(season) + " " + str(teamId) + " " + str(toi) + " " + str(assists) + " " + str(goals) + " " + str(pim) + " " + str(shots) + " " + str(games) + " " + str(hits) + " " + str(ppg) + " " + str(ppp) + " " + str(pptoi) + " " + str(evtoi) + " " + str(fopct) + " " + str(shotpct) + " " + str(gwg) + " " + str(otg) + " " + str(shg) + " " + str(shp) + " " + str(shtoi) + " " + str(blocks) + " " + str(pm) + " " + str(points) + " " + str(shifts))
                        vals = (season, id, teamId, toi, assists, goals, pim, shots, games, hits, ppg, ppp, pptoi, evtoi, fopct, shotpct, gwg, otg, shg, shp, shtoi, blocks, pm, points, shifts)
                        insert = "INSERT INTO SeasonTotals(Season, PlayerId, TeamId, TOI, Assists, Goals, PenMinutes, Shots, GamesPlayed, Hits, PPGoals, PPPoints, PPTOI, EVTOI, FOPct, ShotPct, GWGoals, OTGoals, SHGoals, SHPoints, SHTOI, Blocks, PlusMinus, Points, Shifts) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        try:
                            cursor.execute(insert, vals)
                            db.commit()
                            print(sql)
                        except mysql.connector.errors.IntegrityError:
                            print("Error")


    except mysql.connector.errors.IntegrityError:
        print("Id already exists")


    # vals = ()
    # sql = "INSERT INTO SeasonTotals(TeamID, TeamName) VALUES(%s, %s)"

    # try:
    #     cursor.execute(sql, vals)
    #     db.commit()
    #     print(sql)
    # except mysql.connector.errors.IntegrityError:
    #     print("Id already exists")


def main():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user=os.environ.get("sql-user"),
            database=os.environ.get("sql-db"),
            password=os.environ.get("sql-password"),
            port=3306
        )
    except Error as e:
        print("Error while connecting to MySQL", e)

    if db.is_connected():
        print("You're connected to the database")
        parse_data(db)

if __name__ == "__main__":
    main()