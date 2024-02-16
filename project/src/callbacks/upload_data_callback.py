import base64
import io

from dash.dependencies import Input, Output, State
from dash import html
from src.GUIs.mentions_gui import return_gui_mentions
from src.GUIs.lang_sentiments_gui import return_gui_langu_senti
from src.GUIs.profile_gui import return_gui_profile
from src.GUIs.friends_gui import return_gui_friends


def create_upload_data_callbacks(app):
    @app.callback(Output('output_languages', 'children'),
                  Output('output_sentiments', 'children'),
                  Output('output_menciones', 'children'),
                  Output('output_profile', 'children'),
                  Output('output_circle', 'children'),
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
                return None, None, None, None, None

            if 'account.js' in contents:
                account_decoded = content_decoded(contents['account.js'])
            else:
                # TODO alert
                return None, None, None, None, None

            if 'tweets.js' in contents:
                tweets_decoded = content_decoded(contents['tweets.js'])
            else:
                # TODO alert
                return None, None, None, None, None

            if 'ageinfo.js' in contents:
                ageinfo_decoded = content_decoded(contents['ageinfo.js'])
            else:
                # TODO alert
                return None, None, None, None, None

            if 'follower.js' in contents:
                followers_decoded = content_decoded(contents['follower.js'])
            else:
                # TODO alert
                return None, None, None, None, None

            if 'direct-messages.js' in contents:
                dms_decoded = content_decoded(contents['direct-messages.js'])
            else:
                # TODO alert
                return None, None, None, None, None

            output_languages, output_sentiments = None, None # return_gui_langu_senti(tweets_decoded)
            output_menciones = None #return_gui_mentions(tweets_decoded)
            output_profile = None # return_gui_profile(profile_decoded, ageinfo_decoded, account_decoded, tweets_decoded)
            output_circle = return_gui_friends(dms_decoded, tweets_decoded, followers_decoded, account_decoded)
            return output_languages, output_sentiments, output_menciones, output_profile, output_circle


def content_decoded(content):
    decoded = base64.b64decode(content.split(',')[1])
    return io.StringIO(decoded.decode('utf-8')).getvalue()
