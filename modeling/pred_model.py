import requests, pandas as pd, numpy as np
from sklearn.linear_model import Ridge

from datetime import date

# Python program to get
# Yesterday's date
 
 
# Import date and timedelta class
# from datetime module
from datetime import date
from datetime import timedelta
 
# Get today's date
today = date.today()
print("Today is: ", today)
 
# Yesterday date
yesterday = today - timedelta(days = 1)
print("Yesterday was: ", yesterday)

response = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}".format(yesterday, yesterday)) #2022-10-09
for i in response.json()['dates']:
    for j in i['games']:
        print(j)
        print()