import threading
import requests


class ThreadingFuntions:
    def __init__(self):
        self.resultado_dict = {}
        self.lock = threading.Lock()

    def requests(self, tarea, url):
        res = requests.get(url)
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
