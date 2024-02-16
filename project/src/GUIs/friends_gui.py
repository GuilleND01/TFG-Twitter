import dash
from dash import dcc, html
import plotly.express as px
from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO
from src.scripts.friends_circle import FriendsCircle
import numpy as np


def return_gui_friends(mds_decoded, tweets_decoded, followers_decoded, account_decoded):
    # Llama al procesamiento de los datos
    df = (FriendsCircle(mds_decoded, tweets_decoded, followers_decoded, account_decoded).get_dataframe_wres())
    fig = px.scatter(
        df,
        x="x",
        y="y",
        hover_name="username",
        hover_data=["user_ids", "pond"],
        color_discrete_sequence=["rgba(0,0,0,0)"]  # Establecer el color de los marcadores como transparente
    )

    for i, row in df.iterrows():
        image_bytes = BytesIO(row['img_url'])
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
                sizex=18,
                sizey=18,
                sizing="contain",
                opacity=1,
                layer="above"
            )
        )

    fig.update_layout(
        xaxis=dict(showline=False, linewidth=0, range=[-50, 50]),
        # Establecer el rango del eje x
        yaxis=dict(showline=False, linewidth=0, range=[-50, 50]),
        # Establecer el rango del eje y
        plot_bgcolor='white',
    )

    return html.Div([
        html.H1('Círculo de Amigos'),
        dcc.Graph(id='friends-circle', figure=fig, style={'border-radius': '50%'})
    ], style={'background-color': 'white'})
