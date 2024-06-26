from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls

from callbacks.pie_sentiment_callback import create_pie_sentiment_callbacks
from callbacks.upload_data_callback import create_upload_data_callbacks
from callbacks.download_data_callback import create_download_callback
from callbacks.bar_callbacks import create_bar_clicks
from callbacks.bar_callbacks import create_bubble_clicks
from callbacks.bar_callbacks import create_pic_hover
from callbacks.modal_callbacks import create_modal_callback
from callbacks.offcanvas_callbacks import create_offcanvas_callback
from callbacks.heatmap_callback import create_heatmap_callback
from callbacks.combo_callbacks import create_combo_clicks
from callbacks.languages_callbacks import create_languages_callbacks

# Cambio
app = Dash(__name__, title='WhatTheyKnow', external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

# Aquí o en GUIs
app.layout = html.Div(children=[
    dbc.Navbar(
        dbc.Container(
            [
                html.Div(
                    children=[
                        html.Img(src='assets/Diseño_sin_título__8_-removebg-preview.png', height="60px"),
                        html.Span("WhatTheyKnow", className='h4 mb-0 ms-2'),
                    ]
                    , className='d-flex align-items-center'),
                html.Div(children=[
                    html.Div(id='output_download', className='text-right'),
                    dbc.Button(html.I(className='bi bi-question-circle'),
                               id="open_modal_preg", n_clicks=0, color='black'),
                    dbc.Tooltip('Preguntas frecuentes de los usuarios', target='open_modal_preg', placement='top'),
                    html.Div(id='output_profile', className='text-right')
                ], className='d-flex align-items-center'),
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            children=[
                                html.Img(src='https://cdn-icons-png.flaticon.com/512/5726/5726558.png',
                                         style={'height': '30px', 'width': '30px'},
                                         className='m-1'),
                                html.Div("Preguntas frecuentes", className='m-1 h5'),
                            ], style={'background-color': '#6FADFF'}),
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
                                            "En la página de inicio se encuentran descritas las distintas "
                                            "funcionalidades que es posible realizar con esta herramienta. En caso de "
                                            "subir ficheros para comenzar el procesamiento, los colores de los bordes "
                                            "de las tarjetas cambiarán en función de la posibilidad de"
                                            "ejecución de la funcionalidad correspondiente. El código de colores es "
                                            "el siguiente:",
                                            html.Ul(
                                                children=[
                                                    html.Li([html.Strong('Verde'), ''': se han subido todos los 
                                                    ficheros correspondientes y la funcionalidad se puede ejecutar al 
                                                    completo.''']),
                                                    html.Li([html.Strong('Amarillo'), ''': se han subido algunos de 
                                                    los ficheros correspondientes y aunque la funcionalidad se puede 
                                                    ejecutar, los resultados estarán incompletos.''']),
                                                    html.Li([html.Strong('Rojo'), ''': no se dispone de los ficheros 
                                                    necesarios para comenzar el procesamiento por lo que la 
                                                    funcionalidad no se puede ejecutar.''']),
                                                ]
                                            )
                                        ],
                                        title="¿Qué representa cada uno de los colores de las funcionalidades?"
                                    ),
                                    dbc.AccordionItem(
                                        children=[
                                            html.P('''Sí, una vez hayas realizado un procesamiento de datos empleando la 
                                            herramienta, se ofrece la posibilidad de obtener una copia de los datos 
                                            extraídos para poder emplearlos en consultas posteriores sin tener que 
                                            esperar a que vuelvan a generarse.'''),
                                            html.Br(),
                                            html.P('''Para ello, sitúate en la parte superior, donde aparece un botón de 
                                            descarga de ficheros. Dentro de él se abre un menú en el que se ofrecen 
                                            dos alternativas para la obtención de los datos: descargarlos de forma 
                                            inmediata pulsando el enlace o bien recibirlos en el correo electrónico 
                                            indicando la dirección de destino en el formulario de la parte inferior.''')
                                        ],
                                        title="¿Puedo guardar mis datos para consultas posteriores?"
                                    ),
                                    dbc.AccordionItem(
                                        children=[
                                            '''De forma general, para comenzar el procesamiento es necesaria la subida
                                            del fichero account.js. En particular, para cada una de las funcionalidades
                                            se detallan a continuación los ficheros necesarios:''',
                                            html.Ul(
                                                children=[
                                                    html.Li([html.Strong('Perfil de usuario'), ''': se necesitan de 
                                                    forma obligatoria los ficheros profile.js, ageinfo.js y 
                                                    manifest.js.''']),
                                                    html.Li([html.Strong('Usuarios más mencionados'), ''': se 
                                                    necesita de forma obligatoria el fichero tweets.js.''']),
                                                    html.Li([html.Strong('Idiomas más utilizados'), ''': se 
                                                    necesita de forma obligatoria el fichero tweets.js.''']),
                                                    html.Li([html.Strong('Análisis de sentimientos'), ''': se 
                                                    necesita de forma obligatoria el fichero tweets.js.''']),
                                                    html.Li([html.Strong('Círculo de amigos'), ''': se necesitan de 
                                                    forma obligatoria los ficheros profile.js, 
                                                    direct-message-headers.js, tweets.js, follower.js y following.js''']),
                                                    html.Li([html.Strong('Registro de tu actividad'), ''': se 
                                                    necesitan de forma obligatoria los ficheros tweets.js y 
                                                    menifest.js y, de forma adicional, los ficheros 
                                                    user-link-clicks.js, direct-message-headers.js, 
                                                    direct-message-group-headers.js y ad-impressions.js''']),
                                                    html.Li([html.Strong('Criterios objetivo'), ''': se 
                                                    necesita de forma obligatoria el fichero ad-engagements.js.''']),
                                                    html.Li([html.Strong('Anunciantes más populares'), ''': se 
                                                    necesita de forma obligatoria el fichero ad-engagements.js.''']),
                                                ]
                                            )
                                        ],
                                        title="¿Qué ficheros necesito para cada una de las funcionalidades?"
                                    ),
                                ],
                                start_collapsed=True,
                            ),
                        ], style={'text-align': 'justify'}),
                    ],
                    id="modal_preg",
                    is_open=False,
                    size='lg',
                    className='modal-dialog-centered'
                )
            ]
        ), className='p-2'),
    html.Div([
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P([html.I(className='bi bi-1-circle me-3'),
                            html.Span('Descarga tu archivo de Twitter visitando el siguiente '), html.A(f"enlace",
                                                                                                        href=f"https://help.twitter.com/es/managing-your-account/how-to-download-your-x-archive",
                                                                                                        target="_blank")],
                           className='h5 mb-3'),
                    html.P([html.I(className='bi bi-2-circle me-3'), html.Span(
                        'Arrastra los ficheros que quieras que analicemos. Verás en verdes las funcionalidades que podemos realizar con ellos')],
                           style={"text-align": "center"}, className='h5 mb-3'),
                    html.P(
                        [html.I(className='bi bi-3-circle me-3'), html.Span('Presiona Enviar y espera tus resultados')],
                        className='h5 mb-2'),
                    html.P(
                        'Puedes adjuntar tu fichero de WhatTheyKnow si ya hemos analizado tus datos alguna vez y lo has descargado',
                        className='opacity-25 px-5', style={'text-align': 'center'}),
                ], className='d-flex flex-column align-items-center justify-content-center'),
                dbc.Col([
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
                    html.Div(id='alerta-archivos'),
                    html.Div(children=[dls.RingChase(children=[
                        dbc.Button('Enviar', id='submit', style={'display': 'block', 'margin': '0 auto'},
                                   disabled=True),
                    ], color='#435278', fullscreen=True, debounce=1000)], id='enviar_div')

                ], className='d-flex flex-column align-items-center justify-content-center')
            ]),
            html.Br(),
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
                                    html.H4("Idiomas más utilizados"),
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
                                    html.H4("Registro de tu actividad"),
                                    html.P(
                                        "Consulta en forma de mapa de calor tus horarios de actividad en la aplicación, "
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
                            dbc.CardImg(src="https://cdn-icons-png.flaticon.com/512/1055/1055669.png", top=True,
                                        className='mx-auto', style={'height': '50%', 'width': '50%'}),
                            dbc.CardBody(
                                [
                                    html.H4("Criterios objetivo"),
                                    html.P(
                                        "Consulta de forma gráfica para cada uno de los tipos posibles de criterios"
                                        "los valores por los que han aparecido en los anuncios que has consultado.",
                                    ),
                                ]
                            ),
                        ],
                        id='card-tu', className='p-2', style={'borderWidth': '3px', 'borderStyle': 'outset'})
                ]),
                dbc.Col(children=[
                    dbc.Card(
                        [
                            dbc.CardImg(src="https://cdn-icons-png.flaticon.com/512/2415/2415903.png", top=True,
                                        className='mx-auto', style={'height': '50%', 'width': '50%'}),
                            dbc.CardBody(
                                [
                                    html.H4("Anunciantes más populares"),
                                    html.P(
                                        "Consulta los 5 anunciantes que más anuncios has consultado. Para "
                                        "cada uno de ellos se muestra el anuncio más reciente y los criterios "
                                        "por los que aparece.",
                                    ),
                                ]
                            ),
                        ],
                        id='card-ga', className='p-2', style={'borderWidth': '3px', 'borderStyle': 'outset'})
                ]),
            ], className='row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4'),
        ], id='input-start'),
        dbc.Row(children=[dbc.Col(html.Div(id='output_languages'), className='col-4'),
                          dbc.Col(html.Div(id='output_menciones'), className='col-8')],
                className="d-flex justify-content-evenly"),
        html.Div(id='output_sentiments', className='mt-3'),  # Margin 3 de Bootstrap
        dbc.Row(children=[dbc.Col(html.Div(id='output_heatmap', className='mt-3'), className='col-8'),
                          dbc.Col(html.Div(id='output_circle', className='mt-3'), className='col-4')]),
        dbc.Row(children=[dbc.Col(html.Div(id='output_aden1', className='mt-3'), className='col-4'),
                          dbc.Col(html.Div(id='output_aden2', className='mt-3'), className='col-8')]),
        dcc.Location(id='url', refresh=False),
        html.Div(id='whitebox'),
        html.Div(id='whitebox-1'),
        html.Div(id='whitebox-2'),
        html.Div(id='whitebox-3'),
    ], className="m-3 mt-5")
])

# Creación de los callbacks de la app
create_upload_data_callbacks(app)
create_pie_sentiment_callbacks(app)
create_download_callback(app)
# ... y todos los callbacks de las GUIs
create_bar_clicks(app)
create_bubble_clicks(app)
create_modal_callback(app)
create_offcanvas_callback(app)
create_heatmap_callback(app)
create_combo_clicks(app)
create_pic_hover(app)
create_languages_callbacks(app)


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0")
