from dash import dcc
import plotly.express as px
from src.scripts.usuarios_mas_mencionados import return_user_mentions_df
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import threading


class GestorHilos:
    def __init__(self):
        self.resultado_dict = {}
        self.lock = threading.Lock()

    def urls_imagenes(self, user):
        # Configuración del navegador Chrome
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # remove this for easy debbuing on your laptop /pc
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--enable-javascript")

        # Crear una instancia del navegador Chrome
        driver = webdriver.Chrome(options=chrome_options)

        # URL a abrir
        url = "https://twiteridfinder.com/"
        url_usr = user.replace('@', '')
        driver.get(url)

        element = driver.find_element(By.ID, "tweetbox2")
        element.send_keys(f"https://twitter.com/{url_usr}")

        element2 = driver.find_element(By.ID, 'button_convert')
        element2.click()

        time.sleep(10)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        etiquetas = soup.find('img', id='js-image')

        url_foto = str(etiquetas['src'])
        if 'https://' not in url_foto:
            url_foto = 'https://images.ecestaticos.com/9dglTZcZ96SbPBB7i3X3FP_a4FU=/0x0:0x0/1200x900/filters:fill(white):format(jpg)/f.elconfidencial.com%2Foriginal%2F038%2F7b4%2Fa2e%2F0387b4a2e6487657b19f7168faa3a9c4.jpg'

        self.agregar_resultado({user: url_foto})

    def agregar_resultado(self, resultado):
        with self.lock:
            self.resultado_dict.update(resultado)

    def devuelve_resultado(self):
        return self.resultado_dict

def buscar_urls_imagenes(df_menciones):
    listado_hilos = []
    gestiona_hilos = GestorHilos()

    for index, row in df_menciones.iterrows():
        listado_hilos.append(threading.Thread(target=gestiona_hilos.urls_imagenes, args=(row['usernames'],)))

    for hilo in listado_hilos:
        hilo.start()

    for hilo in listado_hilos:
        hilo.join()

    return gestiona_hilos.devuelve_resultado()


def return_gui_mentions(info_decoded):
    df_menciones = return_user_mentions_df(info_decoded)
    urls_imagenes = buscar_urls_imagenes(df_menciones)
    df_menciones['urls'] = df_menciones.swifter.apply(lambda row: urls_imagenes[row['usernames']],
                                       axis=1)
    return dcc.Graph(id='bar',
                     figure={
                         'data': [
                             {'x': list(df_menciones['usernames']), 'y': list(df_menciones['quantity']), 'type': 'bar'}
                         ],
                         'layout': {
                             'images': [
                                 {
                                     'source': row['urls'],
                                     'xref': 'x',
                                     'yref': 'y',
                                     'x': row['usernames'],
                                     'y': row['quantity'] - 1,
                                     'sizex': 3,
                                     'sizey': 3,
                                     'xanchor': 'center',
                                     'yanchor': 'bottom'
                                 } for index, row in df_menciones.iterrows()
                             ],
                             'barmode': 'group',
                             'title': 'Gráfico de Barras con Imágenes'
                         }
                     })
