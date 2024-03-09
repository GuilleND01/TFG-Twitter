import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from src.scripts.usuarios_mas_mencionados import UserMentions


def return_gui_mentions(mentions_json):
    df_menciones = pd.DataFrame(mentions_json)

    return html.Div(children=[
        html.Div(children=[html.Span('Usuarios a los que más has mencionado', className='ms-3 h5'), html.Button(html.I(className="bi bi-info-circle"),
        id="open_modal_men", className='btn')], className='d-flex justify-content-between align-items-center mb-3'),
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
                      'yaxis': {'range': [0, max(df_menciones['quantity']) * 1.5]},
                  }
            }),
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
        )
    ], className='p-3 bg-light')

