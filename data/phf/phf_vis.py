import pandas as pd

pbp = pd.read_csv('23_PBP_WHKYHAC_SPORTLOGIQ.csv', sep=',')

print(pbp.columns)

summ = pd.read_excel('23_SUMMARY_WHKYHAC_SPORTLOGIQ.xlsx')

print(summ.columns)