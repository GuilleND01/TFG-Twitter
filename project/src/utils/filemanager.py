class FileManager:
    _instance = None  # Instancia de la clase

    file_mask = [
        "account.js",
        "ad-impressions.js",
        "ad-engagements.js",
        "ageinfo.js",
        "profile.js",
        "follower.js",
        "following.js",
        "manifest.js",
        "tweets.js",
        "tweet-headers.js",
        "user-link-clicks.js",
        "direct-message-headers.js",
        "direct-message-group-headers.js",
    ]

    def __init__(self):
        self.file_list = {}
        self.user_id = ''
        self.username = ''
        self.download_file = False
        self.download_content = ''

    @staticmethod
    def get_instance():
        """ Crea una única instancia de la clase """
        if FileManager._instance is None:
            FileManager._instance = FileManager()

        return FileManager._instance

    @staticmethod
    def reset_instance():
        FileManager._instance = FileManager()

    def filter_filename(self, filename):
        return filename in self.file_mask

    def get_file_list(self):
        return self.file_list

    def agg_file(self, filename, content):
        if self.filter_filename(filename):
            self.file_list[filename] = content
            self.download_file = False
            return False

        if filename[:12] == 'whattheyknow':
            self.file_list.clear()
            self.download_content = content
            self.download_file = True
            return True

    def set_user_id(self, _id):
        self.user_id = _id

    def get_id(self):
        return self.user_id

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def get_download_file(self):
        return self.download_file

    def get_download_content(self):
        return self.download_content
