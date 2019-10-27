import os
import numpy as np
import pandas as pd
import holoviews as hv
from holoviews import opts, dim

# Set up holoviews extension
hv.extension('bokeh')

# Load Survey data into Panas Dataframe
surveyData = pd.read_csv('../Survey_Results_Clean_UTF8.csv')

# Grab Tech Savviness and Future outlook columns
df2 = surveyData[['Tech Savviness','Feelings about Future']]

# Throw away incomplete responses
df2 = df2[(df2 != 0).all(1)]

# Lookup table for responses
savvinessTable = ['Luddite','Average User','Technically Savvy','Ultra Nerd']
futureTable = ['Scared as Hell','A Little Wary','On the Fence','Cautiosuly Optomistic','Super Excited!']

# Reorganize into directed acyclic graph for Sankey plot
dag = []
for i in range(4):
    for j in range(5):
        count = df2[df2['Tech Savviness'] == i+1][df2['Feelings about Future'] == j+1].shape[0]
        dag.append([savvinessTable[i],futureTable[j],count])

# Make Sankey plot
sankey = hv.Sankey(dag)

# Save html file
hv.save(sankey,'sankeytest.html')
