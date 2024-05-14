from dash.dependencies import Input, Output
import webbrowser
from dash import clientside_callback, html, no_update, dcc



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

def create_pic_hover(app):
    @app.callback(
        Output("mention-tool", "show"),
        Output("mention-tool", "bbox"),
        Output("mention-tool", "children"),
        Input("bar", "hoverData"),
    )
    def update_tooltip_content(hoverData):
        if hoverData is None:
            return False, None, None

        user = html.Strong(hoverData["points"][0]['x'])
        mentions = hoverData["points"][0]['y']
        url = hoverData["points"][0]['customdata'][0]
        bbox = hoverData["points"][0]["bbox"]

        children = [
            html.Div(html.Img(src=url, width='75px', height='75px', className='rounded-circle'),
                     className='d-flex justify-content-center align-items-center'),
            html.Br(),
            html.Div(
                children=[
                    'Has mencionado al usuario ',
                    html.Br(),
                    html.P([user, f' {mentions} veces'])
                ], style={'text-align': 'center'})
        ]

        return True, bbox, children
