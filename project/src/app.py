import base64
import io
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from scripts.detector_lenguajes import return_language_df
from scripts.analisis_sentimientos import analisis_sentimientos

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, title='WhatTheyKnow')

app.layout = html.Div([
    html.Div([
        dcc.Upload([
            'Arrastre o ',
            html.A('seleccione un archivo')
        ], style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
        }, id='upload-data')
    ]),
    html.Br(),
    html.Div([
        html.Header(),
        dcc.Graph(id='graph')
    ], id='grafica_lenguajes')
], id='dash_columnas')


@app.callback(Output('upload-data', 'style'),
              Output('graph', 'style'),
              Output('graph', 'figure'),
              Input('upload-data', 'contents'))
def update_graph(contents):
    if contents is None:
        return {
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
        }, {'display': 'none'}, px.pie()
    else:
        # Decoding the content
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        file_content = io.StringIO(decoded.decode('utf-8'))

        # Processing the content
        df = return_language_df(file_content.getvalue())
        #df = analisis_sentimientos(file_content.getvalue())
        fig = px.pie(df, values='quantity', names='language', title='Lenguajes en los que más se ha twitteado')
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

        return {'display': 'none'}, {'display': 'block'}, fig


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port="8080")
