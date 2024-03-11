import dash_bootstrap_components as dbc
from src.scripts.user_profile import UserProfile
from dash import html, dcc


def return_gui_profile(profile_data):
    return html.Div(
        [
            dbc.Button(html.I(className="bi bi-person-circle"),
                       id="open-offcanvas", n_clicks=0, color='black', className='btn'),
            dbc.Tooltip('Consulta tu perfil', target='open-offcanvas', placement='top'),
            dbc.Offcanvas(
                children=[
                    html.Div(
                        children=[
                            html.Div(html.Img(src=f"{profile_data['pictures']['header']}",
                                              alt='Header', className='w-100')),
                            html.Br(),
                            html.Div(html.Img(src=f"{profile_data['pictures']['prof_pic']}",
                                              alt='Profile Pic',
                                              style={'border-radius': '50%',
                                                     'vertical-align': 'middle', 'display': 'inline-block',
                                                     'border': '5px solid', 'border-color': 'white',
                                                     'margin-top': '-20%', 'margin-right': '70%'},
                                              className='w-25 h-25')
                                     ),
                            html.Br(),
                            html.Div(
                                children=[
                                    # Nombre de usuario y nombre mostrado
                                    html.P(f"{profile_data['profile']['accountDisplayName']}",
                                           style={'font-weight': 'bold', 'font-size': '20px'}),
                                    html.P(f"{profile_data['profile']['username']}",
                                           style={'font-size': '12px', 'margin-top': '-15px'}),
                                    html.P(f"{profile_data['description']['bio']}")
                                ],
                                style={'display': 'inline-block', 'width': '100%',
                                       'text-align': 'left', 'margin-bottom': '20px', 'margin-top': '-32px'}
                            ),
                            html.Br(),
                            html.Div(
                                children=[
                                    html.Div(  # Icono de la web
                                        children=[
                                            html.Img(src="https://img.icons8.com/ios/50/globe--v1.png",
                                                     alt='Icono web',
                                                     style={'width': '20px', 'height': '20px'}),
                                            html.P(f"{profile_data['description']['website']}",
                                                   style={'margin-left': '-85%'})
                                        ],
                                        style={'column-count': '2'}
                                    ),
                                    html.Div(  # Icono de la localización
                                        children=[
                                            html.Img(
                                                src="https://img.icons8.com/material-outlined/24/place-marker--v1.png",
                                                alt='Icono location',
                                                style={'width': '20px', 'height': '20px'}),
                                            # html.P(f"{profile_data['description']['location']}",
                                            # style={'margin-left': '-85%'})
                                        ],
                                        style={'column-count': '2', 'margin-top': '-10px'}
                                    ),
                                    html.Div(  # Icono del cumpleaños
                                        children=[
                                            html.Img(src="https://img.icons8.com/material-outlined/24/birthday.png",
                                                     alt='Icono cumpleaños',
                                                     style={'width': '20px', 'height': '20px'}),
                                            html.P(
                                                f"{profile_data['age']['birthDate']} ({profile_data['age']['age']} años)",
                                                style={'margin-left': '-85%'})
                                        ],
                                        style={'column-count': '2', 'margin-top': '-10px'}
                                    ),
                                    html.Div(  # Icono de creación de la cuenta
                                        children=[
                                            html.Img(src="https://img.icons8.com/ios/50/twitter--v1.png",
                                                     alt='Icono cuenta',
                                                     style={'width': '20px', 'height': '20px'}),
                                            html.P(f"{profile_data['profile']['createdAt']}",
                                                   style={'margin-left': '-85%'})
                                        ],
                                        style={'column-count': '2', 'margin-top': '-10px'}
                                    )
                                ],
                                style={'display': 'inline-block', 'width': '100%',
                                       'text-align': 'left', 'margin-top': '-10px'}
                            ),
                            html.Br(),
                            html.Div(children=[
                                html.P('Amorch, ' + profile_data['message'])
                            ], style={'border': '3px dotted black'}, className='p-5 d-flex justify-content-center')
                        ],
                        style={'text-align': 'center', 'background-color': 'white', 'padding-top': '10px',
                               'padding-bottom': '20px'}
                    )
                ],
                id="offcanvas",
                title="Tu Perfil",
                is_open=False,
            ),
        ],
        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
    )
