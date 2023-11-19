'''Quiero intentar hacer un callback para que cuando des a un sector del pie chart
te salgan los tres tuits más negativos, positivos o neutrales al aldo

'''

from dash.dependencies import Input, Output

def create_pie_sentiment_callbacks(app):
    @app.callback(
        Output('no-rts-output', 'children'),
        [Input('graph-sentiments-no-rts', 'clickData')]
    )
    def update_paragraph(click_data):
        if click_data is not None:
            category_clicked = click_data['points'][0]['label']
            return f'Has hecho clic en: {category_clicked}'
        else:
            return 'Aquí saldran los 3 tweets con mas polaridad según la que tengas seleccionada del pie'

    @app.callback(
        Output('rts-output', 'children'),
        [Input('graph-sentiments-rts', 'clickData')]
    )
    def update_paragraph(click_data):
        if click_data is not None:
            category_clicked = click_data['points'][0]['label']
            return f'Has hecho clic en: {category_clicked}'
        else:
            return 'Aquí saldran los 3 tweets con mas polaridad según la que tengas seleccionada del pie'
