import dash
#import dash_html_components as html
#import dash_html_components as dbc
import dash_bootstrap_components as dbc
from dash import html
import dash_leaflet as dl
from dash.dependencies import Input, Output
import pandas as pd
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
print(us_cities.head())
import plotly.express as px

positions = [(40, -105)]
markers = [dl.Marker(dl.Tooltip("test"), position=pos, id="marker{}".format(i)) for i, pos in enumerate(positions)]
cluster = dl.MarkerClusterGroup(id="markers", children=markers, options={"polygonOptions": {"color": "red"}})


app = dash.Dash(prevent_initial_callbacks=True)

popovers = html.Div(
    [
        dbc.Button(
            "Click Me",
            id="component-target",
            n_clicks=0,
        ),
        dbc.Popover(
            [
                dbc.PopoverHeader("Popover header"),
                dbc.PopoverBody("And here's some amazing content. Cool!"),
                dl.Map([dl.TileLayer(), dl.Marker(position=(39.7,-104.99),children=[dl.Popup("Hello world!")])],
                     center=(39.7, -104.99),
                     zoom=7,
                     style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
                
            ],
            target="component-target",
            trigger="click",
        ),
        
    ]
)

app.layout = html.Div([
    popovers,
    
])

if __name__ == '__main__':
    app.run_server()
"""
html.Div(dl.Map([dl.TileLayer(), cluster], center=(40, -105), zoom=14, id="map",
                    style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})),
                      html.Div(id='clickdata') 
                      """   