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


    fig_escritos = px.pie(language_without_rts, values='quantity', names='tweet.src_language', hole=.5)
    fig_escritos.update_traces(textposition='inside')
    fig_escritos.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    fig_escritos.update_traces(hovertemplate='Has escrito <b>%{value}</b> tweets en <b>%{label}</b>')
    fig_escritos.update_layout(showlegend=False)

    fig_rts = px.pie(language_rts, values='quantity', names='tweet.src_language', hole=.5)
    fig_rts.update_traces(textposition='inside')
    fig_rts.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    fig_rts.update_traces(hovertemplate='Has retwitteado <b>%{value}</b> tweets en <b>%{label}</b>')
    fig_rts.update_layout(showlegend=False)

    return html.Div(
        children=[
            html.Div(children=[html.Span('Tus idiomas más utilizados', className='ms-3 h5 m-0'), html.Button(html.I(className="bi bi-info-circle"),
            id="open_modal_lang", className='btn')], className='d-flex justify-content-between align-items-center mb-3'),
            html.Div(children=[
                dcc.Tabs(id="tabs-languages", value='tab-1', className="d-flex justify-content-evenly mb-3",children=[
                    dcc.Tab(value='tab-1', label='Tweets', className='estilo_tab',
                            children=[dcc.Graph(figure=fig_escritos)]),
                    dcc.Tab(label='Retweets', className='estilo_tab', children=[dcc.Graph(figure=fig_rts)])
                ])
            ]),
            dbc.Modal(
                [
                    dbc.ModalHeader(
                        children=[
                            html.Img(src='https://cdn-icons-png.flaticon.com/512/3898/3898082.png',
                                     style={'height': '30px', 'width': '30px'},
                                     className='m-1'),
                            dbc.ModalTitle("Lenguajes que más has empleado / retwiteado", className='m-1'),
                        ], style={'background-color': '#6FADFF'}),
                    dbc.ModalBody(children=[
                        html.P('''Esta funcionalidad permite consultar (en dos vistas distintas) los lenguajes en los
                            que más ha publicado el usuario, así como los lenguajes más comunes en los que suele retwitear.
                            El contenido se muestra en forma de gráfica, permitiendo ver claramente los porcentajes.''')
                    ], style={'text-align': 'justify'}),
                ],
                id="modal_lang",
                is_open=False,
                className='modal-dialog-centered'
            ),
        ], className='p-3 bg-light'
    )

