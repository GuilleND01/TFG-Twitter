import dash_bootstrap_components as dbc
from dash import html, dcc


def return_download_gui():
    return html.Div(children=[
        dbc.Button(html.Img(src='https://cdn-icons-png.flaticon.com/512/3325/3325565.png',
                            style={'width': '30px', 'height': '30px'}),
                   id="download", n_clicks=0, color='black'),
        dbc.Tooltip('Descarga un fichero para posteriores consultas', target='download', placement='top'),
        dcc.Download(id='download-file')
    ])
