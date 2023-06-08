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

    plays = plays_data['liveData']['plays']['allPlays']
    shifts = shifts['data']

   
    count_plays = 0

    # New data frame and iterator for each game 
    single_game_corsi_for_shifts = pd.DataFrame(columns=('cf/60', 'duration', 'player'))
    i = 0

    penalty = False
    penalty_release = None
    penalty_release_period = None
    penalty_team = None

    # For each shift
    for shift in shifts:
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
        if shift_period < 5 and shift_team == 'MIN' and shift_code != 505 and shift_player_id != 8470594 and shift_player_id != 8479406:
            try:
                raw_shift_time = shift['duration'].split(':')
                mins = 0
                print(raw_shift_time)
                if raw_shift_time[0] == '00':
                    mins = 0
                else:
                    if raw_shift_time[0][0] == '0':
                        mins = (float(raw_shift_time[0][1]) * 60)
                    else:
                        #someone had a long shift
                        mins = float(raw_shift_time[0])
                seconds = float(raw_shift_time[1])
                shift_duration = float(mins + seconds)
                print(shift_duration)
            except:
                print("error")
            
            #...look for a play...
            for x in range(len(plays) -1):
                count_plays += 1
                play = plays[x]
                play_period = play['about']['period']
                play_time = float(play['about']['periodTime'].replace(":", "."))
                play_team = None
                play_type = play['result']['eventTypeId']
                try:
                    play_team = play['team']['triCode']
                except:
                    play_team = None


                #released by clock
                if (penalty and play_time <= penalty_release and play_period == penalty_release_period):
                    penalty = False
    
                #released by goal
                if play_type == GOAL and play_team != penalty_team and penalty and play_period == penalty_release_period:
                    penalty = False
                    if play_team == 'MIN':
                        shots_for -= 1
                    else:
                        shots_against -= 1


                if play_type == "PENALTY":
                    penalty_time = play['result']['penaltyMinutes']
                    if play_time - penalty_time >= 0:
                        penalty_release = play_time - penalty_time
                        penalty_release_period = play_period
                    else:
                        penalty_release = (play_time - penalty_time) + 20
                        penalty_release_period = play_period + 1
                    penalty = True
                    penalty_team = play['team']['triCode']

                if not penalty:
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
            cf_per_60 = (((shots_for - shots_against) / shift_duration) * 60) * 60
            name = shift['firstName'] + shift['lastName']
            
            single_game_corsi_for_shifts.loc[i] = [cf_per_60, shift_duration, name]

    # Append game dataframe to totals data frame
    total = total.append(single_game_corsi_for_shifts)


print(total)
total.to_excel("output.xlsx")  

        

    
