from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc

'''Llamada desde return_gui_langu_senti'''


def create_gui_sentiments(polarity_rts, polarity_without_rts, tweets_rts, tweets_no_rts):
    fig_escritos = px.pie(polarity_without_rts, values='quantity', names='tweet.polarity')
    fig_escritos.update_traces(textposition='inside')
    fig_escritos.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    fig_rts = px.pie(polarity_rts, values='quantity', names='tweet.polarity')
    fig_rts.update_traces(textposition='inside')
    fig_rts.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    return dcc.Tabs(id="tabs-polarity", value='tab-1', children=[
        dcc.Tab(value='tab-1', label='POLARIDAD DE LOS TWEETS QUE HAS ESCRITO', children=[
            dbc.Row([dbc.Col(dcc.Graph(figure=fig_escritos, id='graph-sentiments-no-rts')),
                     dbc.Col(children=create_div_tweets(tweets_no_rts, 'no_rts'), id='no-rts-output',
                             className="d-flex align-items-center justify-content-center")])
        ]),
        dcc.Tab(label='POLARIDAD DE LOS TWEETS QUE HAS RETWITTEADO', children=[
            dbc.Row([dbc.Col(dcc.Graph(figure=fig_rts, id='graph-sentiments-rts')),
                     dbc.Col(children=create_div_tweets(tweets_rts, 'rts'), id='rts-output',
                             className="d-flex align-items-center justify-content-center")])
        ])
    ])


def create_div_tweets(df, rts):
    '''La función recibe un dataframe y una variable de control "rts" que significa si el div que se va a construir
    corresponde a los tweets con o sin rts. La función devuelve 3 divs con tres párrafos cada uno
    en su interior correspondientes a un sector del pie'''

    positive_tweets = (df[df["tweet.polarity"] == "Sentimiento Positivo"])["tweet.full_text"]
    negative_tweets = (df[df["tweet.polarity"] == "Sentimiento Negativo"])["tweet.full_text"]
    neutral_tweets = (df[df["tweet.polarity"] == "Sentimiento Neutral"])["tweet.full_text"]

    print(positive_tweets)

    return [create_tweets_paragraph(positive_tweets, f"positive{rts}"),
            create_tweets_paragraph(negative_tweets, f"negative{rts}"),
            create_tweets_paragraph(neutral_tweets, f"neutral{rts}")]


def create_tweets_paragraph(df, id_div):
    return html.Div(children=[html.P(df.iloc[i]) for i in range(len(df))], id=id_div, className='d-none')
