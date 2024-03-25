from dash.dependencies import Input, Output
from dash import dcc, html
import dash_bootstrap_components as dbc


def create_pie_sentiment_callbacks(app):

    div_visible_style = 'container h-75 d-flex flex-row align-items-center overflow-auto'
    class_map = {"Sentimiento Positivo": (div_visible_style, "d-none", "d-none", "d-none"),
                 "Sentimiento Negativo": ("d-none", div_visible_style, "d-none", "d-none"),
                 "Sentimiento Neutral": ("d-none", "d-none", div_visible_style, "d-none")}

    @app.callback(
        Output('positiveno_rts', 'className'),
        Output('negativeno_rts', 'className'),
        Output('neutralno_rts', 'className'),
        Output('info_no_rts', 'className'),
        [Input('graph-sentiments-no-rts', 'clickData')]
    )
    def update_paragraph(click_data):

        ''' La función devuelve una tupla con las clases que se van a aplicar a los elemento de Output. Dependiendo
        de el selected_category, se aplican unas u otra definidas en el mapa de arriba.'''
        print(click_data)
        if click_data:
            selected_category = click_data['points'][0]['label']
            return class_map[selected_category]




    @app.callback(
        Output('positiverts', 'className'),
        Output('negativerts', 'className'),
        Output('neutralrts', 'className'),
        [Input('graph-sentiments-rts', 'clickData')]
    )
    def update_paragraph(click_data):
        if click_data:

            selected_category = click_data['points'][0]['label']
            return class_map[selected_category]
