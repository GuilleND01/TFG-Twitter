import re

from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
import requests
from html import unescape
import pandas as pd
import json

def return_gui_sentiments(langu_senti_json):

    polarity_without_rts = pd.DataFrame(json.loads(langu_senti_json['polarity_no_rts']))
    polarity_rts = pd.DataFrame(json.loads(langu_senti_json['polarity_rts']))

    tweets_no_rts = pd.DataFrame(json.loads(langu_senti_json['tweet_no_rts']))
    tweets_rts = pd.DataFrame(json.loads(langu_senti_json['tweet_rts']))


    #fig_escritos = px.pie(polarity_without_rts, values='quantity', names='tweet.polarity')

    fig_escritos = px.pie(polarity_without_rts, values='quantity', names='tweet.polarity', color='tweet.polarity',
    color_discrete_map={'Sentimiento Neutral':'#579CEE', 'Sentimiento Positivo':'#6BAF77', 'Sentimiento Negativo':'#F68F1A'})

    fig_escritos.update_traces(textposition='inside')
    fig_escritos.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    fig_escritos.update_traces(hovertemplate='Has escrito <b>%{value}</b> tweets con <b>%{label}</b>')


    fig_rts = px.pie(polarity_rts, values='quantity', names='tweet.polarity', color='tweet.polarity',
    color_discrete_map={'Sentimiento Neutral':'#579CEE', 'Sentimiento Positivo':'#6BAF77', 'Sentimiento Negativo':'#F68F1A'})
    fig_rts.update_traces(textposition='inside')
    fig_rts.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    fig_rts.update_traces(hovertemplate='Has retwitteado <b>%{value}</b> tweets con <b>%{label}</b>')


    return html.Div(
        children=[html.Div(children=[html.Span('Sentimiento de tu actividad', className='ms-3 h5 m-0'), html.Button(html.I(className="bi bi-info-circle"),
            id="open_modal_senti", className='btn')], className='d-flex justify-content-between align-items-center'),
            html.Div("Conoce cuál es la polaridad de la huella digital que dejas.", className='ms-3 mb-3 opacity-25'),
            html.Div(children=[dcc.Tabs(id="tabs-polarity", className='d-flex justify-content-around mb-3', value='tab-1', children=[
                dcc.Tab(value='tab-1', label=f"Tweets ({langu_senti_json['tweets_despues_limpiar']})", className='estilo_tab',children=[
                        dbc.Row(children=[dbc.Col(dcc.Graph(figure=fig_escritos, id='graph-sentiments-no-rts'), className='col-6'),
                                 dbc.Col(children=create_div_tweets(tweets_no_rts, 'no_rts'), id='no-rts-output',
                                         className="d-flex align-items-center justify-content-center col-6")])
                ]),
                dcc.Tab(label=f"Retweets ({langu_senti_json['retweets_despues_limpiar']})", className='estilo_tab', children=[
                    dbc.Row(children=[dbc.Col(dcc.Graph(figure=fig_rts, id='graph-sentiments-rts'), className='col-6'),
                             dbc.Col(children=create_div_tweets(tweets_rts, 'rts'), id='rts-output',
                                     className="d-flex align-items-center justify-content-center col-6")])
                ])
            ])]),
            dbc.Modal(
              [
                  dbc.ModalHeader(
                      children=[
                          html.Img(src='https://cdn-icons-png.flaticon.com/512/2564/2564959.png',
                                   style={'height': '30px', 'width': '30px'},
                                   className='m-1'),
                          html.Div("Sentimiento de tu actividad", className='m-1 h5'),
                      ], style={'background-color': '#6FADFF'}),
                  dbc.ModalBody(children=[
                      html.P('''Comprende cómo se percibe en términos de sentimientos la información que publicas. Tanto, por parte de tus seguidores como
                        de la comunidad en general. Cuando realices click sobre alguno de los sectores, podrás ver los tres tweets con mayor polaridad para la
                        categoría seleccionada. Desliza a la derecha en el panel para verlos todos.'''),
                      html.P(
                          f"Se han omitido del análisis {langu_senti_json['tweets_antes_limpiar'] - langu_senti_json['tweets_despues_limpiar']} tweets y "
                          f"{langu_senti_json['retweets_antes_limpiar'] - langu_senti_json['retweets_despues_limpiar']} retweets debido a que no contenían texto a analizar."
                          )
                  ], style={'text-align': 'justify'}),
              ],
              id="modal_senti",
              is_open=False,
              className='modal-dialog-centered'
            ),
        ], className='p-3 bg-light'
    )

def create_div_tweets(df, rts):
    '''La función recibe un dataframe y una variable de control "rts" que significa si el div que se va a construir
    corresponde a los tweets con o sin rts. La función devuelve 3 divs con tres párrafos cada uno
    en su interior correspondientes a un sector del pie'''

    positive_tweets = (df[df["tweet.polarity"] == "Sentimiento Positivo"])
    negative_tweets = (df[df["tweet.polarity"] == "Sentimiento Negativo"])
    neutral_tweets = (df[df["tweet.polarity"] == "Sentimiento Neutral"])

    info_tweets = "Selecciona un sector para ver tus tweets con más polaridad en la categoría." if rts == 'no_rts' else \
        "Selecciona un sector para ver tus retweets con más polaridad en la categoría."

    return [html.P(info_tweets, id=f"info_{rts}", className='opacity-50 mx-4'),
            create_tweets_paragraph(positive_tweets, f"positive{rts}"),
            create_tweets_paragraph(negative_tweets, f"negative{rts}"),
            create_tweets_paragraph(neutral_tweets, f"neutral{rts}")]


def create_tweets_paragraph(df, id_div):
    list_tweets = []
    for i in range(len(df)):
        html_tweet = df.iloc[i]["html_tweet"]
        tweet_html = unescape(html_tweet)
        list_tweets.append(html.Iframe(srcDoc=tweet_html))

    return html.Div(children=list_tweets, id=id_div, className='d-none')
