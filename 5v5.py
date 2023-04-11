import requests

game = 2022021244
print("getting game " + str(game))
plays_data = requests.get('http://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(game)).json()

MISSED_SHOT = 'MISSED_SHOT'
SHOT = 'SHOT'
GOAL = 'GOAL'
BLOCK = 'BLOCK'

all_plays = plays_data['liveData']['plays']['allPlays']
count_plays = 0

away_team = plays_data['gameData']['teams']['away']['triCode']
home_team = plays_data['gameData']['teams']['home']['triCode']


home_shots_for = 0
away_shots_for = 0

home_shots_against = 0
away_shots_against = 0
penalty = False
penalty_release = None
penalty_release_period = None
penalty_team = None

for x in range(len(all_plays) -1):
    play = all_plays[x]

    play_period = play['about']['period']
    play_time = float(play['about']['periodTimeRemaining'].replace(":", "."))
    play_team = None
    

    play_type = play['result']['eventTypeId']

    try:
        play_team = play['team']['triCode']
    except:
        play_team = None

    #released by clock
    if (penalty and play_time <= penalty_release and play_period == penalty_release_period):
        penalty = False
        print("released at " + str(play_time) + " in " + str(play_period))
    
    #released by goal
    if play_type == GOAL and play_team != penalty_team and penalty and play_period == penalty_release_period:
        penalty = False
        print("released at " + str(play_time) + " in " + str(play_period))
        if home_team == play_team:
            home_shots_for -= 1
        if away_team == play_team:
            away_shots_for -= 1



    if play_type == "PENALTY":
        penalty_time = play['result']['penaltyMinutes']
        if play_time - penalty_time >= 0:
            penalty_release = play_time - penalty_time
            penalty_release_period = play_period
        else:
            penalty_release = (play_time - penalty_time) + 20
            penalty_release_period = play_period + 1
        print(play['result']['description'] + " at " + str(play_time) + " in " + str(play_period))
        penalty = True
        penalty_team = play['team']['triCode']


    if not penalty:
        if play_type == SHOT or play_type == GOAL:
            play_team = play['team']['triCode']
            
            if home_team == play_team:
                home_shots_for += 1
            if away_team == play_team:
                away_shots_for += 1



print(home_team + " 5 on 5 shots " + str(home_shots_for))
print(away_team + " 5 on 5 shots " + str(away_shots_for))