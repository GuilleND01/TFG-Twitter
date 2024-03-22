from dash.dependencies import Input, Output
from utils.cloudfunctionsmanager import CloudFunctionManager
import json
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def create_heatmap_callback(app):

    @app.callback(
        [Output("graph-heatmap", "figure"),
         Output("switch_frecuencia", "className"),
         Output("texto-periodo", 'children')],
        [Input("opciones", "value"),
        Input("switch_frecuencia", "value")],
    )
    def filter_heatmap(cols, value_switch):

        # Recupero los datos
        cloud_instance = CloudFunctionManager.get_instance()
        heatmap_json = cloud_instance.get_results()['heatmap_activity']

        # Recoger el switch y su valor, trabajar en función del él
        if value_switch == True:
            json_data = json.loads(heatmap_json["data_90"])
            class_switch = 'opacity-100'
            texto_periodo = str(heatmap_json['fecha_90_dias_atras'])[:-12] + " - " + str(heatmap_json['fecha_generacion_archivo'])[:-12]
        else:
            json_data = json.loads(heatmap_json["data_total"])
            class_switch = 'opacity-50'
            texto_periodo = ""

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
                        color_continuous_scale='blues'
        )
        return fig, class_switch, texto_periodo

