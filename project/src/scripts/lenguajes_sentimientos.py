import pandas as pd
import json
import os
from pandas import json_normalize
from src.utils.common_functions import clean_text
from google.cloud import translate_v2 as translate
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.utils.language_codes import language_codes

script_dir = os.path.dirname(__file__)
json_path = os.path.join(script_dir, 'api_keys.json')
translate_client = translate.Client.from_service_account_json(json_path)
analyzer = SentimentIntensityAnalyzer()

tweets_rts = pd.DataFrame
tweets_no_rts = pd.DataFrame


def lenguajes_and_sentimientos(file_content):
    js_code = file_content.replace('window.YTD.tweets.part0 = ', '')

    # Read the json and obtain a df
    json_dat = json.loads(js_code)
    data = json_normalize(json_dat)

    df = pd.DataFrame(data['tweet.full_text'])
    df = df.head(100)

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
    df_contiene_rts[['tweet.src_language', 'tweet.polarity', 'tweet.compound']] \
        = df_contiene_rts['tweet.full_text'].apply(lambda x: pd.Series(get_lang_and_polarity(x)))

    df_sin_rts[['tweet.src_language', 'tweet.polarity', 'tweet.compound']] \
        = df_sin_rts['tweet.full_text'].apply(lambda x: pd.Series(get_lang_and_polarity(x)))

    polarity_without_rts = df_sin_rts.groupby('tweet.polarity').size().reset_index(name='quantity')
    polarity_rts = df_contiene_rts.groupby('tweet.polarity').size().reset_index(name='quantity')

    language_without_rts = df_sin_rts.groupby('tweet.src_language').size().reset_index(name='quantity')
    language_rts = df_contiene_rts.groupby('tweet.src_language').size().reset_index(name='quantity')

    polarity_rts = polarity_rts.sort_values(by=['quantity'], ascending=False)
    polarity_without_rts = polarity_without_rts.sort_values(by=['quantity'], ascending=False)
    language_rts = language_rts.sort_values(by=['quantity'], ascending=False)
    language_without_rts = language_without_rts.sort_values(by=['quantity'], ascending=False)

    # TODO refactorizar este código para que sea DRY
    most_positive_rts = (df_contiene_rts[df_contiene_rts['tweet.polarity'] == "Sentimiento Positivo"]
                         .sort_values(by=['tweet.compound'], ascending=False).head(3))
    most_negative_rts = (df_contiene_rts[df_contiene_rts['tweet.polarity'] == "Sentimiento Negativo"]
                         .sort_values(by=['tweet.compound'], ascending=False).tail(3))
    df_contiene_rts['diff_with_0'] = abs(df_contiene_rts['tweet.compound'] - 0)
    most_neutral_rts = (df_contiene_rts[df_contiene_rts['tweet.polarity'] == "Sentimiento Neutral"]
                        .sort_values(by=['diff_with_0']).head(3))

    most_positive_sin_rts = (df_sin_rts[df_sin_rts['tweet.polarity'] == "Sentimiento Positivo"]
                             .sort_values(by=['tweet.compound'], ascending=False).head(3))
    most_negative_sin_rts = (df_sin_rts[df_sin_rts['tweet.polarity'] == "Sentimiento Negativo"]
                             .sort_values(by=['tweet.compound'], ascending=False).tail(3))
    df_sin_rts['diff_with_0'] = abs(df_contiene_rts['tweet.compound'] - 0)
    most_neutral_sin_rts = (df_sin_rts[df_sin_rts['tweet.polarity'] == "Sentimiento Neutral"]
                            .sort_values(by=['diff_with_0']).head(3))

    global tweets_rts
    tweets_rts = pd.concat([most_positive_rts, most_negative_rts, most_neutral_rts])
    global tweets_no_rts
    tweets_no_rts = pd.concat([most_positive_sin_rts, most_negative_sin_rts, most_neutral_sin_rts])

    return language_rts, language_without_rts, polarity_rts, polarity_without_rts


def get_lang_and_polarity(text):
    # A unique call to the API
    # result = translate_client.translate(text, target_language='en')
    # src_languaje = result['detectedSourceLanguage']
    # compound = analyzer.polarity_scores(result['translatedText'])['compound']

    compound = analyzer.polarity_scores(text)['compound']
    src_languaje = 'es'

    if compound >= 0.05:
        polarity = "Sentimiento Positivo"
    elif -0.05 < compound < 0.05:
        polarity = "Sentimiento Neutral"
    else:
        polarity = "Sentimiento Negativo"

    return src_languaje, polarity, compound


def return_tweets(labels, rts):
    if rts == "no_rts":
        filas_filtradas = tweets_no_rts[tweets_no_rts['tweet.polarity'] == str(labels)]
        return filas_filtradas['tweet.full_text']
    else:
        filas_filtradas = tweets_rts[tweets_rts['tweet.polarity'] == str(labels)]
        return filas_filtradas['tweet.full_text']
