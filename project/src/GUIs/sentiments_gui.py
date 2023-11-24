from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc

from src.scripts.lenguajes_sentimientos import return_tweets

'''Llamada desde return_gui_langu_senti'''


def create_gui_sentiments(polarity_rts, polarity_without_rts):
    fig_escritos = px.pie(polarity_without_rts, values='quantity', names='tweet.polarity')
    fig_escritos.update_traces(textposition='inside')
    fig_escritos.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    fig_rts = px.pie(polarity_rts, values='quantity', names='tweet.polarity')
    fig_rts.update_traces(textposition='inside')
    fig_rts.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    return dcc.Tabs(id="tabs-polarity", value='tab-1', children=[
        dcc.Tab(value='tab-1', label='POLARIDAD DE LOS TWEETS QUE HAS ESCRITO', children=[
            dbc.Row([dbc.Col(dcc.Graph(figure=fig_escritos, id='graph-sentiments-no-rts')),
                     dbc.Col(id='no-rts-output',
                             className="d-flex align-items-center justify-content-center")])
        ]),
        dcc.Tab(label='POLARIDAD DE LOS TWEETS QUE HAS RETWITTEADO', children=[
            dbc.Row([dbc.Col(dcc.Graph(figure=fig_rts, id='graph-sentiments-rts')),
                     dbc.Col(id='rts-output',
                             className="d-flex align-items-center justify-content-center")])
        ])
    ])


def create_div_tweets(label, rts):
    return create_tweets(return_tweets(label, rts))


def create_tweets(df):
    children_P = []
    for i in range(len(df)):
        children_P.append(html.P(df.iloc[i]))

    return html.Div(children=children_P)
