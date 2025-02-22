from abc import ABC, abstractmethod
from slugify import slugify
from yt_dlp import YoutubeDL

import requests

import re
import base64


class Series:
    def __init__(self, url: str, title: str):
        self.url = url
        self.title = title
        self.seasons = []

    def __repr__(self):
        return self.title


class Season:
    def __init__(self, url, title):
        self.url = url
        self.title = title
        self.episodes = []

    def __repr__(self):
        return self.title


class Episode:
    def __init__(self, url, title, number):
        self.url = url
        self.title = title.strip()
        self.number = number
        self.hosters = []

    def __repr__(self):
        return self.title

    def add_hoster(self, path):
        self.hosters.append(f"https://bs.to/{path}")

    @property
    def filename(self):
        return f"{self.number.zfill(2)}_{slugify(self.title)}.mp4"


class Hoster(ABC):
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    def new(url: str) -> "Hoster":
        """Factory method to create a new Hoster object."""

        if "voe" in url:
            return VOE(url)

    @property
    @abstractmethod
    def stream(self):
        """Return the video stream URL."""
        pass

    def download(self, filename: str) -> None:
        """Download the video stream to a file."""

        with YoutubeDL({"outtmpl": filename}) as ydl:
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
