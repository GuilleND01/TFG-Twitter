from dash.dependencies import Input, Output
from dash import dcc
from pandas import json_normalize
import plotly.express as px
from src.utils.cloudfunctionsmanager import CloudFunctionManager


def create_combo_clicks(app):
    @app.callback(
        Output('graph-criteria', 'children'),
        [Input('pombo-box', 'value')]
    )
    def actualizar_resultado_combo(valor_seleccionado):
        cloud_inst_res = CloudFunctionManager.get_instance().get_results()
        df_json = cloud_inst_res['person-criteria']
        if valor_seleccionado is not None:
            print(cloud_inst_res)
            df = json_normalize(eval(df_json[valor_seleccionado]))
            fig = px.bar(df, x="TargetingValue", y="Count",
                         labels={'TargetingValue': 'Criterio', 'Count': 'Anuncios en los que figura'})
            fig.update_traces(
                hovertemplate=
                "El criterio <b>%{x}</b> se ha <br/> empleado en <b>%{y}</b> anuncios"
            )
            return dcc.Graph(
                figure=fig
            )

        return None
