import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
import json

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def return_heatmap_activiy_gui(heatmap_json):

    json_opciones = list(heatmap_json["opciones_checklist"].keys())
    json_data = json.loads(heatmap_json['data_total'])

    dict_contador_total = heatmap_json["contadores_totales"]

    lista_opciones_con_numeros = []
    for key in heatmap_json["opciones_checklist"].keys():
        lista_opciones_con_numeros.append(f"{key} ({dict_contador_total[heatmap_json['opciones_checklist'][key]]})")

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
                    options=lista_opciones_con_numeros,
                    # Depende de los archivos que tenga el usuario, por ejemplo, si no tiene archivo
                    # de mensaje directos en grupos, el cálculo en el servidor no se habrá hecho con ese archivo, entonces
                    # tampoco será una opción de la checklist. Para 990664474792165377 he quitado el de mensajes de grupos para
                    # hacer la prueba
                    value=lista_opciones_con_numeros,  # Por defecto todas marcadas
                    inline=True,
                    labelClassName='me-3'
                )
            ], className='d-flex align-items-center ms-3 mt-3', id='div_opciones'),
            dbc.Modal(
                [
                    dbc.ModalHeader(
                        children=[
                            html.Img(src='https://cdn-icons-png.flaticon.com/512/4066/4066004.png',
                                     style={'height': '30px', 'width': '30px'},
                                     className='m-1'),
                            html.Div("Registro de tu actividad", className='m-1 h5'),
                        ], style={'background-color': '#6FADFF'}),
                    dbc.ModalBody(children=[

                        html.P('''Lleva un control del uso de la red social y de cada una de tus interacciones. Observa 
                        cuáles son tus patrones de actividad a lo largo de la semana y los cambios en tus hábitos a lo largo
                        del tiempo. '''),
                        html.P('''En el panel inferior puedes seleccionar el tipo de interacción que quieres incluir en el mapa de calor. 
                         Además, podrás limitir el análisis a los últimos 90 días.''')

                    ], style={'text-align': 'justify'}),
                ],
                id="modal_heatmap",
                is_open=False,
                className='modal-dialog-centered'
            ),
        ]
        , className='p-3 bg-light'
    )


