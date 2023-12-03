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
        df = pd.DataFrame(self.data[['tweet.full_text', 'tweet.id', 'tweet.edit_info.initial.editTweetIds']])
        #df['url_tweet'] = df.apply(lambda x: obtener_url(x['tweet.id'], x['tweet.edit_info.initial.editTweetIds']))
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

        #df_sin_rts['url'] = df_sin_rts.apply(lambda x: x[''])
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

        self.language_rts = language_rts
        self.language_without_rts = language_without_rts
        self.polarity_rts = polarity_rts
        self.polarity_without_rts = polarity_without_rts

    def get_dataframe_wres(self):
        return self.language_rts, self.language_without_rts, self.polarity_rts, self.polarity_without_rts, \
            self.tweets_rts, self.tweets_no_rts

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

