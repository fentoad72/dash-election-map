import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

df = pd.DataFrame({'place_no': [1],
                   'lat': [40.941357],
                   'lon': [-105.957768],
                   'year': [2017],
                   'value': [200]})


def get_map(df_map):
    fig = go.Figure(go.Scattermapbox(
        lat=df_map['lat'],
        lon=df_map['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=df_map['value']
        ),
    ))
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox={'center': go.layout.mapbox.Center(lat=40.936600, lon=-105.961497), 'zoom': 11}
    )
    return fig


app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='map',
              figure=get_map(df[df['year'] == 2017])),
    html.Div(id='shown-week', style={'textAlign': 'center'})
], )



def update_map(selected_year):
    fig = get_map(filtered_df)
    return fig


if __name__ == '__main__':
    app.run_server()