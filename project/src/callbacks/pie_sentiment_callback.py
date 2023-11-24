'''Quiero intentar hacer un callback para que cuando des a un sector del pie chart
te salgan los tres tuits más negativos, positivos o neutrales al aldo

'''

from dash.dependencies import Input, Output

from src.GUIs.sentiments_gui import create_div_tweets


def create_pie_sentiment_callbacks(app):

    @app.callback(
        Output('no-rts-output', 'children'),
        [Input('graph-sentiments-no-rts', 'clickData')]
    )
    def update_paragraph(click_data):
        if click_data is not None:
            category_clicked = click_data['points'][0]['label']
            return create_div_tweets(category_clicked, "no_rts")

        else:
            return 'Selecciona un sector del gráfico para ver los tweets'

    @app.callback(
        Output('rts-output', 'children'),
        [Input('graph-sentiments-rts', 'clickData')]
    )
    def update_paragraph(click_data):
        if click_data is not None:
            category_clicked = click_data['points'][0]['label']
            return create_div_tweets(category_clicked, "rts")
        else:
            return 'Selecciona un sector del gráfico para ver los tweets'

