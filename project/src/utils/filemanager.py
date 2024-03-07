class FileManager:
    file_mask = [
        "account.js",
        "ad-impressions.js",
        "ageinfo.js",
        "profile.js",
        "follower.js",
        "following.js",
        "tweets.js",
        "tweet-headers.js",
        "user-link-clicks.js",
        "direct-message-headers.js",
        "direct-message-group-headers.js",
    ]

    def __init__(self):
        self.file_list = {}
        self.user_id = ''
        self.download_file = False
        self.download_content = ''

    def filter_filename(self, filename):
        return filename in self.file_mask

    def get_file_list(self):
        return self.file_list

    def agg_file(self, filename, content):
        if self.filter_filename(filename):
            self.file_list[filename] = content
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

    def get_download_file(self):
        return self.download_file

    def get_download_content(self):
        return self.download_content
