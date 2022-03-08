import pandas as pd
import plotly.express as px

fig = px.scatter_mapbox(
    df,  # Our DataFrame
    lat = "latitude_col_name",
    lon = "longitude_col_name",
    center = {"lat": 19.43, "lon": -99.13},  # where map will be centered
    width = 600,  # Width of map
    height = 600,  # Height of map
    hover_data = ["customer_name"],  # what to display when hovering mouse over coordinate
)

fig.update_layout(mapbox_style="open-street-map") # adding beautiful street layout to map

fig.show()