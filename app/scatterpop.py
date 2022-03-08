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

positions = [(40, -105)]
markers = [dl.Marker(dl.Tooltip("test"), position=pos, id="marker{}".format(i)) for i, pos in enumerate(positions)]
cluster = dl.MarkerClusterGroup(id="markers", children=markers, options={"polygonOptions": {"color": "red"}})
def plot_1(us_cities):
    # data preparation 
    fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

app = dash.Dash(prevent_initial_callbacks=True)

fig = plot_1(us_cities)

app.layout = html.Div([
    html.Div([html.H1('NYC Specialized Schools')], style={'textAlign': 'center'}),
    dcc.Graph(figure=fig),
])

if __name__ == '__main__':
    app.run_server()
"""
html.Div(dl.Map([dl.TileLayer(), cluster], center=(40, -105), zoom=14, id="map",
                    style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})),
                      html.Div(id='clickdata') 
                      """   