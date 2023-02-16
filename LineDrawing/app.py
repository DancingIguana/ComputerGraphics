from dash import Dash, dcc, html, Input, Output,ctx
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.express as px
from bresenham import bresenham
from dda import digital_differential_analyzer

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, ])

I = [[0]]

app.layout = html.Div([
    dbc.NavbarSimple(
        brand="Line Drawing",
        brand_href="#",
        color="primary",
        dark=True
    ),
    html.H2("Line drawing algorithms"),
    html.Div(children=[
        html.Div(id="params", children=[
            html.Label("Canvas size"),
            html.Div(children=[
                    # html.Label("Width"),
                daq.NumericInput(
                    id="canvas-width",
                    value=10,
                    label="Width",
                    min=1,
                    max=500
                ),
                # html.Label("Height"),
                daq.NumericInput(
                    id="canvas-height",
                    value=10,
                    label="Height",
                    min=1,
                    max=500
                )], style={"display": "flex", "justify-content": "center"}
            ),
            html.Label("Algorithm"),
            dcc.RadioItems(["DDA", "Bresenham"], "DDA", labelStyle={
                           "display": "block"}, id="method"),
            html.Label("Point 1"),
            html.Div(children=[
                # html.Label("Width"),
                daq.NumericInput(
                    id="x1",
                    value=10,
                    label="X",
                    min=0
                ),
                # html.Label("Height"),
                daq.NumericInput(
                    id="y1",
                    value=10,
                    label="Y",
                    min=0
                )], style={"display": "flex", "justify-content": "center"}
            ),
            html.Label("Point 2"),
            html.Div(children=[
                # html.Label("Width"),
                daq.NumericInput(
                    id="x2",
                    value=10,
                    label="X",
                    min=0
                ),
                # html.Label("Height"),
                daq.NumericInput(
                    id="y2",
                    value=10,
                    label="Y",
                    min=0
                )], style={"display": "flex", "justify-content": "center"}
            ),
            html.Button("Draw", id='btn-nclicks-1', n_clicks=0)
        ],
            style={
            "width": "30%",
            "display": "inline-block",
            "padding": "2%",
            "background-color": "#444"
        }),

        html.Div(children=[
            dcc.Graph(
                id="plot", style={'width': '50vh', 'height': '50vh', "display": "inline-block"}
            ),
        ], style={
            "width": "70%",
            "display": "inline-block",
            "padding": "5px",
            "background-color": "#303030",
            "justify-content": "center"
        })
    ], style={"text-align": "center"}, className="row")

], className="container scalable")


@app.callback(
    [Output("x1", "max"), Output("y1", "max"),
     Output("x2", "max"), Output("y2", "max")],
    Input("canvas-width", "value"),
    Input("canvas-height", "value")
)
def update_point_boundaries(width, height):
    return width - 1, height - 1, width - 1, height - 1


@app.callback(
    Output("plot", "figure"),
    Input("canvas-width", "value"),
    Input("canvas-height", "value"),
    Input("btn-nclicks-1", "n_clicks"),
    Input("method", "value"),
    Input("x1", "value"),
    Input("y1", "value"),
    Input("x2", "value"),
    Input("y2", "value")
)
def update_canvas(width, height, btn, method, x1, y1, x2, y2):
    global I
    if len(I) != height or len(I[0]) != width:
        I = [[0 for i in range(width)] for j in range(height)]
    if "btn-nclicks-1" == ctx.triggered_id:
        try:
            if method == "DDA":
                I = digital_differential_analyzer((x1, y1), (x2, y2), I)
            else:
                I = bresenham((x1, y1), (x2, y2), I)
        except:
            I = I
    fig = px.imshow(I, binary_string=True)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout({
        "plot_bgcolor": "rgba(0,0,0,0)",
        "paper_bgcolor": "rgba(0,0,0,0)",
        "font_color": "white"}
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
