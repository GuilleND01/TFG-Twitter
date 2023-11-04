import pandas as pd
import json
from pandas import json_normalize
from src.utils.common_functions import clean_text
from textblob import TextBlob


def analisis_sentimientos(file_content):
    js_code = file_content.replace('window.YTD.tweets.part0 = ', '')

    # Read the json and obtain a df
    json_dat = json.loads(js_code)
    data = json_normalize(json_dat)

    # Clean the full_text field and create a new dataframe only with it
    df = pd.DataFrame(data['tweet.full_text'].apply(clean_text))
    df['tweet.polarity'] = df['tweet.full_text'].apply(get_polarity)


def get_polarity(text):
    return TextBlob(text).sentiment.polarity
