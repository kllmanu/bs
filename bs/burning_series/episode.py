from slugify import slugify
from pathlib import Path

from bs.burning_series import Series
from bs.burning_series import Season


class Episode:
    def __init__(self, dir, url, title, series: Series, season: Season, episode):
        self.dir = dir
        self.url = url
        self.title = title.strip()
        self.series = series.folder
        self.season = season.title.zfill(2)
        self.episode = episode.zfill(2)
        self.hosters = []

    def __repr__(self):
        return f"S{self.season}E{self.episode} - {self.title}"

    def add_hoster(self, path):
        self.hosters.append(f"https://bs.to/{path}")

    @property
    def filtered_hosts(self):
        filtered_hosts = []

        for host in self.hosters:
            if not "Vidmoly" in host:
                filtered_hosts.append(host)

        return filtered_hosts

    @property
    def filename(self):
        return f"S{self.season}E{self.episode}_{slugify(self.title)}.mp4"

    def exists(self):
        """Create series folder and check if the episode already exists"""

        folder = Path(self.dir) / Path(self.series)
        file = Path(self.filename)

        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)

        return (folder / file).exists()
