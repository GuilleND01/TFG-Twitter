from dash import dcc
import plotly.express as px
from src.scripts.usuarios_mas_mencionados import return_user_mentions_df
from src.callbacks.bar_callbacks import create_bar_clicks

def return_gui_mentions(info_decoded):
    df_menciones = return_user_mentions_df(info_decoded)
    fig_menciones = px.bar(df_menciones, x='usernames', y='quantity', title='Usuarios a los que más has mencionado',
                           text_auto=True)
    fig_menciones.update_traces(textposition='outside')
    fig_menciones.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    return dcc.Graph(id='bar', figure=fig_menciones)
