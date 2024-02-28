import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from src.scripts.usuarios_mas_mencionados import UserMentions


def return_gui_mentions(mentions_json):
    df_menciones = pd.DataFrame(mentions_json)
    return html.Div(
        children=[
            dbc.Row(children=[
                dbc.Col(children=[
                    dcc.Graph(id='bar',
                              figure={
                                  'data': [
                                      {'x': list(df_menciones['usernames']), 'y': list(df_menciones['quantity']),
                                       'type': 'bar',
                                       'marker': {
                                           'color': 'rgba(50, 171, 96, 0.6)',
                                           'line': {'color': 'rgba(50, 171, 96, 1)', 'width': 2},
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
                                              'sizex': 3,
                                              'sizey': 3,
                                              'xanchor': 'center',
                                              'yanchor': 'bottom',
                                          } for index, row in df_menciones.iterrows()
                                      ],
                                      'barmode': 'group',
                                      'title': 'Usuarios a los que más has mencionado',
                                      'yaxis': {'range': [0, max(df_menciones['quantity']) * 1.5]},
                                  }
                              }),
                ], className='col-11'),
                dbc.Col(children=[
                    html.Div(
                        dbc.Button("i", id="open_modal_men", n_clicks=0, className='mx-auto d-block rounded-circle text-center',
                                   style={'border': '2px solid', 'border-color': '#4AA7E4', 'background-color': 'white',
                                                    'color': '#4AA7E4', 'width': '40px', 'height': '40px', 'font-family': 'serif'}),
                        style={'text-align': 'center'}
                    ),
                ], className='col-1 text-center', style={'margin-top': '10px'})
            ]),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Usuarios a los que más has mencionado")),
                    dbc.ModalBody(children=[
                        html.P('''Muestra un gráfico que contiene la información de los usuarios a los que más has
                        mencionado en tus publicaciones, realizando un recuento y representándolo ordenado
                        en forma de barras.'''),
                        html.Br(),
                        html.P('''Cada una de las barras es interactiva y permite acceder al perfil del usuario en
                        cuestión.'''),
                    ], style={'text-align': 'justify'}),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Cerrar", id="close_modal_men", className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                id="modal_men",
                is_open=False,
            ),
        ], style={'border': '3px solid', 'border-color': 'black'}
    )
