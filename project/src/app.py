from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls

from src.callbacks.pie_sentiment_callback import create_pie_sentiment_callbacks
from src.callbacks.upload_data_callback import create_upload_data_callbacks
from src.callbacks.bar_callbacks import create_bar_clicks
from src.callbacks.bar_callbacks import create_bubble_clicks
from src.callbacks.modal_callbacks import create_modal_callback
from src.callbacks.offcanvas_callbacks import create_offcanvas_callback

app = Dash(__name__, title='WhatTheyKnow', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Aquí o en GUIs
app.layout = dbc.Container([
    dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='https://cdn-icons-png.flaticon.com/512/607/607554.png ', height="30px"),
                                className='col-2'),
                        dbc.Col(dbc.NavbarBrand("WhatTheyKnow"), className="col-2"),
                    ],
                    className='text-left'
                ),
                html.Div(children=[
                    html.Div(id='output_profile', className='text-right'),
                    dbc.Button(html.Img(src='https://cdn-icons-png.flaticon.com/512/11569/11569256.png',
                                        style={'width': '30px', 'height': '30px'}),
                               id="open_modal_preg", n_clicks=0, color='black'),
                ], style={'display': 'flex'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Preguntas frecuentes")),
                        dbc.ModalBody(children=[
                            html.P('''Aquí puedes consultar las preguntas más frecuentes que realizan los usuarios y
                            que te pueden ayudar a resolver cualquier duda.'''),
                            dbc.Accordion(
                                [
                                    dbc.AccordionItem(
                                        children=[
                                            '''
                                                El uso de la aplicación es muy sencillo. Necesitas seguir los siguientes
                                                pasos para lograrlo:
                                            ''',
                                            html.Ol(
                                                children=[
                                                    html.Li(
                                                        children=[
                                                            '''
                                                        Descargar el fichero de datos que proporciona Twitter de forma
                                                        gratuita. Puedes consultar cómo visitando el siguiente 
                                                        ''',
                                                            html.A('enlace',
                                                                   href='https://help.twitter.com/es/managing-your-account/how-to-download-your-x-archive'),
                                                            '.'
                                                        ]
                                                    ),
                                                    html.Li(
                                                        'Subir los ficheros solicitados a través del botón de subida.'),
                                                    html.Li('Esperar a que acabe y ¡ya tienes tu información!')
                                                ]
                                            )
                                        ],
                                        title="¿Cómo funciona la aplicación?"
                                    ),
                                    dbc.AccordionItem(
                                        children=[
                                            "This is the content of the second section",
                                        ],
                                        title="¿Qué ficheros necesito?"
                                    ),
                                    dbc.AccordionItem(
                                        children=[
                                            '''
                                                En la versión actual de la aplicación no es posible almacenar los datos
                                                para posteriores consultas, pero en versiones futuras se plantea la
                                                posibilidad de realizar este almacenaje para ahorrar tiempo de 
                                                ejecución.
                                            ''',
                                        ],
                                        title="¿Puedo guardar mis datos para consultas posteriores?"
                                    ),
                                ],
                                start_collapsed=True,
                            ),
                        ], style={'text-align': 'justify'}),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Cerrar", id="close_modal_preg", className="ms-auto", n_clicks=0
                            )
                        ),
                    ],
                    id="modal_preg",
                    is_open=False,
                    size='lm'
                )
            ]
        ),
        color="dark",
        dark=True,
        className='pt-4 pb-4'
    ),
    html.Div([
        html.Div(
            dls.RingChase(children=[
                dcc.Upload([
                    html.Img(src="https://cdn-icons-png.flaticon.com/512/4007/4007710.png",
                             className='m-3',
                             style={'width': '50px', 'height': '50px'}),
                    'Arrastre o seleccione los ficheros'
                ], style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '2px',
                    'borderStyle': 'outset',
                    'borderRadius': '5px',
                    'align-items': 'center',
                    'text-align': 'center'
                }, multiple=True, id='upload-data', className='mt-3 mb-3 p-5 d-flex justify-content-center'),
            ], color='#435278', fullscreen=True, debounce=1000),
            className='d-flex justify-content-center'),
        dcc.Upload([
            html.Img(src="https://cdn-icons-png.flaticon.com/512/4007/4007710.png",
                     className='m-3',
                     style={'width': '50px', 'height': '50px'}),
            'Este es el que pinta y colorea'
        ], style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '2px',
            'borderStyle': 'outset',
            'borderRadius': '5px',
            'align-items': 'center',
            'text-align': 'center'
        }, multiple=True, id='color-data', className='mt-3 mb-3 p-5 d-flex justify-content-center'),
        html.H3('¿Qué puedes hacer?', style={'text-align': 'center'}),
        html.Br(),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Card(
                    [
                        dbc.CardImg(src="https://cdn-icons-png.flaticon.com/512/7169/7169641.png", top=True,
                                    className='mx-auto', style={'width': '50%', 'height': '50%'}),
                        dbc.CardBody(
                            [
                                html.H4("Perfil de usuario"),
                                html.P(
                                    "Consulta la infomación relevante de tu cuenta de Twitter, como tu foto de perfil "
                                    "y banner o el tamaño del contenido que has generado, entre otros.",
                                ),
                            ]
                        ),
                    ],
                    id='card-pu', className='p-2', style={'borderWidth': '3px', 'borderStyle': 'outset'})
            ]),
            dbc.Col(children=[
                dbc.Card(
                    [
                        dbc.CardImg(src="https://cdn-icons-png.flaticon.com/512/5660/5660389.png", top=True,
                                    className='mx-auto', style={'height': '50%', 'width': '50%'}),
                        dbc.CardBody(
                            [
                                html.H4("Usuarios más mencionados"),
                                html.P(
                                    "Consulta en un gráfico los 10 usuarios a los que más has mencionado en tus "
                                    "publicaciones y accede desde aquí a sus perfiles para poder consultarlos.",
                                ),
                            ]
                        ),
                    ],
                    id='card-um', className='p-2', style={'borderWidth': '3px', 'borderStyle': 'outset'})
            ]),
            dbc.Col(children=[
                dbc.Card(
                    [
                        dbc.CardImg(src="https://cdn-icons-png.flaticon.com/512/3898/3898082.png", top=True,
                                    className='mx-auto', style={'height': '50%', 'width': '50%'}),
                        dbc.CardBody(
                            [
                                html.H4("Lenguajes predilectos"),
                                html.P(
                                    "Consulta los porcentajes de los idiomas en los que has escrito tus "
                                    "publicaciones así como el porcentaje en el caso de los retweets que has realizado.",
                                ),
                            ]
                        ),
                    ],
                    id='card-lp', className='p-2', style={'borderWidth': '3px', 'borderStyle': 'outset'})
            ]),
            dbc.Col(children=[
                dbc.Card(
                    [
                        dbc.CardImg(src="https://cdn-icons-png.flaticon.com/512/2564/2564959.png ", top=True,
                                    className='mx-auto', style={'height': '50%', 'width': '50%'}),
                        dbc.CardBody(
                            [
                                html.H4("Análisis de sentimientos"),
                                html.P(
                                    "Obtén un gráfico con la polaridad de tus publicaciones (positivo, negativo, neutral) "
                                    "así como de las publicaciones que has retwitteado",
                                ),
                            ]
                        ),
                    ],
                    id='card-as', className='p-2', style={'borderWidth': '3px', 'borderStyle': 'outset'})
            ]),
            dbc.Col(children=[
                dbc.Card(
                    [
                        dbc.CardImg(src="https://cdn-icons-png.flaticon.com/512/2671/2671250.png ", top=True,
                                    className='mx-auto', style={'width': '50%', 'height': '50%'}),
                        dbc.CardBody(
                            [
                                html.H4("Círculo de Amigos"),
                                html.P(
                                    "Gráfico que te muestra en forma de círculo los usuarios de la aplicación "
                                    "con los que más has interactuado, otorgando una puntuación que puedes consultar.",
                                ),
                            ]
                        ),
                    ],
                    id='card-ca', className='p-2', style={'borderWidth': '3px', 'borderStyle': 'outset'})
            ]),
            dbc.Col(children=[
                dbc.Card(
                    [
                        dbc.CardImg(src="https://cdn-icons-png.flaticon.com/512/4066/4066004.png ", top=True,
                                    className='mx-auto', style={'height': '50%', 'width': '50%'}),
                        dbc.CardBody(
                            [
                                html.H4("Registro de la actividad"),
                                html.P(
                                    "Consulta en forma de mapa de calor tus horarios de actividad en la aplicación,"
                                    "pudiendo apreciar para cada día de la semana tus picos de interacción.",
                                ),
                            ]
                        ),
                    ],
                    id='card-ra', className='p-2', style={'borderWidth': '3px', 'borderStyle': 'outset'})
            ]),
            dbc.Col(children=[
                dbc.Card(
                    [
                        dbc.CardImg(src="https://cdn-icons-png.flaticon.com/512/854/854878.png ", top=True,
                                    className='mx-auto', style={'height': '50%', 'width': '50%'}),
                        dbc.CardBody(
                            [
                                html.H4("Tracking de usuario"),
                                html.P(
                                    "Consulta un registro visual en el que se pueden apreciar todas las localizaciones "
                                    "desde las que has realizado publicaciones y la frecuencia con la que lo has hecho.",
                                ),
                            ]
                        ),
                    ],
                    id='card-tu', className='p-2', style={'borderWidth': '3px', 'borderStyle': 'outset'})
            ]),
            dbc.Col(children=[
                dbc.Card(
                    [
                        dbc.CardImg(src="https://cdn-icons-png.flaticon.com/512/1055/1055669.png", top=True,
                                    className='mx-auto', style={'height': '50%', 'width': '50%'}),
                        dbc.CardBody(
                            [
                                html.H4("Gustos y anuncios"),
                                html.P(
                                    "Obtiene un perfil de usuario para ti en función de la actividad de gustos y "
                                    "anuncios que generas en la aplicación en base a tus interacciones.",
                                ),
                            ]
                        ),
                    ],
                    id='card-ga', className='p-2', style={'borderWidth': '3px', 'borderStyle': 'outset'})
            ]),
        ], className='row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4'),
    ], id='input-start'),
    html.Br(),
    dbc.Row(children=[dbc.Col(html.Div(id='output_languages', className='m3'), className='col-4'),
                      dbc.Col(html.Div(id='output_menciones', className='m3'), className='col-8')]),
    html.Div(id='output_sentiments', className='m3'),  # Margin 3 de Bootstrap
    dbc.Row(children=[dbc.Col(html.Div(id='output_heatmap', className='m3'), className='col-8'),
                      dbc.Col(html.Div(id='output_circle', className='m3'), className='col-4')]),
    html.Div(id='whitebox'),
    html.Div(id='whitebox-1'),
], fluid=True)

# Creación de los callbacks de la app
create_upload_data_callbacks(app)
create_pie_sentiment_callbacks(app)
# ... y todos los callbacks de las GUIs
create_bar_clicks(app)
create_bubble_clicks(app)
create_modal_callback(app)
create_offcanvas_callback(app)

if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port="2020")
