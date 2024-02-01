from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

from src.callbacks.pie_sentiment_callback import create_pie_sentiment_callbacks
from src.callbacks.upload_data_callback import create_upload_data_callbacks
from src.callbacks.bar_callbacks import create_bar_clicks
from src.callbacks.modal_callbacks import create_modal_callback
from src.callbacks.offcanvas_callbacks import create_offcanvas_callback

app = Dash(__name__, title='WhatTheyKnow', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Aquí o en GUIs
app.layout = dbc.Container([
    html.Div([
        dbc.Row(children=[
            dbc.Col(html.H1("WhatTheyKnow", style={'text-align': 'left'}), className='col-10'),
            dbc.Col(html.Div(id='output_profile', className='m3'), className='col-2', style={'display': 'flex',
                'justify-content': 'right', 'align-items': 'center', 'text-align': 'right'}),
        ])
    ]),
    dcc.Upload([
        'Drag and Drop or ',
        html.A('Select a File')
    ], style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center'
    }, multiple=True, id='upload-data', className='mt-3 mb-3'),  # Margin top y margin bottom
    dbc.Row(children=[dbc.Col(html.Div(id='output_languages', className='m3'), className='col-4'),
                      dbc.Col(html.Div(id='output_menciones', className='m3'), className='col-8')]),
    html.Div(id='output_sentiments', className='m3'),  # Margin 3 de Bootstrap
    html.Div(id='whitebox')
], fluid=True)

# Creación de los callbacks de la app
create_upload_data_callbacks(app)
create_pie_sentiment_callbacks(app)
# ... y todos los callbacks de las GUIs
create_bar_clicks(app)
create_modal_callback(app)
create_offcanvas_callback(app)

if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port="8080")
