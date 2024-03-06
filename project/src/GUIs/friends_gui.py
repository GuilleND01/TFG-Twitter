import dash
import pandas as pd
from dash import dcc, html
import plotly.express as px
from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO
from src.scripts.friends_circle import FriendsCircle
import requests
import dash_bootstrap_components as dbc
import numpy as np


def return_gui_friends(friends_json):
    # Llama al procesamiento de los datos
    df = pd.DataFrame(friends_json)
    fig = px.scatter(
        df,
        x="x",
        y="y",
        size='pond',
        opacity=0.8,
        labels={'x': '', 'y': ''},
        title='Círculo de amigos',
        custom_data=['prof_url', 'puntua'],
        # color='rgb'
    )

    for i, row in df.iterrows():
        response = requests.get(row['imgs'])
        image_bytes = BytesIO(response.content)
        img = Image.open(image_bytes)
        '''
        img = img.convert("RGBA")
        size = 18
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        smooth_mask = mask.filter(ImageFilter.GaussianBlur(radius=9))
        img = Image.composite(img, Image.new("RGBA", img.size, "white"), smooth_mask.resize(img.size))'''
        fig.add_layout_image(
            dict(
                source=img,
                xref="x",
                yref="y",
                xanchor="center",
                yanchor="middle",
                x=row["x"],
                y=row["y"],
                sizex=18 * row['pond'],
                sizey=18 * row['pond'],
                sizing="contain",
                opacity=1,
                layer="above"
            )
        )

    fig.update_layout(
        xaxis=dict(showline=False, linewidth=0, range=[-50, 50], tickfont=dict(color="white")),
        # Establecer el rango del eje x
        yaxis=dict(showline=False, linewidth=0, range=[-50, 50], tickfont=dict(color="white")),
        # Establecer el rango del eje y
        plot_bgcolor='white',
    )

    fig.update_traces(
        hovertemplate=
        "La puntuación obtenida es del <b>%{customdata[1]} %</b>"
    )

    return html.Div(children=[
        dbc.Row(children=[
            dbc.Col(children=[
                dcc.Graph(id='friends-circle', figure=fig),
            ], className='col-11'),
            dbc.Col(children=[
                html.Div(
                    dbc.Button("i", id="open_modal_cir", n_clicks=0,
                               className='mx-auto d-block rounded-circle text-center',
                               style={'border': '2px solid', 'border-color': '#4AA7E4', 'background-color': 'white',
                                      'color': '#4AA7E4', 'width': '40px', 'height': '40px', 'font-family': 'serif'}),
                    style={'text-align': 'center'}
                ),
            ], className='col-1 text-center', style={'margin-top': '10px'})
        ]),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Círculo de amigos")),
                dbc.ModalBody(children=[
                    html.P('''Obtiene un listado de los usuarios con los que más has interactuado teniendo en cuenta
                    las siguientes interacciones: mensajes directos, seguir al usuario, menciones y retweets.'''),
                    html.Br(),
                    html.P('''Cada una de las imágenes es interactiva y permite acceder al perfil del usuario al que
                    representa. También aparece la puntuación que ha obtenido tras la ejecución del algoritmo.'''),
                ]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Cerrar", id="close_modal_cir", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal_cir",
            is_open=False,
        ),
    ], style={'background-color': 'white'})
