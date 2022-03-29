




import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

df = pd.DataFrame({'place_no': [1, 1, 1, 2, 2, 2],
                   'lat': [50.941357, 50.941357, 50.941357, 50.932171, 50.932171, 50.932171],
                   'lon': [6.957768, 6.957768, 6.957768, 6.964412, 6.964412, 6.964412],
                   'year': [2017, 2018, 2019, 2017, 2018, 2019],
                   'value': [20, 40, 60, 80, 60, 40]})


def get_map():
    fig = go.Figure(go.Scattermapbox(
    mode = "markers",
    lon = [-95.605], lat = [37.51],
    marker = {'size': 20, 'color': ["cyan"]}))

    fig.update_layout(
    mapbox = {
        'style': "stamen-terrain",
        'center': { 'lon': -95.6, 'lat': 37.5},
        'zoom': 5, 'layers': [{
            'source': './counties.json',
            'type': "fill", 'below': "traces", 'color': "royalblue"}]},
    margin = {'l':0, 'r':0, 'b':0, 't':0})

    return fig


app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='map',
              figure=get_map()),
    
], )





if __name__ == '__main__':
    app.run_server()