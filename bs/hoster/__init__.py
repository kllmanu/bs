from abc import ABC, abstractmethod
from yt_dlp import YoutubeDL

import ast
import os

YTDLP_OPTIONS = ast.literal_eval(os.getenv("YTDLP_OPTIONS", "{}"))
BS_DIR = os.getenv("BS_DIR", "")


class Hoster(ABC):
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    def factory(url: str) -> "Hoster":
        """Factory method to create a new Hoster object."""

        if "voe" in url:
            from bs.hoster.voe import VOE

            return VOE(url)

        if "vidoza" in url:
            from bs.hoster.vidoza import Vidoza

            return Vidoza(url)

    @property
    @abstractmethod
    def stream(self) -> str | None:
        """Return the video stream URL."""
        pass

    def download(self, folder, filename: str) -> None:
        """Download the video stream to a file."""
        ydl_opts = {
            **YTDLP_OPTIONS,
            "outtmpl": os.path.join(BS_DIR, folder, filename),
            "ignoreerrors": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.stream])
