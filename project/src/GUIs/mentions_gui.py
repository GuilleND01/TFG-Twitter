import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

'''
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
               'hovertemplate': 'Has mencionado al usuario <b>%{x}</b> %{y} veces <br>'
                                '<img src="{urls}"/><extra></extra>'
               }
          ]
        }),
'''


def return_gui_mentions(mentions_json):
    df_menciones = pd.DataFrame(mentions_json)

    fig = px.bar(df_menciones,
                 x='usernames',
                 y='quantity',
                 labels={'quantity': 'Cantidad', 'usernames': 'Usuarios'},
                 color_discrete_sequence=['rgba(57, 139, 191, 1)'],
                 custom_data=['urls'],
                 template='plotly_white')

    fig.update_traces(
        hoverinfo="none",
        hovertemplate=None,
    )

    # fig.update_traces(hovertemplate="Has mencionado al usuario <b>%{x}</b> %{y} veces <div><img "
    #                                 "src='%{customdata[0]}' width='40px'></div>")

    return html.Div(children=[
        html.Div(children=[html.Span('Usuarios a los que más has mencionado', className='ms-3 h5 m-0'),
                           html.Button(html.I(className="bi bi-info-circle"),
                                       id="open_modal_men", className='btn')],
                 className='d-flex justify-content-between align-items-center'),
        html.Div("Averigua a quién haces referencia más a menudo en tus tweets.", className='ms-3 mb-3 opacity-25'),
        html.Div(
            children=[
                dcc.Graph(id='bar', figure=fig, clear_on_unhover=True),
                dcc.Tooltip(id="mention-tool", direction="top", className='p-3 rounded'),
            ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    children=[
                        html.Img(src='https://cdn-icons-png.flaticon.com/512/3898/3898082.png',
                                 style={'height': '30px', 'width': '30px'},
                                 className='m-1'),
                        html.Div("Usuarios a los que más has mencionado", className='m-1 h5'),
                    ], style={'background-color': '#6FADFF'}),
                dbc.ModalBody(children=[
                    html.P('''Visualiza en el gráfico la información de los usuarios a los que más has mencionado en 
                    tus publicaciones. Cada una de las barras es interactiva y te permite acceder al perfil del 
                    usuario haciendo click sobre ella.'''),
                    html.Br(),
                    html.P('''De forma adicional, si se sitúa el cursor sobre cada una de las barras, se muestra en 
                    detalle el número de menciones realizadas al usuario junto a la foto de perfil.''')
                ], style={'text-align': 'justify'}),
            ],
            id="modal_men",
            is_open=False,
            className='modal-dialog-centered'
        )
    ], className='p-3 bg-light')
