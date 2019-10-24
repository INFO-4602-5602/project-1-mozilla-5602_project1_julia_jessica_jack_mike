import os 
import pandas as pd
import datetime as dt
from difflib import SequenceMatcher


data_fname = '20171013111831-SurveyExport.csv'

# add dtypes clarification to make this less memory intensive
# https://stackoverflow.com/questions/24251219/pandas-read-csv-low-memory-and-dtype-options

# not sure that the following actually is the correct encoding...
data = pd.read_csv(data_fname,header = [0],encoding='ISO-8859-1')
##data = pd.read_csv(data_fname)


for i in data.columns:
    print(i)
