from slugify import slugify


class Series:
    def __init__(self, url: str, title: str):
        self.url = url
        self.title = title
        self.seasons = []

    def __repr__(self):
        return self.title

    @property
    def folder(self):
        return slugify(self.title)
