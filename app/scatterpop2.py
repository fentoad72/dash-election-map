import dash
#import dash_html_components as html
#import dash_html_components as dbc
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash import html
import dash_leaflet as dl
from dash.dependencies import Input, Output
import pandas as pd
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
print(us_cities.head())
import plotly.express as px

def make_map(lat,lon):
    print(type(lat))
    d = {"latitude" : lat,
         "longitude" : lon,
        "address" : "my address"
        }
    df = pd.DataFrame().append(d, ignore_index=True)        
    
    print("df")
    print(df)
    fig = px.scatter_mapbox(
        df,  # Our DataFrame
        lat = "latitude",
        lon = "longitude",
        center = {"lat": lat , "lon": lon},  # where map will be centered
        width = 600,  # Width of map
        height = 600,  # Height of map
        zoom = 16,
        hover_data = ["address"],  # what to display when hovering mouse over coordinate
    )

    fig.update_layout(mapbox_style="open-street-map") # adding beautiful street layout to map
    fig.update_layout(margin={"r":0,"t":0,"l":50,"b":0})
    return fig

app = dash.Dash(prevent_initial_callbacks=True)
lat = 39.7392
lon = -104.9903
fig = make_map(lat, lon)

app.layout = html.Div([
    html.Div([html.H1('Map')], style={'textAlign': 'center'}),
    dcc.Graph(figure=fig),
])

if __name__ == '__main__':
    app.run_server()
"""
html.Div(dl.Map([dl.TileLayer(), cluster], center=(40, -105), zoom=14, id="map",
                    style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})),
                      html.Div(id='clickdata') 
                      """   