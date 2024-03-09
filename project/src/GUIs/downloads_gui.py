import dash_bootstrap_components as dbc
from dash import html, dcc


def return_download_gui():
    return html.Div(children=[
        dbc.Button(html.I(className='bi bi-file-earmark-arrow-down'),
                   id="download", n_clicks=0, color='black'),
        dbc.Tooltip('Descarga un fichero para posteriores consultas', target='download', placement='top'),
        dcc.Download(id='download-file')
    ])
