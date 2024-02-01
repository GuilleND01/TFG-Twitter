from dash import dcc
import plotly.express as px
import dash_bootstrap_components as dbc


'''Llamada desde return_gui_langu_senti'''

def create_gui_languages(language_rts, language_without_rts):
    fig_escritos = px.pie(language_without_rts, values='quantity', names='tweet.src_language')
    fig_escritos.update_traces(textposition='inside')
    fig_escritos.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    fig_rts = px.pie(language_rts, values='quantity', names='tweet.src_language')
    fig_rts.update_traces(textposition='inside')
    fig_rts.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    return dcc.Tabs(id="tabs-languages", value='tab-1', children=[
        dcc.Tab(value='tab-1', label='Idiomas Tweets', children=[dcc.Graph(figure=fig_escritos)]),
        dcc.Tab(label='Idiomas Retweets', children=[dcc.Graph(figure=fig_rts)])
    ])

