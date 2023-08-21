import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State, dash_table
import base64
import datetime
import io
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
import pandas as pd
from pages import page1, page2, home

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Analytics", className="display-4"),
        html.Hr(),
        html.P(
            "Sales Data Analysis and Visualization", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Upload Data", href="/", active="exact"),
                dbc.NavLink("Trends", href="/page-1", active="exact"),
                dbc.NavLink("Visualization", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home.layout
    elif pathname == "/page-1":
        return page1.layout
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('latin1')))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename.replace(".csv","")+" Data set"),
        dash_table.DataTable(data=df.to_dict('records'), page_size=10, style_table={
                'maxHeight': '50ex',
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },),
        html.Hr(),  # horizontal line
    ])


@callback(Output('output-data-upload', 'children'),
          Input('upload-data', 'contents'),
          State('upload-data', 'filename'),)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
           zip(list_of_contents, list_of_names)]
        return children

if __name__ == "__main__":
    app.run_server(port=8000)