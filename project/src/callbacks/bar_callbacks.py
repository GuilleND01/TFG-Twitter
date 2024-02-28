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

def create_bubble_clicks(app):
    @app.callback(
        Output('whitebox-1', 'children'),
        [Input('friends-circle', 'clickData')]
    )
    def display_click_data(clickData):
        if clickData is not None:
            url = clickData['points'][0]['customdata'][0]
            webbrowser.open_new(url)

        return ''
