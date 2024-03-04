import base64
import io
import requests
import threading

from dash.dependencies import Input, Output, State
from pprint import pprint

from src.GUIs.mentions_gui import return_gui_mentions
from src.GUIs.profile_gui import return_gui_profile
from src.GUIs.friends_gui import return_gui_friends
from src.GUIs.heatmap_activity_gui import return_heatmap_activiy_gui
from src.GUIs.sentiments_gui import return_gui_sentiments
from src.GUIs.languages_gui import return_gui_languages
import dash_bootstrap_components as dbc
from src.utils.bucket import Bucket

buck_inst = Bucket().get_instance()


class GestorHilos:
    def __init__(self):
        self.resultado_dict = {}
        self.lock = threading.Lock()

    def requests(self, tarea, url):
        res = requests.get(url)
        if res.status_code == 200:
            json_procesado = res.json()
        else:
            json_procesado = {}

        self.agregar_resultado({tarea: json_procesado})

    def agregar_resultado(self, resultado):
        with self.lock:
            self.resultado_dict.update(resultado)

    def devuelve_resultado(self):
        with self.lock:
            return self.resultado_dict


def cloud_functions(urls):
    listado_hilos = []
    gestiona_hilos = GestorHilos()

    for item in urls:
        listado_hilos.append(threading.Thread(target=gestiona_hilos.requests, args=(item[0], item[1],)))

    for hilo in listado_hilos:
        hilo.start()

    for hilo in listado_hilos:
        hilo.join()

    return gestiona_hilos.devuelve_resultado()


def create_upload_data_callbacks(app):
    @app.callback(Output('input-start', 'className'),
                  Output('output_languages', 'children'),
                  Output('output_sentiments', 'children'),
                  Output('output_menciones', 'children'),
                  Output('output_profile', 'children'),
                  Output('output_circle', 'children'),
                  Output('output_heatmap', 'children'),
                  Input('upload-data', 'contents'),
                  State('upload-data', 'filename'))
    def update_output(list_of_contents, list_of_names):
        if list_of_contents is not None:
            contents = {}
            # Aquí se haría la subida de los ficheros
            for content, filename in zip(list_of_contents, list_of_names):
                if content is not None:
                    contents[filename] = content

            # Si se han subido correctamente se configuran las urls de las CFs.
            user_id = '990664474792165377'

            urls = list()
            urls.append(['profile',
                         f'https://us-central1-tfg-twitter.cloudfunctions.net/profile?id={user_id}'])
            urls.append(['heat_map',
                         f'https://us-central1-tfg-twitter.cloudfunctions.net/heatmap_activity?id={user_id}'])
            urls.append(['senti_langu',
                         f'https://us-central1-tfg-twitter.cloudfunctions.net/sentimientos_lenguajes?id={user_id}&limit=30&traducir=False'])
            urls.append(['friends_circle',
                         f'https://us-central1-tfg-twitter.cloudfunctions.net/twitter-circle?id={user_id}'])
            urls.append(['user_mentions',
                         f'https://us-central1-tfg-twitter.cloudfunctions.net/user-mentions?id={user_id}'])

            responses = cloud_functions(urls)

            # Genera las GUIs correspondientes
            output_languages = return_gui_languages(responses['senti_langu'])
            output_sentiments = return_gui_sentiments(responses['senti_langu'])
            output_menciones = return_gui_mentions(responses['user_mentions'])
            output_profile = return_gui_profile(responses['profile'])
            output_circle = None # return_gui_friends(responses['friends_circle'])
            output_heatmap = return_heatmap_activiy_gui(responses['heat_map'])

            return 'd-none', output_languages, output_sentiments, output_menciones, output_profile, output_circle, output_heatmap

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
                  Input('color-data', 'contents'),
                  State('color-data', 'filename'))
    def update_output(list_of_contents, list_of_names):
        if list_of_contents is not None:
            filenames = []

            # Comprobamos los nombres de los ficheros que se han subido
            for content, filename in zip(list_of_contents, list_of_names):
                filenames.append(filename)

            scard_pu = {'border': '3px solid red'}
            scard_um = {'border': '3px solid red'}
            scard_lp = {'border': '3px solid red'}
            scard_as = {'border': '3px solid red'}
            scard_ca = {'border': '3px solid red'}
            scard_ra = {'border': '3px solid red'}
            scard_tu = {'border': '3px solid red'}
            scard_ga = {'border': '3px solid red'}

            if "account.js" not in filenames:
                return (dbc.Alert("El archivo account.js es obligatorio", color="danger", dismissable=True),
                        True, scard_pu, scard_um, scard_lp, scard_as, scard_ca, scard_ra, scard_tu, scard_ga)

            # Perfil de usuario
            if ("account.js" in filenames and "profile.js" in filenames and "direct-messages.js" in filenames
                    and "follower.js" in filenames):
                scard_pu = {'border': '3px solid green'}

            # Usuarios mencionados
            if "tweets.js" in filenames:
                scard_um = {'border': '3px solid green'}

            # Lenguajes predilectos
            if "tweets.js" in filenames:
                scard_lp = {'border': '3px solid green'}

            # Análisis de sentimientos
            if "tweets.js" in filenames:
                scard_as = {'border': '3px solid green'}

            # Círculo de amigos
            if ("profile.js" in filenames and "direct-messages.js" in filenames and "tweets.js" in filenames and
                    "follower.js" in filenames):
                scard_ca = {'border': '3px solid green'}

            # Registro de la actividad
            if ("tweet-headers.js" in filenames and "user-link-clicks.js" in filenames and "direct-message-headers.js"
                    in filenames and "direct-message-group-headers.js" in filenames and "ad-impressions.js"
                    in filenames):
                scard_ra = {'border': '3px solid green'}

            # Tracking de usuario

            # Gustos y anuncios

            return None, False, scard_pu, scard_um, scard_lp, scard_as, scard_ca, scard_ra, scard_tu, scard_ga


def content_decoded(content):
    decoded = base64.b64decode(content.split(',')[1])
    return io.StringIO(decoded.decode('utf-8')).getvalue()
