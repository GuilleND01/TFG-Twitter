from dash.dependencies import Input, Output
import webbrowser


def create_bar_clicks(app):
    @app.callback(
        Output('whitebox', 'children'),
        [Input('bar', 'clickData')]
    )
    def display_click_data(clickData):
        if clickData is not None:
            username = str(clickData['points'][0]['x']).replace("@", "")
            url = f"https://www.twitter.com/{username}"
            webbrowser.open_new(url)

        return ''
