class Bucket:
    _instance = None  # Instancia de la clase

    def __init__(self):
        self.files_list = {}  # Diccionario con el nombre de los ficheros
        self.urls = {}  # Diccionario con las Cloud Functions

    @staticmethod
    def get_instance():
        if Bucket._instance is None:
            Bucket._instance = Bucket()

        return Bucket._instance

    ''' Funciones para el listado de ficheros '''

    def get_filelist(self):
        return self.files_list

    def agg_file(self, filename, content):
        self.files_list[filename] = content

    def res_file(self):
        self.files_list = {}

    ''' Funciones para las Cloud Functions '''

    def compose_list(self, user_id):
        self.urls['profile'] = [f'https://us-central1-tfg-twitter.cloudfunctions.net/profile?id={user_id}',
                                False]
        self.urls['heat_map'] = [f'https://us-central1-tfg-twitter.cloudfunctions.net/heatmap_activity?id={user_id}',
                                 False]
        self.urls['senti_langu'] = [
            f'https://us-central1-tfg-twitter.cloudfunctions.net/sentimientos_lenguajes?id={user_id}',
            False]
        self.urls['friends_circle'] = [
            f'https://us-central1-tfg-twitter.cloudfunctions.net/twitter-circle?id={user_id}',
            False]
        self.urls['user_mentions'] = [f'https://us-central1-tfg-twitter.cloudfunctions.net/user-mentions?id={user_id}',
                                      False]

    def toggle_execute(self, function):
        self.urls[function][1] = True

    def get_list(self):
        return self.files_list

    ''' Subida y borrado de datos en el bucket '''

    def upload_data(self):
        pass

    def delete_data(self):
        pass