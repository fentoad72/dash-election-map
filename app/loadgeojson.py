import dash
#import dash_html_components as html
#import dash_html_components as dbc
#import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
import dash_leaflet as dl
from dash.dependencies import Input, Output,State
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import base64
import datetime
import io
import numpy as np

file = '/Users/arbetter/Coding/Streamlit/coloradovoters/co_counties_voters.geojson'

with open(file) as voterdata:
    counties = json.load(voterdata)

counties_gdf = gpd.read_file(file)

print(counties["features"][0])

print(type(counties))

print('cent_lat',type(counties_gdf['CENT_LAT']))

print(counties_gdf.head(10))

print(counties_gdf.columns)

counties_gdf['Republicans'] = counties_gdf['Republicans'].astype(float)
counties_gdf['Democrats'] = counties_gdf['Democrats'].astype(float)
counties_gdf['Unaffiliated'] = counties_gdf['Unaffiliated'].astype(float)

counties_gdf['Total'] = counties_gdf['Republicans'] + counties_gdf['Democrats'] + counties_gdf['Unaffiliated']
counties_gdf['Total'] = counties_gdf['Total']/5000.

px.set_mapbox_access_token(open(".mapbox_token").read())

point = [-105,40]

fig = px.scatter_mapbox(lat=[point[1]], lon=[point[0]]).update_layout(
        mapbox={
            "style":"open-street-map",
            "zoom":7,
            "layers":[
                {   
                    "source": json.loads(counties_gdf.geometry.to_json()),
                    "below":"traces",
                    "type":"line",
                    "color":"purple",
                    "line":{"width": 1.5}
                }
            ],
        },
        margin={"l":0,"r":0,"t":0,"b":0},
    )


lats = counties_gdf['CENT_LAT']
lons = counties_gdf['CENT_LONG']
sizes = counties_gdf['Total']
for i in range(0,len(sizes)):
    sizes[i] = min(sizes[i],250)
    sizes[i] = max(10,sizes[i])
    print('s=',sizes[i])

colors = []
color_key = ["blue","lightblue","grey","pink","red"]
for i in range(0,len(counties_gdf['Max'])):
    m = int(counties_gdf['Max'][i])
    print('i=',i,' m=',m,color_key[m])
    colors.append(color_key[m])

labels = []
reps = counties_gdf['Republicans'].astype(int).astype(str)
uafs = counties_gdf['Unaffiliated'].astype(int).astype(str)
dems = counties_gdf['Democrats'].astype(int).astype(str)
for i in range(0,len(counties_gdf['LABEL'])):
    labels.append(counties_gdf['LABEL'][i] + '\nRep: '+reps[i] + '\nUAF: '+uafs[i]+'\nDems: '+dems[i])

print('lat',type(lats),'lon',type(lons))

fig.add_scattermapbox(lat=lats,lon=lons,mode='markers+text',text=labels,
                      marker_size=sizes,marker_color=colors, below='')

fig.update_traces(line=dict(width=3, color='black'))

#fig.write_image("co_voters.png")
fig.show()
