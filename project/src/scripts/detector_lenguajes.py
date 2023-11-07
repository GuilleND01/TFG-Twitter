from langdetect import detect
import pandas as pd
import json
from pandas import json_normalize


def language_from_code(cod):
    language_codes = {'af': 'Africano', 'ar': 'Árabe', 'bg': 'Búlgaro', 'bn': 'Bengalí', 'ca': 'Catalán', 'cs': 'Checo',
                      'cy': 'Galés', 'da': 'Danés', 'de': 'Alemán', 'el': 'Griego', 'en': 'Inglés', 'es': 'Español',
                      'et': 'Estonio', 'fa': 'Persa', 'fi': 'Finés', 'fr': 'Francés', 'gu': 'Gujarati', 'he': 'Hebreo',
                      'hr': 'Croata', 'hu': 'Húngaro', 'id': 'Indonedsio', 'it': 'Italiano', 'ja': 'Japonés',
                      'kn': 'Kannada', 'ko': 'Coreano', 'lt': 'Lituano', 'lv': 'Letón', 'mk': 'Macedonio',
                      'ml': 'Malasio', 'mr': 'Marathi', 'ne': 'Nepalí', 'no': 'Noruego', 'pl': 'Polaco',
                      'pt': 'Portugués', 'ro': 'Rumano', 'sk': 'Eslovaco', 'sl': 'Esloveno', 'so': 'Somalí',
                      'sq': 'Albanés', 'sv': 'Sueco', 'sw': 'Suajili', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Tailandés',
                      'tl': 'Tagalo', 'tr': 'Turco', 'vi': 'Vietnamita'}

    return language_codes[cod]


def detect_text_language(text):
    return language_from_code(detect(text))


def return_language_df(file_content):
    # Open the js file
    # with open("filename", "r", encoding="UTF-8") as js_file:
    #    js_code = js_file.read()

    # Remove \n
    js_code = file_content.replace('\n', '')
    js_code = js_code.replace('window.YTD.tweets.part0 = ', '')

    # Read the json and obtain a df
    json_dat = json.loads(js_code)
    data = json_normalize(json_dat)

    data = pd.DataFrame(data['tweet.full_text'])

    # Add a new column with the language column (no quantities)
    data['language'] = data.apply(lambda row: detect_text_language(row['tweet.full_text']), axis=1)
    df = pd.DataFrame(data['language'])

    nuevo_df = df.groupby('language').size().reset_index(name='quantity')

    return nuevo_df.sort_values(by=['quantity'], ascending=False)
