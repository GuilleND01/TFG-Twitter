import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
from pandas import json_normalize


def return_gui_advertisers(adv_json):

    return html.Div(children=[
        html.Div(children=[
            html.P(children=[html.Span('Anunciantes más interesados', className='ms-3 h5')],
                   className='d-inline-flex m-0'),
            html.P(children=[
                html.Button(html.I(className="bi bi-info-circle"), id="open_modal_adv", className='btn'),
            ], className='d-flex align-items-center m-0')],
            className='d-flex justify-content-between align-items-center m-0'),
        html.Div("Consulta los anunciantes que están más interesados en tu perfil. ",
                 className='ms-3 mb-3 opacity-25'),
        html.Div(
            children=[
                html.Label('Selecciona una opción:'),
                dcc.Dropdown(
                    id='pombo-bo',
                    options=[{'label': f"{adv} ({adv_json[adv]['advertisements']} anuncios)",
                              'value': adv} for adv in adv_json],
                    value=next(iter(adv_json)),
                    placeholder='Selecciona un anunciante...',
                    clearable=False
                ),
                html.Br(),
                html.Div(id='graph-advertiser')
            ],
            className='p-4 m-2',
            style={'border-radius': '40px',
                   'box-shadow': '0 0.125rem 0.25rem rgba(0, 0, 0, 0.075)',
                   'background-color': 'white'}
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    children=[
                        html.Img(src='https://cdn-icons-png.flaticon.com/512/2415/2415903.png',
                                 style={'height': '30px', 'width': '30px'},
                                 className='m-1'),
                        html.Div("Anunciantes más interesados", className='m-1 h5'),
                    ], style={'background-color': '#6FADFF'}),
                dbc.ModalBody(children=[
                    html.P('''Muestra hasta un máximo de los cinco anunciantes de los que más has recibido 
                                        anuncios en tu perfil. Para cada uno de ellos se muestra la siguiente información: el 
                                        último twit que has recibido de dicho anunciante, el número total de anuncios recibidos y 
                                        una categorización de los motivos por los que te han aparecido las publicaciones de este 
                                        anunciante.'''),
                    html.Br(),
                    html.P('''Para cada uno de los criterios (que se muestran en la parte izquierda de la 
                                        lista) se proporciona el conjunto global al que pertenecen.''')
                ], style={'text-align': 'justify'}),
            ],
            id="modal_adv",
            is_open=False,
            className='modal-dialog-centered'
        )
    ], className='p-3 bg-light')
