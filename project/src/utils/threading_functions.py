import threading
import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token
import os



class ThreadingFuntions:
    def __init__(self):
        self.resultado_dict = {}
        self.lock = threading.Lock()

    def requests(self, tarea, url):

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "tfg-twitter-3c5ccb548a38.json"

        target_audience = url.split('?')[0]
        id_token_request = Request()
        id_token_claims = id_token.fetch_id_token(id_token_request, target_audience)

        headers = {
            'Authorization': 'Bearer ' + id_token_claims,
            'Content-Type': 'application/json'
        }

        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            json_procesado = res.json()
        else:
            json_procesado = {}

        self.agregar_resultado({tarea: json_procesado})

    def agregar_resultado(self, resultado):
        with self.lock:
            self.resultado_dict.update(resultado)

    def devuelve_resultado(self):
        with self.lock:
            return self.resultado_dict
