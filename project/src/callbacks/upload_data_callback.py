import base64
import io
import json

from dash.dependencies import Input, Output, State

from GUIs.mentions_gui import return_gui_mentions
from GUIs.profile_gui import return_gui_profile
from GUIs.friends_gui import return_gui_friends
from GUIs.heatmap_activity_gui import return_heatmap_activiy_gui
from GUIs.sentiments_gui import return_gui_sentiments
from GUIs.languages_gui import return_gui_languages
from GUIs.downloads_gui import return_download_gui
from GUIs.advertiser_info_gui import return_gui_advertisers
from GUIs.person_criteria_gui import return_gui_criteria
import dash_bootstrap_components as dbc
from utils.filemanager import FileManager
from dash import html
from utils.cloudfunctionsmanager import CloudFunctionManager
from utils.bucket import Bucket

#  Instancias de las clases encargadas de la gestión
cloud_instance = CloudFunctionManager.get_instance()

cf_list = []


def create_upload_data_callbacks(app):
    @app.callback(Output('alerta-archivos', 'children'),
                  Output('submit', 'disabled'),
                  Output('card-pu', 'style'),
                  Output('card-um', 'style'),
                  Output('card-lp', 'style'),
                  Output('card-as', 'style'),
                  Output('card-ca', 'style'),
                  Output('card-ra', 'style'),
                  Output('card-tu', 'style'),
                  Output('card-ga', 'style'),
                  Input('upload-data', 'contents'),
                  State('upload-data', 'filename'))
    def update_output(list_of_contents, list_of_names):
        file_mgmt = FileManager.get_instance()
        if list_of_contents is not None:
            # Comprobamos los nombres de los ficheros que se han subido
            for content, filename in zip(list_of_contents, list_of_names):
                if content is not None:
                    if file_mgmt.agg_file(filename, content_decoded(content)):
                        break

            file_list = file_mgmt.get_file_list()

            scard_pu = {'border': '3px solid red'}
            scard_um = {'border': '3px solid red'}
            scard_lp = {'border': '3px solid red'}
            scard_as = {'border': '3px solid red'}
            scard_ca = {'border': '3px solid red'}
            scard_ra = {'border': '3px solid red'}
            scard_tu = {'border': '3px solid red'}
            scard_ga = {'border': '3px solid red'}

            # Si el fichero no es descargado, cogemos el id.
            cf_avai = {}
            if not file_mgmt.get_download_file():
                if "account.js" not in file_list:
                    return (dbc.Alert("El archivo account.js es obligatorio", color="danger", dismissable=True),
                            True, scard_pu, scard_um, scard_lp, scard_as, scard_ca, scard_ra, scard_tu, scard_ga)

                #  Lee el contenido del fichero account.js para sacar el ID de usuario
                ac_json = json.loads(file_list['account.js'].replace('window.YTD.account.part0 = ', ''))[0]
                user_id = ac_json['account']['accountId']
                username = '@' + ac_json['account']['username']
                #  Almacenamos el ID en la instancia
                file_mgmt.set_user_id(user_id)
                file_mgmt.set_username(username)
            else:
                cf_avai = eval(file_mgmt.get_download_content())

            print(file_list.keys())

            # Perfil de usuario
            if (("profile.js" in file_list and "ageinfo.js" in file_list and 'manifest.js' in file_list)
                    or 'profile' in cf_avai):
                scard_pu = {'border': '3px solid green', 'background-color': 'rgba(0, 128, 0, 0.2)', 'opacity': '1'}
                cf_list.append('profile')

            # Usuarios mencionados
            if ("tweets.js" in file_list) or 'user-mentions' in cf_avai:
                scard_um = {'border': '3px solid green', 'background-color': 'rgba(0, 128, 0, 0.2)', 'opacity': '1'}
                cf_list.append('user-mentions')

            # Lenguajes predilectos y análisis de sentimientos
            if "tweets.js" in file_list or 'sentimientos_lenguajes' in cf_avai:
                scard_lp = {'border': '3px solid green', 'background-color': 'rgba(0, 128, 0, 0.2)', 'opacity': '1'}
                scard_as = {'border': '3px solid green', 'background-color': 'rgba(0, 128, 0, 0.2)', 'opacity': '1'}
                cf_list.append('sentimientos_lenguajes')

            # Círculo de amigos
            if (("profile.js" in file_list and "direct-message-headers.js" in file_list and "tweets.js" in file_list and
                 "follower.js" in file_list and "following.js" in file_list) or 'twitter-circle' in cf_avai):
                scard_ca = {'border': '3px solid green', 'background-color': 'rgba(0, 128, 0, 0.2)', 'opacity': '1'}
                cf_list.append('twitter-circle')

            # Registro de la actividad
            if ("tweets.js" in file_list and "manifest.js" in file_list) or 'heatmap_activity' in cf_avai:
                if (("user-link-clicks.js" in file_list and "direct-message-headers.js"
                     in file_list and "direct-message-group-headers.js" in file_list and "ad-impressions.js"
                     in file_list) or 'heatmap_activity' in cf_avai):
                    scard_ra = {'border': '3px solid green', 'background-color': 'rgba(0, 128, 0, 0.2)', 'opacity': '1'}
                else:
                    scard_ra = {'border': '3px solid yellow'}

                cf_list.append('heatmap_activity')

            # Criterios más relevantes
            if 'ad-engagements.js' in file_list or 'person-criteria' in cf_avai:
                scard_tu = {'border': '3px solid green', 'background-color': 'rgba(0, 128, 0, 0.2)', 'opacity': '1'}
                cf_list.append('person-criteria')

            # Anunciantes más interesados
            if "ad-engagements.js" in file_list or 'advertiser-info-1' in cf_avai:
                scard_ga = {'border': '3px solid green', 'background-color': 'rgba(0, 128, 0, 0.2)', 'opacity': '1'}
                cf_list.append('advertiser-info-1')

            return None, False, scard_pu, scard_um, scard_lp, scard_as, scard_ca, scard_ra, scard_tu, scard_ga

    @app.callback(
        Output('input-start', 'className'),
        Output('output_languages', 'children'),
        Output('output_sentiments', 'children'),
        Output('output_menciones', 'children'),
        Output('output_profile', 'children'),
        Output('output_circle', 'children'),
        Output('output_heatmap', 'children'),
        Output('output_download', 'children'),
        Output('output_aden1', 'children'),
        Output('output_aden2', 'children'),
        [Input('submit', 'n_clicks')]
    )
    def actualizar_output(n_clicks):
        if n_clicks is not None:
            buck_inst = None
            file_mgmt = FileManager.get_instance()
            if not file_mgmt.get_download_file():
                _id = file_mgmt.get_id()
                # Crea una instancia del bucket
                buck_inst = Bucket(file_mgmt.get_file_list(), _id)
                # Sube los ficheros almacenados
                buck_inst.upload_data()
                # Guarda el nombre de usuario
                cloud_instance.set_username(file_mgmt.get_username())
                # Crea la lista de las Cloud Functions
                cloud_instance.compose_list(_id, cf_list)
                # Realiza las llamadas
                cloud_instance.launch_functions()
                # Obtiene el resultado
                res = cloud_instance.get_results()
            else:
                res = eval(file_mgmt.get_download_content())
                cloud_instance.set_results(res)

            print(res)

            # Por defecto, las vistas que se van a devolver van a ser None
            lenguajes = None
            sentiments = None
            menciones = None
            profile = None
            circle = None
            heatmap = None
            adinfo = None
            percri = None

            # Comprobamos para cada una de las funcionalidades si tiene resultados
            if 'sentimientos_lenguajes' in res:
                lenguajes = return_gui_languages(res['sentimientos_lenguajes'])
                sentiments = return_gui_sentiments(res['sentimientos_lenguajes'])

            if 'user-mentions' in res:
                menciones = return_gui_mentions(res['user-mentions'])

            if 'profile' in res:
                profile = return_gui_profile(res['profile'])

            if 'twitter-circle' in res:
                circle = return_gui_friends(res['twitter-circle'])

            if 'heatmap_activity' in res:
                heatmap = return_heatmap_activiy_gui(res['heatmap_activity'])

            if 'advertiser-info-1' in res:
                adinfo = return_gui_advertisers(res['advertiser-info-1'])

            if 'person-criteria' in res:
                percri = return_gui_criteria(res['person-criteria'])

            # Borra los ficheros antes de salir
            if not file_mgmt.get_download_file():
                # buck_inst.delete_data()
                down = return_download_gui()
            else:
                down = None

            return 'd-none', lenguajes, sentiments, menciones, profile, circle, heatmap, down, percri, adinfo

    @app.callback(
        Output('enviar_div', 'children'),
        [Input('submit', 'n_clicks')]
    )
    def actualizar_boton_loading(n_clicks):
        if n_clicks is not None:
            return html.Div(className='spinner-border text-primary')
        else:
            return [dls.RingChase(children=[
                dbc.Button('Enviar', id='submit', style={'display': 'block', 'margin': '0 auto'},
                           disabled=True),
            ], color='#435278', fullscreen=True, debounce=1000)]

    @app.callback(
        Output('whitebox-3', 'children'),
        [Input('url', 'href')]
    )
    def on_page_reload(href):
        FileManager.reset_instance()
        cf_list.clear()


def content_decoded(content):
    decoded = base64.b64decode(content.split(',')[1])
    return io.StringIO(decoded.decode('utf-8')).getvalue()
