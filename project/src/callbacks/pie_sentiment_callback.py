from dash.dependencies import Input, Output


def create_pie_sentiment_callbacks(app):

    class_map = {"Sentimiento Positivo": ("w-100", "d-none", "d-none"),
                 "Sentimiento Negativo": ("d-none", "w-100", "d-none"),
                 "Sentimiento Neutral": ("d-none", "d-none", "w-100")}

    @app.callback(
        Output('positiveno_rts', 'className'),
        Output('negativeno_rts', 'className'),
        Output('neutralno_rts', 'className'),
        [Input('graph-sentiments-no-rts', 'clickData')]
    )
    def update_paragraph(click_data):

        ''' La función devuelve una tupla con las clases que se van a aplicar a los elemento de Output. Dependiendo
        de el selected_category, se aplican unas u otra definidas en el mapa de arriba.'''

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
