import dash_bootstrap_components as dbc
from dash import html, dcc


def return_download_gui():
    return html.Div(children=[
        dbc.Button(html.I(className='bi bi-file-earmark-arrow-down'),
                   id="open_modal_down", n_clicks=0, color='black'),
        dbc.Tooltip('Descarga un fichero para posteriores consultas', target='download', placement='top'),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    children=[
                        html.Img(src='https://cdn-icons-png.flaticon.com/512/892/892303.png',
                                 style={'height': '30px', 'width': '30px'},
                                 className='m-1'),
                        dbc.ModalTitle("Recibe tus datos en el email", className='m-1'),
                    ], style={'background-color': '#6FADFF'}),
                dbc.ModalBody(children=[
                    html.P('''Gracias a este formulario puedes introducir el correo al que desees que tus datos sean
                    enviados. Una vez descargados puedes resubirlos a la aplicación en posteriores ejecuciones para 
                    poder reducir los tiempos de espera.'''),
                    html.Br(),
                    html.Div(
                        children=[
                            dbc.Label("Introduzca su correo electrónico: "),
                            dbc.Input(id='input_email', placeholder="Correo electrónico", type="email"),
                        ]
                    ),
                    html.Br(),
                    dbc.Button("Enviar datos", id='submit_button', color="primary", className="mr-2"),
                ], style={'text-align': 'justify'}),
            ],
            id="modal_down",
            is_open=False,
            className='modal-dialog-centered'
        )
    ])
