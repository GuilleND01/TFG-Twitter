import dash
import pandas as pd
from dash import dcc, html
import plotly.express as px
from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO
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

    return html.Div(
        children=[
            html.Div(
                children=[html.Span('Círculo de amigos', className='ms-3 h5 m-0'), html.Button(html.I(className="bi bi-info-circle"),
                    id="open_modal_cir", className='btn')], className='d-flex justify-content-between align-items-center'),
            html.Div("Conoce a tus amigos más cercanos.", className='ms-3 mb-3 opacity-25'),
            html.Div(children=[
                dcc.Graph(id='friends-circle', figure=fig),
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            children=[
                                html.Img(src='https://cdn-icons-png.flaticon.com/512/2671/2671250.png',
                                         style={'height': '30px', 'width': '30px'},
                                         className='m-1'),
                                html.Div("Círculo de Amigos", className='m-1 h5'),
                            ], style={'background-color': '#6FADFF'}),
                        dbc.ModalBody(children=[

                            html.P('''Conoce quiénes son tus amigos más cercanos teniendo en cuenta
                                las siguientes interacciones: mensajes directos, seguir al usuario, menciones y retweets.'''),
                            html.P('''Cada una de las imágenes es interactiva y permite acceder al perfil del usuario al que
                                representa. También aparece la puntuación que ha obtenido tras la ejecución del algoritmo.'''),

                        ], style={'text-align': 'justify'}),
                    ],
                    id="modal_cir",
                    is_open=False,
                    className='modal-dialog-centered'
                ),
            ])
        ], className='p-3 bg-light'
    )

