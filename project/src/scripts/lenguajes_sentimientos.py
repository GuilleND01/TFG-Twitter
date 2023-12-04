from abc import ABC

import pandas as pd
import json
import os
from pandas import json_normalize
from src.utils.common_functions import clean_text
from google.cloud import translate_v2 as translate
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.utils.DataframeProcessing import DataFrameProcessing
from src.utils.language_codes import language_codes


class LanguagesSentiments(DataFrameProcessing):

    def __init__(self, file_content):
        script_dir = os.path.dirname(__file__)
        json_path = os.path.join(script_dir, 'api_keys.json')
        self.translate_client = translate.Client.from_service_account_json(json_path)
        self.analyzer = SentimentIntensityAnalyzer()

        self.tweets_rts = pd.DataFrame
        self.tweets_no_rts = pd.DataFrame
        self.language_rts = pd.DataFrame
        self.language_without_rts = pd.DataFrame
        self.polarity_rts = pd.DataFrame
        self.polarity_without_rts = pd.DataFrame

        self.data = self.filecontent_to_df(file_content)
        self.build_dataframe_wres()

    def build_dataframe_wres(self):
        df = self.data.head(100)

        # Split the dataframe (tweets with rts and without)
        df_contiene_rts = df[df["tweet.full_text"].str.match(r'^RT @\w+:')]
        df_sin_rts = df[~df["tweet.full_text"].str.contains("RT")]


        # Drop the columns that we are not going to use and normalize de user mentions column to get the user ID of the retweet

        '''Ocurre que en la columna user_mentios puede haber más de una mención, pero a la persona a la que has dado rt siempre aparece
        en la primera pos del array de menciones, por eso este apply'''
        df_contiene_rts['user_id_RT'] = df_contiene_rts["tweet.entities.user_mentions"].apply(lambda x: x[0]['id'] if x else None)
        df_contiene_rts = pd.DataFrame(df_contiene_rts[['tweet.full_text', 'tweet.id', 'user_id_RT']])
        df_sin_rts = pd.DataFrame(df_sin_rts[['tweet.full_text', 'tweet.id']])


        # Clean both dataframes
        df_sin_rts["tweet.full_text"] = df_sin_rts["tweet.full_text"].apply(clean_text)
        df_contiene_rts["tweet.full_text"] = df_contiene_rts["tweet.full_text"].apply(clean_text)

        # Delete tweets with id = -1 because in the http request the tweet is not going to exist
        df_contiene_rts = df_contiene_rts[df_contiene_rts["user_id_RT"] != "-1"]

        # Then, drop empty tweets
        df_sin_rts = df_sin_rts[df_sin_rts["tweet.full_text"] != '']
        df_contiene_rts = df_contiene_rts[df_contiene_rts["tweet.full_text"] != '']


        # Get polarity with Vader
        df_contiene_rts[['tweet.src_language', 'tweet.polarity', 'tweet.compound']] \
            = df_contiene_rts['tweet.full_text'].apply(lambda x: pd.Series(self.get_lang_and_polarity(x)))

        df_sin_rts[['tweet.src_language', 'tweet.polarity', 'tweet.compound']] \
            = df_sin_rts['tweet.full_text'].apply(lambda x: pd.Series(self.get_lang_and_polarity(x)))

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

        self.tweets_rts = pd.concat([most_positive_rts, most_negative_rts, most_neutral_rts])
        self.tweets_no_rts = pd.concat([most_positive_sin_rts, most_negative_sin_rts, most_neutral_sin_rts])
        self.tweets_no_rts['url_tweet'] = self.tweets_no_rts.apply(lambda x: self.obtener_url_no_rts(x['tweet.id']), axis=1)
        self.tweets_rts['url_tweet'] = self.tweets_rts.apply(lambda x: self.obtener_url_rts(x['tweet.id'], x['user_id_RT']), axis=1)

        self.language_rts = language_rts
        self.language_without_rts = language_without_rts
        self.polarity_rts = polarity_rts
        self.polarity_without_rts = polarity_without_rts

    def get_dataframe_wres(self):
        return self.language_rts, self.language_without_rts, self.polarity_rts, self.polarity_without_rts, \
            self.tweets_rts, self.tweets_no_rts

    def obtener_url_no_rts(self, tweet_id):
        return f"https://publish.twitter.com/oembed?url=https://twitter.com/joorgemaa/status/{tweet_id}"

    def obtener_url_rts(self, tweet_id, user_id):
        return f"https://publish.twitter.com/oembed?url=https://twitter.com/{user_id}/status/{tweet_id}"

    def get_lang_and_polarity(self, text):
        # A unique call to the API

        '''
        result = self.translate_client.translate(text, target_language='en')
        src_languaje = result['detectedSourceLanguage']
        compound = self.analyzer.polarity_scores(result['translatedText'])['compound']
        '''

        compound = self.analyzer.polarity_scores(text)['compound']

        if compound >= 0.05:
            polarity = "Sentimiento Positivo"
        elif -0.05 < compound < 0.05:
            polarity = "Sentimiento Neutral"
        else:
            polarity = "Sentimiento Negativo"

        return 'es', polarity, compound

