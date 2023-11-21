import pandas as pd
import json
from pandas import json_normalize
import swifter


def return_user_mentions_df(file_content):
    js_code = file_content.replace('window.YTD.tweets.part0 = ', '')

    # Read the json and obtain a df
    json_dat = json.loads(js_code)
    data = json_normalize(json_dat)

    data = data[~data["tweet.full_text"].str.contains("RT")]
    df = pd.DataFrame(data['tweet.entities.user_mentions'])
    df = df[df['tweet.entities.user_mentions'].swifter.apply(lambda x: len(x) > 0)]

    df = df.explode('tweet.entities.user_mentions')
    df['usernames'] = df.swifter.apply(lambda row: '@' + dict(row['tweet.entities.user_mentions'])['screen_name'],
                                       axis=1)
    nuevo_df = df.swifter.groupby('usernames').apply(lambda x: x['usernames'].count()).reset_index(name='quantity')
    nuevo_df = nuevo_df.sort_values(by=['quantity'], ascending=False)

    return nuevo_df[:10]
