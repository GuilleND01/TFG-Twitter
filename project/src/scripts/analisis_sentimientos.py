import pandas as pd
import json
from pandas import json_normalize
from src.utils.common_functions import clean_text
from google.cloud import translate_v2 as translate
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

translate_client = translate.Client.from_service_account_json('../tfgtwitter-735690f3c7f2.json')
analyzer = SentimentIntensityAnalyzer()


def analisis_sentimientos(file_content):
    js_code = file_content.replace('window.YTD.tweets.part0 = ', '')

    # Read the json and obtain a df
    json_dat = json.loads(js_code)
    data = json_normalize(json_dat)

    df = pd.DataFrame(data['tweet.full_text'])
    df = df.head(5)

    # Split the dataframe (tweets with rts and without)
    df_contiene_rts = df[df["tweet.full_text"].str.contains("RT")]
    df_sin_rts = df[~df["tweet.full_text"].str.contains("RT")]

    # Clean both dataframes
    df_sin_rts["tweet.full_text"] = df_sin_rts["tweet.full_text"].apply(clean_text)
    df_contiene_rts["tweet.full_text"] = df_contiene_rts["tweet.full_text"].apply(clean_text)

    # Then, drop empty tweets
    df_sin_rts = df_sin_rts[df_sin_rts["tweet.full_text"] != '']
    df_contiene_rts = df_contiene_rts[df_contiene_rts["tweet.full_text"] != '']

    # Get polarity with Vader
    df_contiene_rts['tweet.polarity'] = df_contiene_rts['tweet.full_text'].apply(get_polarity)
    df_sin_rts['tweet.polarity'] = df_sin_rts['tweet.full_text'].apply(get_polarity)

    df_sin_rts = df_sin_rts.groupby('tweet.polarity').size().reset_index(name='quantity')
    df_contiene_rts = df_contiene_rts.groupby('tweet.polarity').size().reset_index(name='quantity')

    return df_contiene_rts.sort_values(by=['quantity'], ascending=False), df_sin_rts.sort_values(by=['quantity'],
                                                                                                 ascending=False)


def get_polarity(text):
    result = translate_client.translate(text, target_language='en')
    compound_english = analyzer.polarity_scores(result['translatedText'])['compound']

    if compound_english >= 0.05:
        return "Sentimiento Positivo"
    elif -0.05 < compound_english < 0.05:
        return "Sentimiento Neutral"
    else:
        return "Sentimiento Negativo"
