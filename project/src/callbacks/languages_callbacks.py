from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from utils.cloudfunctionsmanager import CloudFunctionManager
import pandas as pd
import json



def create_languages_callbacks(app):
    @app.callback(
        Output("tabla_idiomas_resumen", "children"),
        [Input("open_modal_lang", "n_clicks")],
        [State("modal_lang", "is_open")],
    )
    def toggle_modal(n1, is_open):
        cloud_instance = CloudFunctionManager.get_instance()
        idiomas_rt = pd.read_json(cloud_instance.get_results()['sentimientos_lenguajes']['language_rts'])
        idiomas_tweet = pd.read_json(cloud_instance.get_results()['sentimientos_lenguajes']['language_no_rts'])

        idiomas_rt = idiomas_rt.rename(columns={'quantity': 'Núm. Retweets'})
        idiomas_tweet = idiomas_tweet.rename(columns={'quantity': 'Núm. Tweets'})

        # Unir los dataframes usando un merge externo
        df_combined = pd.merge(idiomas_tweet, idiomas_rt, on='tweet.src_language', how='outer')

        # Llenar los valores NaN con 0
        df_combined = df_combined.fillna(0)


        df_combined = df_combined.rename(columns={'tweet.src_language': 'Idioma'})
        #df_combined = df_combined.sort_values(by='Núm. total Tweets', ascending=False)

        return dash_table.DataTable(
            id='datatable-paging',
            columns=[
                {"name": i, "id": i} for i in sorted(df_combined.columns)
            ],
            page_current=0,
            page_size=5,
            page_action='custom'
        )

    @app.callback(
        Output('datatable-paging', 'data'),
        Input('datatable-paging', "page_current"),
        Input('datatable-paging', "page_size"))
    def update_table(page_current, page_size):
        cloud_instance = CloudFunctionManager.get_instance()
        idiomas_rt = pd.read_json(cloud_instance.get_results()['sentimientos_lenguajes']['language_rts'])
        idiomas_tweet = pd.read_json(cloud_instance.get_results()['sentimientos_lenguajes']['language_no_rts'])

        idiomas_rt = idiomas_rt.rename(columns={'quantity': 'Núm. Retweets'})
        idiomas_tweet = idiomas_tweet.rename(columns={'quantity': 'Núm. Tweets'})

        # Unir los dataframes usando un merge externo
        df_combined = pd.merge(idiomas_tweet, idiomas_rt, on='tweet.src_language', how='outer')

        # Llenar los valores NaN con 0
        df_combined = df_combined.fillna(0)

        df_combined = df_combined.rename(columns={'tweet.src_language': 'Idioma'})
        # df_combined = df_combined.sort_values(by='Núm. total Tweets', ascending=False)
        return df_combined.iloc[
               page_current * page_size:(page_current + 1) * page_size
               ].to_dict('records')
