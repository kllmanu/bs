class Season:
    def __init__(self, url, title):
        self.url = url

        if title.isdigit():
            self.title = title
        else:
            self.title = "0"

        self.episodes = []

    def __repr__(self):
        return self.title
