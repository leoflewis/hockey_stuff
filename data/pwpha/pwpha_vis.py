import pandas as pd

pbp = pd.read_csv('23_PBP_WHKYHAC_SPORTLOGIQ.csv', sep=',')

print(pbp)

print(pbp.columns)

shots = pbp.loc[pbp['eventname'] == 'shot'] 
print(shots)
for col in pbp:
    print(col)
    print(pbp[col].unique())
