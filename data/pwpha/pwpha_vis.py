import pandas as pd

pbp = pd.read_csv('23_PBP_WHKYHAC_SPORTLOGIQ.csv', sep=',')

print(pbp)

print(pbp.columns)

shots = pbp.loc[pbp['eventname'] == 'shot'] 
print(shots['xg_all_attempts'])
print(shots['xg_all_attempts'].max())
for col in pbp:
    print(col)
    print(pbp[col].unique())
xl = pd.ExcelFile('23_SUMMARY_WHKYHAC_SPORTLOGIQ.xlsx')
sheet1 = pd.read_excel(xl, 'SkatersPW')