import os
from google.cloud import storage


class Bucket:
    """ Subida y borrado de datos en el bucket """
    def __init__(self, filelist, _id):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "tfg-twitter-3c5ccb548a38.json"

        storage_client = storage.Client("api_keys.json")
        self.bucket = storage_client.get_bucket("tfg-twitter")
        self.filelist = filelist
        self._id = _id
        self.blobs = []

    def upload_data(self):
        """ Sube los ficheros al bucket """
        for filename, content in self.filelist.items():
            blob = self.bucket.blob(f"{self._id}/{filename}")
            blob.upload_from_string(content)
            self.blobs.append(blob)
            print(f'Subido {filename}')

    def delete_data(self):
        """ Elimina los ficheros del bucket """
        for blob in self.blobs:
            blob.delete()
