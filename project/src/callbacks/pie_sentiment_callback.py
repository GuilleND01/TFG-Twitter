'''Quiero intentar hacer un callback para que cuando des a un sector del pie chart
te salgan los tres tuits más negativos, positivos o neutrales al aldo

'''

from dash.dependencies import Input, Output, State

def create_pie_sentiment_callbacks(app):
    @app.callback(
        Output('paragraph-output', 'children'),
        [Input('graph-escritos', 'clickData')]
    )
    def update_paragraph(click_data):
        if click_data is not None:
            category_clicked = click_data['points'][0]['text']
            return f'Has hecho clic en: {category_clicked}'
        else:
            return 'Aquí saldran los 3 tweets con mas polaridad según la que tengas seleccionada del pie'
