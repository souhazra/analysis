from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import base64
import datetime
import io
import pandas as pd


data_upload_layout = html.Div([
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
])


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
        html.H5(filename.replace(".csv", "") + " Data set"),
        dash_table.DataTable(data=df.to_dict('records'), page_size=10, style_table={
            'maxHeight': '50ex',
            'overflowY': 'scroll',
            'width': '100%',
            'minWidth': '100%',
        }, ),
        html.Hr(),  # horizontal line
    ])
