import base64
import io
import json

from dash.dependencies import Input, Output, State

from src.GUIs.mentions_gui import return_gui_mentions
from src.GUIs.profile_gui import return_gui_profile
from src.GUIs.friends_gui import return_gui_friends
from src.GUIs.heatmap_activity_gui import return_heatmap_activiy_gui
from src.GUIs.sentiments_gui import return_gui_sentiments
from src.GUIs.languages_gui import return_gui_languages
from src.GUIs.downloads_gui import return_download_gui
import dash_bootstrap_components as dbc
from src.utils.filemanager import FileManager
from src.utils.cloudfunctionsmanager import CloudFunctionManager
from src.utils.bucket import Bucket

#  Instancias de las clases encargadas de la gestión
file_mgmt = FileManager()
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

                #  Almacenamos el ID en la instancia
                file_mgmt.set_user_id(user_id)
            else:
                cf_avai = eval(file_mgmt.get_download_content())

            print(file_list.keys())

            # Perfil de usuario
            if ("profile.js" in file_list and "ageinfo.js" in file_list) or 'profile' in cf_avai:
                scard_pu = {'border': '3px solid green'}
                cf_list.append('profile')

            # Usuarios mencionados
            if "tweets.js" in file_list or 'user-mentions' in cf_avai:
                scard_um = {'border': '3px solid green'}
                # cf_list.append('user-mentions')

            # Lenguajes predilectos y análisis de sentimientos
            if "tweets.js" in file_list or 'sentimientos-lenguajes' in cf_avai:
                scard_lp = {'border': '3px solid green'}
                scard_as = {'border': '3px solid green'}
                # cf_list.append('sentimientos_lenguajes')

            # Círculo de amigos
            if (("profile.js" in file_list and "direct-message-headers.js" in file_list and "tweets.js" in file_list and
                    "follower.js" in file_list and "following.js" in file_list) or 'twitter-circle' in cf_avai):
                scard_ca = {'border': '3px solid green'}
                cf_list.append('twitter-circle')

            # Registro de la actividad
            if "tweets.js" in file_list or 'heatmap_activity' in cf_avai:
                if ("user-link-clicks.js" in file_list and "direct-message-headers.js"
                        in file_list and "direct-message-group-headers.js" in file_list and "ad-impressions.js"
                        in file_list):
                    scard_ra = {'border': '3px solid green'}
                else:
                    scard_ra = {'border': '3px solid yellow'}

                # cf_list.append('heatmap_activity')

            # Tracking de usuario

            # Gustos y anuncios

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
        [Input('submit', 'n_clicks')]
    )
    def actualizar_output(n_clicks):
        if n_clicks is not None:
            buck_inst = None
            if not file_mgmt.get_download_file():
                _id = file_mgmt.get_id()
                # Crea una instancia del bucket
                buck_inst = Bucket(file_mgmt.get_file_list(), _id)
                # Sube los ficheros almacenados
                buck_inst.upload_data()
                # Crea la lista de las Cloud Functions
                cloud_instance.compose_list(_id, cf_list)
                # Realiza las llamadas
                cloud_instance.launch_functions()
                # Obtiene el resultado
                res = cloud_instance.get_results()
            else:
                res = eval(file_mgmt.get_download_content())

            print(res)

            # Por defecto, las vistas que se van a devolver van a ser None
            lenguajes = None
            sentiments = None
            menciones = None
            profile = None
            circle = None
            heatmap = None

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

            # Borra los ficheros antes de salir
            if not file_mgmt.get_download_file():
                buck_inst.delete_data()
                down = return_download_gui()
            else:
                down = None

            return 'd-none', lenguajes, sentiments, menciones, profile, circle, heatmap, down


def content_decoded(content):
    decoded = base64.b64decode(content.split(',')[1])
    return io.StringIO(decoded.decode('utf-8')).getvalue()
