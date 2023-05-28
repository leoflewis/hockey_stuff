import pandas as pd
import matplotlib.pyplot as plt

leo_data = pd.read_csv('leo_xG_results.csv')
nst_whole_data = pd.read_csv('Player Season Totals - Natural Stat Trick.csv')
nst_data = nst_whole_data[['Player', 'ixG']]
print(nst_data[['Player', 'ixG']])
print(leo_data)

data = leo_data.set_index("PlayerName").join(nst_data.set_index("Player"))
#data = all_data[['Total', 'ixG']] 
data.plot.scatter(x='Total', y='ixG')
data=data.sort_values(by=['Total'])
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(data)

plt.show()