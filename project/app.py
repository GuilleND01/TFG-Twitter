from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
from detectorlenguajes import retornar_df

app = Dash(__name__, title='WhatTheyKnow')

df = retornar_df()
fig = px.pie(df, values='Cantidad', names='Idioma')
fig.update_traces(textposition='inside')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

app.layout = html.Div([
    html.Header(),
    html.H2('Lenguajes en los que más se ha twitteado', style={'text-align': 'center'}),
    dcc.Graph(figure=fig)
], id='grafica_lenguajes')

  
if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port="8080")
