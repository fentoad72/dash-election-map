# https://stackoverflow.com/questions/62732631/how-to-collapsed-sidebar-in-dash-plotly-dash-bootstrap-components
import os
import sys
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import time
#import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_bootstrap_components._components.Container import Container
from geocode import extract_lat_long_via_address, get_district

#GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY'] = os.environ['GOOGLE_API_KEY']
try:  
  os.environ['GOOGLE_API_KEY']
except KeyError: 
  print('[error]: `GOOGLE_#API_KEY` environment variable required')
  sys.exit(1)

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']  

maps = os.listdir("./app/static")
maps = [ map for map in maps if map.endswith( '.html') ]
maps = [os.path.splitext(map)[0] for map in maps]
home_about = ['about']
maps.remove('about')
maps.sort()
maps = []
maps = home_about + maps
dict = {}
index =0
for map in maps:
    dict[map] = map
dict['about'] = "About IX Power Cartographica"
   
dict['colorado_districtmap_1mar22'] = "Colorado District Map"

    #if '.DS_Store' in maps: maps.remove('.DS_Store')
 

#application = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
application = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])
#application = dash.Dash(external_stylesheets=[dbc.themes.UNITED])
#application = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])


PLOTLY_LOGO = "./static/img/IX_PCarto_sm_23Feb21.png"



search_bar = dbc.Row(
    [    dbc.Col(
            dbc.Button(
                "Sidebar",  color="primary", className="ms-2", id="btn_sidebar", size="sm"
            ),
            width="auto",
        ),  
        
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="60px")),
                        dbc.Col(dbc.NavbarBrand("Colorado Congressional Districts", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://ixwater.com/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ],
        
    ),
    style={
           "background-image": "url(/assets/banner.png)",
           "background-repeat": "no-repeat",
           "background-size" : "cover",
           },
    color="dark",
    dark=True,
)



# add callback for toggling the collapse on small screens
@application.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 75.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f2f1ed",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 82.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "1rem",
    "padding": "1rem 3rem",
    "background-color": "#f2f1ed",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
         
        html.Br(),
        html.H3(
            "Find your Colorado Congressional District", className="lead"
        ),
        html.Br(),
        html.H3(
            "Enter your address below", className="lead"
        ),
        html.Div(
           [
              dbc.Input(id="input", placeholder="ex: 17301 W Colfax Ave Lakewood", size="md", className="mb-3", type="text"),
              html.Br(),
              html.P(id="output"),
        
           ]
        ),
        dbc.Nav(
            [  
                dbc.NavLink(str(dict[map]), href="/" + str(map), id="page-" + str(map) + "-link") for map in maps
            
            ],
            vertical=True,
            pills=True,
        ),

    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(

    id="page-content",
    style=CONTENT_STYLE)

application.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content,
    ],
    style={ "background-color": "#f2f1ed"}
)

#  callback for input
"""
@application.callback(Output("loading-output-2", "children"), Input("input", "value"))
def input_triggers_nested(value):
    time.sleep(1)
    return value
"""    

@application.callback(Output("output", "children"), [Input("input", "value")])
def output_text(value):
    
    #lat, lon = extract_lat_long_via_address(value, GOOGLE_API_KEY)
    districts = extract_lat_long_via_address(value, GOOGLE_API_KEY)
    
    return districts

@application.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on

@application.callback(

    [Output("page-" + str(map) + "-link", "active") for map in maps],
    [Input("url", "pathname")],
)   

def toggle_active_links(pathname):
    if pathname == ["/"]:
        # Treat page 1 as the homepage / index
        #return True, False, False, False
        #list = [False for i in len(maps)]
        #list[0] = True
        return [True] + [False for i in range(len(maps)-1)]
    return [pathname == "/" + str(map) for map in maps]


@application.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/"]:
        #return html.P("IX Power Maps")
        mymap = "./app/static/colorado_districtmap_1mar22.html"
        return html.Div(
              html.Iframe(id="map", srcDoc= open(mymap,'r').read(), width='100%', height='600' )
        )
    elif pathname in ["/" + str(map) for map in maps]:


        mymap = "./app/static/" + pathname[1:] + ".html"
        return html.Div(
              html.Iframe(id="map", srcDoc= open(mymap,'r').read(), width='100%', height='600' )
        )
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P("The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
      
    #print(f"file_name: {file&#91;'Key']}, size: {file&#91;'Size']}")
    application.run_server(debug=True,port=8050,host='0.0.0.0')
