import json
import pandas as pd
import threading
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from src.utils.DataframeProcessing import DataFrameProcessing
from pandas import json_normalize


class GestorHilos:
    def __init__(self):
        self.resultado_dict = {}
        self.lock = threading.Lock()

    def urls_imagenes(self, user):
        # Crear una instancia del navegador Chrome
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--enable-javascript")
        driver = webdriver.Chrome(options=chrome_options)

        # URL a abrir
        url = "https://twiteridfinder.com/"
        driver.get(url)

        element = driver.find_element(By.ID, "tweetbox2")
        element.send_keys(f"{user}")

        driver.execute_script("submitData()")

        wait = WebDriverWait(driver, 10)
        image = wait.until(EC.presence_of_element_located((By.ID, "js-image")))

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            url_foto = image.get_attribute("src")
            if 'https://' not in url_foto:
                url_foto = 'https://pbs.twimg.com/profile_images/1673667148365852673/lJ7aNs77_normal.jpg'
        except NoSuchElementException:
            url_foto = 'https://pbs.twimg.com/profile_images/1673667148365852673/lJ7aNs77_normal.jpg'

        etiquetas = soup.find('div', id='js-results-username')
        username = etiquetas.find('a')
        if username is not None:
            username = username.text
        else:
            username = f'@{user}'

        response = requests.get(url_foto)

        driver.quit()
        self.agregar_resultado({user: [username, response.content]})

    def agregar_resultado(self, resultado):
        with self.lock:
            self.resultado_dict.update(resultado)

    def devuelve_resultado(self):
        return self.resultado_dict


class FriendsCircle(DataFrameProcessing):
    def __init__(self, mds_decoded, tweets_decoded, followers_decoded, account_decoded, profile_decoded):
        self.profile_info = profile_decoded.replace('window.YTD.profile.part0 = ', '')
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

    def build_url_toprofile(self, user_id):
        return f'https://twitter.com/intent/user?user_id={user_id}'

    def build_dataframe_wres(self):
        # Info de account.js
        json_dat_ac = json.loads(self.account_info)

        # Info de profile.js
        json_dat_fi = json.loads(self.profile_info)

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

        # Construimos el dataframe final
        dict_df = {
            'user_ids': capa,
            'x': [0, -23.51, -38.04, -38.04, -23.51,   0,  23.51,  38.04, 38.04, 23.51],
            'y': [40, 32.36,  12.36, -12.36, -32.36, -40, -32.36, -12.36, 12.36, 32.36],
            'imgs': [
                'https://static.vecteezy.com/system/resources/previews/020/168/486/non_2x/cheerful-neat-man-flat-avatar-icon-with-green-dot-editable-default-persona-for-ux-ui-design-profile-character-picture-with-online-status-indicator-color-messaging-app-user-badge-vector.jpg',
                'https://static.vecteezy.com/system/resources/previews/020/168/661/original/pleased-woman-with-earrings-flat-avatar-icon-with-green-dot-editable-default-persona-for-ux-ui-design-profile-character-picture-with-online-status-indicator-color-messaging-app-user-badge-vector.jpg',
                'https://static.vecteezy.com/system/resources/previews/020/168/711/non_2x/excited-boy-with-kinky-hair-flat-avatar-icon-with-green-dot-editable-default-persona-for-ux-ui-design-profile-character-picture-with-online-status-indicator-color-messaging-app-user-badge-vector.jpg',
                'https://static.vecteezy.com/system/resources/previews/020/168/718/original/smiling-female-student-flat-avatar-icon-with-green-dot-editable-default-persona-for-ux-ui-design-profile-character-picture-with-online-status-indicator-colorful-messaging-app-user-badge-vector.jpg',
                'https://static.vecteezy.com/system/resources/previews/020/168/491/non_2x/happy-man-with-curly-red-hair-flat-avatar-icon-with-green-dot-editable-default-persona-for-ux-ui-design-profile-character-picture-with-online-status-indicator-color-messaging-app-user-badge-vector.jpg',
                'https://static.vecteezy.com/system/resources/previews/020/168/701/non_2x/pretty-ginger-haired-girl-flat-avatar-icon-with-green-dot-editable-default-persona-for-ux-ui-design-profile-character-picture-with-online-status-indicator-colorful-messaging-app-user-badge-vector.jpg',
                'https://static.vecteezy.com/system/resources/previews/020/168/719/non_2x/pretty-boy-with-stylish-hairstyle-flat-avatar-icon-with-green-dot-editable-default-persona-for-ux-ui-design-profile-character-picture-with-online-status-color-messaging-app-user-badge-vector.jpg',
                'https://static.vecteezy.com/system/resources/previews/020/168/661/original/pleased-woman-with-earrings-flat-avatar-icon-with-green-dot-editable-default-persona-for-ux-ui-design-profile-character-picture-with-online-status-indicator-color-messaging-app-user-badge-vector.jpg',
                'https://static.vecteezy.com/system/resources/previews/020/168/711/non_2x/excited-boy-with-kinky-hair-flat-avatar-icon-with-green-dot-editable-default-persona-for-ux-ui-design-profile-character-picture-with-online-status-indicator-color-messaging-app-user-badge-vector.jpg',
                'https://static.vecteezy.com/system/resources/previews/020/168/718/original/smiling-female-student-flat-avatar-icon-with-green-dot-editable-default-persona-for-ux-ui-design-profile-character-picture-with-online-status-indicator-colorful-messaging-app-user-badge-vector.jpg',
            ]
        }

        df = pd.DataFrame(dict_df)
        df['prof_url'] = df['user_ids'].apply(lambda x: self.build_url_toprofile(x))
        df['pond'] = 1

        df['puntua'] = df['user_ids'].apply(lambda x: round(df_punt.loc[df_punt['UserId'] == x, 'Punt'].iloc[0], 2))
        new_row = pd.DataFrame({'user_ids': [json_dat_ac[0]['account']["accountId"]], 'x': [0], 'y': [0],
                                'username': ['@' + json_dat_ac[0]['account']['username']],
                                'prof_url': [self.build_url_toprofile(json_dat_ac[0]['account']["accountId"])],
                                'pond': [1.5],
                                'puntua': [1],
                                'imgs': ['https://static.vecteezy.com/system/resources/previews/020/168/486/non_2x/cheerful-neat-man-flat-avatar-icon-with-green-dot-editable-default-persona-for-ux-ui-design-profile-character-picture-with-online-status-indicator-color-messaging-app-user-badge-vector.jpg',]})

        df = pd.concat([df, new_row], ignore_index=True)
        return df
