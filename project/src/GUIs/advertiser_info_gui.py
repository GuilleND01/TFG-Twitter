import dash_bootstrap_components as dbc
from dash import html, dcc


def return_gui_advertisers(adv_json):
    return html.Div(children=[
        html.Div(children=[
            html.P(children=[html.Span('Anunciantes más interesados', className='ms-3 h5')],
                   className='d-inline-flex m-0'),
            html.P(children=[
                html.Button(html.I(className="bi bi-info-circle"), id="open_modal_adv", className='btn'),
            ], className='d-flex align-items-center m-0')],
            className='d-flex justify-content-between align-items-center m-0'),
        html.Div("Consulta los anunciantes que están más interesados en tu perfil. ",
                 className='ms-3 mb-3 opacity-25'),
        dcc.Tabs(
            children=[
                dcc.Tab(
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        html.Iframe(srcDoc=res['recent'], style={'margin': '0', 'padding': '0',
                                                                                 'height': '100%',
                                                                                 'width': '100%',
                                                                                 'border': 'none'
                                                                                 })
                                    ],
                                    className='col-8 d-flex justify-content-center align-items-center'
                                ),
                                dbc.Col(
                                    children=[
                                        dbc.Row(
                                            children=[
                                                html.H1(f" {res['advertisements']}", className="m-1"),
                                                html.H6('anuncios recibidos', className="m-1")
                                            ],
                                            className='m-2'
                                        ),
                                        html.Br(),
                                        dbc.Row(
                                            children=[
                                                dbc.ListGroup(
                                                    children=[
                                                        dbc.ListGroupItem(
                                                            html.Div(
                                                                [
                                                                    html.H6(f"{item['TargetingValue']}",
                                                                            className="mb-1"),
                                                                    html.Small(f"{item['TargetingType']}"),
                                                                ],
                                                                className="d-flex w-100 justify-content-between",
                                                            ),
                                                        )
                                                        for item in eval(res['criteria'])
                                                    ],
                                                    className='h-100 w-100'
                                                )
                                            ], className='m-2'
                                        ),
                                    ],
                                    className='col-4'
                                ),
                            ],
                            className='p-4 m-2',
                            style={'border-radius': '40px',
                                   'box-shadow': '0 0.125rem 0.25rem rgba(0, 0, 0, 0.075)',
                                   'background-color': 'white'}
                        ),
                    ],
                    className='estilo_tab',
                    label=f"{res['advertiser']}"
                )
                for res in adv_json
            ], className="d-flex justify-content-evenly mb-3"
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    children=[
                        html.Img(src='https://cdn-icons-png.flaticon.com/512/1055/1055669.png',
                                 style={'height': '30px', 'width': '30px'},
                                 className='m-1'),
                        dbc.ModalTitle("Anunciantes más interesados", className='m-1'),
                    ], style={'background-color': '#6FADFF'}),
                dbc.ModalBody(children=[
                    html.P('''Muestra hasta un máximo de los cinco anunciantes de los que más has recibido 
                                        anuncios en tu perfil. Para cada uno de ellos se muestra la siguiente información: el 
                                        último twit que has recibido de dicho anunciante, el número total de anuncios recibidos y 
                                        una categorización de los motivos por los que te han aparecido las publicaciones de este 
                                        anunciante.'''),
                    html.Br(),
                    html.P('''Para cada uno de los criterios (que se muestran en la parte izquierda de la 
                                        lista) se proporciona el conjunto global al que pertenecen.''')
                ], style={'text-align': 'justify'}),
            ],
            id="modal_adv",
            is_open=False,
            className='modal-dialog-centered'
        )
    ], className='p-3 bg-light')
