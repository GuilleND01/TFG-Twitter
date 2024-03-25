import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px


def return_gui_mentions(mentions_json):
    df_menciones = pd.DataFrame(mentions_json)

    return html.Div(children=[
        html.Div(children=[html.Span('Usuarios a los que más has mencionado', className='ms-3 h5 m-0'),
                           html.Button(html.I(className="bi bi-info-circle"),
                                       id="open_modal_men", className='btn')],
                 className='d-flex justify-content-between align-items-center'),
        html.Div("Averigua a quién haces referencia más a menudo en tus tweets.", className='ms-3 mb-3 opacity-25'),
        dcc.Graph(id='bar',
                  figure={
                      'data': [
                          {'x': list(df_menciones['usernames']), 'y': list(df_menciones['quantity']),
                           'type': 'bar',
                           'marker': {
                               'color': 'rgba(57, 139, 191, 1)',
                               'line': {'color': 'rgba(31, 103, 165, 1)', 'width': 2},
                               'symbol': 'circle',
                               'size': 12,
                           },
                           'hovertemplate': 'Has mencionado al usuario <b>%{x}</b> %{y} veces <extra></extra>'
                           }
                      ],
                      'layout': {
                          'images': [
                              {
                                  'source': row['urls'],
                                  'xref': 'x',
                                  'yref': 'y',
                                  'x': row['usernames'],
                                  'y': row['quantity'] - 1,
                                  'sizex': 7,
                                  'sizey': 7,
                                  'xanchor': 'center',
                                  'yanchor': 'bottom'
                              } for index, row in df_menciones.iterrows()
                          ],
                          'barmode': 'group',
                          'yaxis': {'range': [0, max(df_menciones['quantity']) * 1.5]},
                      }
                  }),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    children=[
                        html.Img(src='https://cdn-icons-png.flaticon.com/512/3898/3898082.png',
                                 style={'height': '30px', 'width': '30px'},
                                 className='m-1'),
                        dbc.ModalTitle("Usuarios a los que más has mencionado", className='m-1'),
                    ], style={'background-color': '#6FADFF'}),
                dbc.ModalBody(children=[
                    html.P('''Muestra un gráfico que contiene la información de los usuarios a los que más has
                                                mencionado en tus publicaciones, realizando un recuento y representándolo ordenado
                                                en forma de barras.'''),
                    html.Br(),
                    html.P('''Cada una de las barras es interactiva y permite acceder al perfil del usuario en
                                                cuestión.'''),
                ], style={'text-align': 'justify'}),
            ],
            id="modal_men",
            is_open=False,
            className='modal-dialog-centered'
        )
    ], className='p-3 bg-light')
