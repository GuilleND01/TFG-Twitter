from dash import dcc
import plotly.express as px
from src.scripts.detector_lenguajes import language_df


def return_gui_languages(info_decoded):
    """Pongo func de funcionalidad, no se me ocurre otra cosa"""
    df = language_df(info_decoded)
    fig = px.pie(df, values='quantity', names='language', title='Lenguajes en los que más se ha twitteado')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return dcc.Graph(figure=fig)
