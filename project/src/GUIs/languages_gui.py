from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
import json
import pandas as pd

'''Llamada desde return_gui_langu_senti'''


def return_gui_languages(langu_senti_json):

    #language_without_rts = json.loads(langu_senti_json['language_no_rts'])
    #language_rts = json.loads(langu_senti_json['language_rts'])

    language_without_rts = pd.DataFrame(json.loads(langu_senti_json['language_no_rts']))
    language_rts = pd.DataFrame(json.loads(langu_senti_json['language_rts']))


    fig_escritos = px.pie(language_without_rts, values='quantity', names='tweet.src_language')
    fig_escritos.update_traces(textposition='inside')
    fig_escritos.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    fig_escritos.update_traces(hovertemplate='Has escrito <b>%{value}</b> tweets en <b>%{label}</b>')

    fig_rts = px.pie(language_rts, values='quantity', names='tweet.src_language')
    fig_rts.update_traces(textposition='inside')
    fig_rts.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    fig_rts.update_traces(hovertemplate='Has retwitteado <b>%{value}</b> tweets en <b>%{label}</b>')

    return html.Div(
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            dcc.Tabs(id="tabs-languages", value='tab-1', children=[
                                dcc.Tab(value='tab-1', label='Idiomas Tweets',
                                        children=[dcc.Graph(figure=fig_escritos)]),
                                dcc.Tab(label='Idiomas Retweets', children=[dcc.Graph(figure=fig_rts)])
                            ])
                        ],
                        className='col-9'
                    ),
                    dbc.Col(children=[
                        html.Div(
                            dbc.Button("i", id="open_modal_lang", n_clicks=0, className='mx-auto d-block rounded-circle text-center',
                                       style={'border': '2px solid', 'border-color': '#4AA7E4',
                                              'background-color': 'white',
                                              'color': '#4AA7E4', 'width': '40px', 'height': '40px',
                                              'font-family': 'serif'}),
                            style={'text-align': 'center'}
                        ),
                    ], className='col-3 text-center', style={'margin-top': '10px'})
                ]
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Lenguajes que más has empleado / retwiteado")),
                    dbc.ModalBody(children=[
                        html.P('''Esta funcionalidad permite consultar (en dos vistas distintas) los lenguajes en los
                        que más ha publicado el usuario, así como los lenguajes más comunes en los que suele retwitear.
                        El contenido se muestra en forma de gráfica, permitiendo ver claramente los porcentajes.'''),
                    ]),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Cerrar", id="close_modal_lang", className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                id="modal_lang",
                is_open=False,
            ),
        ],
        style={'border': '3px solid', 'border-color': 'black'}
    )

