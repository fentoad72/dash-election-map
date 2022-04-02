import dash
#import dash_html_components as html
#import dash_html_components as dbc
import dash_bootstrap_components as dbc
from dash import dcc 
from dash import html
from dash import dash_table
import dash_leaflet as dl
from dash.dependencies import Input, Output,State
import json
import pandas as pd
import plotly.express as px
import geopandas as gpd
import base64
import datetime
import io

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

### Plot a county map of Colorado (zoomed in to Denver metro)
def plot_map():
    filename = './app/geojson/counties.json'
    file=open(filename)
    counties_gdf = gpd.read_file(file)

    print(counties_gdf.head(10))

    point = [-105, 40]

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
                    "line":{"width": 10.5}
                }
            ],
        },
        margin={"l":0,"r":0,"t":0,"b":0},
    )

    return fig

### The code that parses the file (from https://dash.plotly.com/dash-core-components/upload)
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

def data_to_df(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    print('df',type(df))

#   fig.update_traces(locations=df,selector=dict(type='choropleth'))

    return df

### the Decorator that updates the output when a file is dragged onto the web page
### (also from https://dash.plotly.com/dash-core-components/upload)

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(Output('output-data-upload', 'plot_mods'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def graph_data(list_of_contents, list_of_names, list_of_dates):
# same as update_output but returns df instead of dict
    if list_of_contents is not None:
#       voter_df =  pd.DataFrame.from_dict({ data_to_df(c,n,d) for c,n,d in
#           zip(list_of_contents, list_of_names, list_of_dates) })
#       print(voter_df.head(10))

        print('graph_data')

        plot_mods = ''
        return plot_mods

app.layout = html.Div(children=[html.H1(children='Colorado Counties'),
    dcc.Graph(id='map', figure=plot_map()),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
  ]
 )

if __name__ == '__main__':
    app.run_server()

