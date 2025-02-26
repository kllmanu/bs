from abc import ABC, abstractmethod
from pathlib import Path

import os

from yt_dlp import YoutubeDL


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

        if "doodstream" in url or "d0000d" in url or "dood" in url:
            from bs.hoster.doodstream import Doodstream

            return Doodstream(url)

        if "streamtape" in url:
            from bs.hoster.streamtape import Streamtape

            return Streamtape(url)

    @property
    @abstractmethod
    def stream(self) -> str | None:
        """Return the video stream URL."""
        pass

    def download(self, dir, folder, filename: str) -> None:
        """Download the video stream to a file."""

        folder = Path(dir) / Path(folder)
        file = Path(filename)

        ydl_opts = {
            "outtmpl": f"{folder / file}",
            "ignoreerrors": True,
            "http_headers": {"Referer": self.url},
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.stream])

        # cleanup
        os.system(f"rm -f {folder}/*.part")
