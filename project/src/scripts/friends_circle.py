import json
import pandas as pd
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from src.utils.DataframeProcessing import DataFrameProcessing
from pandas import json_normalize

class GestorHilos:
    def __init__(self):
        self.resultado_dict = {}
        self.local_driver = threading.local()  # Almacenamiento local por hilo

    def get_driver(self):
        if not hasattr(self.local_driver, "driver"):
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--enable-javascript")
            self.local_driver.driver = webdriver.Chrome(options=chrome_options)
        return self.local_driver.driver

    def urls_imagenes(self, user):
        # Crear una instancia del navegador Chrome
        driver = self.get_driver()

        # URL a abrir
        url = "https://twiteridfinder.com/"
        driver.get(url)

        element = driver.find_element(By.ID, "tweetbox2")
        element.send_keys(f"{user}")

        element2 = driver.find_element(By.ID, 'button_convert')
        element2.click()

        time.sleep(10)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        etiquetas = soup.find('img', id='js-image')

        url_foto = str(etiquetas['src'])
        if 'https://' not in url_foto:
            url_foto = 'https://pbs.twimg.com/profile_images/1673667148365852673/lJ7aNs77_normal.jpg'
            #url_foto = 'https://www.lecturas.com/medio/2022/09/08/lydia-lozano_3e165191_800x800.jpg'

        etiquetas = soup.find('div', id='js-results-username')
        username = etiquetas.find('a')
        if username is not None:
            username = username.text
        else:
            username = f'@{user}'

        response = requests.get(url_foto)

        self.agregar_resultado({user: [username, response.content]})

    def agregar_resultado(self, resultado):
        self.resultado_dict.update(resultado)

    def devuelve_resultado(self):
        return self.resultado_dict


class FriendsCircle(DataFrameProcessing):
    def __init__(self, mds_decoded, tweets_decoded, followers_decoded, account_decoded):
        self.account_info = account_decoded.replace('window.YTD.account.part0 = ', '')
        self.mds_info = mds_decoded.replace('window.YTD.direct_messages.part0 = ', '')
        self.follow_info = followers_decoded.replace('window.YTD.follower.part0 = ', '')
        self.twits_info = tweets_decoded.replace('window.YTD.tweets.part0 = ', '')
        self.result = self.build_dataframe_wres()

    def get_dataframe_wres(self):
        return self.result

    def suma_con_pesos(self, row):
        pesos = {'MDs': 0.45, 'Mentions': 0.2, 'Follows': 0.2,
                 'RTs': 0.15}

        return row['MDs'] * pesos['MDs'] + row['Mentions'] * pesos['Mentions'] + row['Follows'] * pesos['Follows'] + \
            row['RTs'] * pesos['RTs']

    def buscar_urls_imagenes(self, id_list):
        listado_hilos = []
        gestiona_hilos = GestorHilos()

        for item in id_list:
            listado_hilos.append(threading.Thread(target=gestiona_hilos.urls_imagenes, args=(item,)))

        for hilo in listado_hilos:
            hilo.start()

        for hilo in listado_hilos:
            hilo.join()

        return gestiona_hilos.devuelve_resultado()

    def build_dataframe_wres(self):
        # Info de account.js
        json_dat_ac = json.loads(self.account_info)

        # Info de direct-messages.js
        json_dat_dm = json.loads(self.mds_info)
        data = json_normalize(json_dat_dm)
        data = data.explode('dmConversation.messages')

        df = pd.DataFrame(data['dmConversation.messages'].apply(lambda x: x['messageCreate']['senderId']))
        df = df[~df["dmConversation.messages"].str.contains(json_dat_ac[0]['account']["accountId"])]

        df = df.groupby('dmConversation.messages').apply(lambda x: x['dmConversation.messages'].count()).reset_index(
            name='MDs')
        df_mds = df.sort_values(by=['MDs'], ascending=False)

        df_mds.columns = ['UserId', 'MDs']

        # Info de follower.js
        json_dat_fol = json.loads(self.follow_info)
        data = json_normalize(json_dat_fol)

        df = pd.DataFrame(data['follower.accountId'])
        df_fol = df.assign(Follows=1)

        df_fol.columns = ['UserId', 'Follows']

        # Info de tweets.js
        json_dat_twe = json.loads(self.twits_info)
        data = json_normalize(json_dat_twe)

        twe_rts = data[data["tweet.full_text"].str.contains("RT")]
        twe_norts = data[~data["tweet.full_text"].str.contains("RT")]

        # 1. Mentions
        df = pd.DataFrame(twe_norts['tweet.entities.user_mentions'])
        df = df[df['tweet.entities.user_mentions'].apply(lambda x: len(x) > 0)]

        df = df.explode('tweet.entities.user_mentions')
        df['usernames'] = df.apply(lambda row: dict(row['tweet.entities.user_mentions'])['id'],
                                   axis=1)
        nuevo_df = df.groupby('usernames').apply(lambda x: x['usernames'].count()).reset_index(name='Mentions')
        nuevo_df = nuevo_df.sort_values(by=['Mentions'], ascending=False)

        df_men = nuevo_df[~nuevo_df["usernames"].str.contains(json_dat_ac[0]['account']["accountId"])]
        df_men.columns = ['UserId', 'Mentions']

        # 2. RTs
        df = pd.DataFrame(twe_rts['tweet.entities.user_mentions'])
        df = df[df['tweet.entities.user_mentions'].apply(lambda x: len(x) > 0)]

        df = df.explode('tweet.entities.user_mentions')
        df['usernames'] = df.apply(lambda row: dict(row['tweet.entities.user_mentions'])['id'],
                                   axis=1)
        nuevo_df = df.groupby('usernames').apply(lambda x: x['usernames'].count()).reset_index(name='Mentions')
        nuevo_df = nuevo_df.sort_values(by=['Mentions'], ascending=False)

        df_rts = nuevo_df[~nuevo_df["usernames"].str.contains(json_dat_ac[0]['account']["accountId"])]
        df_rts.columns = ['UserId', 'RTs']

        # Juntamos los dataframes anteriores
        df_punt = pd.merge(df_mds, df_fol, on='UserId', how='outer').fillna(0)
        df_punt = pd.merge(df_punt, df_men, on='UserId', how='outer').fillna(0)
        df_punt = pd.merge(df_punt, df_rts, on='UserId', how='outer').fillna(0)

        # Limpiamos posibles IDs no válidos y la presencia del usuario
        df_punt = df_punt[~df_punt["UserId"].str.contains(json_dat_ac[0]['account']["accountId"])]
        df_punt = df_punt[~df_punt["UserId"].str.contains("-1")]

        # Hacemos la suma con los pesos
        df_punt['Punt'] = df_punt.apply(self.suma_con_pesos, axis=1)
        df_punt = df_punt.sort_values(by=['Punt'], ascending=False)

        # Cogemos los 10 con mayor peso
        capa = df_punt.iloc[0:10, 0].values.tolist()

        # Buscamos las imágenes y el username
        img_usrs = self.buscar_urls_imagenes(capa)

        # Construimos el dataframe final
        dict_df = {
            'user_ids': capa,
            'x': [0,  -23.51, -38.04, -38.04, -23.51,   0,  23.51,  38.04, 38.04, 23.51],
            'y': [40,  32.36,  12.36, -12.36, -32.36, -40, -32.36, -12.36, 12.36, 32.36],
        }

        df = pd.DataFrame(dict_df)
        df['username'] = df['user_ids'].apply(lambda x: img_usrs[x][0])
        df['img_url'] = df['user_ids'].apply(lambda x: img_usrs[x][1])
        df['pond'] = range(10, 0,
                           -1)  # df['user_ids'].apply(lambda x : df_punt.loc[df_punt['UserId'] == x].values[0][5])
        df['pond'] = 1  # df['pond'].apply(lambda x : x / 100)

        return df
