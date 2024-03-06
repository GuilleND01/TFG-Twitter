from dash.dependencies import Input, Output
from src.utils.cloudfunctionsmanager import CloudFunctionManager
import json
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def create_heatmap_callback(app):

    @app.callback(
        Output("graph-heatmap", "figure"),
        Input("opciones", "value"))
    def filter_heatmap(cols):

        # Recupero los datos
        cloud_instance = CloudFunctionManager.get_instance()
        heatmap_json = cloud_instance.get_results()['heatmap_activity']

        #json_opciones = list(heatmap_json["opciones_checklist"].keys())
        json_data = json.loads(heatmap_json['data'])

        data = []

        for dia in range(len(dias)):
            lista = []
            for franja in range(0, 24):
                clave = f"('{str(franja).zfill(2)}', '{dias[dia]}')"  # Construir la clave
                suma = 0

                #En función de las columnas que se tengan seleccionadas en la checklist, se calcula la suma
                for col in cols:
                    checklist_opt = heatmap_json["opciones_checklist"][col]
                    suma += json_data.get(clave)[checklist_opt] if json_data.get(clave) else 0

                lista.append(suma)
            data.append(lista)

        fig = px.imshow(data, y=dias, x=[f"{str(i).zfill(2)}" for i in range(24)],
                        labels=dict(x="Hora", y="Día", color="Actividad"),
        

        )
        return fig
