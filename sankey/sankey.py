import os
import numpy as np
import pandas as pd
import holoviews as hv
from holoviews import opts, dim
from bokeh.models.mappers import LinearColorMapper

# Set up holoviews extension
hv.extension('bokeh')

# Load Survey data into Panas Dataframe
surveyData = pd.read_pickle('../Survey_Results_Clean.pkl')

# Grab Tech Savviness and Future outlook columns
df2 = surveyData[['Tech Savviness','Feelings about Future',
                  'Price','Features','Safety',
                  'Security','Privacy','Reliability','User Reviews',
                  'Expert Recommendation','Friend or Family Recommendation',
                  'Convenience']]

# Throw away incomplete responses
df2 = df2[(df2 != 0).all(1)].astype("uint8")

numResponses = df2.shape[0]

# Lookup table for responses
savvinessTable = ['Luddite','Average User','Technically Savvy','Ultra Nerd']
optimismTable = ['Scared as Hell','A Little Wary','On the Fence','Cautiously Optimistic','Super Excited!']
importances = list(df2)[2:]

fearTable = savvinessTable + optimismTable
rankTable = savvinessTable + importances
# Generate graph nodes
vdims = [('label','type')]
fearNodes = hv.Dataset(enumerate(fearTable), 'index', vdims)
rankNodes = hv.Dataset(enumerate(rankTable), 'index', vdims)

# Generate graph edges
fearEdges = []
for i in range(4):
    for j in range(5):
        count = df2[df2['Tech Savviness'] == i+1]
        count = 100 * count[count['Feelings about Future'] == j+1].shape[0] / float(numResponses)
        fearEdges.append([i,j+4,count])

rankEdges = []
for i in range(4):
    for j in range(10):
        count = df2[df2['Tech Savviness'] == i+1]
        count = 100 * count[count[importances[j]] == 1].shape[0] / float(numResponses)
        rankEdges.append([i,j+4,count])

choices = ['Fear Level','Importance Rankings']
jankyCmap = ['#d62728','#1f77b4','#2ca02c','#9467bd','#969696','#969696','#969696','#969696','#969696','#969696','#969696','#969696','#969696','#969696']

# Generate directed acyclic graphs for sankey plots
def generateGraph(choice):
    value_dim = hv.Dimension('Percentage', unit='%')
    if choice == 'Fear Level':
        sankey = hv.Sankey((fearEdges,fearNodes), ['From','To'], vdims=value_dim)
        sankey.opts(title='How Tech Savviness Influences Fear of Connectivity')
    elif choice == 'Importance Rankings':
        sankey = hv.Sankey((rankEdges,rankNodes), ['From','To'], vdims=value_dim)
        sankey.opts(title='How Tech Savviness Influences ')
    sankey.opts(labels='label',
                width=1000,
                height=900,
                cmap=jankyCmap,
                edge_color=dim('From').str(),
                fontsize={'title': 18, 'labels': 16},
                node_hover_fill_color='grey')
    return sankey

# Create Holomap
dag_dict = {c:generateGraph(c) for c in choices}
hmap = hv.HoloMap(dag_dict, kdims='Metric')

# Save html file
hv.save(hmap,'sankey.html')
