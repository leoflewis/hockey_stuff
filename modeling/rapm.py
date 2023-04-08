import requests, pandas as pd, numpy as np

MISSED_SHOT = 'MISSED_SHOT'
SHOT = 'SHOT'
GOAL = 'GOAL'
BLOCK = 'BLOCK'

game = 2022021018

plays = requests.get('http://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(game)).json()
shifts = requests.get('https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={}'.format(game)).json()

#For each shift
for shift in shifts['data']:
    shift_period = shift['period']
    shift_start = float(shift['startTime'].replace(":", "."))
    shift_end = float(shift['endTime'].replace(":", "."))

    shift_team = shift['teamAbbrev']

    shots_for = 0
    shots_against = 0

    #...look for a play...
    for play in plays['liveData']['plays']['allPlays']:
        play_period = play['about']['period']
        play_time = float(play['about']['periodTime'].replace(":", "."))
        play_team = play['team']['triCode']

        #...that happened during the shift.
        if play_period == shift_period and play_time >= shift_start and play_time <= shift_end:

            play_type = play['result']['eventTypeId']
            #If the play type of corsi...
            if play_type == MISSED_SHOT or play_type == SHOT or play_time == GOAL:

                #...mark it as for or against... 
                if shift_team == play_team:
                    shots_for += 1
                else:
                    shots_against += 1
            
            #If the play type of corsi...
            if play_type == BLOCK:
                #...mark it as for or against...
                if shift_team == play_team:
                    shots_against += 1
                else:
                    shots_for += 1


    
