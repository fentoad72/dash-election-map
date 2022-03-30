import dash
#import dash_html_components as html
#import dash_html_components as dbc
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash import html
import dash_leaflet as dl
from dash.dependencies import Input, Output
import json
import pandas as pd
import plotly.express as px
import geopandas as gpd

def plot_map():
    filename = './geojson/co_counties.geojson'
    file=open(filename)
    counties_gdf = gpd.read_file(file)

    print(counties_gdf.head(10))

    point = [-105, 40]

    fig = px.scatter_mapbox(lat=[point[1]], lon=[point[0]]).update_layout(
        mapbox={
            "style":"open-street-map",
            "zoom":9,
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

    return fig
#counties_df = pd.read_json('./geojson/co_counties.geojson')
#counties_df.reset_index(level=0,inplace=True)


app = dash.Dash(prevent_initial_callbacks=True)

if __name__ == "__main__":
      
    #print(f"file_name: {file&#91;'Key']}, size: {file&#91;'Size']}")
    app.run_server(debug=True,port=8050,host='0.0.0.0')
