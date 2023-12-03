from dash import dcc
import plotly.express as px
from src.scripts.usuarios_mas_mencionados import UserMentions


def return_gui_mentions(info_decoded):
    df_menciones = UserMentions(info_decoded).get_dataframe_wres()
    return dcc.Graph(id='bar',
                     figure={
                         'data': [
                             {'x': list(df_menciones['usernames']), 'y': list(df_menciones['quantity']), 'type': 'bar'}
                         ],
                         'layout': {
                             'images': [
                                 {
                                     'source': row['urls'],
                                     'xref': 'x',
                                     'yref': 'y',
                                     'x': row['usernames'],
                                     'y': row['quantity'] - 1,
                                     'sizex': 3,
                                     'sizey': 3,
                                     'xanchor': 'center',
                                     'yanchor': 'bottom'
                                 } for index, row in df_menciones.iterrows()
                             ],
                             'barmode': 'group',
                             'title': 'Gráfico de Barras con Imágenes'
                         }
                     })
