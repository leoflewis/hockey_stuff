import pandas as pd

pbp = pd.read_csv('23_PBP_WHKYHAC_SPORTLOGIQ.csv', sep=',')

print(pbp)

print(pbp.columns)

xl = pd.ExcelFile('23_SUMMARY_WHKYHAC_SPORTLOGIQ.xlsx')
sheet1 = pd.read_excel(xl, 'SkatersPW')