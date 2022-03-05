#




from dash import  dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash import dash

app = dash.Dash()

import dash_bootstrap_components as dbc
from dash import Input, Output, html

text_input = html.Div(
    [
        dbc.Input(id="input", placeholder="Type something...", type="text"),
        html.Br(),
        html.P(id="output"),
    ]
)


@app.callback(Output("output", "children"), [Input("input", "value")])
def output_text(value):
    return value
app.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        text_input
    ],
    style={ "background-color": "#f2f1ed"}
)    


if __name__ == '__main__':
    app.run_server(debug=False)
