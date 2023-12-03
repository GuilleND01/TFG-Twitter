import pandas as pd
import json
from pandas import json_normalize
from src.utils.DataframeProcessing import DataFrameProcessing
import swifter

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
            url_foto = 'https://s2.abcstatics.com/media/estilo/2019/03/20/carmen-borrego-k7zH--1248x698@abc.jpg'
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

class UserMentions(DataFrameProcessing):
    def __init__(self, file_content):
        self.data = self.filecontent_to_df(file_content)
        self.build_dataframe_wres()

    def build_dataframe_wres(self):
        data_ft = self.data[~self.data["tweet.full_text"].str.contains("RT")]
        df = pd.DataFrame(data_ft['tweet.entities.user_mentions'])
        df = df[df['tweet.entities.user_mentions'].swifter.apply(lambda x: len(x) > 0)]

        df = df.explode('tweet.entities.user_mentions')
        df['usernames'] = df.swifter.apply(lambda row: '@' + dict(row['tweet.entities.user_mentions'])['screen_name'],
                                           axis=1)
        nuevo_df = df.swifter.groupby('usernames').apply(lambda x: x['usernames'].count()).reset_index(name='quantity')
        nuevo_df = nuevo_df.sort_values(by=['quantity'], ascending=False)

        nuevo_df = nuevo_df[:10]

        urls_imagenes = buscar_urls_imagenes(nuevo_df)
        nuevo_df['urls'] = nuevo_df.swifter.apply(lambda row: urls_imagenes[row['usernames']],
                                                          axis=1)
        self.data = nuevo_df

    def get_dataframe_wres(self):
        return self.data
