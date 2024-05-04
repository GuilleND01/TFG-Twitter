from dash.dependencies import Input, Output
import webbrowser
from dash import clientside_callback



def create_bar_clicks(app):

    clientside_callback("""
    function (clickData) {
        if (clickData !== null) {
            var username = clickData.points[0].x.replace("@", "");
            var url = 'https://www.twitter.com/' + username;
            window.open(url);
        }
    }
    """, Output('whitebox', 'children'), [Input('bar', 'clickData')])


def create_bubble_clicks(app):

    clientside_callback("""
    function (clickData) {
        if (clickData !== null) {
            var url = clickData['points'][0]['customdata'][0];
            window.open(url);
        }
    }
    """, Output('whitebox-1', 'children'), [Input('friends-circle', 'clickData')])
