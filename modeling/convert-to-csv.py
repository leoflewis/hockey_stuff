#importing pandas as pd
import pandas as pd
  
# Read and store content
# of an excel file 
read_file = pd.read_excel ("apm-data.xlsx")
  
# Write the dataframe object
# into csv file
read_file.to_csv ("apm-data.csv", 
                  index = None,
                  header=True)