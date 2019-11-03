import geopandas as gpd
import json
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
from bokeh.io import curdoc
from bokeh.models import Slider, HoverTool
from bokeh.layouts import widgetbox, row, column, gridplot
from bokeh.models import CustomJS, ColumnDataSource
from math import pi
import copy
import math


# --------- my data loading and prep
string_reps = {'1': 'Scared as hell. The future where everything is connected has me scared senseless. Were all doomed!',
               '2': 'A little wary. All this being connected to the internet in every part of our lives makes me a little nervous. Whats going to happen to our privacy?' ,
               '3': 'On the fence.  Im not sure about all this. I think Ill wait and see.',
               '4': 'Cautiously optimistic. Im hopeful were building a better world by becoming more connected in everything we do.',
               '5': 'Super excited! I cant wait for everything to be connected. My life will be so much better.'}
string_reps_abrev = {'1': 'Scared as hell.',
               '2': 'A little wary.' ,
               '3': 'On the fence.',
               '4': 'Cautiously optimistic.',
               '5': 'Super excited!'}
import pandas as pd
# Load Survey data into Panas Dataframe
surveyData = pd.read_csv('Survey_Results_Clean_UTF8.csv')

data_dict = {}
for country in surveyData['Country or Region'].unique():
    d = surveyData.loc[surveyData['Country or Region']==country,'Feelings about Future']
##    print(country,' mode:',d.mode())
    if len(d.value_counts()) > 0:
        if d.value_counts().index[0] != 0:
##            print(country,' mode response: ',string_reps[str(d.value_counts().index[0])])
            mr = d.value_counts().index[0] # storing in numeric encoding
        else:
##            print(country,' mode response: ',string_reps[str(d.value_counts().index[1])])
            mr = d.value_counts().index[0] # storing in numeric encoding
        data_dict[country] = [mr, {}]
        for i in d.value_counts().index:
            if i != 0:
                data_dict[country][1][string_reps_abrev[str(i)]] = d.value_counts()[i]
    else:
        print(country, ' mode response came back empty')
##    break
# --------- end of 

shapefile = 'countries_110m/ne_110m_admin_0_countries.shp'
#Read shapefile using Geopandas
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
#Rename columns.
gdf.columns = ['country', 'country_code', 'geometry']
gdf.head()

#Drop row corresponding to 'Antarctica'
gdf = gdf.drop(gdf.index[159])


datafile = 'share-of-adults-defined-as-obese.csv'
#Read csv file using pandas
df = pd.read_csv(datafile, names = ['entity', 'code', 'year', 'per_cent_obesity'], skiprows = 1)
df[df['code'].isnull()]
##df[df['code'].isnan()]

######### matching
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).quick_ratio()

def best_guess(a, cntry_list):
    best = 0
    possibles = []
    for ct in cntry_list:
        score = similar(a,ct)
        if score > best:# and (score > 0.25)):
            best = score
            possibles = []
            possibles.append(ct)
    if len(possibles) == 0:
        possibles.append('NO MATCH')
    return possibles, score

# loop over medium data countries key entries
new_data_dict = copy.deepcopy(data_dict)
for ct in data_dict.keys():
    bg, score = best_guess(ct, gdf.country.tolist()) # find most similar in the geoson data
    if ct == 'United States':
        bg = ['United States of America']
        new_data_dict[bg[0]] = new_data_dict.pop(ct)
        
    if ct == bg[0]: # this is dumb I don't actually add any
        new_data_dict[bg[0]] = new_data_dict.pop(ct) # replace the medium data key with the new country key
    else:
        if ct != 'United States':
            new_data_dict.pop(ct)
        # could improve later
##        else: pass # dropping
##    elif len(bg) > 1:
##        print('MULTIPLES       ',ct, bg, score)
##    else:
##        print(ct, ' No match')
        
ndf = pd.concat([df['entity'],df['code']],axis=1)
ndf.drop_duplicates()

# add a country code to medium data dict
codes_list = []
year_list = []
dat_list = []
pop_list = []
entitiesL = list(new_data_dict.keys())
for v in range(len(new_data_dict.values())):
    if entitiesL[v] == 'United States of America':
        tmp = 'United States'
    else: tmp = entitiesL[v]
    try:
        cde = ndf[ndf['entity'].str.match(tmp)].values[0][1]
        codes_list.append(cde)
        year_list.append(int(2016)) # bogus
    ##    print(entitiesL[v],' success')
        dat_list.append(float(new_data_dict[entitiesL[v]][0]))
    except IndexError:
        new_data_dict.pop(entitiesL[v])
        pop_list.append(v)
        
##        print(entitiesL[v],' fail')
        pass
#######
for p in pop_list:
    entitiesL.pop(p)

replace_dat = pd.DataFrame()
replace_dat.insert(0,"entity",entitiesL)
replace_dat.insert(1,"code",codes_list)
replace_dat.insert(2,"year",year_list)
replace_dat.insert(3,"mode_fear_response",dat_list) # lieing about the title for now

code_name = pd.DataFrame(replace_dat['entity'])
code_name['code'] = replace_dat['code']
#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][5]
#Reverse color order so that dark blue is highest mode fear response.
palette = palette[::-1]


cdkeys = code_name['entity'].tolist()
cdvals = code_name['code'].tolist()
##code_name_dict = dict(zip(keys, vals))

##print(new_data_dict.keys())
kls = list(new_data_dict.keys())
for r in range(len(cdkeys)):
    try:
##        print(cdkeys[r])
        new_data_dict[cdvals[r]] = new_data_dict.pop(kls[r])
    except KeyError:
        print('key error...')
        pass
##    code_name['entity'] list(new_data_dict.keys())[r]
##print(new_data_dict.keys())
merged = gdf

from bokeh.layouts import column, row
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum

# data for pie chart needs to be in a dict, value, angle, color
def pie_dat(data):
    data = pd.Series(data).reset_index(name='value').rename(columns={'index':'country'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(data)]
    ndata = {}
    for c in range(len(data.columns.to_list())):
        ndata[data.columns[c]]=data[data.columns[c]].to_list()  
    return ndata

# add pie data to the new_data_dict
pop_list = []
for k in list(new_data_dict.keys()):
    if len(new_data_dict[k][1]) == 5:
        new_data_dict[k].append(pie_dat(new_data_dict[k][1]))
        try:
            if not math.isnan(k):
                new_data_dict[k].append(code_name[code_name['code']==k].entity.to_list()[0])
        except TypeError: new_data_dict[k].append(code_name[code_name['code']==k].entity.to_list()[0])
    else:
        print('skipping country: ',k)
        pop_list.append(k)
    try:
        if math.isnan(k): pop_list.append(k)
    except TypeError: pass
        
for k in pop_list:
    new_data_dict.pop(k)

x = new_data_dict['CAN'][1] # whats actually being plotted in the pie chart

source = ColumnDataSource(data=new_data_dict['CAN'][2])

inds = []

#Define function that returns json_data for year selected by user.

def json_data(selectedYear):
    global inds
    yr = selectedYear
##    df_yr = df[df['year'] == yr]
    df_yr = replace_dat[replace_dat['year'] == yr]
    merged = gdf.merge(df_yr, left_on = 'country_code', right_on = 'code', how = 'left')
    inds = merged['country_code'].tolist()
##    merged.fillna('No data', inplace = True)
    merged_json = json.loads(merged.to_json())
    json_data = json.dumps(merged_json)
    return json_data
#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = json_data(2016))
#Define a sequential multi-hue color palette.

##get_ind = gdf.merge(replace_dat[replace_dat['year'] == 2016], left_on = 'country_code', right_on = 'code', how = 'left')

##get_ind = pd.merge(replace_dat[replace_dat['year'] == 2016], left_on = 'country_code', right_on = 'code', how = 'left')


code="""
    if (cb_data.index.indices != null) {
    hovered_index = cb_data.index.indices[0];
    title.text = new_data_dict[inds[hovered_index]][3]
    source.data = new_data_dict[inds[hovered_index]][2]
    source.change.emit();
    }

"""

#######pie 
p3 = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
           tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

p3.wedge(x=0, y=1, radius=0.4,
         start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
         line_color="white", fill_color='color', legend='country', source=source)

p3.axis.axis_label=None
p3.axis.visible=False
p3.grid.grid_line_color = None
#######pie

hover_callback = CustomJS(args=dict(x=x,source=source,new_data_dict=new_data_dict,inds=inds,title=p3.title), code = code)

##hover_callback = CustomJS(args=dict(x=x,new_data_dict=new_data_dict,inds=inds), code = code)
##print('ahsdflasfd')

#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
color_mapper = LinearColorMapper(palette = palette, low = 1, high = 5, nan_color = '#d9d9d9')
#Define custom tick labels for color bar.

tick_labels = {'1': string_reps_abrev['1'], '2': string_reps_abrev['2'], '3':string_reps_abrev['3'], '4':string_reps_abrev['4'], '5':string_reps_abrev['5']}

#Add hover tool
hover = HoverTool(callback = hover_callback, tooltips = [ ('Country','@country'),('our key', '@mode_fear_response')])
##hover = HoverTool(tooltips = [ ('Country/region','@country'),('our key', '@per_cent_obesity')])

#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
#Create figure object.
p = figure(title = 'Mode fear response', plot_height = int(600/1.25) , plot_width = int(950/1.25), toolbar_location = None, tools = [hover])
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.axis.visible=False
#Add patch renderer to figure. 
p.patches('xs','ys', source = geosource,fill_color = {'field' :'mode_fear_response', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)
#Specify layout
p.add_layout(color_bar, 'below')



# Define the callback function: update_plot
def update_plot(attr, old, new):
##    yr = slider.value
    yr = 2016
    new_data = json_data(yr)
    geosource.geojson = new_data
    p.title.text = 'Share of adults who are obese, %d' %yr
    
# Make a slider object: slider 
slider = Slider(title = 'Year',start = 1975, end = 2016, step = 1, value = 2016)
slider.on_change('value', update_plot)
# Make a column layout of widgetbox(slider) and plot, and add it to the current document




##layout = row(p,widgetbox(slider),p3)
##layout = row(p,p3)
layout = gridplot([[p,p3], [None, None]])
curdoc().add_root(layout)
##show(row(p,p3))
