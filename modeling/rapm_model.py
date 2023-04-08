import pandas as pd
from sklearn.linear_model import Ridge
df = pd.read_excel('output.xlsx')
y = df['cf/60']
x = pd.get_dummies(df['player'])
weight=df['duration']
print(y)
print(x)
print(weight)
rdg = Ridge(alpha=1)
rdg.fit(x, y, sample_weight=weight)
print(rdg.score(x, y))
print(rdg.coef_)
print(x.columns)
print(rdg.intercept_)

coef_table = pd.DataFrame(list(x.columns)).copy()
coef_table.insert(len(coef_table.columns),"Coefs",rdg.coef_.transpose())

print(coef_table.sort_values(by=['Coefs']))