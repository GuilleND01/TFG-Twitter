import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
import json

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def return_heatmap_activiy_gui(heatmap_json):

    json_opciones = list(heatmap_json["opciones_checklist"].keys())
    json_data = json.loads(heatmap_json['data_total'])

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

    fig = px.imshow(data, y=dias, x=[f"{str(i).zfill(2)}" for i in range(24)], labels=dict(x="Hora", y="Día", color="Actividad"),
                    color_continuous_scale='blues')

    return html.Div(
        children=[
            html.Div(children=[
                    html.P(children=[html.Span('Registro de tu actividad', className='ms-3 h5 m-0')], className='d-inline-flex m-0'),
                    html.Span(id='texto-periodo', className='ms-2 opacity-75'),
                    html.P(children=[
                        dbc.Switch(id='switch_frecuencia', value=False, label='Ver solo últimos 90 días',
                        ),
                        html.Button(html.I(className="bi bi-info-circle"), id="open_modal_heatmap", className='btn'),
                    ], className='d-flex align-items-center m-0')],
            className='d-flex justify-content-between align-items-center m-0'),
            html.Div("Descubre las horas en las que estás más activo y encuentra patrones de comportamiento. ", className='ms-3 mb-3 opacity-25'),
            html.Div(children=[dcc.Graph(id="graph-heatmap", figure=fig)]),
            html.Div(children=[
                dcc.Checklist(
                    id='opciones',
                    options=json_opciones,
                    # Depende de los archivos que tenga el usuario, por ejemplo, si no tiene archivo
                    # de mensaje directos en grupos, el cálculo en el servidor no se habrá hecho con ese archivo, entonces
                    # tampoco será una opción de la checklist. Para 990664474792165377 he quitado el de mensajes de grupos para
                    # hacer la prueba
                    value=json_opciones,  # Por defecto todas marcadas
                    inline=True,
                    labelClassName='me-3'
                )
            ], className='d-flex align-items-center ms-3 mt-3'),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Registro de tu actividad")),
                    dbc.ModalBody(children=[
                        html.P('''ToDo'''),
                    ]),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Cerrar", id="close_modal_heatmap", className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                id="modal_heatmap",
                is_open=False,
            )
        ]
        , className='p-3 bg-light'
    )


