import hockey_scraper, pandas as pd

data = hockey_scraper.scrape_seasons([2022], False, data_format='Pandas')

print(data['pbp'].columns)

clean_data = pd.DataFrame(data['pbp']).drop(['Date', 'Away_Goalie', 'Description', 'Home_Score', 'Away_Goalie', 'Away_Goalie_Id','Home_Goalie', 'Home_Goalie_Id', 'xC', 'yC', 'Home_Coach','Away_Coach',  'awayPlayer1_id',  'awayPlayer2_id','awayPlayer3_id', 'awayPlayer4_id','awayPlayer5_id',  'awayPlayer6_id','homePlayer1_id', 'homePlayer2_id','homePlayer3_id', 'homePlayer4_id','homePlayer5_id', 'homePlayer6_id', 'p1_name', 'p1_ID', 'p2_name', 'p2_ID', 'p3_name', 'p3_ID'], axis=1)

clean_data = clean_data[ (clean_data.Event == 'SHOT') | (clean_data.Event == 'MISS')]

clean_data = clean_data[(clean_data.Strength == '5x5')]


clean_data.to_excel("apm-data.xlsx") 