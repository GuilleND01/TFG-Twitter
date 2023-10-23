from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
from detectorlenguajes import return_language_df

app = Dash(__name__, title='WhatTheyKnow')

df = return_language_df()
fig = px.pie(df, values='quantity', names='language')
fig.update_traces(textposition='inside')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

app.layout = (
    html.Div([
        html.Div([
            html.Header(),
            html.H2('Lenguajes en los que más se ha twitteado', style={'text-align': 'center'}),
            dcc.Graph(figure=fig)
        ], id='grafica_lenguajes')
    ], id='dash_columnas')
)

  
if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port="8080")
