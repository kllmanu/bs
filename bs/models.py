from abc import ABC, abstractmethod
from slugify import slugify
from yt_dlp import YoutubeDL

import requests

import ast
import os
import re
import base64

YTDLP_OPTIONS = ast.literal_eval(os.getenv("YTDLP_OPTIONS", "{}"))


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

    @property
    def filename(self):
        return f"S{self.season}E{self.episode}_{slugify(self.title)}.mp4"


class Hoster(ABC):
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    def factory(url: str) -> "Hoster":
        """Factory method to create a new Hoster object."""

        if "voe" in url:
            return VOE(url)

        if "vidoza" in url:
            return Vidoza(url)

    @property
    @abstractmethod
    def stream(self) -> str | None:
        """Return the video stream URL."""
        pass

    def download(self, folder, filename: str) -> None:
        """Download the video stream to a file."""
        ydl_opts = {**YTDLP_OPTIONS, "outtmpl": os.path.join(folder, filename)}

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.stream])


class VOE(Hoster):

    @property
    def stream(self) -> str | None:
        res = requests.get(self.url)

        # check for redirect first
        redirect = r"window\.location\.href\s*=\s*'(https?://[^\']+)'"
        match = re.search(redirect, res.text)

        if match:
            res = requests.get(match.group(1))

            hls = r"'hls':\s*'([^']+)'"
            match = re.search(hls, res.text)

            if match:
                return base64.b64decode(match.group(1)).decode("utf-8")


class Vidoza(Hoster):

    @property
    def stream(self) -> str | None:
        return self.url
