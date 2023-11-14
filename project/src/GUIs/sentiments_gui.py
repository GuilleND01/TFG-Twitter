from dash import dcc, html
from src.scripts.analisis_sentimientos import analisis_sentimientos
import plotly.express as px
import dash_bootstrap_components as dbc


def return_gui_sentiments(info_decoded):
    df_contiene_rts, df_sin_rts = analisis_sentimientos(info_decoded)

    fig_escritos = px.pie(df_sin_rts, values='quantity', names='tweet.polarity')
    fig_escritos.update_traces(textposition='inside')
    fig_escritos.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    fig_rts = px.pie(df_contiene_rts, values='quantity', names='tweet.polarity')
    fig_rts.update_traces(textposition='inside')
    fig_rts.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    return dcc.Tabs(id="tabs-example-graph", value='tab-1', children=[
        dcc.Tab(value='tab-1', label='Polaridad de los tweets que has escrito', children=[
            dbc.Row([dbc.Col(dcc.Graph(figure=fig_escritos), id='graph-escritos'),
                     dbc.Col(html.Div(), id='paragraph-output',
                             className="d-flex align-items-center justify-content-center")])
        ]),
        dcc.Tab(label='Polaridad de los tweets que has retwitteado', children=[
            dbc.Row([dbc.Col(dcc.Graph(figure=fig_rts)), dbc.Col(html.P("algo"))])
        ]),
    ])

#def create_Tab():
 # Va a devolver la Tab de dentro de Tabs
