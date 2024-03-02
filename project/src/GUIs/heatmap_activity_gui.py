import dash
from dash import dcc, html
import plotly.express as px
import json

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def return_heatmap_activiy_gui(heatmap_json):

    json_opciones = list(heatmap_json["opciones_checklist"].keys())
    json_data = json.loads(heatmap_json['data'])

    data = []

    for dia in range(len(dias)):
        lista = []
        for franja in range(0, 24):
            clave = f"('{str(franja).zfill(2)}', '{dias[dia]}')"  # Construir la clave
            suma = 0

            """En función de las columnas que se tengan seleccionadas en la checklist, se calcula la suma"""
            for col in json_opciones:
                checklist_opt = heatmap_json["opciones_checklist"][col]
                suma += json_data.get(clave)[checklist_opt] if json_data.get(clave) else 0

            lista.append(suma)
        data.append(lista)

    fig = px.imshow(data, y=dias, x=[f"{str(i).zfill(2)}" for i in range(24)], labels=dict(x="Hora", y="Día", color="Actividad"))

    return html.Div([
        dcc.Graph(id="graph-heatmap", figure=fig),
        html.P("Interacciones incluidas:"),
        dcc.Checklist(
            id='opciones',
            options=json_opciones,  # Depende de los archivos que tenga el usuario, por ejemplo, si no tiene archivo
            # de mensaje directos en grupos, el cálculo en el servidor no se habrá hecho con ese archivo, entonces
            # tampoco será una opción de la checklist. Para 990664474792165377 he quitado el de mensajes de grupos para
            # hacer la prueba
            value=json_opciones,  # Por defecto todas marcadas
            inline=True,
            labelClassName='me-3'
        ),
    ])
