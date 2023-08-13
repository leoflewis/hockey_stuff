import requests, pandas as pd, numpy, math, os
from joblib import load
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import log_loss


df = pd.read_excel("GameData.xlsx")
df = df.drop(df.columns[[0]], axis=1)  

x = df[["homexGDiff", "awayxGdiff",  "homeShotDiff",  "awayShotDiff",  "homeFenDiff",  "awayFenDiff",  "homeGoalDiff",  "awayGoalDiff"]]
y = df["homeWin"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

print(x_train)
print(y_train)

model = LogisticRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
loss = log_loss(y_test, model.predict_proba(x_test))
print(cnf_matrix)
print(loss)
print(y_pred)
print(y_test)