import base64
import io
import json

from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
from scripts.detector_lenguajes import return_language_df
from scripts.analisis_sentimientos import analisis_sentimientos

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, title='WhatTheyKnow')

app.layout = html.Div([

    dcc.Upload([
        'Drag and Drop or ',
        html.A('Select a File')
    ], style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center'
    }, multiple=True, id='upload-data'),
    html.Div(id='output_languages'),
    html.Div(id='output_sentiments')
])


@app.callback(Output('output_languages', 'children'),
              Output('output_sentiments', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        for content, filename in zip(list_of_contents, list_of_names):
            if content is not None:
                if filename == 'tweets.js':
                    tweets_decoded = content_decoded(content)
                    output_languages = func_languages(tweets_decoded)
                    output_sentiments = func_sentiments(tweets_decoded)
                    return output_languages, output_sentiments


def content_decoded(content):
    decoded = base64.b64decode(content.split(',')[1])
    return io.StringIO(decoded.decode('utf-8')).getvalue()


def func_languages(info_decoded):
    """Pongo func de funcionalidad, no se me ocurre otra cosa"""
    df = return_language_df(info_decoded)
    fig = px.pie(df, values='quantity', names='language', title='Lenguajes en los que más se ha twitteado')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return dcc.Graph(figure=fig)


def func_sentiments(info_decoded):
    df_contiene_rts, df_sin_rts = analisis_sentimientos(info_decoded)

    fig_escritos = px.pie(df_sin_rts, values='quantity', names='tweet.polarity')
    fig_escritos.update_traces(textposition='inside')
    fig_escritos.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    fig_rts = px.pie(df_contiene_rts, values='quantity', names='tweet.polarity')
    fig_rts.update_traces(textposition='inside')
    fig_rts.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    return dcc.Tabs(id="tabs-example-graph", value='tab-1', children=[
        dcc.Tab(value='tab-1', label='Polaridad de los tweets que has escrito', children=[dcc.Graph(figure=fig_escritos)]),
        dcc.Tab(label='Polaridad de los tweets que has retwitteado', children=[dcc.Graph(figure=fig_rts)]),
    ])


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port="8080")
