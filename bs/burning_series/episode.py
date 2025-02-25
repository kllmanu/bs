from slugify import slugify

import os

BS_DIR = os.getenv("BS_DIR", "")


class Episode:
    def __init__(self, url, title, season, episode):
        self.url = url
        self.title = title.strip()
        self.season = season.zfill(2)
        self.episode = episode.zfill(2)
        self.hosters = []

    def __repr__(self):
        return f"S{self.season}E{self.episode} - {self.title}"

    def add_hoster(self, path):
        self.hosters.append(f"https://bs.to/{path}")

    def exists(self, series):
        """Create series folder and check if the episode already exists"""
        dest = os.path.join(BS_DIR, series.folder)

        if not os.path.exists(dest):
            os.mkdir(dest)

        return os.path.exists(os.path.join(dest, self.filename))

    @property
    def filename(self):
        return f"S{self.season}E{self.episode}_{slugify(self.title)}.mp4"
