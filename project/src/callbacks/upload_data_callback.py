import base64
import io

from dash.dependencies import Input, Output, State

from src.GUIs.languages_gui import return_gui_languages
from src.GUIs.mentions_gui import return_gui_mentions
from src.GUIs.sentiments_gui import return_gui_sentiments


def create_upload_data_callbacks(app):
    @app.callback(Output('output_languages', 'children'),
                  Output('output_sentiments', 'children'),
                  Output('output_menciones', 'children'),
                  Input('upload-data', 'contents'),
                  State('upload-data', 'filename'))
    def update_output(list_of_contents, list_of_names):
        if list_of_contents is not None:
            for content, filename in zip(list_of_contents, list_of_names):
                if content is not None:
                    if filename == 'tweets.js':
                        tweets_decoded = content_decoded(content)
                        output_languages = None #return_gui_languages(tweets_decoded)
                        output_sentiments = None #return_gui_sentiments(tweets_decoded)
                        output_menciones = return_gui_mentions(tweets_decoded)
                        return output_languages, output_sentiments, output_menciones


def content_decoded(content):
    decoded = base64.b64decode(content.split(',')[1])
    return io.StringIO(decoded.decode('utf-8')).getvalue()
