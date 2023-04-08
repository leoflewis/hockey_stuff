import requests, pandas as pd, numpy as npm, sys
from sklearn.linear_model import Ridge

#saw this on stack overflow. beautiful function    
def minutes_to_seconds(time):
    m, s= time.split(":")
    return (int(m) * 60) + int(s)

# Corsi shot types. For those unfamiliar, corsi is a funny name for any shot, even ones that miss and get blocked.
MISSED_SHOT = 'MISSED_SHOT'
SHOT = 'SHOT'
GOAL = 'GOAL'
BLOCK = 'BLOCK'

#total dataframe
total = pd.DataFrame(columns=('cf/60', 'duration', 'player'))

# For each game
games = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?teamId=30&season=20222023&gameType=R').json()
print(games['dates'][0])
x = 0
for date in games['dates']:
    
    game = date['games'][0]['gamePk']
    print(x)
    print("getting game " + str(game))
    plays_data = requests.get('http://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(game)).json()
    shifts = requests.get('https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={}'.format(game)).json()

    all_plays = plays_data['liveData']['plays']['allPlays']

    # Make a list of only shot plays
    plays = [x for x in all_plays if x['result']['eventTypeId'] == MISSED_SHOT or x['result']['eventTypeId'] == SHOT or x['result']['eventTypeId'] == GOAL or x['result']['eventTypeId'] == BLOCK]
    count_plays = 0

    # New data frame and iterator for each game 
    single_game_corsi_for_shifts = pd.DataFrame(columns=('cf/60', 'duration', 'player'))
    i = 0

    # For each shift
    for shift in shifts['data']:
        i += 1
        shift_player_id = shift['playerId']
        shift_player = shift['lastName']
        shift_period = shift['period']
        shift_start = float(shift['startTime'].replace(":", "."))
        shift_end = float(shift['endTime'].replace(":", "."))
        shift_code = shift['typeCode']
        shift_team = shift['teamAbbrev']

        shots_for = 0
        shots_against = 0
        # (ignoring shootouts)
        if shift_period < 5 and shift_team == 'MIN' and shift_code != 505 and (shift_player_id != 8470594 or shift_player_id != 8479406):
            try:
                shift_duration = float(shift['duration'].replace(":", "."))
            except:
                print("error")
            
            #...look for a play...
            for x in range(len(plays) -1):
                count_plays += 1
                play = plays[x]
                play_period = play['about']['period']
                play_time = float(play['about']['periodTime'].replace(":", "."))
                play_team = None
                play_team = play['team']['triCode']


                #...that happened during the shift.
                if play_period == shift_period and play_time >= shift_start and play_time <= shift_end:

                    play_type = play['result']['eventTypeId']
                
                    #If the play type was of type corsi...
                    if play_type == MISSED_SHOT or play_type == SHOT or play_time == GOAL:

                        #...mark it as for or against... 
                        if shift_team == play_team:
                            shots_for += 1
                        else:
                            shots_against += 1

                    #If the play type of was of type block...
                    elif play_type == BLOCK:
                        #...mark it as for or against...
                        if shift_team == play_team:
                            shots_against += 1
                        else:
                            shots_for += 1
            
            # Append row to game data frame 
            cf_per_60 = ((shots_for - shots_against) / shift_duration) * 60
            name = shift['firstName'] + shift['lastName']
            single_game_corsi_for_shifts.loc[i] = [cf_per_60, shift_duration, name]

    # Append game dataframe to totals data frame
    total = total.append(single_game_corsi_for_shifts)


print(total)
total.to_excel("output.xlsx")  

        

    
