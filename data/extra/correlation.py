import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
import numpy
from sklearn import metrics

leo_data = pd.read_csv('team_xG_results.csv')
nst_whole_data = pd.read_csv('games.csv')
nst_data = nst_whole_data[['Team', 'Points', 'xGF', 'xGA', 'GF','GA', 'SF', 'SA', 'FF', 'FA', 'CF', 'CA']]
nst_data['xG_diff'] = nst_data['xGF'] - nst_data['xGA']
nst_data['G_diff'] = nst_data['GF'] - nst_data['GA']
nst_data['S_diff'] = nst_data['SF'] - nst_data['SA']
nst_data['F_diff'] = nst_data['FF'] - nst_data['FA']
nst_data['C_diff'] = nst_data['CF'] - nst_data['CA']
# print(nst_data)
# print(leo_data)

data = leo_data.set_index("TeamName").join(nst_data.set_index("Team"))
 

fig = plt.figure()
# fig2 = plt.figure()
ax1 = fig.add_subplot()
# ax2 = fig2.add_subplot()

ax1.scatter(x=data['Total'], y=data['xGF'], c='r', label='leo xG vs NST xG')
# ax2.scatter(x=data['xGF'], y=data['Total'], c='r', label='leo vs nst')
# ax1.scatter(x=data['Points'], y=data['xGF'], c='b', label='NST xG')
# ax1.scatter(x=data['Points'], y=data['GF'], c='g', label='GF')
# data=data.sort_values(by=['Total'])
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(data)
plt.legend(loc='upper left')
plt.xlabel("Leo xG")
plt.ylabel("NST xG")
plt.show()
x = numpy.array(data['Total']).reshape(-1, 1)
leo_xg_points = linear_model.LinearRegression()
leo_xg_points.fit(x, data['Points'])
print("leo xGF score: " + str(leo_xg_points.score(x, data['Points'])))

x = numpy.array(data['xGF']).reshape(-1, 1)
nst_xg_points = linear_model.LinearRegression()
nst_xg_points.fit(x, data['Points'])
print("nst xGF score: " + str(nst_xg_points.score(x, data['Points'])))

x = numpy.array(data['xG_diff']).reshape(-1, 1)
nst_xg_diff_points = linear_model.LinearRegression()
nst_xg_diff_points.fit(x, data['Points'])
print("xG diff score: " + str(nst_xg_diff_points.score(x, data['Points'])))

x = numpy.array(data['G_diff']).reshape(-1, 1)
nst_g_diff_points = linear_model.LinearRegression()
nst_g_diff_points.fit(x, data['Points'])
print("Goal diff score: " + str(nst_g_diff_points.score(x, data['Points'])))

x = numpy.array(data['S_diff']).reshape(-1, 1)
nst_s_diff_points = linear_model.LinearRegression()
nst_s_diff_points.fit(x, data['Points'])
print("Shot diff score: " + str(nst_s_diff_points.score(x, data['Points'])))

x = numpy.array(data['C_diff']).reshape(-1, 1)
nst_c_diff_points = linear_model.LinearRegression()
nst_c_diff_points.fit(x, data['Points'])
print("Corsi diff score: " + str(nst_c_diff_points.score(x, data['Points'])))

x = numpy.array(data['F_diff']).reshape(-1, 1)
nst_f_diff_points = linear_model.LinearRegression()
nst_f_diff_points.fit(x, data['Points'])
print("Fenwick diff score: " + str(nst_f_diff_points.score(x, data['Points'])))

x = data[['G_diff', 'xG_diff']]
g_xg_diff_points = linear_model.LinearRegression()
g_xg_diff_points.fit(x, data['Points'])
print("Goal diff + xG diff score: " + str(g_xg_diff_points.score(x, data['Points'])))

x = data[['G_diff', 'xGF']]
g_xg_diff_points = linear_model.LinearRegression()
g_xg_diff_points.fit(x, data['Points'])
print("Goal diff + NST xGF score: " + str(g_xg_diff_points.score(x, data['Points'])))

x = data[['G_diff', 'Total']]
g_xg_diff_points = linear_model.LinearRegression()
g_xg_diff_points.fit(x, data['Points'])
print("Goal diff + Leo xGF score: " + str(g_xg_diff_points.score(x, data['Points'])))

x = data[['G_diff', 'S_diff']]
g_s_diff_points = linear_model.LinearRegression()
g_s_diff_points.fit(x, data['Points'])
print("Goal diff + Shot diff score: " + str(g_s_diff_points.score(x, data['Points'])))

x = numpy.array(data['Total']).reshape(-1, 1)
leo_xg_nst_xg = linear_model.LinearRegression()
leo_xg_nst_xg.fit(x, data['xGF'])
print("leo xG vs NST xG score: " + str(leo_xg_nst_xg.score(x, data['xGF'])))