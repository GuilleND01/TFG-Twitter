import threading
from src.utils.threading_functions import ThreadingFuntions


class CloudFunctionManager:
    _instance = None  # Instancia de la clase

    def __init__(self):
        self.urls = {}  # Diccionario con las Cloud Functions
        self.results = {}  # Diccionario con los resultados de las llamadas

    @staticmethod
    def get_instance():
        """ Crea una única instancia de la clase """
        if CloudFunctionManager._instance is None:
            CloudFunctionManager._instance = CloudFunctionManager()

        return CloudFunctionManager._instance

    def compose_list(self, _id, cf_list):
        for cf in cf_list:
            if cf == 'sentimientos_lenguajes':
                self.urls[cf] = f'https://us-central1-tfg-twitter.cloudfunctions.net/{cf}?id={_id}&limit=30&traducir=False'
            else:
                self.urls[cf] = f'https://us-central1-tfg-twitter.cloudfunctions.net/{cf}?id={_id}'

        print(self.urls)

    def launch_functions(self):
        thread_list = []
        thread_mgmt = ThreadingFuntions()

        for item in self.urls:
            thread_list.append(threading.Thread(target=thread_mgmt.requests, args=(item, self.urls[item],)))

        for hilo in thread_list:
            hilo.start()

        for hilo in thread_list:
            hilo.join()

        self.results = thread_mgmt.devuelve_resultado()

    def get_results(self):
        return self.results
