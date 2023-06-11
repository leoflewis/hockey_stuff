import pandas as pd
from sklearn.linear_model import Ridge
import matplotlib.pyplot as plt
import numpy as np

pd.options.display.max_columns = None


f = pd.ExcelFile('23_SUMMARY_WHKYHAC_SPORTLOGIQ.xlsx')

pw = pd.read_excel(f,'SkatersPW')

pw['xG diff/60'] = ((pw['XGF WOI (AA Model)'] - pw['XGA WOI (AA Model)']) / (pw['TOI'] / 1000)) * 60

print(pw[['Player', 'TOI', 'XGF WOI (AA Model)', 'XGA WOI (AA Model)', 'xG diff/60']])

y = pw['xG diff/60']
x = pd.get_dummies(pw['Player'])
weight = pw['TOI']
rdg = Ridge(alpha=1)
rdg.fit(x, y, sample_weight=weight)

print(rdg.score(x, y))
print(rdg.coef_)
print(x.columns)
print(rdg.intercept_)

coef_table = pd.DataFrame(list(x.columns)).copy()
coef_table.insert(len(coef_table.columns),"Coefs",rdg.coef_.transpose())

print(coef_table.sort_values(by=['Coefs']))

std = coef_table['Coefs'].std()
avg = coef_table['Coefs'].mean()

coef_table['z_Score'] = (coef_table['Coefs'] - avg) / std
coef_table['color'] = np.where(coef_table['z_Score'] > 0, 'blue', 'red')
print(coef_table.sort_values(by=['Coefs']))

df = pd.DataFrame(coef_table[[0,'z_Score']])

ax = df.plot.bar(x=0, y='z_Score', color=coef_table['color'], rot=0)
plt.xticks(rotation='vertical')
plt.show()