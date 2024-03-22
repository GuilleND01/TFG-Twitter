from dash import Input, Output, State, html
from src.utils.cloudfunctionsmanager import CloudFunctionManager
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import ssl
import smtplib


html_code = f'''
    <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
            <h1>¡Tus datos ya están listos!</h1>
            <h2>Puedes encontrarlos en el fichero adjunto para poder descargarlos</h2>
            <p>Una vez los hayas descargado, puedes volver a subirlos a la aplicación para evitar tiempos de espera
            y tener tus datos siempre disponibles. Recuerda que si subes estos datos de forma manual, no podrás volver
            a realizar una descarga hasta que subas los ficheros proporcionados por el propio Twitter.</p>
            <br>
            <p>En caso de tener alguna duda del funcionamiento o algún problema con la ejecución, no dudes en contactar 
            a este correo: infowhattheyknow@gmail.com</p>
        </body>
    </html>
'''


def create_download_callback(app):
    @app.callback(
        Output('whitebox-2', 'children'),
        [Input('submit_button', 'n_clicks')],
        [State('input_email', 'value')]
    )
    def update_output(n_clicks, input_value):
        cloud_inst = CloudFunctionManager.get_instance()

        if n_clicks is not None and input_value is not None:
            # Datos del correo
            email_emisor = 'infowhattheyknow@gmail.com'
            email_contrasena = 'atojjyzkljifaiqj'

            email_receptor = input_value

            asunto = f'Datos del usuario {cloud_inst.get_username()}'

            em = MIMEMultipart()
            em['From'] = email_emisor
            em['To'] = email_receptor
            em['Subject'] = asunto
            em.attach(MIMEText(html_code.strip(), 'html'))

            adjunto = MIMEBase('application', 'octet-stream')
            adjunto.set_payload(str(cloud_inst.get_results()).encode('utf-8'))
            encoders.encode_base64(adjunto)
            adjunto.add_header('Content-Disposition', f'attachment; filename=whattheyknow-{cloud_inst.get_id()}.json')
            em.attach(adjunto)

            contexto = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
                smtp.login(email_emisor, email_contrasena)
                smtp.sendmail(email_emisor, email_receptor, em.as_string())
            print(input_value)

        return None
