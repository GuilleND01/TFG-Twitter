from dash import html, dcc
import dash_bootstrap_components as dbc


def return_gui_criteria(cri_json):
    return html.Div(children=[
        html.Div(children=[
            html.P(children=[html.Span('Criterios de tus anuncios', className='ms-3 h5')],
                   className='d-inline-flex m-0'),
            html.P(children=[
                html.Button(html.I(className="bi bi-info-circle"), id="open_modal_cri", className='btn'),
            ], className='d-flex align-items-center m-0')],
            className='d-flex justify-content-between align-items-center m-0'),
        html.Div("Criterios por los que aparecen tus anuncios.",
                 className='ms-3 mb-3 opacity-25'),
        html.Div(
            children=[
                html.Label('Selecciona una opción:'),
                dcc.Dropdown(
                    id='pombo-box',
                    options=[{'label': key, 'value': key} for key in cri_json],
                    value=next(iter(cri_json)),
                    placeholder='Selecciona un tipo de criterio...',
                    clearable=False
                ),
                html.Br(),
                html.Div(id='graph-criteria')
            ],
            className='p-4 m-2',
            style={'border-radius': '40px',
                   'box-shadow': '0 0.125rem 0.25rem rgba(0, 0, 0, 0.075)',
                   'background-color': 'white'}
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    children=[
                        html.Img(src='https://cdn-icons-png.flaticon.com/512/1055/1055669.png',
                                 style={'height': '30px', 'width': '30px'},
                                 className='m-1'),
                        dbc.ModalTitle("Criterios preferentes", className='m-1'),
                    ], style={'background-color': '#6FADFF'}),
                dbc.ModalBody(children=[
                    html.P('''Permite seleccionar entre los tipos de criterios posibles y mostrar para cada uno
                    los cinco valores como máximo que más figuran en los anuncios que se han visualizado.''')
                ], style={'text-align': 'justify'}),
            ],
            id="modal_cri",
            is_open=False,
            className='modal-dialog-centered'
        )
    ], className='p-3 bg-light', style={'border-radius': '40px'})
