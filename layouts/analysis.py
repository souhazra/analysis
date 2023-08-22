import time
import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from dash import Input, Output, dcc, html, callback, State
from layouts.data_upload import data_upload_layout, parse_contents
import plotly.express as px

total_revenue_card = dbc.Card(
    [
        dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
        dbc.CardBody(
            [
                html.H4("Total Revenue", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                html.Div(id="output-total-revenue"),
            ]
        ),
    ],
    style={"width": "18rem"},
)

def get_total_revenue(df):
    return df.Sales.sum()