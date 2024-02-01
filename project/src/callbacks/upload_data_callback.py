import base64
import io

from dash.dependencies import Input, Output, State
from src.GUIs.mentions_gui import return_gui_mentions
from src.GUIs.lang_sentiments_gui import return_gui_langu_senti
from src.GUIs.profile_gui import return_gui_profile


def create_upload_data_callbacks(app):
    @app.callback(Output('output_languages', 'children'),
                  Output('output_sentiments', 'children'),
                  Output('output_menciones', 'children'),
                  Output('output_profile', 'children'),
                  Input('upload-data', 'contents'),
                  State('upload-data', 'filename'))
    def update_output(list_of_contents, list_of_names):
        if list_of_contents is not None:
            contents = {}
            for content, filename in zip(list_of_contents, list_of_names):
                if content is not None:
                    contents[filename] = content

            if 'profile.js' in contents:
                profile_decoded = content_decoded(contents['profile.js'])
            else:
                # TODO alert
                return None, None, None, None

            if 'account.js' in contents:
                account_decoded = content_decoded(contents['account.js'])
            else:
                # TODO alert
                return None, None, None, None

            if 'tweets.js' in contents:
                tweets_decoded = content_decoded(contents['tweets.js'])
            else:
                # TODO alert
                return None, None, None, None

            if 'ageinfo.js' in contents:
                ageinfo_decoded = content_decoded(contents['ageinfo.js'])
            else:
                # TODO alert
                return None, None, None, None

            output_languages, output_sentiments = return_gui_langu_senti(tweets_decoded)
            output_menciones = return_gui_mentions(tweets_decoded)
            output_profile = return_gui_profile(profile_decoded, ageinfo_decoded, account_decoded, tweets_decoded)
            return output_languages, output_sentiments, output_menciones, output_profile


def content_decoded(content):
    decoded = base64.b64decode(content.split(',')[1])
    return io.StringIO(decoded.decode('utf-8')).getvalue()
